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
| P0.7 Cloudflare CDN /assets/* | ❌ Requer CF panel | Precisa purgar cache /sw.js e /manifest.json no dashboard CF |

---

# Task 8: Migração ERPNext v16 (Estável)

> ⚠️ **AUDITORIA P0 (2026-05-25):** A documentação menciona "ERPNext v16" mas a produção
> roda `frappe/erpnext:v15`. v16 NÃO está em uso. Atualizado abaixo para refletir a realidade.

- [x] Realizar backup completo (Banco + Arquivos).
- [ ] Migrar apps para branch `version-16`. ← **NÃO FEITO** — produção está em v15 (decisão: manter v15, migrar Q3 2026)
- [ ] Executar `bench update --upgrade`. ← **NÃO FEITO** (dependente do item acima)
- [x] Validar integridade e Identidade "Raízes de Luxo". ← parcial

## 1a) Mercado Pago e Basecommerce

- [x] Implementar classes/funções para Mercado Pago e Basecommerce, semelhantes ao Stripe.
- [x] Criar: `create_mercadopago_checkout`, `handle_mercadopago_webhook`.
- [x] Abstrair o fluxo de pagamentos (strategy/factory pattern).
- [x] Centralizar webhooks de pagamentos.

## 1b) Checkout UI/UX

- [/] Oferecer seleção de gateway pelo usuário.
- [x] Implementar tela de histórico de pagamentos/faturas.

## 1c) Entrada de cupons/descontos

- [ ] Permitir cupons em promoções e códigos especiais. ← **DocType `Coupon` não declarado no app** — endpoint existe mas quebra em runtime (P1.3)

## 1d) Testes automatizados para pagamentos

- [x] Simular falha, duplicidade, chargeback nos sandboxes. (Testes unitários com mock implementados)

---

# Task 2: Plataforma de Cursos de Idiomas – Funcionalidades Avançadas

- [ ] Certificados digitais automáticos com código de verificação. ← **DocType `LMS Certificate` não declarado** — quebra em runtime (P1.3)
- [x] Quiz/prova de nível com feedback instantâneo. ← usa DocTypes do frappe/lms oficial
- [x] Suporte a aulas ao vivo e gravadas (Zoom, Meet, Vimeo/Youtube).
- [x] Feedback automatizado (IA): avaliações de áudio/texto, dashboards. (Serviço de IA integrado)
- [/] Recursos extras: escuta ativa, gravação de áudio, flashcards. ← **DocType `LMS Flashcard` não declarado** — placeholder apenas (P1.3)
- [ ] Gamificação: emblemas, níveis, rankings. ← **DocType `LMS Badge Log` não declarado** — código existe, DocType não (P1.3)
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

- [ ] Painel de suporte para chamados. ← **DocType `Support Ticket` não declarado** — placeholder (P1.3)
- [ ] Monitoramento automático: dashboard, webhooks para falhas/fraudes. ← Stack Prometheus/Grafana configurada mas NÃO rodando (workers faltavam — corrigido P0.1)
- [x] Métricas: Google Analytics 4, Hotjar/Clarity, LGPD.

---

# Task 7: Frappe LMS (Official)

- [x] Instalar o app `erpnext`, `crm`, `hrms` e `helpdesk`.
- [x] Configurar o Portal LMS inicial.
- [x] Configurar Central de Ajuda e Suporte ao Cliente (Help Desk).
- [x] Configurar Módulo de RH (HRMS) e Operações de Pessoal.
- [x] Implementar Teste de Nivelamento (Placement Test) no LMS.
- [x] Implementar Agendamento de Aulas Individuais (Booking System).
- [ ] Implementar Flashcards (SRS). ← **DocType `LMS Flashcard` não declarado** (P1.3)
- [ ] Expandir IA de Pronúncia para Análise Fonética. ← P3 (requer GPU ou Replicate API)
- [ ] Configurar Gamificação (Pontos, Níveis, Rankings). ← **DocType `LMS Badge Log` não declarado** (P1.3)
- [x] Migrar as customizações do `vedium_core` (Mercado Pago, IA) para trabalhar com o oficial.

---

## DocTypes faltantes (bloqueadores P1.3)

> Código referencia estes DocTypes que **não existem** no banco/app ainda.
> Criar em `vedium_core/doctype/` na Fase P1.

| DocType           | Usado em                    | Prioridade |
| ----------------- | --------------------------- | ---------- |
| `LMS Certificate` | `api.py`, `gamification.py` | P1.3       |
| `LMS Badge Log`   | `gamification.py`           | P1.3       |
| `LMS Flashcard`   | `api.py`                    | P1.3       |
| `Support Ticket`  | `api.py`                    | P1.3       |
| `Coupon`          | `api.py`                    | P1.3       |
