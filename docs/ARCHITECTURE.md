# Arquitetura — Vedium

> Documento canônico. Substitui `ARQUITETURA.md`, `ARQUITETURA_PROPOSTA.md`
> e `ESTADO_ATUAL.md` (arquivados em `docs/archive/`).
> Última revisão: **2026-06-11**

---

## 1. Visão geral

Vedium é uma plataforma de cursos de idiomas premium (Inglês Executivo,
Iorubá Ancestral, Português para Estrangeiros) construída sobre o
**Frappe Framework v16** com **ERPNext v16** e **Frappe LMS 2.x**.

- **Site institucional** (vediums.com): páginas SEO server-rendered pelo
  Frappe (`vedium_core/www/`), tema "Raízes de Luxo".
- **Plataforma de aprendizagem** (app.vediums.com): Frappe LMS oficial +
  customizações em `vedium_core` (pagamentos, gamificação, IA).
- **ERP/CRM** (app.vediums.com/app): ERPNext, CRM, HRMS, Helpdesk.

---

## 2. Stack real (verificada no container em 2026-06-12)

> Histórico: a auditoria de 2026-05-25 (task.md arquivado) afirmou que a
> produção rodava v15 — estava ERRADA. `docker inspect` confirma imagem
> `frappe/erpnext:v16`. O Dockerfile da raiz (Python 3.11/Node 20) é
> apenas o ambiente de DEV, não reflete produção.

| Camada | Tecnologia | Versão (produção) |
|---|---|---|
| Backend | Frappe Framework | **v16** (16.18.x) |
| ERP | ERPNext | **v16** (16.19.x) |
| LMS | Frappe LMS | 2.x (branch `main`) |
| CRM | Frappe CRM | 1.x (branch `main`) |
| Helpdesk | Frappe Helpdesk | 1.x (branch `main`) |
| Linguagem | Python | **3.14** |
| Runtime JS | Node.js | **24** |
| Frontend | Jinja2 + Tailwind CSS | Tailwind v3 |
| DB | MariaDB | 10.6 |
| Cache/fila | Redis | 7-alpine (3 instâncias: cache, queue, socketio) |
| Web | Nginx | host do servidor |
| Container | Docker Compose | v2 |
| CDN/edge | Cloudflare | proxy ativo |
| Monitoramento | Uptime Kuma | container `vedium-uptime-kuma` |
| Pagamentos | Stripe + Mercado Pago | + Basecommerce (stub) |
| IA | Groq (Llama 3 70B) | código parcial; tutor ainda não é produto pronto |

⚠️ `bench list-apps` mostra frappe/erpnext como `UNVERSIONED` porque eles
vêm **baked na imagem** `frappe/erpnext:v16` (sem `.git` — verificado no
container). Consequência: **NUNCA rodar `bench update`** para frappe/erpnext;
o upgrade deles é trocar a tag da imagem no compose. Já `lms`, `crm` e
`helpdesk` são repositórios git dentro do volume (branch `main`) e são
atualizados via `git pull` controlado + `bench migrate`.

---

## 3. Topologia em produção

```
                  ┌───────────────────┐
Internet ────────►│ Cloudflare (proxy)│
                  └─────────┬─────────┘
                            │ TLS
                            ▼
                  ┌───────────────────┐
                  │  Nginx (host VM)  │ ── serve /opt/vedium/site/ (estático)
                  └─────────┬─────────┘
                            │ proxy_pass → 127.0.0.1:8005
                            ▼
                  ┌───────────────────────────────────────┐
                  │  vedium-frappe (Docker)               │
                  │  - gunicorn (app)                     │
                  │  - worker-default / -long / -short    │
                  │  - scheduler                          │
                  │  - vedium_core + frappe + erpnext+lms │
                  └────┬─────────┬───────────┬────────────┘
                       │         │           │
                       ▼         ▼           ▼
                   MariaDB    Redis×3      Site files
                   10.6       7-alpine     (volume)
```

Hostnames:
- `vediums.com` — marketing + páginas SEO (Frappe via host-rewrite no nginx).
- `app.vediums.com` — LMS + ERP (host nativo, sem rewrite).

---

## 4. Estrutura do `vedium_core`

