# 11 — Estado do Ambiente (checklist vivo)

**Verificado em produção (`app.vediums.com`) em:** 2026-07-10. Este doc
**envelhece rápido** — reconfirme no servidor antes de confiar num item
com mais de poucas semanas.

## Apps instalados

`frappe`, `erpnext`, `payments`, `lms`, `vedium_core`, `telephony`,
`helpdesk`, `crm`, `hrms`, `insights`, `wiki`.

Não instalados/fora do stack atual: `education`, `builder`, `drive`,
`frappe_whatsapp`, `raven`. Ver [doc 04](04-ecossistema-frappe-oficial.md)
para trade-offs e critérios de adoção.

## Cursos e certificação

- **Catálogo publicado atual:** 6 Inglês, 3 Iorubá, 3 PLE e 5 Hebraico
  (17 cursos no total, incluindo `hebraico-particular`, que é oferta
  consultiva 1:1 e não deve fechar checkout de valor fixo).
- Cursos de assinatura/nível têm `evaluator` vinculado,
  `enable_certification=1` **e**
  `paid_certificate=1` (ligado nesta sessão — ver [doc 05](05-fluxo-jornada-do-aluno.md)).
- `LMS Settings.send_calendar_invite_for_evaluations = 1` (ligado — o job
  `schedule_evals` gera Google Meet automaticamente pros agendamentos).
- **2 matrículas (`LMS Enrollment`) no total** — plataforma em estágio
  bem inicial de volume real.

## Agendamento / Google Meet

- `Google Calendar`: 3 contas — `ivonmatos@vediums.com`,
  `almirseller@yahoo.com`, e a compartilhada "Vedium Aulas ao Vivo"
  (owner: Administrator). Todas com `enable=1`.
- `LMS Google Meet Settings`: 3 registros (Almir, Kayode, Busayo — criados
  nesta sessão), todos apontando pro calendário compartilhado.
- `LMS Zoom Settings`: **não confirmado nesta rodada** (SSH instável no
  momento da checagem) — reconfirmar antes de assumir.
- `LMS Batch`: **1 criada** — `ple-b-sico-turma-agosto-2026`
  (`PLE Básico - Turma Agosto/2026`), curso
  `portugues-para-estrangeiros-basico`, professor/evaluator
  `almirseller@yahoo.com`, 8 vagas, segundas 19:00-20:00 BRT.
  Ainda está em rascunho (`published=0`, `allow_self_enrollment=0`).
- `LMS Live Class`: **9 criadas** para essa turma, de 2026-08-03 a
  2026-09-28, todas com `Google Meet` via `Vedium Meet` e links gerados.

## Permissões (correções de segurança desta sessão)

- `Support Ticket`: papel `All` tinha CRUD completo (create/write/delete)
  — reduzido pra `read` restrito ao próprio dono (`if_owner=1`). Ver
  commit `383a2ff`.
- `LMS Course`: não tinha NENHUMA permissão pro papel `LMS Student` — bug
  de plataforma que quebrava a tela de agendamento pra todo aluno.
  Corrigido via `Custom DocPerm` (read=1). Ver [doc 05](05-fluxo-jornada-do-aluno.md).
- `Lesson Slot` (doctype legado, não usar): permanece com `All` só
  leitura, sem escrita — corrigido em sessão anterior (2026-07-01).

## Traduções (i18n da plataforma, não do site)

- `Translation` (pt-BR, específicas da Vedium, via doctype nativo, não
  arquivo `.po`): "Get Certified" → "Agendar aula/gerar certificado",
  "Schedule an evaluation to get certified." → "Agende uma aula com o
  professor para avançar no curso.", "Upcoming Evaluations" → "Próximas
  aulas agendadas". Cadastradas nesta sessão — cobertura parcial, só o
  fluxo de agendamento/certificação.
- Cobertura pt-BR do LMS nativo como um todo: **não auditada**. O arquivo
  comunitário `pt_BR.po` do `frappe/lms` tem lacunas conhecidas (achado
  real: `msgstr` vazio pra "Get Certified" apesar do usuário estar com
  `User.language=pt-BR` configurado corretamente).

## CRM (`crm`)

- **Corrigido nesta sessão** (patch manual, ⚠️ ver risco abaixo):
  `ModuleNotFoundError`/`ImportError` em `crm/utils/__init__.py` —
  função `is_frappe_version` importava `get_frappe_version` de
  `frappe.pulse.utils`, que existe como módulo mas não tem essa função
  na versão de `frappe` instalada (desalinhamento de versão entre `crm`
  1.72.0 e o `frappe` do servidor). Trocado por `frappe.__version__`
  direto no arquivo.
- ⚠️ **Risco**: é um patch manual no arquivo do app, **não um commit
  git** — um `bench update`/reinstall do app `crm` sem re-aplicar esse
  patch (ou sem uma versão upstream que já corrija isso) desfaz a
  correção. Não confirmado se existe fix oficial upstream mais recente.
- CRM Lead/Deal ainda **não é usado** pelo `public_funnel.py` (que
  continua criando `Support Ticket` pra leads de matrícula/B2B) — a
  correção só destravou o acesso à página `/crm`, não migrou nenhum
  fluxo.

## Helpdesk (`helpdesk`)

- Instalado com fixtures básicas: 2 `HD Team`, 4 `HD Ticket Status`, 4
  `HD Ticket Priority`.
- Configurado em 2026-07-08 para operação inicial:
  - `HD Agent`: `ivonmatos@vediums.com`
  - papéis do usuário: `Agent`, `Agent Manager`, `System Manager`
  - `HD Team`: `Vedium Support`
  - `HD Settings.default_priority`: `Medium`
  - `HD Settings.default_ticket_status`: `Open`
  - `HD Settings.ticket_reopen_status`: `Open`
- Fluxos públicos e `open_support_ticket()` agora criam `HD Ticket`
  nativo via `vedium_core.helpdesk.create_ticket`, com fallback para
  `Support Ticket` legado só se Helpdesk não estiver disponível.
- **1 `HD Ticket` real no banco ainda é o seed da instalação**; smoke test
  criou e removeu um ticket temporário `0799` validando `Vedium Support`,
  `Open` e `Medium`.
- Atendimento por e-mail recebido: `suporte@vediums.com` foi configurado
  via Microsoft 365 OAuth em `Email Account` (`append_to = HD Ticket`).
  Testes IMAP/SMTP passaram; manter OAuth/Connected App documentados no
  runbook operacional.

## BI e Wiki

- `insights` instalado e acessível em `/insights`. Com baixo volume de
  matrículas, dashboards ainda valem mais como infraestrutura pronta do
  que como BI útil.
- `wiki` instalado e acessível em `/wiki`. Espaços publicados:
  `Manual dos Professores` (`professores`, 14 documentos) e
  `Central de Ajuda para Alunos` (`ajuda`, 47 documentos). Em 2026-07-10,
  drafts bons foram mergeados e drafts vazios/ruins do Administrator foram
  arquivados para evitar novo sumiço visual das páginas.

## Rollout de i18n (tradução do site)

Ver [[project_i18n_n_language_rollout]] na memória do agente pro estado
exato — resumo em 2026-07-03: inglês, espanhol e francês completos e
implantados; alemão parcialmente commitado (pausado a pedido do usuário
pra focar nesses fixes de plataforma); russo e mandarim não iniciados.

## Cobrança

- Stripe é o gateway ativo/principal. MercadoPago e BaseCommerce existem
  no código (`get_gateway`) mas não confirmados como ativos em produção
  nesta rodada. Gateway cripto **desativado deliberadamente** (ADR, ver
  histórico do git).
