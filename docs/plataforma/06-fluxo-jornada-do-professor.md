# 06 — Fluxo: Jornada do Professor

**Verificado em produção:** 2026-07-08. Instrutor → evaluator → slots →
aula → certifica. Agendamento é nativo do Frappe LMS; notificação ganhou
fallback custom da Vedium porque a entrega nativa não notificou professor
de forma confiável.

## 1. Vínculo instrutor ↔ curso — 🟢 Nativo

- `Course Instructor` (child table de `LMS Course`) — vínculo simples,
  cadastrado pelo moderador ao criar o curso.
- Hoje: Almir (`almir@vediums.com`, cursos PLE), Kayode
  (`kayode@vediums.com`, cursos de Inglês), Busayo (`busayo@vediums.com`,
  cursos de Iorubá) — um professor por trilha de idioma.

## 2. Virar "Evaluator" (quem pode agendar/avaliar) — 🟢 Nativo

- `Course Evaluator` — registro por professor (`autoname: field:evaluator`,
  um só por pessoa). Ganha automaticamente o papel `Batch Evaluator`
  (`validate_evaluator_role`, roda no `validate()` do doctype).
- `LMS Course.evaluator` — vínculo curso → professor específico. Sem isso
  E sem `enable_certification=1`, o agendamento não aparece pro aluno (ver
  [doc 05](05-fluxo-jornada-do-aluno.md#4-agendamento-de-aula-com-o-professor--nativo-destravado-nesta-sessão)).
  Hoje: cursos publicados de assinatura/nível usam esse vínculo; oferta
  consultiva 1:1 pode exigir tratamento comercial antes do checkout.

## 3. Cadastrar disponibilidade — 🟢 Nativo

- Professor acessa `app.vediums.com/user/<username>` (aba "My
  availability", `ProfileEvaluator.vue`) e cadastra `Evaluator Schedule`
  (dia da semana + horário início/fim, sem limite de linhas, todos os 7
  dias disponíveis — **não existe restrição de dia** no doctype nem no
  código nativo).
- Mesma tela: bloqueio de período ("I am unavailable", `unavailable_from`/
  `unavailable_to`) e botão "Authorize Google Calendar Access" (OAuth,
  ação manual e pessoal de cada professor — não pode ser feita via
  script/admin).
- ⚠️ **Achado real (2026-07-03)**: um professor relatou "só consegui
  liberar até quinta, sexta não consegui mais". Investigado a fundo — não
  existe trava de código pra isso (nem no doctype, nem no controller
  nativo `CourseEvaluator.validate_time_slots`/`validate_overlaps`).
  Causa mais provável: dificuldade de UX na tela nativa (só em inglês,
  fluxo de "Add Slot" exige clicar de novo pra cada linha) — não uma falha
  do sistema.

## 4. Aula em grupo (turma) — 🟢 Nativo, configurado nesta sessão

- `LMS Google Meet Settings` — um registro por professor
  (`member` + `google_calendar`). Configurado pros 3 professores em
  2026-07-03, todos apontando pro calendário compartilhado "Vedium Aulas
  ao Vivo" (não depende de cada professor autorizar o próprio Google
  Calendar pessoal pra isso).
- `LMS Batch` — turma/cohorte com data de início/fim, professor(es),
  cronograma. Piloto criado: `PLE Básico - Turma Agosto/2026`, 8 vagas,
  segundas 19:00-20:00 BRT, ainda rascunho/privado. Decisão de produto:
  cobrança fica 100% no Stripe (`paid_batch=0`), não usa a cobrança nativa
  do Batch.
- `LMS Live Class` — sessão específica dentro de uma Batch, com
  `conferencing_provider: Google Meet`.

## 5. Aluno agenda, professor é notificado — 🟢 Nativo + fallback Vedium

- Aluno cria `LMS Certificate Request` (ver [doc 05](05-fluxo-jornada-do-aluno.md)).
- `LMSCertificateRequest.after_insert` nativo pode enviar e-mail, mas não
  foi confiável em produção. Desde 2026-07-08, `hooks.py` também chama
  `vedium_core.notifications.notify_lms_certificate_request`, que envia
  e-mail enfileirado para o professor (`evaluator`) e para a operação
  (`contato@vediums.com`) e cria `Notification Log` no Desk quando possível.
- Google Meet é gerado automaticamente pelo job periódico `schedule_evals`
  (`LMS Settings.send_calendar_invite_for_evaluations` precisa estar
  ligado) — não é instantâneo, roda em lote.
- Professor vê a própria agenda em `app.vediums.com/user/<username>`
  (aba de calendário, `ProfileEvaluationSchedule.vue`) — lista
  `LMS Certificate Request` filtrado por `evaluator = professor`.

## 6. Dar a aula e certificar — 🟢 Nativo

- Aula acontece no Google Meet gerado.
- Depois: professor emite avaliação/certificado
  (`create_lms_certificate_evaluation`, mapeia `LMS Certificate Request` →
  `LMS Certificate Evaluation`) — ação restrita a papéis privilegiados
  (`Moderator`, `Batch Evaluator`, `System Manager`).

## O que NÃO é nativo (lacuna real, não construída ainda)

- **Pagamento ao professor por aula dada**: não existe automação. O
  Frappe HR (`hrms`) resolveria isso via `Salary Structure` baseado em
  `Timesheet` (`hour_rate`), mas exigiria integração custom ligando
  presença real (`LMS Live Class Participant`/`LMS Certificate Request`
  completado) ao lançamento do Timesheet — nada disso existe hoje. Ver
  [doc 04](04-ecossistema-frappe-oficial.md#3-instalado-nesta-sessão-ainda-subutilizado).
  Hoje o pagamento aos professores presumivelmente é feito fora da
  plataforma (não verificado nesta sessão).
- **Avaliação de desempenho do professor pelo aluno**: existe nativo
  (`LMS Batch Feedback`), mas só funciona por Batch — o piloto PLE ainda
  está privado, então isso ainda não gera dado real.
