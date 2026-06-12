# Changelog

Registro de mudanças relevantes do Vedium. Formato baseado em
[Keep a Changelog](https://keepachangelog.com/) (datas absolutas, ordem
cronológica reversa).

## [Não lançado] — 2026-06-11 (QA rodada 2)

### Adicionado (fechamento dos QAs)
- **E-mail de boas-vindas na confirmação de matrícula** (fila de e-mail,
  nunca bloqueia a matrícula se falhar).
- **Check de regressão no CI diário**: POST com header Origin em
  `app.vediums.com/api/method/ping` — pega o bug histórico GET=200/POST=404
  que o curl simples mascarava.
- `custom_setup.setup_custom_fields` agora roda no `after_migrate`
  (idempotente) — garante `User.vedium_points`, dependência da gamificação.

### Removido (fechamento dos QAs)
- Hook `boot_session` e módulo `startup/` (no-op morto).
- Scripts seed retirados do pacote deployado: `sample_data.py`,
  `crypto_setup.py`, `set_perms.py` → `scripts/migrations/oneshot/`
  (set_perms continha grant de admin hardcoded).

### Robustez
- Rate-limit (formulários públicos e AI Tutor) migrado para **janela fixa
  por bucket de tempo** — elimina o caso em que `incr` sem TTL deixava a
  chave órfã e bloqueava o IP/usuário para sempre.

### Corrigido
- **Cupom com `max_uses` agora é consumido de verdade**: `used_count` é
  incrementado (UPDATE atômico) quando o pagamento confirma. Cupom viaja no
  `metadata.coupon_code` (Stripe) e no 3º segmento do `external_reference`
  (Mercado Pago, retrocompatível com o formato antigo de 2 segmentos).
- `analytics_events.py`: `NameError` por `_` não importado; consultas agora
  só enxergam cursos publicados (não vaza título/preço de rascunho).
- `/aluno_360`: redirect de login aponta para `app.vediums.com/login`
  (relativo quebrava via vediums.com).

### Segurança
- **Gateway crypto desabilitado por padrão**: exige `CRYPTO_ENABLED` +
  `CRYPTO_API_KEY` no site_config. `crypto_service.py` não retorna mais
  URL mock nem "COMPLETED" falso sem API key — agora falha explicitamente.
- **Rate-limit por IP** nos formulários públicos: contato (5/h) e
  candidatura (3/h).
- Criação do DocType `Candidatura` movida para `after_migrate` (não mais
  disparada por request de guest).
- `get_monitoring_dashboard` restrito a System Manager/Vedium Ops e agora
  retorna dados REAIS (Error Log 24h, scheduler, último backup, tamanho do
  banco) em vez de valores aleatórios.

### Alterado
- **Endpoints GEO (`/ai/*.json`) reescritos com a oferta real**: idiomas
  derivados do catálogo publicado, telefone do CNPJ, URLs `/curso/<slug>` e
  `/catalogo`, pagamentos Stripe/Mercado Pago. Removidas alegações falsas
  (Tech Hebrew, crypto, free trial, /pricing, /practice) — art. 30 CDC.
- **PWA formalmente desativado**: `web_manifest` removido do hooks, link de
  manifest removido do base.html, `sw.js` substituído por kill-switch que
  desregistra o SW antigo e limpa caches nos navegadores de quem já visitou.
- 4 novos testes pure para parsing do `external_reference` (21 no total).

### Adicionado
- `docs/ARCHITECTURE.md` — documento canônico de arquitetura.
- `CHANGELOG.md` — este arquivo.
- `scripts/migrations/oneshot/README.md` — histórico dos scripts P0.
- Fallback defensivo em endpoints que consultam DocTypes opcionais
  (forum, comunidade, idiomas, acessibilidade, sessões, flashcards, quizzes).
- Testes pure (sem Frappe bench) para lógica de cupom.
- Endpoint `/sitemap.xml` com `Content-Type: application/xml`.

### Alterado
- Webhooks Stripe/MercadoPago: **falham duro** em produção (`DEVELOPER_MODE=0`)
  se `STRIPE_WEBHOOK_SECRET` / `MERCADOPAGO_WEBHOOK_SECRET` não configurado.
- `gamification.add_points`: usa UPDATE atômico SQL (corrige race condition).
- `seo_utils.generate_sitemap`: URLs corrigidas (`/curso/<slug>`, `/catalogo`).
- README: stack real (Frappe v15, Python 3.11, Node 20) — não mais "v16".
- CI: `pip-audit` agora falha em CVEs críticos (sem `|| true`).

### Removido
- **Prometheus** completamente (endpoints `get_metrics`, `_user_can_view_metrics`;
  `prometheus.yml`, `grafana/`, `promtail-docker-config.yaml`,
  `metrics.vediums.com.conf`, serviços `prometheus`/`grafana` do compose).
  Razão: ADR-005 — overhead desproporcional para o tráfego atual.

### Arquivado
- `ESTADO_ATUAL.md`, `ARQUITETURA.md`, `ARQUITETURA_PROPOSTA.md`,
  `task.md`, `MODELO_LICAO.md`, `QA-CHECKLIST.md` → `docs/archive/`.
- 8 scripts `fix_*.py` / `check_db.py` → `scripts/migrations/oneshot/`.

---

## [2026-06-02]
- Layout unificado em todas as páginas (navbar/footer compartilhados).
- LMS movido para host nativo `app.vediums.com` (corrige POST 404).

## [2026-06-01]
- Consolidação do site vediums.com na plataforma Frappe.
- Página `/curso/<slug>` SEO server-rendered.

## [2026-05-29]
- Plataforma em estado de "lançamento": apps + e-mail Resend + signup +
  Stripe (custom) + Google Meet + cursos.

## [2026-05-26]
- Sprint P0 estabilização: workers, scheduler, healthchecks, backup, PWA,
  CDN, DocTypes faltantes (LMS Certificate, LMS Badge Log, LMS Flashcard,
  Support Ticket, Coupon).
