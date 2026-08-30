# 24 — Auditoria das páginas legais

Auditoria da Fase F.4 realizada em **29 de agosto de 2026**, antes e depois da migração local para Next.js. Nenhum deploy, alteração de DNS, Stripe ou Frappe foi executado.

## Fonte de verdade e divergências encontradas

| Rota | Fonte Frappe atual | Produção | Artefato histórico | Decisão registrada |
|---|---|---|---|---|
| `/privacidade` | `vedium_core/vedium_core/www/privacidade.html` | 200 e conteúdo idêntico ao template atual | `deploy/site/privacidade.html`, versão de 29/05/2026 e texto materialmente diferente | Migrar o documento público/Frappe de 05/07/2026; não usar o HTML estático antigo |
| `/termos` | `vedium_core/vedium_core/www/termos.html` | 200 e conteúdo idêntico ao template atual | `deploy/site/termos.html`, versão de 29/05/2026 e texto materialmente diferente | Migrar o documento público/Frappe de 05/07/2026; não usar o HTML estático antigo |
| `/cancelamento-reembolso` | `vedium_core/vedium_core/www/cancelamento-reembolso.html` | 200 e conteúdo idêntico ao template atual | Nenhum equivalente em `deploy/site` | Migrar o documento público/Frappe de 05/07/2026 |

Não foi encontrada fonte de conteúdo dessas três páginas em DocType/banco. Os documentos atuais são templates versionados no app Frappe. O snapshot público e os templates atuais têm paridade textual exata; os HTMLs de `deploy/site` são históricos e não normativos.

Versão técnica auditada:

- `SOURCE_VERSION`: commit `44d2c303e06cad1664cae2d98547ba1736fc068e` (último commit que toca os três templates; 27/08/2026).
- `MIGRATED_TO_NEXT_AT`: 29/08/2026. Esta data é técnica e **não** substitui a data jurídica exibida.
- Data jurídica preservada: 5 de julho de 2026.

## Snapshot de produção

O snapshot textual integral está materializado nos três arquivos de conteúdo abaixo. Eles contêm todos os headings, parágrafos, listas, tabelas, links, avisos, dados de entidade, contato, data e carimbo legal capturados da produção:

- `frontend/src/content/legal/privacy.ts`
- `frontend/src/content/legal/terms.ts`
- `frontend/src/content/legal/cancellation-refund.ts`

Os hashes normalizados desses snapshots estão em `25-legal-content-parity.md`. A verificação automatizada lê o texto público em `.vd-legal .container`, lê o snapshot servido pelo Next em `[data-legal-source-content]`, remove apenas o índice adicional e normaliza whitespace/markup. Portanto, o snapshot não depende do DOM antigo para ser reconstituído.

## Auditoria HTTP e SEO de produção

| Campo | `/privacidade` | `/termos` | `/cancelamento-reembolso` |
|---|---|---|---|
| HTTP status | 200 | 200 | 200 |
| Final URL | `https://vediums.com/privacidade` | `https://vediums.com/termos` | `https://vediums.com/cancelamento-reembolso` |
| Title | `Política de Privacidade - Vedium` | `Termos de Uso e Contratação - Vedium` | `Cancelamento e Reembolso - Vedium` |
| Meta description | Como a Vedium coleta, usa e protege dados pessoais em conformidade com a LGPD. Direitos dos titulares, DPO e canais de contato. | Termos de Uso e Contratação da Vedium: cadastro, planos, pagamento, aulas ao vivo, cancelamento e propriedade intelectual. | Regras de cancelamento de assinatura, direito de arrependimento de 7 dias corridos e reembolso na Vedium. Sem fidelidade, sem multa. |
| Canonical | self | self | self |
| Robots | `index, follow` | `index, follow` | `index, follow` |
| H1 | Política de Privacidade | Termos de Uso e Contratação | Política de Cancelamento e Reembolso |
| H2 do documento | 13 | 14 | 10 |
| Word count normalizado | 932 | 854 | 544 |
| Links no documento | 13 | 14 | 6 |
| Última atualização exibida | 05/07/2026 | 05/07/2026 | 05/07/2026 |

### Headings reais

- Privacidade: `1. Quem somos...` até `13. Atualizações`.
- Termos: `1. Aceitação` até `14. Alterações`.
- Cancelamento: `1. Assinatura mensal` até `10. Como solicitar cancelamento ou reembolso`.

O header/footer Frappe antigo acrescenta headings de interface fora do documento. Eles não fazem parte do snapshot jurídico. O Next mantém exatamente um H1 e usa H2 para todas as seções jurídicas.

## Entidade e contato

### Dados preservados

- Razão social nos documentos: `VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA`.
- CNPJ: `58.434.869/0001-24`.
- Endereço presente nos Termos: Av. Eng. Luiz Carlos Berrini, 1681, Conj. Salas 111 e 112, Cidade Monções, São Paulo/SP, CEP 04571-011.
- Contato dos Termos e cancelamento: `contato@vediums.com`.
- DPO da Política de Privacidade: `dpo@vediums.com`.

