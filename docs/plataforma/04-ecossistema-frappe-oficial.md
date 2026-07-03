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

| Feature | Doctype/campo confirmado | Resolve o quê pra Vedium | Esforço |
|---|---|---|---|
| **Aula em grupo** | `LMS Batch` (turma com `start_date`/`end_date`, `instructors`, `seat_count`, `timetable`) + `LMS Live Class` (`conferencing_provider`: Zoom **ou** Google Meet) | Hoje só existe 1-a-1 (Course Evaluator). Turma fechada tipo "Inglês Iniciante — Turma Julho" é isso, sem inventar doctype. | Médio — 0 `LMS Batch` existe hoje; decidir se cobrança fica no `LMS Batch.paid_batch` nativo ou continua 100% Stripe (não fazer os dois pro mesmo produto). |
| **Presença real de aula** | `LMS Live Class Participant` (`joined_at`, `left_at`, `duration`) | "O aluno realmente compareceu" via dado real do Zoom/Meet, não matrícula. | Baixo — já existe, é dado gerado quando há Live Class. |
| **Aluno avalia professor** | `LMS Batch Feedback` (`instructors`, `content`, `value`) | Hoje não existe nenhum mecanismo disso. | Baixo — ativa junto com Batch. |
| **Fórum de dúvida por curso/lição** | Componente `Discussions.vue` genérico (por doctype/docname), provável `Discussion Topic`/`Discussion Reply` do framework | Tira dúvida sem WhatsApp/e-mail. Provavelmente já visível no tema padrão do LMS. | Baixo — checar se está habilitado em `LMS Settings`. |
| **Badges com motor de regra** | `LMS Badge` (`condition` = expressão Python avaliada em evento `New`/`Value Change`/`Manual`) + `LMS Badge Assignment` | Complementa (não substitui) a gamificação custom (`LMS Badge Log`, que tem "level"/pontos e o nativo não tem). | Médio — usar como complemento, não migração 1:1. |

---

## 2. Já instalado, quebrado ou ambíguo — decisão + esforço baixo/médio

