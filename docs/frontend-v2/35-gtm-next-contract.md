# 35 — Contrato de GTM + Consent Mode no Next (Fase G.2, Parte A)

Resolve o bloqueador #1 da Fase G.1 ("GTM real ainda não integrado ao
frontend Next"). Nenhum deploy, DNS ou mudança de produção -- só código
local + verificação empírica via Playwright contra o dev server.

## 1. Auditoria do que já existe em produção (antes de escrever qualquer linha)

Fonte: leitura direta do código Frappe real (`vedium_core/`) + docs já
existentes desta mesma base (`docs/redesign/baseline/analytics-
contracts.md`, `docs/redesign/45-consent-remediation-result.md`,
`docs/redesign/29-home-v2-analytics-contract.md`) -- não foi inventado
nada, tudo abaixo é o que já roda hoje:

| Item | Valor real |
|---|---|
| Container GTM | `GTM-P6Q2FXLK` -- único em todo o site, confirmado por teste automatizado de produção |
| GA4 | `G-TMBTXVRMLE`, roda **100% de dentro do GTM** (tag "GA4 - Base Config", trigger "All Pages") -- NÃO hardcoded em nenhum template |
| Meta Pixel | ID `1539456614495904`, arquivo `meta-pixel.js` tem lógica de gate por consentimento correta, **mas nunca é referenciado por nenhuma página real** -- confirmado via CDP que `window.fbq` nunca é definido. Bug pré-existente, já documentado, decisão de religar pendente de humano (`docs/redesign/45-consent-remediation-result.md`, seção 11) |
| Consent Mode v2 | 4 sinais (`analytics_storage`, `ad_storage`, `ad_user_data`, `ad_personalization`), default `denied`, `wait_for_update: 500` |
| Storage | `localStorage.vedium_cookie_consent` (`"1"`/`"accepted"`/`"essential"`/`"rejected"`) + `localStorage.vedium_cookie_preferences` (JSON `{analytics, marketing}`) |
| Eventos de consentimento | `vedium:consent` (aceitar tudo), `vedium:consent-rejected` (recusar tudo), `vedium:consent-preferences` (granular, `CustomEvent` com `detail: {analytics, marketing}`) |
| `public_cta_click` | Reaproveitado literalmente (missão F.3) -- **mas em produção tem duplicidade sistemática conhecida** (listener global capture-phase + onclick local, ambos disparando no mesmo clique) |
| Formulário de contato (`contato.html`) | **Zero eventos de analytics** hoje -- nem pageview custom, nem submit. Não é uma lacuna do Next, é o estado real da produção |
| Pathfinder (`pathfinder_*`) | Feature exclusiva da Home V2 (não existe em nenhuma página Jinja legada) -- 3 eventos já auditados e documentados quando criados (`docs/redesign/29-home-v2-analytics-contract.md`), preservados sem renomear |
| Teste de nível | Eventos (`level_test_completed` etc.) disparam DENTRO da página `/teste-de-nivel`, que continua 100% Frappe -- nenhuma ação necessária no Next além de manter o link de saída funcionando |

## 2. O que estava faltando no Next (achado da Fase G.1, confirmado aqui)

Busca completa em `frontend/src` antes desta fase: **zero** referências a
`dataLayer`, `gtm`, `GTM`, `googletagmanager`, `consent` fora do
`TrackedWhatsappLink` já existente. Ou seja: nenhum GTM, nenhum GA4,
nenhum Consent Mode, **e nenhuma barra de cookies** -- o Next não tinha
absolutamente nenhuma interface de consentimento LGPD, o que é uma
lacuna maior do que só "falta analytics".

## 3. O que foi implementado

### GTM + Consent default (`src/components/analytics/AnalyticsScripts.tsx`)

- Script inline `consent default` com `strategy="beforeInteractive"` --
  Next injeta no `<head>` e garante execução antes de QUALQUER script
  `afterInteractive` (GTM incluso), por semântica documentada do próprio
  `next/script` (`node_modules/next/dist/docs/01-app/02-guides/
  scripts.md`: "cookie consent managers" é o exemplo canônico de
  `beforeInteractive`, "tag managers" o de `afterInteractive`). Isso
  resolve o P0 da missão (seção 3) sem precisar do mecanismo de guard por
  posição de arquivo que o Frappe precisa (o Next só renderiza cada
  Script uma vez, declarado no root layout).
