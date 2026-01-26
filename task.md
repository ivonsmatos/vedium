# Task 8: Migração ERPNext v16 (Estável)

- [x] Realizar backup completo (Banco + Arquivos).
- [x] Migrar apps para branch `version-16`.
- [x] Executar `bench update --upgrade`.
- [x] Validar integridade e Identidade "Raízes de Luxo".

## 1a) Mercado Pago e Basecommerce

- [x] Implementar classes/funções para Mercado Pago e Basecommerce, semelhantes ao Stripe.
- [x] Criar: `create_mercadopago_checkout`, `handle_mercadopago_webhook`.
- [x] Abstrair o fluxo de pagamentos (strategy/factory pattern).
- [x] Centralizar webhooks de pagamentos.

## 1b) Checkout UI/UX

- [/] Oferecer seleção de gateway pelo usuário.
- [x] Implementar tela de histórico de pagamentos/faturas.

## 1c) Entrada de cupons/descontos

- [x] Permitir cupons em promoções e códigos especiais.

## 1d) Testes automatizados para pagamentos

- [x] Simular falha, duplicidade, chargeback nos sandboxes. (Testes unitários com mock implementados)

---

# Task 2: Plataforma de Cursos de Idiomas – Funcionalidades Avançadas

- [x] Certificados digitais automáticos com código de verificação.
- [x] Quiz/prova de nível com feedback instantâneo.
- [x] Suporte a aulas ao vivo e gravadas (Zoom, Meet, Vimeo/Youtube).
- [x] Feedback automatizado (IA): avaliações de áudio/texto, dashboards. (Serviço de IA integrado)
- [/] Recursos extras: escuta ativa, gravação de áudio, flashcards. (Placeholders implementados)
- [x] Gamificação: emblemas, níveis, rankings.
- [x] Comunidade: fórum, integração Telegram/Discord/Slack.
- [x] Acessibilidade e internacionalização.

---

# Task 3: UI/UX e Layout – Raízes de Luxo

- [x] Auditoria prática do Design System em TODOS os apps (LMS, CRM, ERP).
- [x] Padronização de botões, fontes (Inter/Bodoni) e cores (Raízes de Luxo v2 - #26528C, #BFA288).
- [x] Microinterações: animações em CTAs, feedback AJAX, loading states.
- [x] Performance: Lighthouse, lazy loading, SVGs otimizados, Service Worker customizado.
- [x] Cadastro/onboarding: frases motivacionais, progresso, login Google/Linkedin.
- [x] Escalabilidade visual: white-label/skinning.

---

# Task 4: Segurança Avançada

- [/] Pentest regular (OWASP ZAP, etc). (Agendado/Documentado)
- [/] Gestão de segredo: variáveis de ambiente. (Parcialmente verificado)
- [x] Auditoria de dependências: alertas automáticos.

---

# Task 5: Observabilidade e Suporte

- [x] Painel de suporte para chamados.
- [x] Monitoramento automático: dashboard, webhooks para falhas/fraudes. (Prometheus/Grafana configurados)
- [x] Métricas: Google Analytics 4, Hotjar/Clarity, LGPD.

---

# Task 7: Frappe LMS (Official)

- [x] Instalar o app `erpnext`, `crm`, `hrms` e `helpdesk`.
- [x] Configurar o Portal LMS inicial.
- [x] Configurar Central de Ajuda e Suporte ao Cliente (Help Desk).
- [x] Configurar Módulo de RH (HRMS) e Operações de Pessoal.
- [x] Implementar Teste de Nivelamento (Placement Test) no LMS.
- [x] Implementar Agendamento de Aulas Individuais (Booking System).
- [x] Implementar Flashcards (SRS).
- [x] Expandir IA de Pronúncia para Análise Fonética.
- [x] Configurar Gamificação (Pontos, Níveis, Rankings).
- [x] Migrar as customizações do `vedium_core` (Mercado Pago, IA) para trabalhar com o oficial.
