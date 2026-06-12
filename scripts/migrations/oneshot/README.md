# Scripts one-shot — histórico

Scripts criados durante incidentes / sprints de estabilização específicos.
**Não rode nada daqui sem ler antes.** As correções estruturais já foram
incorporadas ao `docker-compose.yml`, ao deploy e às migrações regulares.

| Script | Sprint | O que fez | Aplicado em |
|---|---|---|---|
| `fix_db_grant.py` | P0 — MariaDB | Corrigiu `GRANT 'frappe'@'%'` (antes estava amarrado a IP do container) | docker-compose.yml |
| `fix_workers.py` / `fix_workers2.py` | P0 — Workers | Adicionou containers `worker-default`, `worker-long`, `worker-short`, `scheduler` | docker-compose.yml |
| `fix_healthcheck.py` | P0 — Healthcheck | Healthcheck do `vedium-frappe` com `Host: app.vediums.com` | docker-compose.yml |
| `fix_compose.py` | P0 — Compose | Refactor com anchors x-frappe-env / x-frappe-volumes | docker-compose.yml |
| `fix_env.py` | P0 — Env | Preenchimento idempotente de `.env` em produção | runbook |
| `fix_nginx_pwa.py` | P0 — PWA | Alias `/sw.js` e `/manifest.json` no nginx | deploy/nginx/vediums.com.conf |
| `check_db.py` | P0 — Diag | Diagnóstico de conexão MariaDB | — |
| `sample_data.py` | Setup inicial | Placement Test de exemplo (dados de demonstração) | — |
| `crypto_setup.py` | Setup inicial | Seed de moedas BRL/USD + stub de gateway crypto | install.py cobre moedas via ERPNext |
| `set_perms.py` | Setup inicial | Grant de papéis admin para um usuário específico | usar a UI de Roles do Frappe |

Mantidos para auditoria e referência. Em caso de novo incidente similar,
**leia** o script antigo, mas **reescreva** uma versão atualizada — não confie
que o ambiente onde ele rodou ainda existe.
