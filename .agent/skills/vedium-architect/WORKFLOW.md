# VEDIUM DEVELOPMENT WORKFLOW

Este documento define o ciclo de vida de desenvolvimento do projeto Vedium,
desde a concepção visual até à entrada em produção.

> Última atualização: **2026-07-05** (alinhado com CI/CD real).

---

## 1. ESTRATÉGIA GIT (Git Workflow)

Utilizamos **Feature Branch Workflow**. O código na branch `main` deve estar
sempre pronto para produção — push → deploy automático.

### As Branches

- **main**: Produção. Código estável. **Bloqueada para commits diretos.**
  Push para `main` dispara `deploy.yml` (deploy automatizado).
- **feat/nome**: Para novas features (ex: `feat/chat-groq`, `feat/dark-mode`).
- **fix/nome**: Para correção de erros (ex: `fix/mobile-menu-scroll`).
- **docs/nome**: Documentação.
- **chore/nome**: Ajustes de configuração, dependências.
- **hotfix/nome**: Correções urgentes em produção.

### O Fluxo Diário

1. Atualize o local: `git checkout main` → `git pull origin main`.
2. Crie a branch: `git checkout -b feat/nova-tela-login`.
3. Desenvolva e commite (**Conventional Commits**: `feat:`, `fix:`, `docs:`, `chore:`).
4. Suba para o GitHub: `git push origin feat/nova-tela-login`.
5. Abra um **Pull Request (PR)** para `main`.
6. CI roda automaticamente (`test.yml`): lint + audit + gitleaks + testes.
7. Após review + CI verde → merge → deploy automático.

---

## 2. PROCESSO DE UI/UX (Design System "Raízes de Luxo")

### Princípios

- Dark Mode por padrão (`bg-slate-900` / `bg-slate-800`).
- Tipografia clara (`text-slate-100` / `text-slate-400`).
- Ações primárias em `bg-indigo-600` / `hover:bg-indigo-700`.
- Marca: Azul `#2E6DA4` / Vermelho `#A12D1C`.
- Mobile-first (PWA instalável).

### Workflow de Frontend

1. **Source CSS**: `vedium_core/input.css` — defina classes custom aqui.
2. **Config**: `vedium_core/tailwind.config.js` — cores e extensões do tema.
3. **Build**: `npm run build-css` dentro de `vedium_core/`.
4. **Watch** (durante dev): `npm run watch-css`.
5. **Output**: `vedium_core/vedium_core/public/css/vedium.css`.
6. **NUNCA** usar CSS inline (`style="..."`) salvo exceções documentadas.

### Regras de Página

- Novas páginas: `www/<page-name>.html` + `www/<page_name>.py`.
- Estender layout base via Jinja `{% extends %}` ou `{% block %}`.
- Atualizar `sitemap.py` para incluir a nova página.
- Se multilíngue: criar versões em `www/en/`, `www/es/`, etc.

---

## 3. GARANTIA DE QUALIDADE (QA & Testing)

### Nível 1: Testes do Desenvolvedor (Local)

Antes de abrir o PR:

- [ ] Código roda sem erros no container Docker (`make shell` → `bench start`).
- [ ] Build do Tailwind passa sem avisos (`npm run build-css`).
- [ ] Funcionalidade testada em **Mobile** e **Desktop**.
- [ ] Sem `print()` ou `console.log()` de debug.
- [ ] Testes passam: `pytest -v vedium_core/vedium_core/tests/test_pure_*.py`.
- [ ] Lint passa: `flake8 . --select=E9,F63,F7,F82`.

### Nível 2: Code Review (No Pull Request)

O CI (`test.yml`) roda automaticamente:

- [ ] **Lint (syntax)**: Erros de sintaxe bloqueiam merge.
- [ ] **Lint (style)**: Warnings reportados (não bloqueiam).
- [ ] **pip-audit**: Vulnerabilidades em dependências bloqueiam merge.
- [ ] **gitleaks**: Segredos vazados bloqueiam merge.
- [ ] **Testes pure**: `test_pure_*.py` DEVEM passar.

Review manual verifica:

- [ ] Lógica de negócio segura? Permissões verificadas?
- [ ] Segue padrões do Skill.md?
- [ ] Chaves de API expostas? → **REJEITAR IMEDIATAMENTE**.
- [ ] Endpoints públicos têm rate limiting?
- [ ] DocTypes opcionais usam `_safe_get_all()`?