| App/Doctype | Situação confirmada | Ação recomendada |
|---|---|---|
| **`crm` (Frappe CRM)** | `ModuleNotFoundError` em produção. Causa raiz real: [issue frappe/crm#1594](https://github.com/frappe/crm/issues/1594) — import quebrado de `frappe.pulse.utils` (módulo que não existe) dentro de `crm/utils/__init__.py`, corrigido oficialmente trocando por `frappe.__version__`. **Não é falta do app** — é versão do app `crm` desalinhada/desatualizada. | Atualizar o app `crm` (bench update) e reverificar. Se resolver, o `CRM Lead`/`CRM Deal` (funil, SLA, telefonia nativa, web form público) é upgrade real sobre o `Support Ticket` custom que `public_funnel.py` cria hoje pra leads de matrícula/B2B. |
| **`Support Ticket` (custom) vs `Helpdesk` (`HD Ticket`)** | Helpdesk instalado, 0 uso real. `HD Ticket` tem SLA por prioridade, KB pesquisável (`HD Article`), portal do cliente, templates por tipo. `Support Ticket` custom é raso (sem SLA, sem dono/atribuição). | Consolidar em UM: `CRM Lead` pros intents de venda (matrícula, B2B, aula-diagnóstica) do `public_funnel.py`, `HD Ticket` pra dúvida/problema (financeiro, técnico Zoom, pedagógico). Aposentar `Support Ticket` custom depois da migração — hoje a ambiguidade "qual eu uso" é pior que qualquer um dos dois isolados. |
| **`LMS Certificate` nativo vs custom** | Colisão de NOME confirmada (mesmo doctype name), já sinalizada em [doc 02](02-dicionario-doctypes.md) mas sem detalhe de schema até agora. Nativo: `template` (Link → Print Format, obrigatório — motor de PDF do Frappe), sem `verification_code`. Custom (`vedium_core`): `verification_code` (usado por `/certificado?code=`), sem `template`. | Decisão de produto, não pesquisa: se o link público de verificação (`verification_code`) é importante pro marketing/confiança, ele não existe no nativo de fábrica — precisa virar Custom Field no doctype nativo, migrando o custom pra dentro dele (não manter os dois). |

---

## 3. Não instalado — candidatos com trade-offs reais

| App | Gratuito? | Resolveria | Ressalva |
|---|---|---|---|
| **Frappe HR (`hrms`)** | Sim, self-hosted (Frappe Cloud é só hosting gerenciado opcional) | Folha/férias/13º pra professor **CLT**. Pagamento por hora-aula é possível via `Salary Structure` + `Timesheet` (`hour_rate`), mas não liga sozinho a "deu aula" — precisa integração (ex.: Live Class Participant → Timesheet). | Modelo pressupõe vínculo formal (Employee/Employment Type). Pra maioria freelance, o encaixe é frágil sem essa integração custom. Payroll é genérico — localização CLT/INSS/FGTS não vem pronta, não confirmado se existe app BR separado. |
| **Frappe Education** | App separado ativo (release v16.1.0, 2026-06-29), licença a confirmar manualmente no repo | `fee_schedule`/`fee_structure` = cobrança recorrente formal com contas a receber; `student_attendance` = frequência formal desacoplada de "assistiu o Zoom". | **Overlap real e não-integrado com a LMS** (dois cadastros de aluno/curso, um em Student/Program, outro em LMS Member/Course). Só vale a pena SE o objetivo for mover a cobrança pra dentro do ERPNext (contas a receber, boleto/NF) — não como camada extra ao Stripe, que já funciona. |
| **Frappe Insights** | Sim, self-hosted | Dashboard de matrícula/churn/receita/engajamento direto em cima dos doctypes nativos do LMS, sem escrever report Python. Conecta MySQL/Postgres/DuckDB/BigQuery, não só o próprio site. | Esforço baixo — instalar + apontar pro banco atual + montar dashboard via UI. Sem mudança de schema. |
| **Frappe Wiki** | Sim, self-hosted | Base de conhecimento interna (material de apoio pro professor, FAQ interno, políticas) separada do conteúdo de curso publicado. | Baixo esforço, sem dev. |
| **`frappe_whatsapp`** | Sim (terceiro, mas é a MESMA dependência que o CRM oficial usa pra aba de WhatsApp) | Lembrete de aula automático, confirmação de agendamento — hoje só e-mail (Resend) + botão manual. Usa WhatsApp Cloud API da Meta direto, sem middleman pago. | Gargalo é burocracia de aprovação de template pela Meta, não código. Resolve junto com o CRM se os dois forem adotados juntos. |
| **Frappe Builder** | Sim, self-hosted | Landing page de campanha pontual sem depender de deploy de código. | Redundante com o site Jinja atual pras páginas institucionais já resolvidas; risco de fugir do design system da marca (azul `#2E6DA4`/vermelho `#A12D1C`) se não recriar um template-base. |
| **Frappe Drive** | Sim, self-hosted | Professor compartilhar material solto fora da estrutura de curso (handout extra, gravação de aula 1-a-1) com permissão granular — diferente do anexo de lição do LMS (atrelado à publicação do curso). | Precisa definir fronteira de uso clara, senão vira duplicação de "onde o aluno procura material". |
| **Raven (chat estilo Slack)** | Sim, mas **NÃO é app oficial da org `frappe`** — é `The-Commit-Company/raven`, projeto do Frappe Incubator, AGPL | Chat síncrono real entre alunos/professores — diferente do fórum assíncrono por curso que a LMS já tem. | Mesma classe de risco de manutenção que já se materializou no bug do `crm` (app fora do núcleo `frappe`/`erpnext`/`lms`). Só vale se houver demanda real validada de chat síncrono — o link atual de `/comunidade` pro fórum nativo já cobre "dúvida sobre curso". |

---

## 4. Não pesquisado nesta rodada (fora do escopo do pedido original)

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