- Snippet do GTM copiado da variante **com guard de dedupe**
  (`d.querySelector('script[src*="'+i+'"]')`), a mesma de
  `templates/includes/site_footer.html` -- não a variante sem guard de
  `www/index.html`, que é a origem do bug real e já documentado de
  `<noscript>` duplicado em 7 páginas de produção. Decisão consciente:
  não replicar um bug conhecido numa base nova.
- GA4 **não** foi adicionado separadamente -- carrega de dentro do
  container, exatamente como em produção (missão, Parte A, seção 2).
- Meta Pixel **não** foi adicionado -- replica o estado real de produção
  (nunca carrega hoje, em nenhum frontend). Adicionar ao Next sozinho
  criaria MAIS tracking do que a produção tem hoje, o que não é
  paridade, é uma correção de bug pré-existente fora do escopo desta
  fase (a mesma decisão já tomada em `docs/redesign/29-home-v2-
  analytics-contract.md`, seção 2).

### Barra de cookies (`public/assets/vedium_core/js/cookie-consent.js`, `.../v2/consent-mode-v2.js`)

Cópias vendorizadas **byte-a-byte** dos 2 arquivos reais de produção
(`vedium_core/vedium_core/public/js/cookie-consent.js` e
`.../public/js/v2/consent-mode-v2.js`), carregadas via `next/script`
(`strategy="afterInteractive"`). Nenhuma linha de lógica foi reescrita --
mesmo texto (6 idiomas), mesmas chaves de `localStorage`, mesmos eventos,
mesma ausência de dark pattern (Aceitar/Recusar no mesmo nível
hierárquico). Isso é o que garante o contrato cross-backend pedido pela
missão (seção 4-5): se o usuário decidir em uma página Frappe e depois
visitar uma página Next no mesmo domínio/navegador (ou vice-versa), o
`localStorage` é compartilhado (mesma origem `vediums.com`) e a decisão é
respeitada nos dois lados, sem repetir a pergunta.

### Camada central de dataLayer (`src/lib/analytics/`)

- `dataLayer.ts` -- único ponto que chama `window.dataLayer.push`.
- `contracts.ts` -- tipos dos 4 eventos que o Next dispara hoje
  (`public_cta_click`, `pathfinder_language_select`,
  `pathfinder_goal_select`, `pathfinder_submit`) -- nenhum nome novo
  inventado.
- `event.ts` -- funções nomeadas (`trackPublicCtaClick`,
  `trackPathfinder*`) que os componentes chamam, em vez de montar o
  objeto do evento na mão (missão, seção 7).
- `whatsapp.ts` -- `isWhatsappHref()`, único critério pra reconhecer link
  de WhatsApp (mesmo padrão do listener global de produção).

### Cobertura de WhatsApp (achado real corrigido nesta fase)

Antes desta fase, só Contato e a página 404 disparavam
`public_cta_click` em cliques de WhatsApp -- Header (barra utilitária),
Footer, e todo CTA de página de curso/B2B que passava pelo `Button`/
`TextLink` genérico **não disparava nada**. Corrigido de forma
centralizada: `Button.tsx` e `TextLink.tsx` agora detectam
`isWhatsappHref()` e delegam a renderização pro `TrackedWhatsappLink`
(que já existia) em vez de `next/link` -- um único ponto de mudança
cobre Header, Footer, Hero, CTAs de curso, B2B e qualquer página futura
que use esses componentes, sem precisar tocar cada arquivo de conteúdo
individualmente.

## 4. Verificação empírica (Playwright, não só leitura de código)

Script `frontend/scripts/check-gtm-consent.mjs`, rodado contra o dev
server local. Todos os resultados abaixo são de execução real no
Chromium, lendo `window.dataLayer`/`localStorage` de fato, não inferidos
do código-fonte.

