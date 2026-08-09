# 16 — Brevo: o que fazer FORA do código (checklist do dono)

> **Objetivo:** deixar o kit de e-mail (96 modelos em `Cliente/Vedium/emailmkt`)
> no ar e ligar o "cutover" com **um único comando**. O lado Frappe já está
> pronto: sincroniza contatos, emite eventos e tem gates anti-duplicação.
> Falta o que só pode ser feito **no painel do Brevo** (+ 1 toggle no Stripe).
>
> Complementa o [09-integracao-brevo-api.md](09-integracao-brevo-api.md) (parte
> técnica) e o `README.md`/`QA-BREVO.md` do kit em `Cliente/Vedium/emailmkt`.

---

## Visão geral: quem faz o quê

| Camada | Responsável | Estado |
|---|---|---|
| Sincronizar contato + atributos + eventos | Frappe (`brevo.py`) | ✅ pronto |
| Renderizar e enviar os e-mails de ciclo de vida | **Brevo (você)** | ⏳ este doc |
| Não enviar em dobro durante a transição | Frappe (chave `BREVO_LIFECYCLE_LIVE`) | ✅ pronto |

Enquanto você não termina os passos abaixo, o **Frappe é o remetente interino**
(boas-vindas, dunning e nudge de ativação saem por e-mail simples). Ao concluir,
você liga a chave e o Brevo assume — sem e-mail duplicado, sem buraco.

> **Estado verificado (2026-08-09):** ✅ passos **1, 2 e 4 concluídos** — chave OK
> (`test_connection` conecta na conta VEDIUM GLOBAL), atributos criados
> (`setup_brevo_schema` rodou), domínio `vediums.com` autenticado. `is_enabled`=
> true → **eventos já estão sendo emitidos** e `upsert_contact`/`track_event`
> foram testados e **passam** com os atributos atuais. Rodado um backfill de
> contatos (8 matrículas + 2 leads). ⚠️ Havia 15 eventos antigos travados em
> "Queued" — eram de **antes de os atributos existirem** (o Brevo rejeitava o
> upsert com HTTP 400); são obsoletos e não precisam ser reenviados (reenviar
> dispararia onboarding pra quem já é aluno). **Falta:** passos **3, 5, 6 e 8.**

---

## Passo a passo

### 1. Chaves e conexão (uma vez)
No site config do Frappe (servidor) — se ainda não estiver feito:

```bash
docker exec vedium-frappe bench --site app.vediums.com set-config BREVO_API_KEY "xkeysib-..."
docker exec vedium-frappe bench --site app.vediums.com set-config BREVO_ENABLED 1
docker exec vedium-frappe bench --site app.vediums.com set-config BREVO_CONTACT_LIST_IDS "[<ID_da_lista>]"
```

Use uma **API key normal** do Brevo (não token MCP). Teste a conexão:

```bash
docker exec vedium-frappe bench --site app.vediums.com execute vedium_core.brevo.test_connection
```

### 2. Criar os atributos de contato (uma vez)
Rode isto — cria no Brevo os atributos que os modelos leem, sem apagar nada:

```bash
docker exec vedium-frappe bench --site app.vediums.com execute vedium_core.brevo.setup_brevo_schema
```

Isso garante estes atributos (nomes exatos, MAIÚSCULAS):

- **Lidos no corpo dos modelos:** `COURSE`, `LEVEL`, `COMPANY`,
  `ENROLLMENT_STATUS`, `LIFECYCLE_STAGE`, `COMMUNICATION_LANGUAGE`
- **Técnicos/segmentação:** `VEDIUM_USER_ID`, `VEDIUM_COURSE_ID`,
  `VEDIUM_COURSE`, `VEDIUM_STATUS`, `VEDIUM_TRIAL_END`,
  `VEDIUM_BILLING_PERIOD`, `VEDIUM_PAYMENT_CURRENCY`, `VEDIUM_CRM_STATUS`,
  `VEDIUM_SOURCE`

