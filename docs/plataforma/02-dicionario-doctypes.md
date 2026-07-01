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
| `Support Ticket` | Chamado vindo do funil público | `subject`, `description`, `category`, `status`, `opened_by` | ⚠️ ambíguo, ver nota | Coexiste com `HD Ticket` nativo. Ambos vazios de uso real em produção — ver "Pontos de atenção" abaixo. |
| ~~`Flashcard`~~ | ~~Flashcard c/ SRS (SM-2)~~ | ~~frente/verso + `next_review`/`interval`/`ease_factor`~~ | 🗑️ **removido 2026-07-01** | Órfão confirmado: 0 referências em `vedium_core/` (nem leitura nem escrita, inclusive o método `update_srs` nunca era chamado) e 0 registros em produção. Doctype JSON+.py removidos do repo. Tabela `tabFlashcard` pode ficar órfã no MySQL de produção (schema mais completo que o LMS Flashcard, incluía repetição espaçada — se algum dia quiser reviver spaced repetition, este era o modelo mais adequado, mas hoje é código morto). |
| `LMS Flashcard` | Flashcard em uso | `user`, `front`, `back`, `course` | ✅ **é o canônico** | Único doctype de flashcard em uso: lido por `api.get_flashcards` e `www/meu_progresso.py`. 0 registros em produção hoje (ninguém salvou flashcard ainda), mas é o modelo ativamente referenciado pelo código — não é órfão, só ainda sem dados. |
| `LMS Certificate` (custom) | Certificado | `enrollment`, `member`, `course`, `issue_date`, `verification_code` | 🔴 **colisão confirmada** | O JSON custom tem `name: "LMS Certificate"` (módulo "Vedium Core") — **mesmo nome do doctype nativo do LMS**. Como nome de doctype é único no Frappe, um sobrescreve o outro no `bench migrate` (o último a migrar vence). Precisa resolver: renomear o custom (ex.: `Vedium Certificate`) ou eliminá-lo e usar o nativo. |
| `Lesson Slot` | Horário de aula (modelo antigo) | `teacher`, `student`, `course`, `start_time`, `end_time`, `status`, `meeting_link` | 🔴 **Legado** | **Substituído pelo agendamento nativo.** 0 registros em produção (confirmado 2026-07-01). Permissão travada (role "All" só leitura) como correção de segurança. Leitura morta em `meu_progresso.py` removida 2026-07-01. Único uso restante: `public_funnel.get_available_diagnostic_slots`, mantido de propósito (sempre vazio) até decisão de produto. Não referenciar em código novo além disso. |

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
2. ✅ **Flashcards duplicados — resolvido 2026-07-01.** `Flashcard` (modelo
   com SRS/SM-2) tinha 0 referências em todo `vedium_core/` e 0 registros em
   produção — órfão confirmado, removido do repo (JSON + .py). `LMS Flashcard`
   é o único canônico (lido por `api.get_flashcards` e `meu_progresso.py`).
   Não havia dado para migrar (Flashcard também estava vazio em produção).
3. ⚠️ **Suporte duplicado — investigado 2026-07-01, permanece ambíguo, NÃO migrado.**
   Evidência coletada em produção:
   - `Support Ticket` (custom, criado pelo funil público): **0 registros**.
   - `HD Ticket` (nativo Helpdesk): **1 registro**, e é o ticket-seed
     `"Welcome to Helpdesk"` de `john@example.com` criado pela própria
     instalação do app — não é um chamado real de cliente.
   - Usuários "System User" reais no site: só `Administrator`,
     `ivonmatos@vediums.com` (dono) e `almirseller@yahoo.com`. **Nenhum**
     tem role `Agent`, `Agent Manager` ou `HD Agent` — ou seja, não há
     evidência de que alguém da equipe opere a tela `/helpdesk` no dia a dia.
   - Conclusão: **não dá para dizer que a equipe "usa" HD Ticket** (não tem
     agente configurado, não tem ticket real) **nem que usa Support Ticket**
     (zero registros — o funil público existe mas aparentemente ninguém
     preencheu o formulário ainda, ou os leads chegam só por e-mail/WhatsApp).
     Como a tarefa exige evidência de uso real e não há nenhuma nos dois
     lados, a migração **não foi feita** — forçá-la seria suposição, não
     dado. Sinal indireto: `reports.py` (digest semanal) e `integrations.py`
     (`get_student_360`) já leem `HD Ticket`, sugerindo que a intenção de
     produto era consolidar em `HD Ticket`, mas isso não foi confirmado com
     uso real. Reavaliar quando houver um agente de suporte configurado de
     fato — nesse momento, comparar de novo as contagens.
4. ✅ **`Lesson Slot` legado** — leitura morta em `meu_progresso.py` removida
   2026-07-01 (0 registros em produção, para sempre). Doctype **mantido** (não
   removido do repo) porque `public_funnel.get_available_diagnostic_slots`
   ainda o consulta ativamente para a aula diagnóstica pública — remover o
   doctype quebraria esse endpoint. Reavaliar remoção só se/quando a aula
   diagnóstica migrar para o Course Evaluator nativo (decisão de produto, fora
   de escopo desta limpeza).
