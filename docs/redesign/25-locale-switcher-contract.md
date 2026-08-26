# 25 — Seletor de idioma funcional no Header V2 (Fase B.6E, Parte D)

> **Regra crítica da missão**: o seletor de idioma do Header V2 não podia mais ser decorativo. Teria que funcionar reutilizando/portando o contrato REAL já existente (`baseline/ui-contracts.md`), nunca uma lógica paralela inventada por conveniência.

## 1. Estado antes desta fase

`header.html` já carregava os atributos certos (`data-vd-language-open`, `data-vd-nav-current`, `data-vd-nav-urls`) desde a Fase B.3 — mas **nenhum elemento de menu/modal existia** pra eles controlarem, e `v2_nav_urls` nunca era passado pela página. O botão "PT ▾" era 100% decorativo: clicar não fazia nada.

## 2. O que foi lido antes de implementar (regra da missão)

- `docs/redesign/baseline/ui-contracts.md` — seção "Seletor de idioma/locale": 12 locales em 4 grupos (Global/Américas/EMEA/Ásia) num modal; mecânica de `updateLocaleLinks()`.
- `templates/includes/site_navbar.html` (linhas 1-13, 117-140) — como `data-vd-nav-urls`/`data-vd-nav-current` são calculados no servidor (namespace `vd_nav`, a partir de `landing.alternates`/`post.alt`/`alt_langs`, dependendo do tipo de página).
- `public/js/vedium-language.js` (não minificado, 806 linhas) — `getPageNavUrls()`, `updateLocaleLinks()`, `markActive()`, `setModalOpen()`, `MULTI_REGION_LOCALES`, `LOCALE_LANG_FAMILY`.
- `docs/redesign/02-route-and-seo-map.md` — quais home traduzidas existem de fato (`/`, `/en`, `/es`, `/fr`, `/de`, `/ru`).

## 3. Locales encontrados (confirmados no código, não assumidos)

6 famílias de idioma com conteúdo real publicado: **pt-br, en, es, fr, de, ru**. Os outros 6 códigos do modal de produção (en-us, en-au, es-ar, es-co, fr-ca, zh-cn) são "bandeiras irmãs" da mesma família — não têm conteúdo próprio, sempre caem na mesma página real da família (com `?locale=` preservando só a preferência regional). Por instrução explícita da missão ("mostrar no menu SOMENTE locales realmente suportados"), o LocaleMenu v2 mostra só as 6 famílias reais — não replica as 6 bandeiras irmãs decorativas.

## 4. Como o seletor real funciona (resumo do mecanismo, não reimplementado)

1. O `<header>` real expõe `data-vd-nav-urls` (JSON `{locale: url}`) e `data-vd-nav-current`, calculados no servidor por página (landing/post/curso têm tradução real; páginas institucionais reciprocam só com PT).
2. No `DOMContentLoaded`, `updateLocaleLinks()` lê esses atributos e reescreve o `href` de cada link `[data-vd-locale]`: usa a URL real da família se existir; senão cai em `en`; senão em `pt-br`. **Nunca** troca prefixo cego sem checar existência (bug real de produção de 2026-07-03, documentado no próprio código: bandeira EUA em `/en/portuguese-for-executives` gerava `/en-us/portuguese-for-executives`, 404).
3. `markActive(locale)` marca `.is-active` nos links e atualiza bandeira/label se os atributos `data-vd-current-flag`/`data-vd-current-label` existirem no DOM.
4. `MULTI_REGION_LOCALES` preserva a bandeira regional escolhida via querystring `?locale=`, sem localStorage (removido deliberadamente antes desta fase).

## 5. O que foi portado para o V2 (e o que foi construído novo)

**Reutilizado, não reimplementado** — o script real de produção:
```html
<script defer src="/assets/vedium_core/js/vedium-language.min.js"></script>
```
incluído literalmente em `design_system_v2.html` e `design_system_v2_b2b.html`. `updateLocaleLinks()`/`markActive()` rodam sem nenhuma modificação. Efeitos colaterais do script (limpeza de cookie legado, tracking de clique WhatsApp via `dataLayer`) são inofensivos/benéficos nesta página; `localizePage()` já é um no-op desligado desde 2026-07-02 (documentado no próprio arquivo).

