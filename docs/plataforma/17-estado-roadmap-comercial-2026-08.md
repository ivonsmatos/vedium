# 17 — Estado do Roadmap Comercial/Pedagógico (2026-08)

> Documento vivo do que foi construído nas frentes P2–P9 (operação, automação
> comercial, experiência do aluno, retenção, indicação, crescimento, SEO) e do
> que falta. Complementa a estratégia (matriz comercial, doc 13), o ciclo de
> vida de e-mail (doc 16 — Brevo) e o runbook (doc 12).

**Virada estratégica (2026-08-08):** com a infra crítica fechada, o foco passou
de "consertar plataforma" para "operação comercial/pedagógica previsível".
Roadmap: **P1** Produto · **P2** Operação · **P3** Automação comercial ·
**P4** Experiência do aluno · **P5** Acompanhamento pedagógico · **P6** Retenção ·
**P7** Indicação · **P8** Crescimento/dashboard · **P9** SEO/conteúdo.

Princípio que guiou tudo: **não duplicar função nativa** — Frappe/LMS/CRM já
fazem muito; o `vedium_core` só liga o que falta e **emite eventos** (o corpo/
entrega do e-mail é do Brevo — ver doc 16).

---

## ✅ Feito e no ar

### P1 — Produto (concluída antes desta rodada)
Matriz comercial (doc 13), certificação por avaliação (20/20 cursos), professores
(evaluator+instrutor), preços domésticos + **cobrança USD real** (público
internacional), catálogo Stripe↔Frappe completo.

### P2 — Operação
| Entrega | Módulo | Comportamento |
|---|---|---|
| Gerador de aulas ao vivo (turma + 1:1) | `live_class_scheduler.py` | cria `LMS Live Class` recorrentes; Meet nativo. Via `bench execute` (sem UI ainda). |
| Onboarding de aluno — nudge de ativação | `student_onboarding.py` | job diário: matriculou e não começou em 3d → evento `student_not_activated` + e-mail interino. Idempotente (`custom_activation_nudged_on`). |
| Onboarding de professor + turma | `teacher_onboarding.py` | turma nova → canal Raven + e-mail ao professor (detalhes+checklist); professor novo → boas-vindas 1x. |
| Ausência (A09) | `attendance_events.py` | job diário: faltas consecutivas (≥3) → evento `student_absent` + check-in. Sobre a presença **nativa** (Registro de Aula). Idempotente (`custom_absence_alerted_on`). |
| Dunning (A20) | `stripe_billing.py` | falha de cartão → e-mail dia-0 + lembretes (d3/d7/d9) + portal Stripe; `send_dunning_reminders` diário. |
| Lembrete de vencimento (A20-01) | `stripe_billing._invoice_upcoming` | `invoice.upcoming` → evento `payment_due_soon`. ⚠️ requer ligar o evento no Stripe (ver doc 16, passo 7). |

*Falta em P2:* **UI** pros geradores de aula (hoje linha de comando) — baixo valor.

### P3 — Automação comercial (modelo Lead→Deal nativo do Frappe CRM)
| Entrega | Módulo | Comportamento |
|---|---|---|
| 🔴 **Funil form→CRM (bug corrigido)** | `crm_pipeline.py` + `public_funnel.py` | os formulários gravavam `source` inválido → o lead **falhava em silêncio** (nenhum lead do site chegava ao CRM). Agora: origem válida (`resolve_lead_source`), estágio "New" (`resolve_lead_status`), curso estruturado (`custom_curso_interesse`). |
| Carrinho abandonado (A07) | `stripe_billing.create_subscription_checkout` | emite `checkout_started`; link de recuperação = página do curso (a sessão Stripe expira). |
| Tarefa comercial + alerta 24h | `crm_pipeline.on_lead_created` / `alert_stale_leads` | lead novo → ToDo "primeiro contato"; lead em "New" +24h → e-mail à coordenação (idempotente). |
| Lead parado → nutrição | `crm_pipeline.emit_lead_nurture_events` | job diário: lead inicial parado ~7d → evento `lead_stale` (A02/A13). Lead perdido → reativação já é `lead_status_changed`. |
| Lead → Brevo com curso | `brevo.py` | lead sync manda `COURSE` (nutrição personaliza por curso). |

