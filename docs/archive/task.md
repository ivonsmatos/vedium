---

# Sprint P0 — Estabilização Produção (status 2026-05-26)

| Item | Status | Notas |
|------|--------|-------|
| P0.1 Workers + Scheduler | ✅ Done | Stable, all containers healthy |
| P0.2 Backup restic crontab | ✅ Done | `0 2 * * * . /opt/vedium/.env && /opt/vedium/scripts/backup.sh` — **⚠️ precisa configurar `RESTIC_REPOSITORY`, `RESTIC_PASSWORD`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` no `.env`** |
| P0.3 PWA sw.js + manifest | ✅ Done | nginx alias `/opt/vedium/pwa/` → HTTP 200. **⚠️ copiar de novo após update do vedium_core**: `cp /var/lib/docker/volumes/vedium_frappe-bench-data/_data/apps/vedium_core/vedium_core/public/js/sw.js /opt/vedium/pwa/sw.js` |
| P0.4 Audit task.md | ✅ Done | Este arquivo atualizado |
| P0.5 Makefile | ✅ Done | Committed |
| P0.6 Healthchecks | ✅ Done | All containers healthy |
| P0.7 Cloudflare CDN /assets/* | ✅ Done | Cache purgado via API (sw.js + manifest.json) |
| P1.3 DocTypes faltantes | ✅ Done | LMS Certificate, LMS Badge Log, LMS Flashcard, Support Ticket, Coupon criados e migrados |
| Git deploy no servidor | ✅ Done | Deploy key SSH + `/opt/vedium-src` clonado + `scripts/app-deploy.sh` (git pull → rsync → migrate) |
| **Upgrade ERPNext v15 → v16** | ✅ Done | Frappe 16.18.3 / Python 3.14.2 / volume `frappe-bench-v16` — commit `9d83b55` |
| **Grafana node-exporter** | ✅ Done | Adicionado ao docker-compose (profile observability, network_mode:host) — métricas reais de CPU/memória/disco |
| **Grafana alertas** | ✅ Done | 3 regras ativas (CPU>85%, memória>90%, disco>85%) — falso positivo site-down removido |
| **SMTP Grafana** | ⚠️ Pendente | Host corrigido para `smtp.office365.com:587` — **bloqueado: SmtpClientAuthentication desabilitado no tenant M365**. Ver seção "Task 5" abaixo |

---

# Task 8: Migração ERPNext v16 ✅ Concluída (2026-05-26)

> ✅ **UPGRADE CONCLUÍDO (2026-05-26):** Frappe 16.18.3 / ERPNext v16 / Python 3.14.2
> Volume `frappe-bench-v16` (external). Todos os containers healthy.

- [x] Realizar backup completo (Banco + Arquivos).
- [x] Migrar apps para branch `version-16`. ← **CONCLUÍDO** — produção em v16 desde 2026-05-26
- [x] Executar `bench update --upgrade`. ← **CONCLUÍDO** — `pyproject.toml` atualizado para `requires-python = ">=3.11"`
- [x] Validar integridade e Identidade "Raízes de Luxo". ← validado, site saudável

## 1a) Mercado Pago e Basecommerce

- [x] Implementar classes/funções para Mercado Pago e Basecommerce, semelhantes ao Stripe.
- [x] Criar: `create_mercadopago_checkout`, `handle_mercadopago_webhook`.
- [x] Abstrair o fluxo de pagamentos (strategy/factory pattern).
- [x] Centralizar webhooks de pagamentos.

## 1b) Checkout UI/UX

- [/] Oferecer seleção de gateway pelo usuário.
- [x] Implementar tela de histórico de pagamentos/faturas.

## 1c) Entrada de cupons/descontos

- [x] Permitir cupons em promoções e códigos especiais. ← DocType `Coupon` criado e migrado (P1.3 ✅)

## 1d) Testes automatizados para pagamentos

- [x] Simular falha, duplicidade, chargeback nos sandboxes. (Testes unitários com mock implementados)

---

# Task 2: Plataforma de Cursos de Idiomas – Funcionalidades Avançadas

- [x] Certificados digitais automáticos com código de verificação. ← DocType `LMS Certificate` criado e migrado (P1.3 ✅)
- [x] Quiz/prova de nível com feedback instantâneo. ← usa DocTypes do frappe/lms oficial
- [x] Suporte a aulas ao vivo e gravadas (Zoom, Meet, Vimeo/Youtube).
- [x] Feedback automatizado (IA): avaliações de áudio/texto, dashboards. (Serviço de IA integrado)
- [x] Recursos extras: escuta ativa, gravação de áudio, flashcards. ← DocType `LMS Flashcard` criado (P1.3 ✅)
- [x] Gamificação: emblemas, níveis, rankings. ← DocType `LMS Badge Log` criado (P1.3 ✅)
- [x] Comunidade: fórum, integração Telegram/Discord/Slack.
- [x] Acessibilidade e internacionalização.

---

# Task 3: UI/UX e Layout – Raízes de Luxo

- [x] **Substituição de Layout**: Migração completa para o tema "Zilom" com branding "Vedium".
- [ ] **Conteúdo e Tradução (PT-BR)**:
  - [x] Hero Section: Headlines e CTAs.
  - [x] Pilares: Diferenciais e Tecnologia.
  - [x] Soluções: Corporate, Pro, Students, Kids.
  - [x] Trilhas: Descrições dos idiomas.
  - [x] Prova Social: Depoimentos.
  - [ ] Menus e Rodapé: Tradução geral e ajustes finais.
- [x] Auditoria prática do Design System em TODOS os apps (LMS, CRM, ERP).
- [x] Padronização de botões, fontes (Inter/Bodoni) e cores (Raízes de Luxo v2 - #26528C, #BFA288).
- [x] Microinterações: animações em CTAs, feedback AJAX, loading states.
- [x] Performance: Lighthouse, lazy loading, SVGs otimizados, Service Worker customizado.
- [x] Cadastro/onboarding: frases motivacionais, progresso, login Google/Linkedin.
- [x] Escalabilidade visual: white-label/skinning.

---

# Task 4: Segurança Avançada

- [/] Pentest regular (OWASP ZAP, etc). (Agendado/Documentado)
- [/] Gestão de segredo: variáveis de ambiente. (Parcialmente verificado)
- [x] Auditoria de dependências: alertas automáticos.

---

# Task 5: Observabilidade e Suporte

- [x] Painel de suporte para chamados. ← DocType `Support Ticket` criado e migrado (P1.3 ✅)
- [x] **Monitoramento automático: stack Prometheus/Grafana rodando em produção** (profile `observability`)
  - [x] Prometheus coletando métricas — targets: `node-exporter` + `prometheus` (2/2 UP)
  - [x] node-exporter instalado (`network_mode: host`) — CPU, memória, disco do host
  - [x] Grafana v13.0.1 com 3 alertas ativos: CPU >85%, Memória >90%, Disco >85%
  - [x] Uptime Kuma monitorando uptime do site (http + TLS)
  - [⚠️] **SMTP Grafana bloqueado**: tenant Microsoft 365 tem `SmtpClientAuthentication` desabilitado
    - SMTP host já configurado: `smtp.office365.com:587`
    - **Fix opção A**: Exchange Admin Center → Recipients → `contato@ivonmatos.com.br` → Mail flow → SMTP AUTH → Enable
    - **Fix opção B**: Criar conta Gmail dedicada para alertas e trocar SMTP para `smtp.gmail.com:587`
    - Ref: https://aka.ms/smtp_auth_disabled
- [x] Métricas: Google Analytics 4, Hotjar/Clarity, LGPD.

---

# Task 7: Frappe LMS (Official)

- [x] Instalar o app `erpnext`, `crm`, `hrms` e `helpdesk`.
- [x] Configurar o Portal LMS inicial.
- [x] Configurar Central de Ajuda e Suporte ao Cliente (Help Desk).
- [x] Configurar Módulo de RH (HRMS) e Operações de Pessoal.
- [x] Implementar Teste de Nivelamento (Placement Test) no LMS.
- [x] Implementar Agendamento de Aulas Individuais (Booking System).
- [x] Implementar Flashcards (SRS). ← DocType `LMS Flashcard` criado e migrado (P1.3 ✅)
- [ ] Expandir IA de Pronúncia para Análise Fonética. ← P3 (requer GPU ou Replicate API)
- [x] Configurar Gamificação (Pontos, Níveis, Rankings). ← DocType `LMS Badge Log` criado e migrado (P1.3 ✅)
- [x] Migrar as customizações do `vedium_core` (Mercado Pago, IA) para trabalhar com o oficial.

---

## DocTypes faltantes (bloqueadores P1.3)

> Código referencia estes DocTypes que **não existem** no banco/app ainda.
> Criar em `vedium_core/doctype/` na Fase P1.

| DocType           | Usado em                    | Prioridade           |
| ----------------- | --------------------------- | -------------------- |
| `LMS Certificate` | `api.py`, `gamification.py` | ✅ Criado 2026-05-25 |
| `LMS Badge Log`   | `gamification.py`           | ✅ Criado 2026-05-25 |
| `LMS Flashcard`   | `api.py`                    | ✅ Criado 2026-05-25 |
| `Support Ticket`  | `api.py`                    | ✅ Criado 2026-05-25 |
| `Coupon`          | `api.py`                    | ✅ Criado 2026-05-25 |
