# Assinaturas recorrentes Stripe

## Modelo comercial implementado

- O checkout usa `mode="subscription"` e o `Product Price ID` do
  `Subscription Plan` explicitamente ligado ao curso.
- Os planos semestral e anual têm permanência mínima de 6 e 12 meses,
  respectivamente, com cobrança mensal.
- Somente BRL e USD, cartão e Price recorrente mensal ativo são aceitos.
- Boleto não é considerado aprovado para recorrência.
- Descontos são aplicados somente à primeira mensalidade.

## Permanência e cancelamento

Uma solicitação feita antes do fim da permanência mínima recebe o status
`Cancellation Requested` e fica pendente de análise. O código não cria multa,
não inventa cobrança e não envia cancelamento automático à Stripe antes dessa
data. Após a permanência, a solicitação agenda `cancel_at_period_end`.

Se a Stripe informar que uma assinatura foi apagada antes do fim da
permanência, a matrícula permanece em `Cancellation Requested` para análise.
Após o prazo, passa para `Cancelled`.

## Acesso ao LMS

`Active`, `Trial`, `Cancellation Requested` e `Pending Review` mantêm acesso.
`Suspended`, `Cancelled`, `Ended` e `Expired` bloqueiam curso, capítulos,
lições, quizzes, progresso, discussões, turma e aula ao vivo. Administradores,
moderadores, avaliadores e professores vinculados continuam autorizados.

Falha de pagamento inicia tolerância de 10 dias. `invoice.paid` limpa a falha
e reativa automaticamente o acesso. Contestação ou reembolso integral suspende
o acesso; reembolso parcial fica em `Pending Review`.

## Webhook

Endpoint de produção:

`https://app.vediums.com/api/method/vedium_core.api.stripe_webhook`

Eventos obrigatórios:

- `checkout.session.completed`
- `invoice.paid`
- `invoice.payment_failed`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `charge.refunded`
- `charge.dispute.created`

A assinatura é validada com `STRIPE_WEBHOOK_SECRET`. Cada `event.id` é
registrado de forma idempotente em `Integration Request`, sem payload, headers,
chaves ou dados pessoais. Eventos falhos ficam como `Failed` e podem ser
reenviados pela Stripe; eventos concluídos não são processados novamente.
