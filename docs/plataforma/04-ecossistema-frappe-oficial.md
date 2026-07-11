# 04 — Ecossistema Frappe: Apps Oficiais e Adoção pra Escola de Idiomas

**Pesquisado em:** 2026-07-03, direto nas fontes (frappe.io, docs.frappe.io, GitHub —
`gh api` nos repos oficiais pra confirmar doctype/campo real, não descrição de
marketing). Cobre: apps já instalados e subutilizados, apps instalados com
problema conhecido, e apps oficiais **não instalados** que resolveriam alguma
lacuna real de operar uma escola de idiomas 100% online.

## Regra de ouro (reforça o [doc 01](01-mapa-nativo-vs-custom.md))

> Antes de escrever código custom novo, verifique se um app oficial Frappe já
> resolve — e, ANTES DISSO, se o app já instalado tem uma feature que a Vedium
> simplesmente não configurou ainda. Boa parte do ganho abaixo é **configuração,
> não instalação nem código**.

---

## 1. Já instalado, mal aproveitado — ganho rápido, zero app novo

Tudo isso já está no stack (`frappe`, `erpnext`, `lms`, `payments`) porque a
Frappe LMS traz muito mais do que curso/aula/quiz.

**Status em 2026-07-10** (revisitado nesta sessão):

| Feature | Doctype/campo confirmado | Resolve o quê pra Vedium | Esforço | Status |
|---|---|---|---|---|
| **Aula em grupo** | `LMS Batch` (turma com `start_date`/`end_date`, `instructors`, `seat_count`, `timetable`) + `LMS Live Class` (`conferencing_provider`: Zoom **ou** Google Meet) | Turma fechada tipo "PLE Básico — Turma Agosto" é isso, sem inventar doctype. | Médio — cobrança continua 100% Stripe (`paid_batch=0`) para não duplicar sistemas. | ✅ **Piloto criado**: `PLE Básico - Turma Agosto/2026`, 8 vagas, segundas 19:00-20:00 BRT, 9 `LMS Live Class` com Google Meet. Ainda rascunho/privada até decisão de abertura comercial. |
| **Presença real de aula** | `LMS Live Class Participant` (`joined_at`, `left_at`, `duration`) | "O aluno realmente compareceu" via dado real do Zoom/Meet, não matrícula. | Baixo — já existe, é dado gerado quando há Live Class. | ⚪ Automático — só passa a gerar dado quando existir a primeira Live Class (depende do item acima). |
| **Aluno avalia professor** | `LMS Batch Feedback` (`instructors`, `content`, `value`) | Hoje não existe nenhum mecanismo disso. | Baixo — ativa junto com Batch. | ⚪ Mesma dependência — só funciona por Batch. |
| **Fórum de dúvida por curso/lição** | Componente `Discussions.vue` genérico (por doctype/docname) | Tira dúvida sem WhatsApp/e-mail. | Baixo | ✅ **Confirmado ligado** (`LMS Settings.show_discussions = 1`). Nada a fazer. |
| **Badges com motor de regra** | `LMS Badge` (`condition` = expressão Python avaliada em evento `New`/`Value Change`/`Manual`) + `LMS Badge Assignment` | Complementa (não substitui) a gamificação custom (`LMS Badge Log`). | Médio | ✅ **Feito (2026-07-09)**: 3 badges nativos criados via `scripts/migrations/oneshot/setup_lms_badges.py` — `Primeira Lição` (`LMS Course Progress`, New), `Nota Máxima` (`LMS Quiz Submission`, `doc.percentage == 100`), `Nível Concluído` (`LMS Certificate`, New). O "bloqueio de asset" anterior foi resolvido reaproveitando os ícones SVG já embarcados em `public/images/icones/SVG/SOLID/`. O LMS avalia a `condition` e cria o `LMS Badge Assignment` sozinho — zero código de runtime. Limite nativo: `condition` roda por `frappe.safe_eval` sobre o doc (sem query), então badge de agregado (ex.: "10 lições") continua sendo só da gamificação custom. |

---

## 2. Já instalado, quebrado ou ambíguo — decisão + esforço baixo/médio

**Status em 2026-07-03:**

| App/Doctype | Situação confirmada | Ação recomendada | Status |
|---|---|---|---|
| **`crm` (Frappe CRM)** | `ImportError` em produção: `crm/utils/__init__.py` chamava `get_frappe_version()` de `frappe.pulse.utils`, função que não existe na versão de `frappe` instalada (desalinhamento `crm` 1.72.0 × `frappe` do servidor — módulo existe, função não). | Corrigir o import. | ✅ **Corrigido** (patch manual de 2 linhas: `frappe.__version__` no lugar). ⚠️ Não é um commit git — um futuro `bench update` do app `crm` pode sobrescrever sem aviso (ver [doc 11](11-estado-do-ambiente.md)/[doc 12](12-runbook-de-operacao.md)). `/crm` responde normal agora. |
| **`Support Ticket` (custom) vs `Helpdesk` (`HD Ticket`)** | Helpdesk instalado. `Support Ticket` custom tinha permissão insegura (`role All` com CRUD completo, vazava dado de outro aluno). | Consolidar em UM: `CRM Lead` pra vendas, `HD Ticket` pra suporte. | ✅ **Consolidado em 2026-07-08**: `ivonmatos@vediums.com` configurado como `Agent`/`Agent Manager`, time `Vedium Support` criado, defaults `Open`/`Medium` aplicados, e fluxos públicos + `open_support_ticket()` agora criam `HD Ticket` nativo via `vedium_core.helpdesk.create_ticket`. `Support Ticket` ficou apenas como fallback técnico caso Helpdesk não exista. Pendente só caixa IMAP `suporte@` para ticket por e-mail recebido. |
| **`LMS Certificate` nativo vs custom** | Colisão de NOME (mesmo doctype name). | Reconciliar — manter nativo com extensões via Custom Field. | ✅ **Já estava resolvido** de sessão anterior (script `fix_certificate_collision.py`), confirmado nesta sessão via SSH: `module=LMS`, Custom Fields `verification_code`/`enrollment` presentes. Nada a fazer. |

