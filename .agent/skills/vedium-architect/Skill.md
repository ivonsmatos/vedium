---
name: vedium-architect
description: >
  Arquiteto e engenheiro principal do projeto Vedium — plataforma de cursos de
  idiomas premium sobre Frappe Framework v16 / ERPNext v16 / Frappe LMS 2.x,
  rodando em Docker Compose com deploy automatizado via GitHub Actions.
  Use este skill em QUALQUER tarefa de código, infraestrutura ou arquitetura do
  projeto: criação de páginas, endpoints, pagamentos, Docker, CI/CD, testes,
  i18n, SEO, performance, compliance. Para decisões de "usar nativo vs custom",
  consulte também o skill `frappe-platform` (.claude/skills/frappe-platform/).
---

# VEDIUM ARCHITECT SKILL

> Última atualização: **2026-07-05** (auditoria completa do repositório).

## 1. IDENTITY & MISSION

You are the Lead Architect for **Vedium**, a high-ticket LMS platform for
premium language courses (Executive English, Ancestral Yoruba, Portuguese for
Foreigners) built on the Frappe ecosystem.

**Core Principles — non-negotiable:**

1. **No Forks:** NEVER modify `apps/frappe`, `apps/erpnext`, `apps/lms`,
   `apps/crm`, or `apps/helpdesk`. ALL changes go into `vedium_core`.
2. **High-End UI:** "Raízes de Luxo" design system (Dark Mode, Tailwind v3).
3. **Performance-first:** Frappe Caffeine, lazy imports, pagination everywhere.
4. **Git Strategy:** Only version files inside `vedium_core` + `deploy/` +
   `docs/`. Infrastructure is Docker-managed.
5. **Nativo primeiro:** Before writing custom code, check if Frappe/ERPNext/LMS
   already provides the feature natively — see
   [01-mapa-nativo-vs-custom.md](../../docs/plataforma/01-mapa-nativo-vs-custom.md).

---

## 2. TECH STACK (verified in production 2026-07-05)

| Layer | Technology | Version |
|---|---|---|
| Backend | Frappe Framework | **v16** (16.18.x) |
| ERP | ERPNext | **v16** (16.19.x) |
| LMS | Frappe LMS | **2.x** (branch `main`) |
| CRM | Frappe CRM | 1.x (branch `main`) |
| Helpdesk | Frappe Helpdesk | 1.x (branch `main`) |
| Language | Python | **3.14** |
| Runtime JS | Node.js | **24** |
| Frontend | Jinja2 + **Tailwind CSS v3** |  |
| Database | MariaDB | **10.6** |
| Cache/Queue | Redis | 7-alpine (×3: cache, queue, socketio) |
| Web Server | Nginx | host VM |
| CDN/Edge | Cloudflare | proxy active |
| Monitoring | Uptime Kuma | Docker container |
| Payments | Stripe + Mercado Pago | + Basecommerce (stub) + Crypto (disabled) |
| AI | Groq (Llama 3 70B) | via `ai_controller.py` |
| Custom App | **`vedium_core`** | All custom logic lives here |

> ⚠️ `bench list-apps` shows frappe/erpnext as `UNVERSIONED` because they come
> baked into the `frappe/erpnext:v16` image (no `.git`). **NEVER run
> `bench update`** for frappe/erpnext. Upgrade = change the image tag in
> `deploy/docker-compose.yml`.

---

## 3. PROJECT STRUCTURE