*Adiado em P3 (decisão de processo):* semear **CRM Deal Status** ("Checkout
iniciado") — o nativo já traz o pipeline; adicionar é ação de UI e depende de
rodarem deals (high-touch) vs self-serve. Sem auto-avanço de deal.

### P4 — Experiência do aluno: Home do Aluno
`www/aluno.py` + `www/aluno.html` → **`app.vediums.com/aluno`** (server-rendered,
logada, 302 no gate). **Agrega** (não duplica o LMS; linka pra ele): próxima aula
ao vivo + botão Meet (`LMS Live Class.join_url`), progresso por curso, presença %
(Registro de Aula), status de pagamento (+ portal Stripe), atalhos (LMS, Raven,
pagamentos, suporte). Cada seção é defensiva (nunca 500).

### Transversal — ponte Frappe→Brevo (habilita todo o ciclo de vida)
`brevo.py`: atributos que os modelos leem (`COURSE`/`LEVEL`/`COMPANY` +
segmentação), `params.*` ricos, chave de cutover **`BREVO_LIFECYCLE_LIVE`**,
gates anti-duplicação. Ver doc 16 e [[project_email_lifecycle_brevo]].

---

## ✅ P5–P9 (2026-08-09) — implementadas

| Fase | Entrega | Módulo |
|---|---|---|
| **P5 Acompanhamento pedagógico** | resumo mensal de evolução por aluno (competências + presença) → evento `monthly_evolution` (A08-05) + e-mail interino; cron dia 1 do mês | `pedagogical_report.py` |
| **P6 Retenção** | `detect_dormant_students` (começou e sumiu ~10d → `student_inactive`/A09) + `weekly_at_risk_digest` (progresso abaixo do esperado → coordenação). Engajado→indicação (A12) reusa `progress_milestone(=100)` | `retention_events.py` |
| **P7 Indicação** | 🔴 corrigido bug de `source` inválido no lead de indicação; `referral_metrics()` (conversões, MRR trazido, recompensa média) p/ medir CAC. Core + página `minhas-indicacoes` já existiam | `referrals.py` |
| **P8 Crescimento/dashboard** | `funnel_metrics()` — camada de DADOS do funil (leads/origem, matrículas, MRR, ticket médio, churn, conversão por idioma, indicação). ⏳ **dashboard visual** monta-se no **Insights** (UI) + GA4 (visitantes) consumindo isto | `funnel_metrics.py` |
| **P9 SEO/clusters** | mapa hub-and-spoke (idioma → pilar + teste) + helper Jinja `cluster_for_category` (registrado) p/ linkar spoke→pilar→teste. ⏳ **escrever os artigos** do cluster (via `blog-publisher`) + cruzar links é conteúdo | `content_clusters.py` |

**Pendências não-código restantes:** montar o painel no **Insights** (consome
`funnel_metrics` + GA4); escrever os **artigos dos clusters** SEO e wirar a seção
"conteúdos relacionados" nos templates (usando `cluster_for_category`).

---

## 🔑 Ações que dependem de você (fora do código)

1. **Setup do Brevo → cutover** (destrava TODOS os e-mails de ciclo de vida que
   já estou emitindo): seguir o **doc 16** (importar modelos, criar atributos,
   mapear automações aos eventos, autenticar domínio) e então
   `bench --site app.vediums.com set-config BREVO_LIFECYCLE_LIVE 1`.
2. **(Opcional) Rotear tarefas comerciais** a uma pessoa específica:
   `bench --site app.vediums.com set-config VEDIUM_COMMERCIAL_EMAIL "vendas@vediums.com"`
   (default = `contato@vediums.com`).
3. **(Opcional, A20-01) Ligar `invoice.upcoming`** no webhook do Stripe (doc 16,
   passo 7) — habilita o lembrete de vencimento.
4. **Decisões de processo pendentes:** rodam-se **deals** (pipeline high-touch) ou
   é self-serve? · duração oficial da aula / carga-horária / material didático
   (coordenação) · desconto de frequência no 1:1 Particular.

> ⚠️ Nota de operação: custom fields às vezes não são criados pelo `after_migrate`
> automático — quando um deploy adiciona campo, rodar
> `bench --site app.vediums.com execute vedium_core.custom_setup.setup_custom_fields`.

---

## Referências
- Código: `student_onboarding.py`, `teacher_onboarding.py`, `attendance_events.py`,
  `crm_pipeline.py`, `stripe_billing.py`, `gamification.py`, `brevo.py`,
  `www/aluno.py`/`aluno.html`.
- Docs: [13 — Catálogo/Matriz](13-catalogo-de-produtos.md) ·
  [16 — Brevo setup externo](16-brevo-setup-externo.md) ·
  [15 — Registro de Aula](15-registro-de-aula-vedium.md).
- Kit de e-mail: `Cliente/Vedium/emailmkt/` (96 modelos A01–A20 + campanhas).