---

## 3. Instalado nesta sessão, ainda subutilizado

| App | Estado atual | Próximo uso real |
|---|---|---|
| **Frappe HR (`hrms`)** | Instalado. Ainda sem integração operacional com aulas dadas ou Timesheet. | Só vira produto útil quando houver modelo formal de pagamento/contrato de professor. |
| **Frappe Insights** | Instalado e acessível. | Criar dashboards quando houver volume; hoje é infraestrutura pronta com pouco dado. |
| **Frappe Wiki** | Instalado e acessível. Espaços `Manual dos Professores` e `Central de Ajuda para Alunos` publicados. | Usar como base interna/FAQ, com cuidado para mergear Draft Changes antes de considerar conteúdo publicado. |

## 4. Não instalado — candidatos com trade-offs reais

| App | Gratuito? | Resolveria | Ressalva |
|---|---|---|---|
| **Frappe Education** | App separado ativo (release v16.1.0, 2026-06-29), licença a confirmar manualmente no repo | `fee_schedule`/`fee_structure` = cobrança recorrente formal com contas a receber; `student_attendance` = frequência formal desacoplada de "assistiu o Zoom". | **Overlap real e não-integrado com a LMS** (dois cadastros de aluno/curso, um em Student/Program, outro em LMS Member/Course). Só vale a pena SE o objetivo for mover a cobrança pra dentro do ERPNext (contas a receber, boleto/NF) — não como camada extra ao Stripe, que já funciona. |
| **`frappe_whatsapp`** | Sim (terceiro, mas é a MESMA dependência que o CRM oficial usa pra aba de WhatsApp) | Lembrete de aula automático, confirmação de agendamento — hoje só e-mail (Resend) + botão manual. Usa WhatsApp Cloud API da Meta direto, sem middleman pago. | Gargalo é burocracia de aprovação de template pela Meta, não código. Resolve junto com o CRM se os dois forem adotados juntos. |
| **Frappe Builder** | Sim, self-hosted | Landing page de campanha pontual sem depender de deploy de código. | Redundante com o site Jinja atual pras páginas institucionais já resolvidas; risco de fugir do design system da marca (azul `#2E6DA4`/vermelho `#A12D1C`) se não recriar um template-base. |
| **Frappe Drive** | Sim, self-hosted | Professor compartilhar material solto fora da estrutura de curso (handout extra, gravação de aula 1-a-1) com permissão granular — diferente do anexo de lição do LMS (atrelado à publicação do curso). | Precisa definir fronteira de uso clara, senão vira duplicação de "onde o aluno procura material". |
| **Raven (chat estilo Slack)** | Sim, mas **NÃO é app oficial da org `frappe`** — é `The-Commit-Company/raven`, projeto do Frappe Incubator, AGPL | Chat síncrono real entre alunos/professores — diferente do fórum assíncrono por curso que a LMS já tem. | Mesma classe de risco de manutenção que já se materializou no bug do `crm` (app fora do núcleo `frappe`/`erpnext`/`lms`). Só vale se houver demanda real validada de chat síncrono — o link atual de `/comunidade` pro fórum nativo já cobre "dúvida sobre curso". |

---

## 5. Decisão específica: atendimento e tutor IA

Atualizado em 2026-07-08 no [doc 14](14-atendimento-e-tutor-ia.md):

- **Dúvidas humanas:** usar primeiro discussões nativas do LMS, assignments e
  batches/live classes.
- **Suporte operacional:** Helpdesk é o destino natural quando houver volume,
  SLAs ou mais de uma pessoa atendendo; no volume atual, manter simples.
- **WhatsApp:** útil para comercial/suporte administrativo, não como tutor
  pedagógico.
- **Tutor IA:** não há recurso nativo pronto no Frappe Learning. A Vedium tem
  código parcial em `vedium_core`, mas transformar isso em produto exige
  DocTypes, widget autenticado, base de conhecimento, logs e fallback humano.

---

## 6. Não pesquisado nesta rodada (fora do escopo do pedido original)

- Gateway de SMS nativo do framework (`SMS Settings`) — mencionado de passagem, não aprofundado.
- `frappe/gameplan` (gestão de projeto interno) — não pesquisado, baixa prioridade presumida pra escola pequena/média.
- Localização fiscal brasileira (CLT/INSS/FGTS dentro do HR, nota fiscal dentro do ERPNext) — sinalizado como lacuna de confirmação no item Frappe HR acima, não confirmado se existe app BR oficial/comunidade.

## Como essa pesquisa foi feita

3 agentes em paralelo, cada um usando `WebFetch`/`WebSearch` nas fontes oficiais
(frappe.io, docs.frappe.io) e `gh api repos/frappe/<repo>/contents/<path>` pra
baixar e ler o JSON real de doctype (schema de campo, não descrição de
marketing) direto do GitHub. Onde um agente não conseguiu confirmar algo
(ex.: licença exata do `frappe/education`, dashboard de instrutor pronto no
LMS), está marcado explicitamente acima como não confirmado — trate como
hipótese a verificar, não fato.
