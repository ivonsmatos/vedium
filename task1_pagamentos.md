# Task 1: Pagamentos Online – Ampliação e Robustez

## Subtarefas

1. Implementar classes/funções para Mercado Pago e Basecommerce, semelhantes ao Stripe.
2. Criar: `create_mercadopago_checkout`, `handle_mercadopago_webhook`.
3. Abstrair o fluxo de pagamentos (strategy/factory pattern).
4. Centralizar webhooks de pagamentos.
5. Oferecer seleção de gateway pelo usuário no checkout.
6. Implementar tela de histórico de pagamentos/faturas.
7. Permitir cupons em promoções e códigos especiais.
8. Testes automatizados: simular falha, duplicidade, chargeback nos sandboxes.

## Referências

- vedium_core/api.py
- vedium_core/docs/api.md
- deploy/apps.txt
- deploy/SECURITY.md

## Critérios de Aceite

- Integração funcional com Mercado Pago e Basecommerce.
- Fluxo de pagamento extensível para novos gateways.
- Webhooks centralizados e rastreáveis.
- Checkout com seleção de gateway e cupons.
- Testes automatizados cobrindo cenários críticos.