**Construído novo** — só a interface de abrir/fechar (a missão pediu um menu simples "PT ▾", não o modal de 12 bandeiras em 4 grupos):
- `header.html`: painel `<ul data-v2-locale-menu hidden>` com 6 `<a data-vd-locale="...">` (um por família real), ancorado no botão via `data-v2-locale-root` (não `data-vd-language-open`/`data-vd-language-modal` — esses atributos continuam existindo no botão real de produção pro modal completo; usar os mesmos aqui criaria um segundo consumidor incompatível do mesmo contrato de abertura). `href` de cada link já vem correto renderizado no servidor (mesmo mapa usado em `data-vd-nav-urls`) — funciona mesmo sem JS, e o script real só confirma/sobrescreve com o mesmo valor ou um melhor.
- `design-system-v2.js`: nova função `initLocaleMenu()` — abre/fecha por clique, Esc fecha e devolve foco ao botão, clique fora fecha, `aria-expanded` sincronizado. Não duplica nem substitui a lógica de resolução de URL.
- `header-footer.css`: `.v2-hdr-locale-menu` — popup ancorado, fundo sempre sólido (funciona em cima do header overlay ou sólido), nunca card pesado.

### Bug real encontrado durante o teste (não em revisão de código)

Primeira tentativa colocou `data-vd-nav-urls`/`data-vd-nav-current` num `<div>` da utility bar. `vedium-language.js` lê esses atributos especificamente via `document.querySelector("header[data-vd-nav-urls]")` — só funciona na tag `<header>` de verdade. Sem isso, `getPageNavUrls()` voltava vazio e `updateLocaleLinks()` caía no fallback de troca de prefixo cega, gerando `/en/design_system_v2` — **reproduzindo por engano o exato bug de 2026-07-03** que este mecanismo existe pra evitar. Encontrado testando de verdade (clique real + inspeção do `href` resolvido de cada locale via CDP), não por leitura de código. Corrigido movendo os atributos pra tag `<header data-v2-header ...>`.

### URLs resolvidas nesta página (preview representa a Home)

Não existe página V2 traduzida ainda. Como a página de preview representa conceitualmente a Home, `v2_nav_urls` tem um default (em `header.html`, sobrescrevível por chamador futuro) apontando pras Homes REAIS já publicadas: `{"pt-br":"/", "en":"/en/", "es":"/es/", "fr":"/fr/", "de":"/de/", "ru":"/ru/"}`. Nenhuma URL nova ou inventada.

## 6. Acessibilidade (verificado, não só implementado)

Testado via CDP (clique real, teclado, foco) em `http://vedium.local:8005/design_system_v2`:

| Requisito (seção 30 da missão) | Verificado como |
|---|---|
| Abre por clique | `Input.dispatchMouseEvent` real no botão → `aria-expanded` vira `true`, painel visível |
| Esc fecha | `keydown Escape` no container → fecha e **devolve foco ao botão** (`document.activeElement === toggle`) |
| Clique fora fecha | clique em `document.body` → painel fecha |
| `aria-expanded`/`aria-haspopup` | presentes e sincronizados (`aria-haspopup="true"`, não `"dialog"` — é um disclosure, não modal) |
| Item atual identificado | `aria-current="true"` + classe `.is-active` no link do locale atual (calculado no servidor) |
| Painel oculto fora da ordem de tab | confirmado — `hidden` nativo remove do tab order; `Tab` a partir do botão fechado pula direto pro próximo elemento real da página |
| Mobile funcional | `.v2-hdr-utility` (barra que contém o seletor) não tem nenhuma regra de `display:none` em mobile; testado em 390px, painel abre/fecha normalmente |
| Header overlay/sólido | `.v2-hdr-locale-menu` tem fundo sempre opaco, independente do estado `is-solid` do header |

**Limitação de metodologia registrada**: `Input.dispatchKeyEvent` com `key:"Enter"` num `<button>` focado via CDP não disparou o `click` nativo nos testes (confirmado que é uma limitação de simulação do CDP, não um bug do produto — ativação de `<button>` por Enter/Espaço é comportamento nativo do HTML, não implementado via JS neste código, logo não pode ser "quebrado" por ele). Verificação real de ativação por clique (mouse real, `.click()` programático) e de Esc/foco/tab-order acima já cobre a garantia funcional.

## 7. O que NÃO foi alterado

Visual do Header aprovado permanece idêntico — só markup/JS estritamente necessário pro menu funcionar (novo painel, novo atributo `data-v2-locale-toggle`/`data-v2-locale-root`/`data-v2-locale-menu`, novas 30 linhas de CSS escopadas a `.v2-hdr-locale*`). Hash MD5 do Hero (`.v2-editorial-hero`) confirmado idêntico ao baseline antes/depois desta fase.
