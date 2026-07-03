# 11 — Estado do Ambiente (checklist vivo)

**Verificado em produção (`app.vediums.com`) em:** 2026-07-03. Este doc
**envelhece rápido** — reconfirme no servidor antes de confiar num item
com mais de poucas semanas.

## Apps instalados

`frappe`, `erpnext`, `payments`, `lms`, `vedium_core`, `telephony`,
`helpdesk`, `crm`. Nenhum outro (ver [doc 04](04-ecossistema-frappe-oficial.md)
pros candidatos não instalados: `hrms`, `education`, `insights`, `wiki`,
`builder`, `drive`, `frappe_whatsapp`).

## Cursos e certificação

- **12 cursos publicados**: 3 Iorubá, 3 PLE, 6 Inglês.
- Todos os 12 com `evaluator` vinculado, `enable_certification=1` **e**
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
- `LMS Batch`: **0 criadas**. Nenhuma turma em grupo ativa ainda; a
  infraestrutura está pronta (Meet configurado pros 3 professores), falta
  só a decisão de negócio de abrir uma turma de verdade.

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
- `HD Settings.default_priority`: **não confirmado** nesta rodada (SSH
  instável).
- **1 `HD Ticket` só** (o seed da instalação) — nunca usado de verdade em
  produção.

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
