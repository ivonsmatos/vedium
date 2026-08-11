# 19 — Registro Completo de Engenharia (ciclo P2–P9, 2026-08)

> **O que este documento é:** o inventário definitivo, módulo a módulo, de tudo
> que foi construído no ciclo comercial/pedagógico (P2–P9) e nas frentes
> transversais (ponte Brevo, segurança, ferramental). É o "índice de engenharia"
> do trabalho — o **estado/roadmap** está no [doc 17](17-estado-roadmap-comercial-2026-08.md),
> o **setup externo do Brevo** no [doc 16](16-brevo-setup-externo.md) e os
> **achados de segurança** no [doc 18](18-qa-seguranca-arquitetura.md). Aqui está
> a foto completa do que existe no código, para quem for dar manutenção.

**Princípio que guiou tudo:** não duplicar função nativa. Frappe/LMS/CRM já fazem
muito; o `vedium_core` só **liga o que falta e emite eventos** — o corpo e a
entrega do e-mail de ciclo de vida são do **Brevo** (o Frappe é dono dos
**dados/eventos**, o Brevo é dono das **mensagens**).

---

## 1. Visão geral do ciclo

| Fase | Frente | Entregou |
|---|---|---|
| **P2** | Operação | Geradores de aula (turma + 1:1), onboarding de aluno/professor, ausência (A09), dunning (A20), lembrete de vencimento (A20-01) |
| **P3** | Automação comercial | Funil form→CRM (bug crítico corrigido), carrinho abandonado (A07), tarefa+alerta comercial, nutrição de lead parado |
| **P4** | Experiência do aluno | Home do Aluno agregadora em `/aluno` |
| **P5** | Acompanhamento pedagógico | Resumo mensal de evolução por aluno (A08-05) |
| **P6** | Retenção | Win-back de aluno dormente + digest semanal de risco |
| **P7** | Indicação | Correção do funil de indicação + métricas de CAC |
| **P8** | Crescimento | Camada de dados do funil + **dashboard nativo** (Number Cards + Chart) |
| **P9** | SEO/conteúdo | Mapa hub-and-spoke + helper Jinja de clusters |
| **T** | Transversal | Ponte Frappe→Brevo, remediação de segurança, 5 subagentes, guia de skills, `.gitattributes` |

---

## 2. Mapa de módulos novos

Todos em `vedium_core/vedium_core/`. Cada um é **defensivo** (nunca derruba a
request/job) e **idempotente** (marca o que já processou num custom field).

| Módulo | Responsabilidade | Como dispara |
|---|---|---|
| `live_class_scheduler.py` | Gera `LMS Live Class` recorrentes por turma (Meet nativo) | `generate_live_classes_for_batch()` — via UI (botão) ou `bench execute`; guard de staff |
| `student_onboarding.py` | Nudge de ativação (matriculou e não começou em 3d) | job **diário** `detect_inactive_students` → evento `student_not_activated` |
| `teacher_onboarding.py` | Boas-vindas ao professor + canal/checklist da turma | doc_event `after_insert` da turma + gatilho de novo professor |
| `attendance_events.py` | Faltas consecutivas (≥3) → check-in (A09) | job **diário** `detect_absent_students` → evento `student_absent` |
| `retention_events.py` | Win-back de dormente (~10d) + digest semanal de risco | job **diário** `detect_dormant_students` + **semanal** `weekly_at_risk_digest` |
| `pedagogical_report.py` | Resumo mensal de evolução (competências + presença) | cron **dia 1** `emit_monthly_evolution` → evento `monthly_evolution` |
| `crm_pipeline.py` | Origem/estágio corretos do lead, tarefa comercial, nutrição | doc_event de lead + jobs `alert_stale_leads` / `emit_lead_nurture_events` |
| `funnel_metrics.py` | Camada de dados do funil + cria o dashboard nativo | `funnel_metrics()` (dados) + `ensure_funnel_dashboard()` (no `after_migrate`) |
| `content_clusters.py` | Mapa hub-and-spoke (idioma→pilar+teste) | helper Jinja `cluster_for_category` |
| `public_funnel.py` (edit) | Captura do teste de nível → lead + `LEVEL` | `save_placement_result()` (guest, rate-limited) |

