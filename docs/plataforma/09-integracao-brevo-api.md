# Integração Frappe → Brevo pela API

## Objetivo

Sincronizar a base operacional da Vedium com o Brevo sem transformar o Brevo
na fonte da verdade acadêmica ou financeira.

- **Frappe/LMS/Stripe:** matrícula, curso, status, trial e pagamento.
- **Brevo:** contatos, segmentação, automações e comunicação de marketing.

A integração usa:

- `POST /v3/contacts` com `updateEnabled=true` para criar ou atualizar contatos;
- `POST /v3/events` para disparar eventos comportamentais;
- `Integration Request` no Frappe para idempotência, sem armazenar payload ou
  dados pessoais no log;
- filas do Frappe para não bloquear matrícula, checkout ou edição administrativa.

## 1. Criar a chave correta no Brevo

Crie uma **chave API comum** em Brevo → SMTP e API → Chaves de API.

Não use a chave MCP nessa integração. Não grave a chave no GitHub, em arquivo
`.env` versionado, em print ou em conversa.

## 2. Configurar o site Frappe

No servidor, dentro de `/home/frappe/frappe-bench`:

```bash
bench --site app.vediums.com set-config BREVO_API_KEY "SUA_CHAVE_API"
bench --site app.vediums.com set-config BREVO_ENABLED 1
```

Opcional: adicionar todos os contatos sincronizados a uma ou mais listas já
existentes no Brevo:

```bash
bench --site app.vediums.com set-config BREVO_CONTACT_LIST_IDS '[12, 18]'
```

Opcional: permitir que telefones brasileiros sem DDI sejam normalizados para
`+55`:

```bash
bench --site app.vediums.com set-config BREVO_DEFAULT_COUNTRY_CODE "+55"
```

A configuração fica em `sites/app.vediums.com/site_config.json`, fora do
repositório.

## 3. Fazer deploy da branch/PR

Após merge e atualização do servidor:

```bash
cd /home/frappe/frappe-bench
bench --site app.vediums.com migrate
bench --site app.vediums.com clear-cache
bench restart
```

## 4. Validar a conexão

```bash
bench --site app.vediums.com execute vedium_core.brevo.test_connection
```

Resultado esperado:

```json
{
  "connected": true,
  "company": "Vedium",
  "email": "...",
  "enterprise": false
}
```

Erro `401` significa chave ausente, inválida ou revogada. Erro `429` indica
limite temporário da API.

## 5. Criar os atributos Vedium no Brevo

```bash
bench --site app.vediums.com execute vedium_core.brevo.setup_brevo_schema
```

A operação é idempotente: cria somente atributos ausentes e não altera nem
exclui atributos existentes.

Atributos criados:

- `VEDIUM_USER_ID`
- `VEDIUM_COURSE_ID`
- `VEDIUM_COURSE`
- `VEDIUM_STATUS`
- `VEDIUM_TRIAL_END`
- `VEDIUM_BILLING_PERIOD`
- `VEDIUM_PAYMENT_CURRENCY`
- `VEDIUM_CRM_STATUS`
- `VEDIUM_SOURCE`

## 6. Sincronizar a base existente

```bash
bench --site app.vediums.com execute vedium_core.brevo.enqueue_full_sync
```

O comando apenas enfileira os registros. Acompanhe os workers e os registros de
`Integration Request` com serviço `Brevo API`.

A importação de matrículas atualiza contatos sem disparar automações históricas.
Leads existentes são enviados com o evento `lead_imported`.

## 7. Eventos enviados automaticamente

### Matrícula e trial

- `enrollment_created`
- `trial_started`
- `trial_expired`
- `enrollment_activated`
- `enrollment_pending_review`
- `enrollment_suspended`
- `enrollment_cancelled`
- `enrollment_ended`
- `cancellation_requested`

### Pagamento

- `payment_failed`
- `payment_recovered`

### CRM

O módulo contém suporte para:

- `lead_created`
- `lead_updated`
- `lead_status_changed`
- `lead_converted`
- `lead_imported`

A ativação automática de eventos do `CRM Lead` deve ser feita somente depois de
confirmar qual formulário/DocType é a origem oficial dos leads da Vedium. Nesta
primeira etapa, a sincronização automática está ligada ao ciclo de matrícula do
LMS, que já é uma fonte confirmada no ambiente.

## 8. Criar as automações no Brevo

No Brevo, crie workflows iniciados por **evento personalizado**.

Exemplos iniciais:

1. `trial_started` → boas-vindas ao trial, orientação de acesso e lembrete antes
   do vencimento.
2. `trial_expired` → convite para matrícula, sem urgência artificial.
3. `enrollment_created` ou `enrollment_activated` → onboarding do aluno.
4. `payment_failed` → aviso transacional e orientação para regularização.
5. `payment_recovered` → confirmação de regularização e continuidade.
6. `cancellation_requested` → confirmação do pedido e explicação do processo.

Use propriedades do evento para ramificar por curso, status, período e moeda.

## 9. Segurança e LGPD

- A chave é lida somente do `site_config`.
- Headers e payloads nunca são gravados nos logs de erro.
- `Integration Request` guarda somente chave técnica, tipo e situação do envio.
- O Frappe continua sendo a fonte da verdade.
- Descadastro e bloqueio de marketing no Brevo não devem ser revertidos por
  rotinas de sincronização.
- Mensagens financeiras e acadêmicas precisam ser classificadas corretamente
  como transacionais ou de marketing.

## 10. Desativação de emergência

A integração pode ser interrompida sem remover código:

```bash
bench --site app.vediums.com set-config BREVO_ENABLED 0
bench --site app.vediums.com clear-cache
bench restart
```

Matrículas e pagamentos continuam funcionando; apenas os envios ao Brevo são
ignorados.
