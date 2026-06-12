# Vedium — Arquitetura & Infraestrutura Proposta

> Documento estratégico consolidado. Versão 1.0 — 2026-05-17
> Base: análise do código (`vedium_core/`), estado do servidor (45.151.122.234),
> docs internos (`README.md`, `ARQUITETURA.md`, `ESTADO_ATUAL.md`, `task.md`) e
> contexto de negócio (CNPJ 58.434.869/0001-24 — VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA).

---

## 1. Resumo Executivo

A Vedium é uma **EdTech high-ticket B2B + B2C premium** (Inglês Executivo, Hebraico
Tech, Iorubá Ancestral) construída sobre **Frappe/ERPNext + LMS**. O stack é o
correto para o estágio: um monólito metadata-driven que entrega ERP, CRM, LMS e
HR num único produto, com TCO baixo.

**Estado real (não o documentado):**

- ✅ Stack rodando estável em produção (`app.vediums.com`).
- ✅ Empresa, plano de contas (86 contas), CRM básico configurados.
- ⚠️ **Documentação mente sobre versões**: README diz "Frappe v16 / Python 3.14
  / Node 24" — a produção roda `frappe/erpnext:v15`, Python 3.11, Node 20.
- 🚨 **Workers e scheduler do Frappe não estão rodando** (faltam containers).
  Consequência prática: emails de confirmação, jobs assíncronos, tarefas
  agendadas (backup, reindex, métricas) **não executam**.
- 🚨 `task.md` marca como `[x]` features (certificados, gamificação, quiz,
  fórum, flashcards) que dependem de **DocTypes customizados não declarados
  no app** — o código os referencia mas eles não existem no banco.
- 🚨 **PWA quebrada**: console retorna `sw.js 404`.
- 🚨 Sem backup automatizado verificado, sem replicação, sem observabilidade
  ativa, sem CI/CD funcional.

**Prioridade:** estabilizar o que existe **antes** de adicionar mais features.

---

## 2. Contexto de Negócio (do que a arquitetura precisa servir)

| Dimensão | Realidade |
|---|---|
| **Modelo** | LMS premium + ERP corporativo + CRM B2B |
| **Ticket** | High-ticket (cursos premium + contratos B2B) |
| **Volume** | Baixo-médio (centenas/milhares de alunos, não milhões) |
| **Margem** | Alta — não pode haver downtime nem perda de receita |
| **Compliance** | LGPD obrigatório, emissão fiscal Brasil (NF-e/NFS-e futura) |
| **Geografia** | Brasil primário; alunos globais (multi-fuso, multi-idioma) |
| **Diferencial** | UX premium "Raízes de Luxo" — UI lenta = quebra de proposta |

**Implicação arquitetural:** otimizar para **confiabilidade + UX**, não para escala
horizontal massiva. Single-region é suficiente. **Backups, observabilidade e
performance percebida** valem mais que sharding.

---

## 3. Princípios Arquiteturais (não-negociáveis)

1. **Frappe-first**: nunca forkar `frappe/lms/erpnext`. Tudo via `vedium_core`
   (hooks, custom fields, overrides).
2. **Stateless workers, stateful data**: app é descartável, dados são sagrados.
   Toda mudança no schema passa por migração versionada.
3. **Single source of truth**: 1 banco MariaDB (produção) + 1 Redis (3
   instâncias lógicas: cache/queue/socketio).
4. **Observabilidade nativa**: cada novo serviço expõe `/health` e métricas
   Prometheus. Sem isso, não vai pra prod.
5. **Secrets fora do repo**: tudo em `.env` no servidor, futuramente Doppler/Vault.
6. **CI = gate**: nada vai pra `main` sem testes + lint + security check passando.
7. **PR pequeno**: um deploy = uma mudança. Reverter precisa ser trivial.

---

## 4. Arquitetura Alvo

### 4.1 Visão de Camadas

