# Task 1: Pagamentos Online – Ampliação e Robustez

## 1a) Mercado Pago e Basecommerce

- Implementar classes/funções para Mercado Pago e Basecommerce, semelhantes ao Stripe.
- Criar: `create_mercadopago_checkout`, `handle_mercadopago_webhook`.
- Abstrair o fluxo de pagamentos (strategy/factory pattern).
- Centralizar webhooks de pagamentos.

## 1b) Checkout UI/UX

- Oferecer seleção de gateway pelo usuário.
- Implementar tela de histórico de pagamentos/faturas.

## 1c) Entrada de cupons/descontos

- Permitir cupons em promoções e códigos especiais.

## 1d) Testes automatizados para pagamentos

- Simular falha, duplicidade, chargeback nos sandboxes.

---

# Task 2: Plataforma de Cursos de Idiomas – Funcionalidades Avançadas

- Certificados digitais automáticos com código de verificação.
- Quiz/prova de nível com feedback instantâneo.
- Suporte a aulas ao vivo e gravadas (Zoom, Meet, Vimeo/Youtube).
- Feedback automatizado (IA): avaliações de áudio/texto, dashboards.
- Recursos extras: escuta ativa, gravação de áudio, flashcards.
- Gamificação: emblemas, níveis, rankings.
- Comunidade: fórum, integração Telegram/Discord/Slack.
- Acessibilidade e internacionalização.

---

# Task 3: UI/UX e Layout

- Auditoria prática do Design System (design_audit.md).
- Microinterações: animações em CTAs, feedback AJAX, loading states.
- Performance: Lighthouse, lazy loading, SVGs otimizados, Service Worker customizado.
- Cadastro/onboarding: frases motivacionais, progresso, login Google/Linkedin.
- Escalabilidade visual: white-label/skinning.

---

# Task 4: Segurança Avançada

- Pentest regular (OWASP ZAP, etc).
- Gestão de segredo: variáveis de ambiente.
- Auditoria de dependências: alertas automáticos.

---

# Task 5: Observabilidade e Suporte

- Painel de suporte para chamados.
- Monitoramento automático: dashboard, webhooks para falhas/fraudes.
- Métricas: Google Analytics 4, Hotjar/Clarity, LGPD.

---

# Task 6: Documentação

- API pública: Swagger/Redoc, exemplos reais.
- Onboarding rápido para professores.
- OpenAPI Schemas automáticos para endpoints de pagamentos.