| Verificação | Resultado |
|---|---|
| GTM container correto (`GTM-P6Q2FXLK`) | PASS |
| `consent default` roda antes do GTM, payload correto (4 sinais `denied`, `wait_for_update:500`) | PASS |
| Barra de cookies aparece na 1ª visita | PASS |
| ACCEPT -- todos os 4 sinais viram `granted`, barra some, `localStorage` atualizado | PASS |
| REJECT -- todos os 4 sinais viram `denied`, `localStorage` = `"rejected"` | PASS |
| MANAGE (analytics=sim, marketing=não) -- `analytics_storage:granted`, resto `denied` | PASS |
| Persistência após reload | PASS -- barra não reaparece, último `consent update` preservado |
| Persistência entre navegação (Home → Como Funciona) | PASS -- mesmo resultado, sem re-perguntar |
| WhatsApp Header -- 1 clique = 1 `public_cta_click`, `cta:"WhatsApp"` | PASS |
| WhatsApp Footer -- 1 clique = 1 evento, `cta:"+55 (11) 91129-3075"` (texto visível real) | PASS |
| WhatsApp curso (pillar, `/curso-de-hebraico-online`) -- 1 evento, `cta:"Fale com a Vedium"` | PASS |
| WhatsApp B2B (`/empresas`) -- 1 evento, `cta:"Fale com a Vedium"` | PASS |
| WhatsApp Contato -- 1 evento, `cta:"+55 11 91129-3075"` | PASS |
| Erros de console na Home | 0 |
| **WHATSAPP EVENT DUPLICATES** | **0** |

**Achado colateral, não um bug**: `/curso-de-ingles-online` (conteúdo em
`content/languages/english.ts`) não tem nenhum CTA de WhatsApp na página
-- só Hebraico, Espanhol, Iorubá e PLE têm `secondaryCta` apontando pro
WhatsApp. Isso é uma assimetria real de conteúdo entre os 5 pilares de
curso, preexistente a esta fase (não introduzida aqui) -- registrado
para conhecimento, não corrigido (mudar conteúdo de página está fora do
escopo de uma fase de analytics).

## 5. Regressão obrigatória (mudança em componente compartilhado)

`Header.tsx`, `Footer.tsx`, `Button.tsx` e `TextLink.tsx` foram
alterados -- os 4 são usados em praticamente todas as páginas. Sweep
completo de overflow horizontal (`check-overflow-global.mjs`, 15 rotas x
6 larguras) rerodado depois da mudança: `{ totalChecks: 90,
overflowsFound: 0 }` -- nenhuma regressão. Capturas de tela da barra de
cookies (desktop 1440px e mobile 375px, estado inicial e painel de
preferências aberto) conferem visualmente: mesmo estilo da produção, sem
sobreposição com Header/Hero.

## 6. Formulário de contato -- decisão deliberada de NÃO adicionar tracking

A missão pede (seção 10): "Validar analytics do formulário: submit
attempt/success/error somente se esses eventos já fizerem parte do
contrato aprovado. Não inventar taxonomy nova sem necessidade." A
auditoria da seção 1 confirma que `contato.html` real **não tem nenhum
evento hoje**. Não existe contrato aprovado para inventar aqui --
`ContactForm.tsx` continua sem disparar nenhum evento de
submit/success/error, exatamente igual à produção. Nenhum dado pessoal
(nome, e-mail, telefone, mensagem) é ou seria enviado ao `dataLayer` em
nenhum cenário -- confirmado por leitura do código (`ContactForm.tsx`
não importa nada de `lib/analytics`).

## 7. Gate desta parte

| Campo | Resultado |
|---|---|
| GTM CONTAINER | PASS |
| CONSENT MODE | PASS |
| CONSENT CROSS-BACKEND CONTRACT | PASS (mesmas chaves de storage/eventos, vendorizado byte-a-byte) |
| DATALAYER | PASS (camada central única, sem payload arbitrário) |
| DUPLICATE EVENTS | 0 |
| WHATSAPP TRACKING | PASS |
| CONSOLE ERRORS | 0 |
| SECURITY (nenhum dado pessoal no dataLayer) | PASS |