```
┌─────────────────────────────────────────────────────────────────┐
│  EDGE        Cloudflare (DNS + WAF + CDN + DDoS) → assets/* CDN │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│  INGRESS     Nginx (TLS 1.3, HSTS, rate-limit, gzip/brotli)     │
└────────┬───────────────────────┬──────────────────────┬─────────┘
         │ /                     │ /socket.io           │ /assets
         ▼                       ▼                      ▼
┌────────────────┐      ┌────────────────┐      ┌────────────────┐
│ vedium-frappe  │      │ vedium-socketio│      │  Cloudflare    │
│ (gunicorn x4)  │      │ (node)         │      │  R2 / CDN      │
│ custom_wsgi    │      │                │      │  cache 1y      │
└───┬───────┬────┘      └────────┬───────┘      └────────────────┘
    │       │                    │
    │       │ enqueue            │ pub/sub
    │       ▼                    ▼
    │   ┌────────────────────────────────┐
    │   │ vedium-worker-default          │  ⚠ FALTA HOJE
    │   │ vedium-worker-long             │  ⚠ FALTA HOJE
    │   │ vedium-worker-short            │  ⚠ FALTA HOJE
    │   │ vedium-scheduler (cron)        │  ⚠ FALTA HOJE
    │   └─────────┬──────────────────────┘
    │             │
    ▼             ▼
┌────────────────────────────────┐    ┌──────────────────────────┐
│  vedium-mariadb 10.6           │    │  vedium-redis-cache      │
│  - 1 master                    │    │  vedium-redis-queue      │
│  - daily logical backup → S3   │    │  vedium-redis-socketio   │
│  - hourly snapshot volume      │    └──────────────────────────┘
└────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  OBSERVABILIDADE                                                │
│  Prometheus → Grafana → Alertmanager → Telegram/Email           │
│  Loki (logs) ← promtail (todos os containers)                   │
│  Uptime: Uptime Kuma (push de health checks)                    │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Stack Final (versões pinadas, alinhadas com a realidade)

| Camada | Tecnologia | Versão | Por quê |
|---|---|---|---|
| Edge | Cloudflare | — | DNS + WAF + CDN gratuito; já tem |
| Ingress | Nginx | 1.27 | Já em uso; otimizar config |
| App | Frappe Framework | **v15** (não v16) | v16 ainda não estável; migrar depois |
| ERP | ERPNext | v15 | Idem |
| LMS | frappe/lms | v15 | Idem |
| Pagamentos | frappe/payments + Stripe + MercadoPago | — | Já integrado |
| Linguagem | Python | 3.11 | Vem com a imagem oficial Frappe |
| Frontend SSR | Jinja2 + Tailwind | v3.4 | Já em uso |
| Frontend SPA | Vue 3 + Vite (do LMS) | — | Build automatizado no Docker |
| Banco | MariaDB | 10.6 | Compatibilidade Frappe |
| Cache/Queue | Redis | 7-alpine | x3 instâncias lógicas |
| Container | Docker + Compose v2 | — | Sem Kubernetes — overkill |
| Métricas | Prometheus + Grafana | latest | Já tem `prometheus.yml` |
| Logs | Loki + Promtail | latest | Centralização barata |
| Uptime | Uptime Kuma | latest | Self-host gratuito |
| Backup | restic + S3 (Wasabi/R2) | — | Encriptado, versionado |
| CI/CD | GitHub Actions | — | Já existe estrutura |
| Secrets | `.env` → Doppler (futuro) | — | Migração P2 |

> **Decisão crítica:** **NÃO migrar para Frappe v16 agora.** A v15 está estável,
> os apps oficiais (lms, erpnext, payments) têm suporte LTS, e v16 ainda quebra
> integrações. Atualizar a documentação para refletir v15 — **honestidade > marketing interno**.

### 4.3 Camada de Aplicação — Reorganização do `vedium_core`

**Estrutura atual** (problemática — tudo solto em `vedium_core/`):

```
vedium_core/
├── api.py              ← 900 linhas, faz tudo
├── gamification.py
├── geo_endpoints.py
├── crypto_setup.py
├── controllers/
│   └── ai_controller.py
├── services/
│   ├── ai_service.py
│   └── crypto_service.py
└── www/                ← HTML solto
```

**Estrutura proposta** (modular por domínio):

```
vedium_core/
├── hooks.py
├── install.py
├── modules.txt
│
├── doctype/                          ← TODOS os DocTypes customizados aqui
│   ├── lms_certificate/              ← Hoje referenciado, não existe
│   ├── lms_badge_log/
│   ├── lms_flashcard/
│   ├── support_ticket/
│   └── coupon/
│
├── api/                              ← Endpoints whitelisted, 1 arquivo por domínio
│   ├── __init__.py
│   ├── payments.py                   ← create_checkout, webhooks
│   ├── courses.py                    ← get_published_courses, etc.
│   ├── certificates.py
│   ├── gamification.py
│   ├── support.py
│   └── public.py                     ← contact form, etc.
│
├── services/                         ← Lógica de negócio reusável
│   ├── gateways/
│   │   ├── base.py                   ← PaymentGateway ABC
│   │   ├── stripe_gw.py
│   │   ├── mercadopago_gw.py
│   │   ├── basecommerce_gw.py
│   │   └── crypto_gw.py
│   ├── ai_service.py
│   ├── certificate_service.py
│   └── notification_service.py
│
├── hooks/                            ← Document Events organizados
│   ├── lms_course_progress.py
│   └── lms_enrollment.py
│
├── tasks/                            ← scheduler_events
│   ├── daily.py
│   ├── hourly.py
│   └── weekly.py
│
├── permissions/
│   └── lms_permissions.py
│
├── www/                              ← Páginas públicas (site institucional)
│   ├── index.html / index.py
│   ├── catalogo.html / catalogo.py
│   └── ...
│
├── templates/
│   ├── includes/
│   └── pages/
│
├── public/
│   ├── css/                          ← compilado (output do Tailwind)
│   ├── js/
│   ├── images/
│   └── manifest.json
│
└── tests/
    ├── test_payments.py
    ├── test_certificates.py
    └── test_api.py