```
vedium/
├── vedium_core/                    # Frappe custom app (ALL custom code)
│   └── vedium_core/
│       ├── hooks.py                # Routes, CSS, JS, events, i18n redirects
│       ├── install.py              # before/after_install, after_migrate
│       ├── api.py                  # Public API (payments, gamification, etc.)
│       ├── gamification.py         # Points / badges (atomic UPDATE)
│       ├── integrations.py         # LMS→CRM sync, Contact unification
│       ├── referrals.py            # Referral program (coupon_code reuse)
│       ├── marketing_landing_content.py  # Landing pages data (304KB!)
│       ├── blog_content.py         # Blog posts data (64KB)
│       ├── seo_utils.py            # Sitemap, schema markup
│       ├── geo_endpoints.py        # GEO/AI optimization
│       ├── course_translations.py  # i18n for course pages
│       ├── controllers/
│       │   └── ai_controller.py    # Groq AI Tutor + rate limit
│       ├── services/
│       │   ├── ai_service.py       # Audio analysis (speaking/listening)
│       │   └── crypto_service.py   # Coinbase Commerce
│       ├── www/                    # Server-rendered pages (90+ files)
│       │   ├── index.html/py       # Home (89KB)
│       │   ├── catalogo.html/py    # Course catalog
│       │   ├── curso.html/py       # Course detail (/curso/<slug>)
│       │   ├── en/es/fr/de/        # Translated pages
│       │   └── sitemap.py          # Dynamic sitemap
│       ├── templates/              # Jinja includes & layouts
│       ├── tests/                  # test_pure_* (no Frappe bench needed)
│       ├── translations/           # i18n files
│       └── vedium_core/doctype/    # Custom DocTypes
│           ├── coupon/             # Discount coupons
│           ├── lms_certificate/    # Certificate with verification_code
│           ├── lms_badge_log/      # Gamification badges
│           ├── placement_test/     # Public placement test
│           ├── support_ticket/     # Support (legacy — HD Ticket preferred)
│           └── referral/           # Referral program
├── deploy/                         # Production config
│   ├── docker-compose.yml          # PRODUCTION compose (8 services)
│   ├── nginx/vediums.com.conf      # Nginx vhosts
│   ├── scripts/                    # backup.sh, restore.sh, security-monitor
│   └── .env.example
├── docker-compose.yml              # DEV compose (5 services)
├── Dockerfile                      # Dev image (Python 3.14, Node 24)
├── Makefile                        # up, down, logs, shell, migrate, backup
├── .github/workflows/              # CI/CD (7 workflows)
│   ├── deploy.yml                  # Push to main → production
│   ├── test.yml                    # Lint + pip-audit + gitleaks + tests
│   ├── security-check.yml          # Daily: SSL, availability, monitor
│   ├── backup.yml                  # Scheduled backup
│   └── ...
└── docs/                           # Canonical docs
    ├── ARCHITECTURE.md
    ├── ROADMAP.md
    └── plataforma/                 # 12 operational docs
```

---

## 4. PAYMENTS ARCHITECTURE

The biggest module in `api.py` — **Strategy + Factory pattern**:

```python
get_gateway("stripe"|"mercadopago"|"basecommerce"|"crypto") → PaymentGateway
gateway.create_checkout(course, user, coupon_code=None) → URL
gateway.handle_webhook(event) → creates LMS Enrollment
```

### Gateways

| Gateway | Status | Webhook HMAC | Notes |
|---|---|---|---|
| **Stripe** | ✅ Active | `STRIPE_WEBHOOK_SECRET` (mandatory in prod) | `/api/method/vedium_core.api.stripe_webhook` |
| **Mercado Pago** | ✅ Active | `MERCADOPAGO_WEBHOOK_SECRET` (mandatory in prod) | `X-Signature` header validated |
| **Basecommerce** | ⚠️ Stub | — | `create_checkout` returns placeholder URL |
| **Crypto** | 🔴 Disabled | Not implemented | `CRYPTO_ENABLED` + `CRYPTO_API_KEY` required |

### Checkout flow
1. User calls `create_checkout(course, gateway, coupon_code)`.
2. Coupon validated (or referral code via `referrals.validate_referral_code`).
3. Discounted price passed to gateway's `create_checkout`.
4. User pays on external page (Stripe/MP).
5. Webhook → HMAC verified → `create_enrollment_if_paid()` → LMS Enrollment created.
6. Coupon `used_count` incremented atomically.
7. Welcome email sent (queued, never blocks enrollment).
8. CRM Lead synced via `integrations.sync_student_to_crm` (background job).

### Security rules
- **Production (DEVELOPER_MODE=0):** Webhook secret is MANDATORY. Missing → 401.
- **Dev:** Accepted without verification but logged.
- Never process unverified payloads in production.

---

## 5. DOCKER & INFRASTRUCTURE

### Dev environment
- `docker-compose.yml` (root) — 5 services: frappe, mariadb, redis×3.
- Frappe container runs `sleep infinity` — you `make shell` and `bench start`.
- Workspace bind-mounted at `/workspace:cached`.

### Production environment
- `deploy/docker-compose.yml` — **8 services**:
  - `vedium-frappe` (gunicorn, 4 workers, `--preload`)
  - `vedium-socketio` (node socketio.js)
  - `vedium-worker-default`, `-short`, `-long` (RQ workers)
  - `vedium-scheduler` (cron jobs)
  - `vedium-mariadb` (10.6, healthchecked)
  - `vedium-redis-cache`, `-queue`, `-socketio` (all healthchecked)
  - `vedium-uptime-kuma` (optional, profile `observability`)

### Key infra rules
- MariaDB: NOT exposed outside Docker network.
- Redis: Internal only, no auth (⚠️ should add `requirepass`).
- Gunicorn: Bound to 127.0.0.1:8005, Nginx proxies externally.
- SocketIO: Bound to 127.0.0.1:9000.
- Volumes: `frappe-bench-v16` (external), `vedium-sites`, `mariadb-data`.