Front-end / páginas:
- `www/aluno.py` + `www/aluno.html` — Home do Aluno (server-rendered, logada).
- `public/js/lms_batch.js` — botão "Gerar aulas ao vivo" no form do LMS Batch.
- `www/teste-de-nivel-ingles.html` (edit) — bloco de captura de e-mail no teste.

---

## 3. Ponte Frappe→Brevo (transversal — habilita todo o ciclo de vida)

Arquivo: `brevo.py`. O Frappe **emite eventos** e mantém **atributos de contato**;
o Brevo escuta e dispara os modelos (A01–A20). Detalhes de setup no
[doc 16](16-brevo-setup-externo.md) e no [[project_email_lifecycle_brevo]].

**Chave de cutover:** `BREVO_LIFECYCLE_LIVE` — enquanto `0`, o Frappe envia
e-mails interinos; em `1`, cala-se e deixa o Brevo ser dono (evita duplicidade).
Ver `lifecycle_owned_by_brevo()`.

**Atributos de contato sincronizados:** `COURSE`, `LEVEL`, `COMPANY`,
`ENROLLMENT_STATUS`, `LIFECYCLE_STAGE`, `COMMUNICATION_LANGUAGE` (+ os já
existentes). Permitem a segmentação/personalização dos modelos.

**Catálogo de eventos (`LIFECYCLE_EVENTS`, 22 eventos)** — todos primados no
dropdown do Brevo via `seed_event_catalog()`:

| Grupo | Eventos |
|---|---|
| Engajamento/pedagógico | `student_not_activated`, `student_absent`, `student_inactive`, `progress_milestone`, `monthly_evolution` |
| Pagamento | `checkout_started`, `payment_failed`, `payment_recovered`, `payment_due_soon` |
| Trial | `trial_started`, `trial_expired` |
| Matrícula | `enrollment_activated`, `enrollment_suspended`, `enrollment_cancelled`, `cancellation_requested`, `enrollment_pending_review`, `enrollment_ended` |
| Comercial (CRM) | `lead_created`, `lead_updated`, `lead_stale`, `lead_status_changed`, `lead_converted` |

> `enrollment_created` fica **fora** da lista de seed de propósito (já tem
> automação A08 ativa; disparar pro contato-semente entraria no onboarding real).

**Garantias do `emit_contact_event()`:** guardado por `is_enabled()`, nunca lança
exceção (best-effort), e dedup por Integration Request. Emissores espalhados:
`attendance_events`, `crm_pipeline`, `gamification`, `pedagogical_report`,
`retention_events`, `stripe_billing`.

---

## 4. Automações agendadas (`hooks.py → scheduler_events`)

| Frequência | Job | Fase | Efeito |
|---|---|---|---|
| **Diário** | `student_onboarding.detect_inactive_students` | P2 | nudge de ativação → `student_not_activated` |
| **Diário** | `attendance_events.detect_absent_students` | P2 | faltas ≥3 → `student_absent` |
| **Diário** | `crm_pipeline.alert_stale_leads` | P3 | lead 'New' +24h → alerta à coordenação |
| **Diário** | `crm_pipeline.emit_lead_nurture_events` | P3 | lead parado ~7d → `lead_stale` |
| **Diário** | `retention_events.detect_dormant_students` | P6 | sumiu ~10d → `student_inactive` |
| **Diário** | `stripe_billing.send_dunning_reminders` | P2 | dunning d0/d3/d7/d9 |
| **Semanal** | `retention_events.weekly_at_risk_digest` | P6 | digest de progresso abaixo do esperado |
| **Cron dia 1** (`0 11 1 * *`) | `pedagogical_report.emit_monthly_evolution` | P5 | resumo mensal → `monthly_evolution` |

(Convivem com os pré-existentes: `trial.expire_trials`,
`stripe_billing.suspend_overdue_enrollments`, `lgpd._audit_pending_requests`,
`reports.send_weekly_digest`, lembrete de rascunho de Registro de Aula.)

