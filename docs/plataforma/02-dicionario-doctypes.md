# 02 — Dicionário de Doctypes & Modelo de Domínio

**Objetivo:** dizer o que cada doctype representa no negócio da Vedium, como se
relacionam, e **quais são custom, nativos ou legados** — para ninguém reusar o
doctype errado.

**Verificado em produção:** 2026-07-01. **Fonte custom:** `vedium_core/vedium_core/doctype/`.

## Como ler

- **Nativo** = definido por Frappe/ERPNext/LMS. Não editar o schema; estender via Custom Field.
- **Custom** = definido em `vedium_core`. Nosso schema, nossa manutenção.
- **Legado** = existe mas foi substituído; não usar em código novo.

---

## Mapa de relações (núcleo)

```
User ──< Course Instructor >── LMS Course ──< Course Chapter ──< Course Lesson
 │                                  │  │
 │ (é professor)                    │  └──< LMS Quiz
 │                                  │
 ├── Course Evaluator               ├──< LMS Enrollment >── User (aluno)
 │      └──< Evaluator Schedule     │        │
 │      (disponibilidade 1-a-1)     │        └── amount, currency, payment_reference
 │                                  │
 └── vedium_points (custom field)   ├── enable_certification ──► LMS Certificate Evaluation ──► (Google Meet)
                                     │
                                     └──< LMS Live Class (via LMS Batch) ──► (Zoom)

Checkout custom:  Coupon ─┐
                          ├─► api.create_checkout (Stripe) ─► webhook ─► create_enrollment_if_paid ─► LMS Enrollment
              Referral ───┘                                                     │
                                                                                └─► Referral Conversion ─► Coupon (recompensa)
```

---

## Doctypes NATIVOS que sustentam o negócio

| Doctype | App | Representa | Campos-chave | Relações |
|---|---|---|---|---|
| `LMS Course` | lms | Um curso/nível (ex.: "Inglês – Beginner") | `title`, `published`, `paid_course`, `course_price`, `currency`, `evaluator`, `enable_certification`, `category` | tem instrutores, capítulos, matrículas |
| `Course Instructor` | lms | Vínculo professor↔curso (child table) | `parent` (curso), `instructor` (User) | **fonte da verdade de quem leciona o quê** |
| `Course Chapter` / `Course Lesson` | lms | Estrutura de conteúdo | `title`, `idx` | pertencem ao curso |
| `LMS Enrollment` | lms | Matrícula de um aluno num curso | `member`, `course`, `status`, `amount`, `currency`, `payment_reference` | liga User↔Course; `after_insert` dispara sync CRM |
| `Course Evaluator` | lms | Professor como avaliador, com disponibilidade | `evaluator` (User), `schedule` (tabela), `unavailable_from/to` | base do agendamento 1-a-1 |
| `Evaluator Schedule` | lms | Um slot recorrente de disponibilidade | `day`, `start_time`, `end_time` | child de Course Evaluator |
| `LMS Certificate Evaluation` | lms | Uma avaliação 1-a-1 agendada | membro, curso, data, slot, evaluator | gera evento Google Meet |
| `LMS Live Class` | lms | Aula ao vivo em grupo | via Zoom | pertence a `LMS Batch` |
| `LMS Batch` / `LMS Batch Timetable` | lms | Turma/cohorte e sua grade | datas, vagas | agrupa alunos p/ Live Class |
| `LMS Certificate` | lms | Certificado emitido | `member`, `course`, `verification_code`, `issue_date` | ⚠️ ver conflito custom abaixo |
| `CRM Lead` | crm | Lead comercial | `email`, `status` | 🔴 app `crm` quebrado em prod (ver [doc 08]) |
| `HD Ticket` | helpdesk | Chamado de suporte nativo | `raised_by`, `subject`, `status` | ⚠️ funil público usa `Support Ticket` custom |
| `Email Account` | frappe | Conta de envio/recebimento | "Vedium Resend", outgoing ligado | ver [doc 08] |
| `Google Settings` / `Google Calendar` | frappe | Integração de calendário | `enable`, `client_id` | ligado; cada professor autoriza o seu |