> `FIRSTNAME`/`LASTNAME`/`SMS` já são padrão do Brevo. **Não** use
> `COURSE_INTEREST` — o Frappe manda o curso em `COURSE`.
> ⚠️ `LEVEL` ainda não é populado pelo Frappe (o teste de nível é client-side e
> não persiste o resultado — ver backlog). Os modelos usam `|default`, então não
> quebra; só não personaliza por nível até isso ser construído.

### 3. Importar os 96 modelos
No Brevo: **Marketing → Templates → Email → New template → Start from scratch →
HTML custom code**. Para cada linha de `Cliente/Vedium/emailmkt/brevo/catalogo.csv`:

1. Copie o HTML indicado na coluna `arquivo_html`.
2. Copie `assunto` e `pre_cabecalho` do CSV.
3. Nomeie com o `id` como prefixo (ex.: `A08-01 | Boas-vindas e acesso`).
4. Defina remetente e **reply-to monitorado**.
5. Salve e ative.

O CSV funciona como fila de implantação (abre no Excel). São 75 automações
(A01–A20) + 21 campanhas semanais.

### 4. Autenticar o domínio remetente (uma vez)
No Brevo: **Senders, Domains & Dedicated IPs → Domains** → autentique
`vediums.com` (SPF, DKIM, DMARC). Sem isso, entregabilidade cai e cai em spam.

### 5. Montar as automações (o coração)
No Brevo: **Automations → Create → Event based**. Cada fluxo é disparado por um
**evento que o Frappe já emite**. Mapa evento → fluxo do kit:

Todos os eventos abaixo **já são emitidos pelo Frappe hoje** (estão chegando no
Brevo; só falta a automação que os consome). Mapa evento → fluxo do kit:

> ✅ **Catálogo de eventos "primado" (2026-08-09):** o Brevo só lista no dropdown
> de "evento personalizado" eventos já **recebidos ao menos uma vez**. Rodamos
> `bench execute vedium_core.brevo.seed_event_catalog` → **22 eventos disparados**
> (todos da tabela, menos `enrollment_created` que já existia) para um contato-
> semente `brevo-seed@vediums.com`. Então **todos já aparecem** no dropdown para
> montar as automações. Depois: **apague o contato `brevo-seed@vediums.com`** no
> Brevo (não entra em automação futura, mas é lixo) e **exclua a automação antiga
> quebrada "A03 - Teste iniciado"** (aponta pra `test_started`, evento que o
> Frappe **não** emite — nunca vai funcionar). Ao adicionar um evento novo no
> futuro, rode o seed de novo.

| Evento emitido pelo Frappe | Fluxo do kit | Observação |
|---|---|---|
| `enrollment_created` / `enrollment_activated` | **A08** (onboarding) | matrícula paga confirmada |
| `student_not_activated` | **A08-03 / A09** | matriculou e não começou em 3 dias (job diário) |
| `progress_milestone` (param `milestone` = 25/50/75/100) | **A10** | ramifique por `params.milestone` |
| `student_absent` (param `absences`) | **A09** (contato de cuidado) | faltas consecutivas (job diário, sobre a presença nativa) |
| `checkout_started` | **A07** (carrinho abandonado) | emitido ao iniciar o checkout; SAIR em `enrollment_created` |
| `payment_failed` | **A20-03** (falha) | inicia a régua de cobrança |
| `payment_recovered` | — (SAÍDA do A20) | condição de saída, não envio |
| `payment_due_soon` | **A20-01** (lembrete de vencimento) | ⚠️ requer o passo 7 (Stripe) |
| `trial_started` | fluxo de trial | opcional |
| `enrollment_cancelled` / `cancellation_requested` | **A14** (cancelamento) | transacional |
| `lead_created` | **A01** (nutrição inicial) | do CRM; já manda `contact.COURSE` |
| `lead_stale` (param `days_idle`) | **A02 / A13** (nutrição/reengajamento) | lead parado ~7 dias (job diário) |
| `lead_status_changed` / `lead_converted` | ramificar por estágio | lead perdido = status `Unqualified`/`Junk` → **A14** |

Params disponíveis nos eventos (para os `{{ params.* }}`):
- **Matrícula/marco/ativação:** `student_portal_url`, `onboarding_url`,
  `progress_url`, `course_url`, `billing_url`, `payment_update_url` (ambos =
  portal de cobrança Stripe), `course`, `course_level`, `amount`, `milestone`,
  `progress_percent`.
