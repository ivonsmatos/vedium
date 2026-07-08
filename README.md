# Vedium

Plataforma de cursos premium de idiomas — Inglês Executivo, Iorubá Ancestral
e Português para Estrangeiros — construída sobre o **Frappe Framework**.

🌐 **Site**: <https://vediums.com>
📚 **Plataforma LMS**: <https://app.vediums.com>

> 📖 Para arquitetura, decisões e roadmap, leia
> [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) e
> [`docs/ROADMAP.md`](docs/ROADMAP.md).
> Para histórico, [`CHANGELOG.md`](CHANGELOG.md).

---

## Stack

Verificado direto no container de produção em 2026-06-12
(`docker inspect` + `bench list-apps`):

| Camada | Tecnologia | Produção | Dev local (Dockerfile) |
|---|---|---|---|
| Backend | Frappe Framework | **v16** (imagem `frappe/erpnext:v16`) | bench |
| ERP | ERPNext | **v16** | bench |
| LMS | Frappe LMS | 2.x (`main`) | bench |
| CRM / Helpdesk | Frappe CRM 1.x / Helpdesk 1.x | instalados | — |
| Linguagem | Python | **3.14** | 3.11 |
| Runtime JS | Node.js | **24** | 20 LTS |
| Frontend | Jinja2 + Tailwind CSS v3 | — | — |
| Banco de Dados | MariaDB | 10.6 | 10.6 |
| Cache | Redis | 7-alpine ×3 | 7-alpine ×3 |
| Web Server | Nginx | host VM | — |
| CDN/Edge | Cloudflare | proxy ativo | — |

> ⚠️ O `Dockerfile` da raiz é o ambiente de **desenvolvimento** (bench);
> produção usa a imagem oficial `frappe/erpnext:v16`. Não confundir as
> versões de um com o outro.

---

## Estrutura

```
vedium/
├── vedium_core/                # App Frappe customizado
│   └── vedium_core/
│       ├── hooks.py            # Rotas, CSS, eventos
│       ├── api.py              # API pública whitelisted
│       ├── gamification.py     # Pontos / badges
│       ├── controllers/        # Tutor IA parcial (Groq)
│       ├── services/           # Áudio IA em mock, crypto
│       ├── www/                # Páginas server-rendered (SEO)
│       └── vedium_core/doctype/# DocTypes customizados
├── deploy/                     # Configuração de produção
│   ├── docker-compose.yml      # Compose de produção
│   ├── nginx/                  # Vhosts
│   ├── scripts/                # backup.sh, restore.sh, monitor
│   └── .env.example
├── docs/                       # Documentação canônica
├── scripts/migrations/         # Migrações de dados / oneshots
├── .github/workflows/          # CI/CD (test, deploy, backup, security-check)
├── docker-compose.yml          # Compose de desenvolvimento
├── Dockerfile                  # Imagem dev (workspace bind-mount)
└── Makefile                    # up, down, logs, shell, migrate, backup…
```

---

## Setup local

### Pré-requisitos
- Docker + Docker Compose
- Git
- Node.js 20+ (para build CSS local, opcional)

### Subir

```bash
git clone https://github.com/vedium-global/vedium.git
cd vedium
cp deploy/.env.example .env       # preencha as CHANGE_ME
docker compose up -d
./init.sh                          # inicializa bench dentro do container
./install_apps.sh                  # instala frappe + erpnext + lms
```

Comandos comuns via `make`:

```bash
make up        # docker compose up -d
make logs      # tail -f
make shell     # bash no vedium-frappe
make migrate   # bench --site <site> migrate
make backup    # backup local
make status    # docker compose ps
```

---

## Deploy de produção

Push para `main` dispara o workflow `deploy.yml` (rsync para servidor +
`bench install-app` + `bench migrate` + clear cache).

Segredos necessários no repositório (Settings → Secrets):

| Secret | Para que serve |
|---|---|
| `SSH_PRIVATE_KEY` | Acesso SSH ao servidor |
| `SSH_KNOWN_HOSTS` | Output de `ssh-keyscan <servidor>` |
| `DEPLOY_USER` | Usuário SSH no servidor |
| `DEPLOY_HOST` | IP/hostname do servidor |

Variáveis opcionais (Settings → Variables):

| Variable | Default |
|---|---|
| `SITE_NAME` | `app.vediums.com` |
| `SITE_URL` | `https://vediums.com` |

Detalhes operacionais: [`deploy/RUNBOOK.md`](deploy/RUNBOOK.md).
Segurança detalhada: [`deploy/SECURITY.md`](deploy/SECURITY.md).

---

## Segurança

- TLS 1.2/1.3 via Let's Encrypt (renovação automática).
- HSTS habilitado (2 anos, includeSubDomains).
- Rate limiting no login (nginx).
- Backup criptografado offsite via restic + Wasabi/R2.
- Webhooks de pagamento exigem HMAC válido em produção.
- pip-audit + gitleaks no CI.
- Conformidade LGPD/GDPR (em construção — ver roadmap).

---

## Domínios

| Domínio | Função |
|---|---|
| `vediums.com` | Marketing + páginas SEO (Frappe, host-rewrite) |
| `www.vediums.com` | Redirect → `vediums.com` |
| `app.vediums.com` | LMS + ERP (Frappe, host nativo) |

---

## Contribuindo

- Branches: `feat/<nome>`, `fix/<nome>`, `docs/<nome>`, `chore/<nome>`.
- Commits semânticos (Conventional Commits).
- PR precisa passar no CI (test.yml) e ter 1 review.
- Não modificar `frappe`, `erpnext` ou `lms` — toda customização vive em
  `vedium_core`.

Detalhes: [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Licença

Copyright © 2026 Vedium Global Education. Todos os direitos reservados.

## Contato

- Email: <contato@vediums.com>
- Instagram: <https://www.instagram.com/vediumsglobal/>
- LinkedIn: <https://www.linkedin.com/company/vediums>