```
vedium_core/
├── vedium_core/
│   ├── hooks.py                    # Configuração Frappe (rotas, CSS, eventos)
│   ├── install.py                  # before/after_install, after_migrate
│   ├── api.py                      # API pública whitelisted (legacy monolito)
│   ├── gamification.py             # Points / badges
│   ├── seo_utils.py                # Sitemap, schema markup
│   ├── geo_endpoints.py            # GEO/AI optimization endpoints
│   ├── analytics_events.py         # GTM / GA4 server-side
│   ├── careers.py                  # Página de carreiras
│   ├── controllers/
│   │   └── ai_controller.py        # Tutor IA Groq parcial + rate limit
│   ├── services/
│   │   ├── ai_service.py           # Áudio speaking/listening em mock
│   │   └── crypto_service.py       # Coinbase Commerce
│   ├── www/                        # Páginas server-rendered
│   │   ├── index.py                # Home
│   │   ├── catalogo.py             # Lista de cursos
│   │   ├── curso.py                # Detalhe (URL: /curso/<slug>)
│   │   ├── carreiras.py
│   │   └── aluno_360.py
│   └── vedium_core/doctype/        # DocTypes customizados
│       ├── coupon/
│       ├── lms_certificate/
│       ├── lms_badge_log/
│       ├── lms_flashcard/
│       ├── support_ticket/
│       ├── placement_test/ + question/
│       ├── lesson_slot/
│       └── flashcard/
└── public/                         # Assets (CSS/JS/imagens)
```

---

## 5. Pagamentos

Padrão Strategy + Factory implementado em `api.py`:

```python
get_gateway("stripe"|"mercadopago"|"basecommerce"|"crypto") → PaymentGateway
gateway.create_checkout(course, user) → URL
gateway.handle_webhook(event) → cria LMS Enrollment
```

- **Stripe**: webhook em `/api/method/vedium_core.api.stripe_webhook` com
  verificação HMAC obrigatória em produção.
- **Mercado Pago**: webhook centralizado em
  `/api/method/vedium_core.api.handle_payment_webhook?gateway=mercadopago`,
  HMAC `X-Signature` validado.
- **Basecommerce**: stub (TODO).
- **Crypto**: `handle_webhook` levanta `NotImplementedError` por segurança.

**Cupons**: DocType `Coupon` com `discount_percent`, `valid_from`, `valid_to`,
`max_uses`, `used_count`. Aplicado em `create_checkout(coupon_code=...)`.

---

## 6. Princípios não-negociáveis

1. **Nunca modificar apps oficiais** (`frappe`, `erpnext`, `lms`). Toda
   customização vive em `vedium_core`.
2. **Webhooks em produção exigem segredo** — sem `STRIPE_WEBHOOK_SECRET`
   ou `MERCADOPAGO_WEBHOOK_SECRET`, falha duro com `DEVELOPER_MODE=0`.
3. **URLs públicas estáveis** — `vedium_core.api.<func>` não pode mudar
   de caminho sem aviso de 90 dias; webhooks externos estão registrados.
4. **DocTypes não-existentes devem ter fallback** — endpoints que consultam
   DocTypes opcionais retornam `[]` se a tabela não existe.
5. **Branch main = sempre verde** — features em `feat/<nome>`, fixes em
   `fix/<nome>`, hotfixes em `hotfix/<nome>`.

---

## 7. Decisões registradas

| ID | Decisão | Data | Motivo |
|---|---|---|---|
| ADR-001 | ~~Manter v15~~ **SUPERADO**: produção já roda v16 (verificado 2026-06-12) — a premissa do ADR era falsa | 2026-06-12 | Auditoria de maio leu o ambiente errado (Dockerfile dev) |
| ADR-002 | Docker Compose (não Kubernetes) | 2026-05-29 | <1k MAU; complexidade k8s não se paga |
| ADR-003 | Cloudflare (não AWS CloudFront) | 2026-05-29 | Custo zero, DNS+WAF+cache no mesmo painel |
| ADR-004 | Single-master MariaDB | 2026-05-29 | Replica = manutenção extra sem ganho real ainda |
| ADR-005 | Remover Prometheus | 2026-06-11 | Overhead desproporcional ao tráfego; usar Uptime Robot + Grafana Cloud free quando precisar |
| ADR-006 | API pública continua em `vedium_core.api.*` | 2026-06-11 | Webhooks externos já registrados; refactor seria breaking |

---

## 8. Referências

- [README.md](../README.md) — quickstart
- [CHANGELOG.md](../CHANGELOG.md) — histórico
- [docs/ROADMAP.md](ROADMAP.md) — próximas entregas
- [docs/RUNBOOK.md](RUNBOOK.md) — incidentes e operação
- [deploy/SECURITY.md](../deploy/SECURITY.md) — segurança detalhada