**Document Events** registrados no ciclo:
- Lead novo → `crm_pipeline.on_lead_created` (cria a ToDo de primeiro contato).
- Usuário virou professor → `teacher_onboarding.on_user_became_professor`.
- Turma nova (`after_insert`) → `teacher_onboarding.on_batch_created`.

**Jinja method:** `content_clusters.cluster_for_category` (P9).
**doctype_js:** `LMS Batch → public/js/lms_batch.js`.

---

## 5. Campos custom adicionados (`custom_setup.py`)

> ⚠️ O `after_migrate` **nem sempre** cria custom fields. Após um deploy que
> adiciona campo, rodar
> `bench --site app.vediums.com execute vedium_core.custom_setup.setup_custom_fields`.

| Doctype | Campo | Para quê |
|---|---|---|
| LMS Enrollment | `custom_activation_nudged_on` | idempotência do nudge de ativação (P2) |
| LMS Enrollment | `custom_last_progress_milestone` | último marco de progresso emitido (A10) |
| LMS Enrollment | `custom_absence_alerted_on` | idempotência do alerta de ausência (A09) |
| CRM Lead | `custom_curso_interesse` | curso estruturado do lead (nutrição por curso) |
| CRM Lead | `custom_stale_alerted_on` | idempotência do alerta de lead parado (P3) |
| CRM Lead | `custom_nivel` | nível capturado no teste de nível (P-funil) |

---

## 6. Os 3 itens de plataforma (fechados neste ciclo)

1. **UI dos geradores de aula** — botão "Gerar aulas ao vivo" no form do LMS
   Batch (`lms_batch.js`): dialog com dias da semana (MultiCheck), host (Link) e
   duração; chama `generate_live_classes_for_batch` (guard de staff). Antes só
   por `bench execute`.

2. **Captura do teste de nível → `LEVEL`** — a página do teste captura e-mail +
   nível e faz POST em `save_placement_result` (guest, rate-limited, CSRF
   `fetch`). Grava `custom_nivel` no CRM Lead com origem/estágio corretos e envia
   o atributo `LEVEL` pro Brevo. Degrada com elegância (a página funciona mesmo
   se o endpoint falhar).

3. **Dashboard do funil em código** (`funnel_metrics.ensure_funnel_dashboard`) —
   cria no Desk, idempotente, o Dashboard **"Vedium Funil"**:
   - 4 **Number Cards**: Alunos ativos (Count), MRR R$/mês (Sum de
     `custom_contract_monthly_amount`), Leads (total), Matrículas (total).
   - 1 **Dashboard Chart** "Vedium - Alunos por status" (Group By
     `custom_vedium_status`, Donut).
   - Wirado no **`after_migrate`** (via `install.py → _ensure_funnel_dashboard`)
     para sobreviver a rebuilds do site sem re-execução manual.

   > A **camada de dados** (`funnel_metrics()`) — leads por origem, matrículas,
   > MRR, ticket médio, churn, conversão por idioma, indicação — fica separada
   > para o **Insights**/GA4 consumirem. O topo do funil (visitantes) vive no GA4.

---

## 7. Remediação de segurança

Auditoria pelo subagente `security-auditor`; detalhes e severidade no
[doc 18](18-qa-seguranca-arquitetura.md). Resumo dos fixes:

| Achado | Severidade | Fix |
|---|---|---|
| `careers.approve_candidatura_as_professor` sem guard → **auto-promoção a professor** | 🔴 Crítico | guard de staff (System Manager/Administrator/HR Manager/Vedium Ops) |
| `funnel_metrics` / `referrals.referral_metrics` expunham MRR/churn a qualquer logado | 🟠 Alto | guard de staff (`_STAFF_ROLES`) |
| `api.issue_certificate` sem checagem de dono | 🟠 Alto | ownership: dono da matrícula **ou** staff, senão `PermissionError` |
| `get_leaderboard`/`verify_certificate` vazavam e-mail do aluno | 🟡 Médio | retornam `full_name`/dados, não o e-mail (PII) |
| `submit_listening/speaking_exercise` sem limite | 🟡 Médio | `rate_limit_by_ip` + validação de URL de áudio |
| `get_forum_topics`/`get_course_sessions` vazavam `created_by`/`live_url`/`video_url` | 🟡 Médio | removidos do retorno |
| `certificate_pdf` caía no PK-name como fallback | 🟢 Baixo | fallback removido |
| `wiki_import.import_manifest` sem guard + path traversal | 🟠 Alto | guard de staff + `startswith(base)` |
| checkouts públicos sem limite | 🟡 Médio | `rate_limit_by_ip` |