- **Carrinho (`checkout_started`):** `course`, `course_level`, `checkout_url`
  (= página do curso, para re-iniciar), `billing_period`, `classes_per_week`.
- **Cobrança (`payment_due_soon`):** `course`, `course_level`, `amount`,
  `due_date`, `billing_url`, `payment_update_url`.
- **Ausência (`student_absent`):** `course`, `absences`, `support_checkin_url`.

> ⚠️ Alguns gatilhos que você listou são **internos** (não Brevo): "lead novo →
> tarefa comercial" e "24h sem contato → alerta" já rodam no **CRM/Frappe**
> (ToDo + e-mail à coordenação, ver P3), não precisam de automação no Brevo.

**Regras de automação (do README do kit):** dedup por `event_id`; saída em
compra/resposta/descadastro/conclusão; limite 1 e-mail de marketing/24h e 3/7
dias; prioridade para pós-teste, checkout e onboarding; nunca enviar com
`params.*` obrigatório vazio.

### 6. Testes de prova (antes de ligar)
- Dispare um evento real e um duplicado (confirmar dedup).
- Renderize com contato completo **e** com campos vazios (fallbacks).
- Confira links espelho/preferências/descadastro.
- Gmail + Outlook + mobile.
- Revisão do DPO (permissão/preferências/privacidade) e do professor de Iorubá
  no conteúdo A15.

### 7. (Opcional, para A20-01) Ligar o `invoice.upcoming` no Stripe
O evento `payment_due_soon` (lembrete 3 dias antes) depende de o Stripe avisar a
fatura que vem. No painel do Stripe: **Developers → Webhooks → seu endpoint →
Add events → `invoice.upcoming`**. O handler no Frappe já trata (ver `stripe_billing.py`).
> Configure o "Upcoming invoice" para ~3 dias antes em **Billing → Settings**.

### 8. 🔑 O CUTOVER (um comando)
Quando os passos 1–6 estiverem prontos e testados:

```bash
docker exec vedium-frappe bench --site app.vediums.com set-config BREVO_LIFECYCLE_LIVE 1
```

A partir daí, `brevo.lifecycle_owned_by_brevo()` fica `True`: o Frappe **para de
enviar** boas-vindas/dunning/nudge por conta própria (só emite os eventos) e o
Brevo assume o corpo e a entrega. Para reverter (voltar o Frappe a enviar):

```bash
docker exec vedium-frappe bench --site app.vediums.com set-config BREVO_LIFECYCLE_LIVE 0
```

---

## Checklist rápido

- [x] 1. `BREVO_API_KEY` / `BREVO_ENABLED` / `BREVO_CONTACT_LIST_IDS` + `test_connection` ✅
- [x] 2. `setup_brevo_schema` (atributos) ✅
- [ ] 3. 96 modelos importados (via `catalogo.csv`)
- [x] 4. Domínio `vediums.com` autenticado (SPF/DKIM/DMARC) ✅
- [ ] 5. Automações montadas (evento → fluxo, tabela acima)
- [ ] 6. Testes de prova (real + duplicado + campos vazios + clientes)
- [ ] 7. (Opcional) `invoice.upcoming` no Stripe → `payment_due_soon`
- [ ] 8. **`BREVO_LIFECYCLE_LIVE 1`** — cutover

---

## O que o Frappe já garante (não precisa fazer nada)

- Upsert de contato com `COURSE`/`ENROLLMENT_STATUS` (matrícula) e `COMPANY` (lead).
- Emissão idempotente dos eventos acima (dedup durável via Integration Request).
- `params.*` com links reais (área do aluno, portal de cobrança Stripe).
- Nudge de ativação diário (`student_not_activated`) e marcos (`progress_milestone`).
- Gates anti-duplicação amarrados na chave `BREVO_LIFECYCLE_LIVE`.

Referências: `vedium_core/brevo.py`, `student_onboarding.py`, `gamification.py`,
`stripe_billing.py`; memória do projeto: ciclo de vida de e-mail = kit Brevo.