### Nível 3: Produção (Pós-deploy)

O `deploy.yml` inclui smoke tests automatizados:

- [ ] curl `vediums.com` → HTTP 200/301/302/403.
- [ ] curl `app.vediums.com` → HTTP 200/301/302/403.
- [ ] Healthcheck do container → `healthy`.

O `security-check.yml` roda diariamente:

- [ ] SSL certificate not expiring.
- [ ] POST com Origin funciona (regressão nginx).
- [ ] Containers rodando (≥5).
- [ ] Backup recente.

---

## 4. DOCKER: DEV vs PROD

### Desenvolvimento (local)

```bash
# Subir containers
docker compose up -d            # ou: make up

# Entrar no container
make shell                       # bash no vedium-frappe

# Dentro do container
bench start                      # roda gunicorn + workers + scheduler
bench --site <site> migrate      # migrações de schema
bench build --app vedium_core    # rebuild JS/CSS
```

### Produção (servidor)

```bash
ssh user@servidor
cd /opt/vedium

make status     # ver containers + health
make logs       # tail de todos os logs
make workers    # status das filas Redis + workers
make health     # testar /api/method/ping
make backup     # backup manual via restic
make migrate    # bench migrate
make restart    # reiniciar todos os containers
```

> ⚠️ Gunicorn **NÃO** hot-reloads Python. Após alterar `.py`, SEMPRE
> reiniciar: `docker restart vedium-frappe`.
> Os workers e scheduler TAMBÉM precisam ser reiniciados — eles são processos
> Python de longa duração com módulos carregados uma vez.

---

## 5. DEPLOY (CI/CD)

Push para `main` → `deploy.yml` executa automaticamente:

1. rsync do código para `/opt/vedium/` no servidor.
2. rsync do site institucional para `/opt/vedium/site/`.
3. SSH remoto:
   - `docker cp vedium_core` para dentro do container.
   - `pip install -e apps/vedium_core`.
   - `bench install-app vedium_core` (idempotente).
   - `bench migrate` (aplica alterações de DocType).
   - Migrations oneshot (certificado, PWA icon, email sender).
   - `npm install` + `npm run build-css` + `bench build`.
   - `bench clear-cache` + `bench clear-website-cache`.
   - `docker restart vedium-frappe` + todos os workers.
   - Wait for healthchecks.
4. Smoke test: curl nos dois domínios.

### Secrets necessários no GitHub

| Secret | Para que serve |
|---|---|
| `SSH_PRIVATE_KEY` | Acesso SSH ao servidor |
| `SSH_KNOWN_HOSTS` | `ssh-keyscan <servidor>` |
| `DEPLOY_USER` | Usuário SSH |
| `DEPLOY_HOST` | IP/hostname |

---

## 6. DEFINITION OF DONE (DoD)

Uma tarefa só é "Pronta" quando:

1. ✅ Código está mergeado na `main`.
2. ✅ CSS compilado e responsivo (mobile + desktop).
3. ✅ `bench migrate` testado (se há mudanças de DocType).
4. ✅ UI aprovada visualmente.
5. ✅ Testes `test_pure_*` passam.
6. ✅ CI verde (lint + audit + gitleaks).
7. ✅ Deploy automático concluído com smoke test OK.
8. ✅ Documentação atualizada (se feature nova).

---

## 7. COMANDOS ÚTEIS

### Frontend

```bash
# Watch mode (durante dev)
cd vedium_core && npm run watch-css

# Build final (antes do commit)
cd vedium_core && npm run build-css
```

### Backend

```bash
# Após git pull
bench --site <site> migrate
bench --site <site> clear-cache

# Rebuild assets
bench build --app vedium_core

# Console interativo
bench --site <site> console

# Rodar testes (sem Frappe bench — roda local)
pytest -v vedium_core/vedium_core/tests/test_pure_*.py

# Lint
flake8 vedium_core/vedium_core/ --max-line-length=120
```

### Infraestrutura

```bash
# Status completo
make status && make workers && make health

# Logs de erro
make logs-frappe | grep -i error

# Backup manual
make backup

# Listar snapshots de backup
make restore-list
```