---

## 8. Ferramental de plataforma

**5 subagentes** versionados em `.claude/agents/` (rodam via Task):
- `security-auditor` — auditoria da superfície de ataque (read-only).
- `frappe-code-reviewer` — revisa diff contra idiomas Frappe + footguns do repo.
- `deploy-verifier` — ritual de deploy (CRLF, testes afetados, push, watch, `setup_custom_fields`).
- `billing-e2e-tester` — prova a cadeia de cobrança ponta a ponta (BRL/USD).
- `brevo-events-qa` — QA da ponte Frappe→Brevo e do cutover.

**Guia de skills** em `.claude/skills/README.md`.

**`.gitattributes`** — força **LF** nos arquivos-fonte (mata o footgun recorrente
de CRLF: o editor no Windows gravava CRLF em arquivos LF → git via o arquivo
inteiro como alterado). Assets de terceiros e binários marcados para não
renormalizar.

---

## 9. Testes adicionados (pure, sem Frappe)

`test_pure_pedagogical_retention.py`, `test_pure_teacher_onboarding.py`,
`test_pure_attendance.py`, `test_pure_crm_pipeline.py`, `test_pure_growth.py`,
`test_pure_aluno_home.py`, `test_pure_security.py`, `test_pure_live_class_ui.py`,
`test_pure_placement.py` — mais atualizações em `test_pure_stripe_billing.py`,
`test_pure_marketing_pages.py`, `test_pure_referrals.py`,
`test_pure_gamification.py`. Rodam no CI (`flake8 E9,F63,F7,F82` bloqueia build +
pytest dos `test_pure_*`).

---

## 10. Ações manuais pendentes (fora do código)

Do lado do **dono** (ver [doc 16](16-brevo-setup-externo.md) e
[doc 17 §Ações](17-estado-roadmap-comercial-2026-08.md)):

1. **Brevo → cutover:** importar os 96 modelos (A01–A20), mapear as automações
   aos 22 eventos (já primados no dropdown), autenticar domínio, então
   `bench --site app.vediums.com set-config BREVO_LIFECYCLE_LIVE 1`.
2. Apagar o contato `brevo-seed@vediums.com` e a automação A03 quebrada.
3. Configurar as 21 campanhas (estáticas, sem dependência do Frappe).
4. (Opcional) `VEDIUM_COMMERCIAL_EMAIL` para rotear a tarefa comercial.
5. (Opcional) Ligar `invoice.upcoming` no webhook do Stripe (A20-01).
6. Decisões de processo: rodam-se **deals** (high-touch) ou self-serve? · duração
   oficial da aula/carga-horária · desconto de frequência no 1:1 Particular.

**Pendências opcionais de código (não solicitadas):** escrever os artigos dos
clusters SEO e wirar "conteúdos relacionados" nos templates; montar o painel
visual no Insights consumindo `funnel_metrics` + GA4; split do `api.py`; navbar
login-aware no `/aluno`.

---

## Referências

- **Estado/roadmap:** [17 — Estado do Roadmap](17-estado-roadmap-comercial-2026-08.md)
- **Brevo (setup externo):** [16 — Brevo Setup Externo](16-brevo-setup-externo.md)
- **Segurança & arquitetura:** [18 — QA Segurança](18-qa-seguranca-arquitetura.md)
- **Produto/preços:** [13 — Catálogo/Matriz](13-catalogo-de-produtos.md)
- **Deploy/footguns:** [12 — Runbook](12-runbook-de-operacao.md)
- **Kit de e-mail:** `Cliente/Vedium/emailmkt/` (96 modelos A01–A20 + campanhas)
- **Código:** módulos listados na §2.
