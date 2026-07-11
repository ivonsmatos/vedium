# 05 — Fluxo: Jornada do Aluno

**Verificado em produção:** 2026-07-10 (`app.vediums.com`), inclui a correção
do fluxo nativo de agendamento feita nesta mesma data.

Checkout → matrícula → aula → certificado, com o "onde vive cada peça"
(nativo LMS vs. custom `vedium_core`) explícito em cada etapa.

## 1. Descoberta e checkout — 🔵 Custom

- Aluno navega o site (`vediums.com`, `www/*.html`) e chega numa página de
  curso (`www/curso.html`/`curso.py`) ou landing (`marketing_landing.html`).
- Clica em matricular → `api.create_checkout_session` (Stripe) ou
  `create_mercadopago_checkout`/`create_basecommerce_checkout` — cria a
  sessão de pagamento fora do Frappe.
- Pagamento confirmado → webhook (`api.handle_payment_webhook` /
  `stripe_webhook`) → `api.create_enrollment_if_paid`.

## 2. Matrícula — 🟢 Nativo (criada por código custom)

- `create_enrollment_if_paid` cria um `LMS Enrollment` nativo, com
  `ignore_permissions=True` (roda em contexto de webhook, sem sessão do
  aluno).
- **Desde 2026-07-03**: a matrícula já nasce com `purchased_certificate=1`
  — o certificado/avaliação já está incluso no preço pago no Stripe, não é
  produto separado. Sem isso, o botão nativo de agendamento manda o aluno
  pra uma tela de cobrança *dentro* do LMS, cobrando de novo (ver §4).
- Cupom (se houver) é consumido de forma atômica só depois do pagamento
  confirmado, e o programa de indicação é acionado.
- E-mail de confirmação de matrícula é disparado (`frappe.sendmail`).

## 3. Consumo do curso — 🟢 Nativo

- Aluno acessa `app.vediums.com/lms/courses/<slug>` — conteúdo (capítulos,
  lições, quiz) é 100% nativo do Frappe LMS.
- Progresso é rastreado nativamente (`LMS Course Progress`,
  `LMS Enrollment.progress`).
- **PLE (Português para Estrangeiros):** cada nível tem 3 quizzes de
  exercícios de fixação (10 questões por módulo) e 1 prova final (banco de
  80 questões, sorteia 40, nota mínima 70%, até 3 tentativas). O rollout é
  idempotente pelo comando:
  `bench --site app.vediums.com execute vedium_core.scripts.migrations.oneshot.setup_ple_quizzes.run`.
- **Gate pedagógico dentro do PLE:** Módulo 2 exige aprovação no exercício do
  Módulo 1; Módulo 3 exige aprovação no exercício do Módulo 2; Avaliação Final
  exige aprovação no exercício do Módulo 3. O gate entre níveis continua por
  certificado do curso anterior, sem liberar curso pago de graça.
- ⚠️ **Pegadinha real**: `LMS Enrollment` **não tem campo `status`** (só
  `progress`) — código que assume esse campo quebra com
  `Unknown column 'status'` (achado e corrigido em `www/meu_progresso.py`
  nesta sessão). Deriva um status ("Concluído"/"Em andamento") a partir de
  `progress >= 100`.

## 4. Agendamento de aula com o professor — 🟢 Nativo (destravado nesta sessão)

Este é o ponto que mais gerou retrabalho — documentado em detalhe porque é
fácil repetir o erro.

**O problema original**: o botão nativo "Get Certified" (que leva à tela de
agendamento, `CourseCertification.vue`) só aparece quando
`LMS Course.paid_certificate = 1`. Esse campo modela "certificado vendido
separado, com preço próprio dentro do LMS" — não é o modelo da Vedium.
Como nenhum curso tinha isso ligado, **nenhum aluno via o botão em curso
nenhum**, em produção, desde sempre.

**A correção (2026-07-03), 100% configuração nativa, sem página custom**:

1. `LMS Course.paid_certificate = 1` em todo curso publicado com
   `evaluator` vinculado.
2. `LMS Enrollment.purchased_certificate = 1` em toda matrícula (histórico
   + automático em toda matrícula nova via `create_enrollment_if_paid`) —
   sem isso, o botão levaria à cobrança nativa em vez do agendamento.
3. Script idempotente:
   `vedium_core/scripts/migrations/oneshot/enable_native_scheduling_button.py`.

**Bug de plataforma encontrado e corrigido durante a validação**: o
doctype nativo `LMS Course` **não tinha nenhuma permissão de leitura para
o papel `LMS Student`** — só `System Manager`/`Course Creator`/`Moderator`.
A tela de agendamento (`CourseCertification.vue`) lê o curso via
`frappe.client.get_value` (API genérica, permission-checked) e falhava com
`PermissionError` pra qualquer aluno. Ninguém tinha batido nesse código
antes porque `paid_certificate` nunca esteve ligado. Corrigido com um
`Custom DocPerm` dando `read=1` pro papel `LMS Student` em `LMS Course` —
mecanismo padrão do Frappe pra estender permissão de doctype de outro app,
sem tocar no código-fonte do `lms`.

**Traduções**: o texto "Get Certified" (e outros da tela) não tinha
tradução pt-BR no arquivo comunitário do LMS (`msgstr` vazio) — mesmo com
`User.language = "pt-BR"` configurado corretamente. Corrigido via doctype
nativo `Translation` (override por site, sem tocar em código):
"Get Certified" → **"Agendar aula/gerar certificado"** (tradução
deliberadamente não-literal — o texto original confunde o aluno sobre o
que o botão realmente faz).

**Fluxo final, validado ponta a ponta em produção**:
`app.vediums.com/lms/courses/<slug>` → botão "Agendar aula/gerar
certificado" → `/courses/<slug>/certification` → modal "Schedule your
evaluation" com os horários reais do professor (`Evaluator Schedule`) →
aluno escolhe → cria `LMS Certificate Request` → Google Meet gerado
automaticamente (job `schedule_evals`, roda a cada poucas horas).

**Aula em grupo (turma/batch)**: mesmo mecanismo de Google Meet, via
`LMS Google Meet Settings` — configurado para os 3 professores (Almir,
Kayode, Busayo), todos apontando pro calendário compartilhado
"Vedium Aulas ao Vivo". O piloto `PLE Básico - Turma Agosto/2026` já foi
criado com 9 `LMS Live Class`, ainda privado/rascunho. Decisão de produto:
turmas ficam com `paid_batch = 0` — cobrança continua 100% no Stripe, não
duplica sistema de pagamento.

## 5. Certificação — 🟢 Nativo

- Depois da avaliação/aula, o professor emite o certificado (`LMS
  Certificate`, nativo — ver [doc 02](02-dicionario-doctypes.md) pra
  histórico da colisão de nome já resolvida com o custom).
- Aluno vê o certificado na mesma tela de certificação
  (`CourseCertification.vue` mostra `certificate.data` quando existe).

## O que NÃO existe (e não deveria ser construído)

- Nenhuma página/API custom de agendamento no site (`vediums.com`). Uma
  tentativa nesse sentido foi feita e revertida na mesma sessão — ver
  commit `dd787ac` ("agendamento 100% nativo, sem pagina custom") e
  [[feedback_site_is_only_marketing_functions_live_in_frappe]] na memória
  do agente. **Regra permanente**: o site é só vitrine; toda função do
  aluno/professor vive dentro do Frappe (`app.vediums.com`).