---

## 6. CI/CD PIPELINE

### On push to `main` → `deploy.yml`
1. Checkout code.
2. Setup SSH (via `webfactory/ssh-agent`).
3. `rsync` code to server (`/opt/vedium/`).
4. `rsync` marketing site to `/opt/vedium/site/`.
5. SSH into server:
   - `docker cp vedium_core` into container.
   - `pip install -e apps/vedium_core`.
   - `bench install-app vedium_core` (idempotent).
   - `bench migrate`.
   - Run oneshot migrations (certificate collision, PWA icon, email sender).
   - `npm install` + `npm run build-css` + `bench build --app vedium_core`.
   - `bench clear-cache` + `bench clear-website-cache`.
   - **`docker restart vedium-frappe`** (gunicorn doesn't hot-reload Python!).
   - **`docker restart` all workers + scheduler** (same reason).
   - Wait for healthchecks (30 iterations × 5s).
   - Run idempotent course creation scripts.
6. Smoke test: curl vediums.com and app.vediums.com.

### On push/PR → `test.yml`
- Lint: `flake8` (syntax errors block, style warnings only).
- Security: `pip-audit --strict` + `gitleaks`.
- Tests: `pytest -v vedium_core/vedium_core/tests/test_pure_*.py`.
- ⚠️ CI uses Python 3.11 but production uses 3.14.

### Daily → `security-check.yml`
- SSL certificate expiration check.
- Website availability (GET + POST with Origin header).
- Security monitor script on server.
- Backup freshness check.
- Container health check (expect ≥5 running).

---

## 7. CODING STANDARDS

### A. Frontend & Styling (Tailwind Build Process)

1. **Source:** `vedium_core/input.css` — custom classes.
2. **Config:** `vedium_core/tailwind.config.js` — theme extensions.
3. **Build:** `npm run build-css` inside `vedium_core/`.
4. **Output:** `vedium_core/vedium_core/public/css/vedium.css`.
5. **Loaded via hooks.py:**
   - `app_include_css` / `web_include_css` → `vedium.css` + `luxo_theme.css`
   - `web_include_js` → `pwa-register.js`, `cookie-consent.js`, `meta-pixel.js`

**Design System Colors ("Raízes de Luxo"):**
- Backgrounds: `bg-slate-900` (main), `bg-slate-800` (cards)
- Text: `text-slate-100` (primary), `text-slate-400` (muted)
- Primary Action: `bg-indigo-600` / `hover:bg-indigo-700`
- Brand Blue: `#2E6DA4` — theme color for PWA / navbar
- Brand Red: `#A12D1C` — accents
- Track colors:
  - Leadership (English): `text-indigo-400`
  - Roots (Yoruba): `text-orange-600`
  - Gateway (Portuguese): `text-emerald-500`

### B. Creating New Pages

1. Create `www/<page-name>.html` + `www/<page_name>.py`.
2. HTML uses Jinja2 — extend the base layout or use `{% block %}`.
3. The `.py` controller sets `context` (title, meta, data).
4. Add route to `hooks.py` `website_route_rules` if needed.
5. For translated versions: create `www/en/<page-name>.html` etc.
6. Update `SAME_SLUG_TRANSLATIONS` in `hooks.py` if keeping same slug.
7. Update `sitemap.py` to include the new page.

### C. Backend Logic

1. Business logic in `vedium_core/` modules (not all in `api.py`).
2. API endpoints: `@frappe.whitelist()` (logged) or `@frappe.whitelist(allow_guest=True)`.
3. Rate limiting: Use `rate_limit_by_ip(action, limit, window_sec)` for public endpoints.
4. DocType fallback: Use `_safe_get_all()` for optional DocTypes.
5. Lazy imports: Heavy deps (`stripe`, `mercadopago`, `groq`) inside functions.
6. Error logging: `frappe.log_error(msg, title=f"Vedium.{module}.{func}")`.
7. Background jobs: `frappe.enqueue(..., enqueue_after_commit=True)`.

### D. Testing

- Pattern: `test_pure_*.py` — tests that run WITHOUT Frappe bench.
- Run: `pytest -v vedium_core/vedium_core/tests/test_pure_*.py`
- Current coverage: ~15% (6 test files: API, marketing pages, payments, referrals, webhooks, e2e).
- All tests MUST pass before merge (enforced by `test.yml`).

---

## 8. INTERNATIONALIZATION (i18n)

### Architecture

The project supports **12 language prefixes** (pt-br, en, en-us, en-au, es,
es-ar, es-co, fr, fr-ca, de, ru, zh-cn) mapped to **6 language families**
(en, es, fr, de, ru, zh-cn) via `LANGUAGE_PREFIX_FAMILY` in `hooks.py`.

### How it works

1. `LANGUAGE_ROUTE_RULES` — maps `/<prefix>/<route>` → Portuguese controller.
2. `SAME_SLUG_TRANSLATIONS` — pages with real translated HTML keeping same slug.
3. `LANGUAGES_WITH_OWN_HOME` — families with their own `www/<family>/index.html`.
4. `_build_language_prefix_redirects()` — auto-generates 301 redirects based on
   which translations actually exist (driven by `LANDINGS[...]["alt"]`).
5. Translation agents (`.claude/agents/translator-*.md`) publish pages and
   update `SAME_SLUG_TRANSLATIONS` — no manual `hooks.py` edit needed.

### Key rule
Never serve content in the wrong language. If a translated page doesn't exist,
redirect to the canonical Portuguese version — never show Portuguese under an
English URL.

---

## 9. PERFORMANCE GUIDELINES

1. **Enable Frappe Caffeine** — `caffeine_enabled: 1` in `site_config.json`.
2. **Pagination** — ALL `get_*` endpoints must accept `limit` + `start` (offset).
3. **Avoid N+1 queries** — Use JOINs or `frappe.qb` instead of loops with `frappe.db.count`.
4. **Lazy content loading** — `marketing_landing_content.py` (304KB) and
   `blog_content.py` (64KB) are loaded into every worker's memory. Move to
   JSON/DocType when possible.
5. **Static assets** — Use Cloudflare cache (30d TTL for `/assets/*`).
6. **Redis** — Set `maxmemory 256mb` + `allkeys-lru` on cache instance.
7. **MariaDB** — Tune InnoDB buffer pool to 50-70% of DB RAM.

---

## 10. SECURITY RULES

1. **Never** hardcode API keys — use `frappe.conf.get("KEY_NAME")`.
2. **Never** commit `.env` or `site_config.json`.
3. **Webhooks** in production REQUIRE HMAC secret — fail hard without it.
4. **Rate limit** public endpoints — use `rate_limit_by_ip()`.
5. **Escape user input** — `frappe.utils.escape_html()` in email bodies.
6. **Docker** — assume code runs in container; no `apt-get` except in Dockerfile.
7. **CSP** — must be present on both `vediums.com` and `app.vediums.com`.
8. **Redis** — add `requirepass` for defense-in-depth.
9. **IP addresses** — NEVER commit real server IPs in docs/runbooks.

---

## 11. COMMON RECIPES

### Recipe: Add a new payment gateway

1. Create class extending `PaymentGateway` in `api.py` (or new `payments/` module).
2. Implement `create_checkout()` and `handle_webhook()`.
3. Add to `get_gateway()` factory.
4. Add HMAC verification in `handle_payment_webhook()`.
5. Add env vars to `deploy/.env.example`.
6. Write `test_pure_*.py` for the new gateway.

### Recipe: Override a Core LMS Template

1. Identify original in `apps/lms/lms/templates/...`.
2. Create override in `vedium_core/templates/overrides/`.
3. Add route map to `hooks.py` `website_route_rules`.

### Recipe: Add a translated page

1. Create `www/<lang>/<page>.html` with translated content.
2. If same slug: add to `SAME_SLUG_TRANSLATIONS` in `hooks.py`.
3. If different slug: add to `LANDINGS[...]["alt"]` in `marketing_landing_content.py`.
4. The redirect system auto-generates 301s — no manual redirect needed.

### Recipe: AI Controller Implementation

1. Wrap Groq calls in `try/except`.
2. Check `check_rate_limit(user)` before call.
3. Use `frappe.conf.get("GROQ_API_KEY")` — never hardcode.
4. Log errors with `frappe.log_error(traceback, "Vedium.ai.{func}")`.

---

## 12. KEY REFERENCES

- [README.md](../../README.md) — quickstart
- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — canonical architecture
- [docs/ROADMAP.md](../../docs/ROADMAP.md) — priorities
- [deploy/RUNBOOK.md](../../deploy/RUNBOOK.md) — operations
- [deploy/SECURITY.md](../../deploy/SECURITY.md) — security details
- [CHANGELOG.md](../../CHANGELOG.md) — history
- [docs/plataforma/](../../docs/plataforma/) — 12 operational docs
- [.claude/skills/frappe-platform/](../../.claude/skills/frappe-platform/SKILL.md) — native vs custom decisions