```

**Ganho:** localizar bug em `create_checkout` vai de "grep nos 900 linhas" para
"abrir `api/payments.py`". Onboarding de dev novo cai de dias para horas.

---

## 5. Roadmap em 4 Fases

### Fase P0 — Estabilização (1–2 semanas) — **OBRIGATÓRIO**

**Objetivo:** parar de sangrar. Tornar o que existe confiável.

| # | Tarefa | Impacto | Esforço |
|---|---|---|---|
| P0.1 | Adicionar containers `vedium-worker-default`, `vedium-worker-long`, `vedium-worker-short`, `vedium-scheduler` ao `docker-compose.yml` | 🔴 Crítico — desbloqueia emails, cron, fila | 2h |
| P0.2 | Backup automatizado: `restic` daily → Wasabi/R2 com retenção 30d + teste de restore mensal | 🔴 Crítico — perda de dados = empresa morta | 4h |
| P0.3 | Corrigir PWA: gerar `sw.js` e `manifest.json` corretos servidos em `/sw.js` e `/manifest.json` (nginx ou frappe) | 🟠 UX premium quebrado | 2h |
| P0.4 | Auditar `task.md`: marcar como `[ ]` o que **não tem DocType declarado**. Criar issues por feature. Sincronizar README com realidade (v15, não v16) | 🔴 Confiar nos docs = bug futuro | 3h |
| P0.5 | Centralizar `docker-compose.yml`: deletar o da raiz, manter só `deploy/docker-compose.yml`. Adicionar `Makefile` com targets `make up / down / logs / shell / migrate / backup` | 🟡 DX | 2h |
| P0.6 | Healthchecks em todos os containers (`HEALTHCHECK` no Dockerfile + `depends_on: condition: service_healthy`) | 🟠 Crashloop silencioso hoje | 2h |
| P0.7 | Configurar Cloudflare como CDN para `/assets/*` (cache 1 ano com hash no nome) | 🟡 Performance percebida | 1h |

**Critério de saída P0:**

- [ ] `curl https://app.vediums.com/api/method/ping` retorna 200 em <300ms.
- [ ] Email de confirmação chega ao se inscrever num curso.
- [ ] Backup automático rodando + 1 restore testado em servidor de staging.
- [ ] `task.md` reflete realidade.
- [ ] Score Lighthouse mobile >85.

### Fase P1 — Produção Robusta (3–4 semanas)

**Objetivo:** ter um produto operacionalmente maduro.

| # | Tarefa | Impacto | Esforço |
|---|---|---|---|
| P1.1 | Stack de observabilidade: Prometheus + Grafana + Loki + Promtail + Alertmanager (Telegram alerts) | 🔴 Hoje você não sabe se está caindo | 1d |
| P1.2 | Refatorar `vedium_core` para a estrutura modular (seção 4.3) | 🟠 Velocidade de desenvolvimento | 2–3d |
| P1.3 | Criar DocTypes que o código referencia: `LMS Certificate`, `LMS Badge Log`, `LMS Flashcard`, `Support Ticket`, `Coupon`, etc. | 🔴 Endpoints atualmente quebram em runtime | 2d |
| P1.4 | CI/CD real: GitHub Actions com `pytest`, `flake8`, `black`, `bandit` (security), build do CSS, deploy automático para staging | 🟠 Hoje deploy é "git pull + reza" | 1d |
| P1.5 | Ambiente de **staging** (`staging.vediums.com`) com dados sintetizados — espelho do prod | 🔴 Hoje testa-se em produção | 1d |
| P1.6 | Rate limiting na aplicação (`frappe.rate_limiter`) em endpoints críticos: login, checkout, webhooks, contato | 🟠 Brute-force / spam | 4h |
| P1.7 | LGPD: página `/privacidade`, banner de cookies, endpoint `delete_my_data`, registro de consentimento | 🔴 Lei | 1d |
| P1.8 | Migrar secrets para Doppler ou 1Password Secrets Automation (mantém `.env` local mas centraliza prod) | 🟡 Rotação de senha sem deploy | 4h |

**Critério de saída P1:**

- [ ] Dashboard Grafana com SLOs visíveis (uptime, p95 latência, erro 5xx %).
- [ ] Alerta no Telegram quando container reinicia ou disco >80%.
- [ ] PR mergeado dispara deploy automático em staging.
- [ ] Página `/privacidade` no ar.

### Fase P2 — Escala & Conversão (4–6 semanas)

**Objetivo:** sustentar crescimento e otimizar funil.

| # | Tarefa | Impacto |
|---|---|---|
| P2.1 | Read replica MariaDB para queries pesadas (relatórios ERP) | Performance |
| P2.2 | Migrar uploads de mídia para Cloudflare R2 (vídeos das aulas, certificados) — Frappe S3 backend | Custo + velocidade |
| P2.3 | Stripe Tax + nota fiscal automática (NFS-e via webhook → emissor brasileiro tipo NFE.io) | Fiscal |
| P2.4 | Checkout one-page otimizado (não usar fluxo padrão do Frappe — fazer SPA Vue) | Conversão |
| P2.5 | A/B testing framework (GrowthBook self-hosted ou simples toggle via custom field) | Otimização |
| P2.6 | Pixel Meta + GA4 server-side + UTM tracking persistente | Atribuição |
| P2.7 | Email marketing transacional via Resend ou Postmark (não usar SMTP genérico) | Deliverability |
| P2.8 | Multi-idioma real: PT/EN/ES (i18n do Frappe + traduções customizadas) | Internacional |

### Fase P3 — Diferenciação (8+ semanas)

**Objetivo:** features que justificam o ticket premium.

- IA de pronúncia real (Whisper + análise fonética via servidor GPU dedicado ou Replicate API).
- App mobile React Native (não dependa de PWA).
- Marketplace de professores (B2B2C — Vedium ganha % por aula).
- Integração Zoom/Meet nativa para aulas ao vivo.
- Whitelabel para escolas parceiras (multi-tenancy por subdomínio).

---

## 6. Decisões Arquiteturais Críticas (com trade-offs)

### Decisão 1 — Manter monólito Frappe, NÃO microsserviços

**Por quê:** Frappe entrega ERP + CRM + LMS + HR num único produto. Quebrar
em microsserviços traz complexidade operacional (auth distribuída, transações
distribuídas, deploy coordenado) sem ganho real para o volume previsto.

**Trade-off aceito:** acoplamento alto entre módulos. Mitigação: usar o
`vedium_core` modular (seção 4.3) para isolar lógica customizada.

### Decisão 2 — Docker Compose, NÃO Kubernetes

**Por quê:** 1 servidor, 1 DB, ~50k requests/dia previstos = Compose dá conta.
K8s adiciona 3–5 camadas de complexidade que você paga sem usar.

**Trade-off aceito:** sem auto-scaling horizontal. Mitigação: vertical scaling
fácil (servidor tem 47GB RAM, está usando 5GB).

### Decisão 3 — MariaDB single-master, sem cluster

**Por quê:** Galera/InnoDB Cluster aumenta latência de write e complica
backup. Para o ticket atual, RPO de 24h (backup diário) é aceitável; RTO de
1h é alcançável com restore + DNS switch.

**Trade-off aceito:** janela de downtime em falha de hardware. Mitigação:
backup contínuo binlog + replica passiva em servidor secundário (P2).

### Decisão 4 — Cloudflare como Edge, NÃO AWS CloudFront

**Por quê:** já está sendo usado (DNS), free tier suficiente, R2 sem egress fee.

**Trade-off aceito:** lock-in moderado. Mitigação: tudo configurável via API,
trocável em 1 dia se necessário.

### Decisão 5 — Frappe v15, NÃO v16

**Por quê:** v16 ainda quebra apps do ecossistema (lms tem PRs abertos, payments
sem release v16 estável). Migração de schema é não-trivial.

**Trade-off aceito:** ficar 1 major atrás. Mitigação: planejar migração para Q3
2026 quando v16 estiver maduro.

---

## 7. Riscos Atuais e Mitigação Imediata

| # | Risco | Probabilidade | Impacto | Mitigação P0 |
|---|---|---|---|---|
| R1 | Perda de dados (sem backup verificado) | Média | **Catastrófico** | P0.2 — restic + restore mensal |
| R2 | Workers fora do ar → emails não saem → cliente reclama | Alta | Alto | P0.1 — adicionar workers |
| R3 | DocTypes faltantes → endpoints crasham em runtime quando alguém usa | Alta | Médio | P1.3 — criar DocTypes ou remover endpoints |
| R4 | Senha admin única (reutilizada, **PRECISA SER ROTACIONADA**) — sem rotação, sem MFA | Alta | Alto | P0+ — rotacionar a senha, ativar 2FA no Administrator, criar usuário pessoal Ivon |
| R5 | Server compartilhado com 7+ projetos (Optimahub, EcoMed, OpenProject, Vetta) — vizinhança ruidosa pode derrubar tudo | Média | Alto | P2 — separar VPS dedicado para Vedium quando faturar >R$30k/mês |
| R6 | Sem CDN — todo asset pesa no gunicorn | Alta | Médio | P0.7 — Cloudflare |
| R7 | Docs mentem (v16 vs v15) → onboarding de dev futuro vai falhar | Alta | Médio | P0.4 — sincronizar |
| R8 | Sem ambiente de staging — testa-se em produção | Alta | Alto | P1.5 — staging |

---

## 8. O que Fazer ESTA SEMANA (Próximos Passos Concretos)

**Sprint imediato — 5 dias úteis:**

```
Dia 1 (segunda)
  - [ ] P0.1 — adicionar workers + scheduler no docker-compose
  - [ ] P0.6 — healthchecks
  - [ ] Testar: enviar email, verificar fila

Dia 2 (terça)
  - [ ] P0.2 — script restic, primeiro backup, teste de restore
  - [ ] Configurar cronjob no host

Dia 3 (quarta)
  - [ ] P0.4 — auditar task.md, sincronizar README, listar DocTypes faltantes
  - [ ] P0.5 — Makefile + remover docker-compose duplicado

Dia 4 (quinta)
  - [ ] P0.3 — corrigir PWA (sw.js + manifest)
  - [ ] P0.7 — Cloudflare CDN para /assets/*

Dia 5 (sexta)
  - [ ] Smoke test full: login, comprar curso (sandbox), receber email, ver no ERP
  - [ ] Commit + push de tudo
  - [ ] Documentar runbook em deploy/RUNBOOK.md
```

---

## 9. Métricas de Sucesso (como saber se a arquitetura está funcionando)

| Métrica | Target | Como medir |
|---|---|---|
| **Uptime** | >99.5% mês | Uptime Kuma |
| **p95 latência** | <500ms | Prometheus (frappe_request_duration) |
| **Erro 5xx** | <0.1% requests | Loki |
| **Lighthouse mobile** | >85 | Lighthouse CI no GH Actions |
| **TTM deploy** | <10min do push ao live | GH Actions |
| **MTTR** | <30min | Alertmanager → on-call |
| **Backup RPO/RTO** | 24h / 1h | Teste mensal de restore |
| **Conversão checkout** | >40% (visitante → comprador) | GA4 + custom DocType "Funnel Event" |

---

## 10. Apêndice — Arquivos Críticos a Alterar/Criar

| Arquivo | Ação | Fase |
|---|---|---|
| `deploy/docker-compose.yml` | Adicionar workers, scheduler, prometheus, grafana, loki, promtail | P0/P1 |
| `deploy/.env.example` | Atualizar com novas vars (RESTIC_PASSWORD, GRAFANA_PWD, etc.) | P0 |
| `deploy/scripts/backup.sh` | Reescrever para usar restic | P0 |
| `deploy/scripts/restore.sh` | **CRIAR** — não existe hoje | P0 |
| `deploy/RUNBOOK.md` | **CRIAR** — procedimentos de incidente | P0 |
| `deploy/nginx/vediums.com.conf` | Otimizar cache, rate-limit | P0/P1 |
| `Makefile` | **CRIAR** | P0 |
| `vedium_core/hooks.py` | Limpar, organizar, adicionar `scheduler_events` reais | P1 |
| `vedium_core/api.py` | **QUEBRAR** em `api/payments.py`, `api/courses.py`, etc. | P1 |
| `vedium_core/doctype/*` | **CRIAR** DocTypes faltantes | P1 |
| `vedium_core/tests/` | **CRIAR** suite de testes mínima | P1 |
| `.github/workflows/ci.yml` | **CRIAR/AJUSTAR** | P1 |
| `README.md` | Reescrever — refletir realidade (v15) | P0 |
| `task.md` | Reauditar item por item | P0 |
| `ARQUITETURA.md` | Substituir pelo conteúdo deste documento | P0 |

---

**Próximo passo recomendado:** aprovar este documento e iniciar **Sprint P0 — Dia 1**
amanhã. Posso começar pelo `docker-compose.yml` com workers e scheduler — é a
mudança de maior impacto e menor risco.