## Doctypes CUSTOM (`vedium_core`)

| Doctype | Representa | Campos-chave | Status | Observações |
|---|---|---|---|---|
| `Coupon` | Cupom de desconto | `coupon_code`, `discount_percent`, `active`, `max_uses`, `used_count`, `valid_to` | ✅ em uso | `used_count` incrementado no webhook. |
| `Referral` | Código de indicação de um usuário | `referral_code`, `referrer`, `active`, `discount_percent`, `reward_percent`, `total_conversions` | ✅ em uso | Trafega pelo mesmo `coupon_code` do checkout. |
| `Referral Conversion` | Indicação que virou matrícula | `referrer`, `referee`, `course`, `reward_coupon`, `converted_on` | ✅ em uso | 1 recompensa por indicado. |
| `Placement Test` | Teste de nível público | perguntas, resultado CEFR | ✅ em uso | Pré-matrícula, sem login. |
| `Placement Test Question` | Pergunta do teste de nível | enunciado, alternativas | ✅ em uso | child/related do Placement Test. |
| `LMS Badge Log` | Registro de emblema conquistado | `user`, `badge`, `level`, `awarded_on` | ✅ em uso | Alimenta gamificação/streak. |
| `Support Ticket` | Chamado vindo do funil público | `subject`, `description`, `category`, `status`, `opened_by` | ⚠️ reconciliar | Coexiste com `HD Ticket` nativo. |
| `Flashcard` | Flashcard (modelo A) | frente/verso | ⚠️ duplicado | Coexiste com `LMS Flashcard`. |
| `LMS Flashcard` | Flashcard (modelo B) | `user`, `front`, `back`, `course` | ⚠️ duplicado | Usado em `meu-progresso.py`. Definir o canônico. |
| `LMS Certificate` (custom) | Certificado | `enrollment`, `member`, `course`, `issue_date`, `verification_code` | 🔴 **colisão confirmada** | O JSON custom tem `name: "LMS Certificate"` (módulo "Vedium Core") — **mesmo nome do doctype nativo do LMS**. Como nome de doctype é único no Frappe, um sobrescreve o outro no `bench migrate` (o último a migrar vence). Precisa resolver: renomear o custom (ex.: `Vedium Certificate`) ou eliminá-lo e usar o nativo. |
| `Lesson Slot` | Horário de aula (modelo antigo) | `teacher`, `student`, `course`, `start_time`, `end_time`, `status`, `meeting_link` | 🔴 **Legado** | **Substituído pelo agendamento nativo.** Permissão travada (role "All" só leitura) como correção de segurança. Não referenciar em código novo. |

## Campos custom em doctypes nativos

| Doctype nativo | Campo custom | Tipo | Para quê | Definido em |
|---|---|---|---|---|
| `User` | `vedium_points` | Int (read-only) | Gamificação | `custom_setup.py` |
| `User` | `preferred_language` | Link → Language | Idioma preferido | `custom_setup.py` |

> Campos custom são criados idempotentemente no `install.py` (`setup_custom_fields`),
> que roda no after-migrate. `gamification.add_points` depende de `User.vedium_points`.

## Pontos de atenção (dívida de modelo)

1. 🔴 **`LMS Certificate` — colisão de nome confirmada** (nativo do LMS + custom
   em "Vedium Core", ambos `name: "LMS Certificate"`). No `bench migrate`, um
   sobrescreve o outro. Resolver antes de qualquer trabalho em certificação
   ([doc 07]): renomear o custom para `Vedium Certificate` ou removê-lo em favor
   do nativo.
2. ⚠️ **Flashcards duplicados** (`Flashcard` + `LMS Flashcard`) — escolher um,
   migrar, aposentar o outro.
3. ⚠️ **Suporte duplicado** (`Support Ticket` custom + `HD Ticket` nativo) — o
   ideal é o funil público criar `HD Ticket`; hoje cria o custom.
4. 🔴 **`Lesson Slot` legado** — manter só até confirmar que nada o usa, depois
   avaliar remoção. `meu-progresso.py` ainda o lê (tolerante a vazio).
