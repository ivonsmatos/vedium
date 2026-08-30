# 21 — SEO Parity: `/contato` (CURRENT vs Next local)

Mesmo método dos docs anteriores. Rota Next só existe localmente.

## 1. Rota — auditoria ANTES de construir

Confirmado por HTTP nesta sessão:

| URL | Status |
|---|---|
| `/contato` | **200** |
| `/fale-conosco` | 404 |
| `/contact` | erro de conexão (não resolve) |

`/contato` já é a rota real, já indexada, e já é para onde
`content/site/footer.ts` aponta nesta base de código local
(`{ label: "Contato", href: "/contato" }`). Nenhuma rota concorrente
criada.

## 2. Canais oficiais confirmados

| Canal | Valor | Fonte |
|---|---|---|
| WhatsApp | +55 11 91129-3075 | `content/site/header.ts` (`WHATSAPP_HREF`), já usado em toda a base |
| E-mail institucional | contato@vediums.com | HTML de produção de `/contato` **e** hardcoded como destinatário em `vedium_core/public_funnel.py` (`_create_ticket`) — confirmado por duas fontes independentes |
| E-mail de suporte | suporte@vediums.com | HTML de produção de `/contato` |
| Instagram | @vediumsglobal | Já usado no `sameAs` do JSON-LD `EducationalOrganization` (Home e `/sobre`) |
| Site | vediums.com | — |

Nenhum endereço físico, horário de atendimento, telefone fixo, SLA ou
unidade citado em nenhuma fonte — nada disso foi publicado (missão
seção 2).

## 3. Metadados

| Campo | CURRENT (produção) | NEXT |
|---|---|---|
| `<title>` | "Contato - Vedium" | idêntico |
| description | "Fale com a Vedium: WhatsApp, e-mail e suporte ao aluno. Atendimento 100% online, em todo o Brasil. Tire suas dúvidas sobre os cursos de Inglês e Iorubá." | Atualizada — a produção cita só "Inglês e Iorubá" (desatualizado; hoje são 5 idiomas + B2B, mesmo catálogo já confirmado em todas as fases anteriores). Nova description: "Fale com a Vedium sobre cursos de idiomas, nível, aulas particulares ou soluções para empresas." (texto sugerido pela própria missão F.3, seção 22) |
| canonical | `https://vediums.com/contato` | idêntico |
| robots | `index, follow, max-image-preview:large` | idêntico |

## 4. Hreflang

Produção tem hreflang completo (pt-br, en, es, fr, de, x-default) —
mesmo achado já repetido em `/como-funciona` e `/sobre`: essas traduções
não existem nesta base Next. Contrato mínimo usado: só `pt-br` (self) +
`x-default` (self).

## 5. Schema

`Organization` mínimo (mesmo contrato de `20-institutional-entity-
contract.md`, seção 2) com `ContactPoint` — reaproveita exatamente o
`contactPoint` já usado no `EducationalOrganization` da Home/`/sobre`
(mesmo telefone `+55-11-91129-3075`, mesmo e-mail `contato@vediums.com`).
**Nenhum telefone diferente, nenhum ContactPoint conflitante** (missão
seção 23). `BreadcrumbList` também incluído.

## 6. Formulário existente em produção (achado crítico)

A produção **já tem** um padrão de captura de interesse em várias
landing pages internas (`/aula-diagnostica`, `/matricula`, etc., via o
template compartilhado `templates/includes/public_intent_page.html`),
com um endpoint real e funcional:

```
POST /api/method/vedium_core.public_funnel.submit_public_intent
```

Detalhes completos, incluindo CRM/Brevo/e-mail/anti-spam, em
`23-contact-form-integration-audit.md`. Esse achado muda o formulário
de "PENDING" para "implementável com backend real" — não foi preciso
desabilitar o formulário do Contato.

## 7. Contrato de analytics já existente (achado crítico)

O mesmo template `public_intent_page.html` já dispara, via listener
delegado:

```js
window.dataLayer.push({event:'public_cta_click', cta: link.textContent.trim(), location: location.pathname});
```

em cliques de `a[href*="wa.me"]` e no teste de nível. Esse é o contrato
real já em uso — reaproveitado literalmente (mesmo nome de evento,
mesmos campos) nos CTAs de WhatsApp desta página, sem inventar nome
novo. Nenhuma página Next construída até agora (Home, 5 idiomas, B2B,
Como Funciona, Sobre) tinha esse listener portado ainda — ele só existia
nas páginas legadas Jinja. Esta fase é a primeira a portar o evento para
o Next, escopado só aos CTAs desta página (não é retrofit do site
inteiro, que estaria fora do escopo desta missão).

## 8. Internal links

Confirmados: os 5 `/curso-de-*`/`/portugues-para-estrangeiros`,
`/empresas`, `/como-funciona`, `/sobre`, `/privacidade` (link do aviso
de LGPD do formulário). `/termos` e `/cancelamento-reembolso` foram
auditados (ambos 200) só como referência — nenhuma migração de página
legal feita nesta fase (missão seção 31).

## Veredito

**SEO PARITY: PASS.** Título/canonical/robots recuperados literalmente;
description atualizada com justificativa documentada (catálogo real de
5 idiomas, mesmo texto sugerido pela missão); hreflang mínimo e
verdadeiro; nenhum e-mail/telefone/endereço inventado; contrato de
analytics e endpoint de formulário reaproveitados de uma fonte real já
existente, não inventados do zero.