Classificação dos canais: **CURRENT / VERIFIED**. Os e-mails coincidem com o backend do formulário, o contrato institucional e a página de Contato. O endereço foi preservado sem alteração; não há fonte autorizando removê-lo ou substituí-lo.

### LEGAL REVIEW REQUIRED — grafia da razão social no Footer Next

O contrato institucional (`docs/frontend-v2/20-institutional-entity-contract.md`) e os documentos legais usam `EDUCACAO`, sem acento. O Footer Next congelado usa `EDUCAÇÃO`, com acento, em `frontend/src/content/site/footer.ts`. O CNPJ é o mesmo. O Footer compartilhado não foi modificado nesta fase. Confirmar a grafia cadastral oficial e corrigir o contrato global em uma fase autorizada; não alterar silenciosamente o texto jurídico.

## Links legais

Resultado dos 33 links encontrados nos documentos (12 destinos únicos):

- `TOTAL LINKS`: 33
- `VALID`: 33
- `BROKEN`: 0
- `REDIRECTED`: 0

Inclui três PDFs, as três páginas migradas, `/cookies`, `/gravacao-imagem-voz`, `/privacidade/meus-dados`, `/propriedade-intelectual` e os canais `mailto:`. Todos respondem em produção. No Next isolado, os documentos/PDFs não migrados são preservados por rewrites explícitos para `app.vediums.com`; todos retornaram 200 após o build.

## Formulário e Política de Privacidade

**FORM/PRIVACY CONSISTENCY: PASS.** O formulário coleta nome, e-mail, telefone opcional, assunto/objetivo, idioma e mensagem; encaminha para ticket/CRM e envia e-mails. A política atual cobre cadastro (nome, e-mail, telefone, idioma e dados necessários), comunicações e histórico de suporte, e-mail/CRM/suporte como operadores, finalidade de relacionamento e retenção de leads. O formulário ainda exibe aviso de privacidade com link para `/privacidade`.

## Cookies e Consent Mode

### LEGAL REVIEW REQUIRED — contrato de consentimento não foi portado ao Next

A política menciona cookies, dados técnicos e transferência internacional ao usar analytics. A implementação Frappe possui Consent Mode v2 e banner com aceitar/recusar/preferências (`docs/redesign/45-consent-remediation-result.md`). O frontend Next atual não carrega GTM, GA4, Meta Pixel, `cookie-consent.js` nem `consent-mode-v2.js`; existe apenas um `dataLayer.push` local nos links rastreados de WhatsApp, sem carregador de analytics.

Diferença exata: a página legal foi migrada, mas o mecanismo de consentimento auditado no Frappe não existe no runtime Next. Não foi acrescentada nem reescrita cláusula. Antes de deploy/cutover do Next, decidir se o runtime permanecerá sem analytics ou portar o contrato de consentimento e validar o container GTM. Até essa decisão: **COOKIE/PRIVACY CONSISTENCY = LEGAL REVIEW REQUIRED**.

## Cobrança e política jurídica

### BILLING / LEGAL CONTRACT MISMATCH — LEGAL REVIEW REQUIRED

Os documentos afirmam que “Planos mensais B2C não têm fidelidade nem multa” e que o cancelamento impede novas cobranças futuras. Já `docs/plataforma/08-fluxo-pagamento-assinaturas.md` e `stripe_billing.py` implementam permanência mínima de 6/12 meses para planos semestral/anual cobrados mensalmente; cancelamentos antecipados ficam em `Cancellation Requested` e não são enviados automaticamente à Stripe.

Pode haver distinção comercial válida entre “plano mensal” e “plano semestral/anual com cobrança mensal”, mas os textos e o código não eliminam a ambiguidade. Nenhuma cláusula nem regra Stripe foi alterada. Revisão jurídica/comercial deve confirmar quais ofertas B2C estão cobertas e alinhar checkout, política e operação.

## Classificação de mudanças

### MIGRATED AS-IS

- Todo o texto jurídico, datas, entidades, contatos, prazos, condições, exceções, links e referências cruzadas.
- Titles, descriptions, canonicals, robots e URLs.

### TECHNICAL FORMATTING CHANGE

- Renderer server-side tipado, headings semânticos e listas reais.
- Tabelas com headers/escopo, região rolável e foco de teclado.
- Índice gerado exclusivamente dos headings existentes.
- Coluna de leitura limitada, foco visível e responsividade.
- Navegação adicional entre os três documentos, fora do snapshot de paridade.

### CONTENT DIFFERENCE

- Nenhuma entre produção/Frappe atual e o Next.
- Os HTMLs antigos de `deploy/site` divergem, mas não foram usados.

### LEGAL REVIEW REQUIRED

- Grafia da razão social no Footer Next.
- Contrato Consent Mode/cookies do runtime Next.
- Ambiguidade entre permanência mínima de billing e “planos mensais sem fidelidade”.

## Deploy

`DEPLOY: NOT PERFORMED`
