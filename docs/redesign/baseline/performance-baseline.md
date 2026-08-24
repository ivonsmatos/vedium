# Baseline de Performance e Acessibilidade Estrutural

> **Fase A (baseline técnico) — 2026-08-24.** Documento read-only. Nenhuma dependência nova foi instalada. Medições feitas via `curl` (peso de HTML, contagem de assets referenciados) e inspeção de arquivos estáticos já versionados em `vedium_core/public/`. **Não há Lighthouse/PageSpeed/WebPageTest nesta auditoria** — isso está registrado como pendência de acesso externo, não simulado.

## Metodologia e limite

Sem headless browser disponível nesta sessão, os números abaixo medem **HTML entregue pelo servidor** (peso do documento + contagem de tags que referenciam assets), não o total de requests reais do navegador (que inclui CSS/JS carregando fontes, subrequests, etc). Trate como proxy direcional, não como métrica de Core Web Vitals equivalente a um Lighthouse real.

## Peso de página (amostra, CONFIRMADO EM PRODUÇÃO)

| Página | Tamanho do HTML | Tempo de resposta (TTFB+download) | `<link stylesheet>` | `<script src>` | `<img>` |
|---|---|---|---|---|---|
| `/` (home) | 147 KB | 1,13 s | 12 | 9 | 43 |
| `/curso-de-ingles-online` | 63 KB | 1,17 s | 6 | 7 | 15 |
| `/curso/ingles-basico-a1` | 79 KB | 1,52 s | 9 | 8 | 17 |
| `/blog` | 37 KB | 1,13 s | 6 | 6 | 26 |

A home é a página mais pesada da amostra tanto em HTML quanto em contagem de assets — consistente com ser o template com mais seções (T1, ver `route-families.csv`).

## Principais fontes de assets grandes (arquivos estáticos no repo, top 10 por tamanho)

| Arquivo | Tamanho |
|---|---|
| `vendors/fontawesome/webfonts/fa-solid-900.svg` | 917 KB |
| `vendors/fontawesome/webfonts/fa-brands-400.svg` | 748 KB |
| `vendors/bootstrap/css/bootstrap.min.css` | 155 KB |
| `vedium_assets/css/vedium.css` | 145 KB |
| `vendors/fontawesome/webfonts/fa-regular-400.svg` | 145 KB |
| `vendors/swiper/swiper.min.js` | 141 KB |
| `vendors/swiper/swiper-bundle.min.js` | 140 KB |
| `vedium_assets/css/vedium.min.css` | 108 KB |
| `vendors/fontawesome/webfonts/fa-solid-900.woff` | 104 KB |
| `vendors/icomoon-icons/fonts/icomoon.svg` | 94 KB |

**Achado**: FontAwesome está incluído em formato **SVG font** (900KB+ por peso, arquivo legado — formato removido nas versões modernas do FontAwesome por ser pesado e menos performático que woff2). Duas versões de `vedium.css` coexistem (fonte + minificada, 145KB/108KB) — normal se só a minificada é servida, mas vale confirmar no redesign que a não-minificada não está sendo referenciada por engano em algum template.

## Terceiros / requests externos

- **`flagcdn.com`** — bandeiras do seletor de idioma carregam de um CDN externo (`https://flagcdn.com/w20/*.png`), sem `rel="preconnect"` ou `rel="dns-prefetch"` no `<head>` (CONFIRMADO: zero ocorrências de `preload`/`preconnect`/`dns-prefetch` na home).
- **GTM + Meta Pixel**: carregados globalmente (ver `analytics-contracts.md`), ambos de domínios externos (`googletagmanager.com`, Meta), sem preconnect.
- **`fonts/reey-font`**: fonte customizada carregada via stylesheet próprio (`vendors/reey-font/stylesheet.css`), não via Google Fonts.

## Render-blocking / lazy loading

- **Lazy loading de imagem**: 29 de 44 `<img>` da home usam `loading="lazy"` (15 sem o atributo) — adoção parcial, não total.
- **CSS assíncrono via truque `media="print" onload`**: confirmado em `animate.min.css`, `custom-animate.min.css`, `fontawesome/all.min.css`, `jarallax.css` — técnica válida de carregar CSS não-crítico sem bloquear render. **Achado a verificar no redesign**: essas mesmas 4 folhas de estilo aparecem DUAS VEZES no HTML da home (uma vez com o truque, uma vez sem) — pode ser um padrão `<noscript>` de fallback intencional (comum acompanhar o truque `media=print` com um `<noscript><link rel=stylesheet></noscript>` para navegadores sem JS) ou uma duplicação real; não confirmado qual dos dois nesta auditoria — **NÃO CONFIRMADO, verificar manualmente antes do redesign decidir se remove**.
- `bootstrap.min.css` e `public-foundations.min.css` carregam de forma render-blocking padrão (sem o truque acima).

## Fontes potenciais de LCP/CLS/INP (INFERIDO — sem medição de campo real)

- **LCP**: a home tem hero com imagem de fundo (`page-header` com `background-image` inline, confirmado em `curso.html` e templates institucionais) — candidato a elemento LCP; sem `preload` da imagem de hero, o navegador só a descobre depois de parsear o CSS.
- **CLS**: `<img>` sem `width`/`height` explícitos pode causar layout shift; a amostra de `curso.html` mostra pelo menos uma imagem COM `width="1200" height="675"` explícitos (imagem de capa do curso) — bom sinal pontual, não uma varredura completa.
- **INP**: JS carregado é majoritariamente jQuery + plugins de tema (Bootstrap, Swiper, animate.css, jarallax) — carga de JS relativamente tradicional (não é uma SPA pesada), risco de INP alto é menor que em stacks React/Vue client-heavy, mas não medido diretamente.

---

## Acessibilidade estrutural

> Mesma amostra e mesmo método (regex sobre HTML servido) — não substitui um auditor de acessibilidade real (axe, WAVE) nem teste com leitor de tela.

### H1 — achado confirmado, prioridade alta

Da amostra de 66 URLs (`seo-snapshot.csv`), **13 responderam com ZERO `<h1>`**:
- `/en`, `/es`, `/fr`, `/de`, `/ru` (as 5 homes traduzidas — só a home pt-BR tem H1)
- `/en/catalogo`, `/es/catalogo`, `/fr/catalogo`, `/de/catalogo`, `/ru/catalogo` (os 5 catálogos traduzidos)
- `/sobre`, `/en/sobre`, `/contato`

Nenhuma URL da amostra teve **múltiplos** H1 (0 ocorrências). **Achado real, confirmado em produção, não é opinião de auditoria** — qualquer redesign que preserve ou mova esses templates deve decidir conscientemente se adiciona H1 a essas 13 páginas (ganho de acessibilidade e SEO) em vez de simplesmente herdar a lacuna.

### Imagens sem alt

Amostra da home: **1 `<img>` sem nenhum atributo `alt`** (tag bare `<img>`, sem `src` capturado no mesmo match — possivelmente um placeholder ou imagem carregada via JS). Amostra pequena (1 página) — não é uma varredura completa do site.

### Links sem texto discernível

**3 tags `<a></a>` completamente vazias** encontradas na home via regex — podem ser ícones sem `aria-label` (inacessíveis a leitor de tela) ou artefatos de template. Não foi possível isolar o contexto exato via regex nesta auditoria — **candidato a inspeção manual antes do redesign**.

### Landmarks

Home tem exatamente **1 `<header>`, 1 `<nav>`, 1 `<footer>`** — e **ZERO `<main>`**. Confirmado via contagem: o tema usa `<div class="page-wrapper">` como contêiner principal, não a tag semântica `<main>`. Isso é comum em temas Bootstrap legados (o caso deste projeto, tema baseado em Envato/Eduall — ver `docs/redesign/03-template-component-map.md`), mas é uma lacuna real de acessibilidade a decidir conscientemente no redesign.

### Campos sem labels / contraste / teclado

**NÃO AVALIADO nesta Fase A** — exige inspeção visual e/ou ferramenta de acessibilidade real (axe-core, WAVE), fora do escopo de uma checagem via `curl`. Registrado como pendência, não como "sem problemas".

### Idioma declarado

`<html lang="pt-BR">` confirmado corretamente na home pt-BR (não testado se todas as 6 variantes de idioma declaram `lang` corretamente — a amostra de `seo-snapshot.csv` tem a coluna `language` preenchida para as 66 URLs, útil pra checagem cruzada rápida).

## Resumo de achados de performance/acessibilidade pra regressão

| Achado | Severidade | Ação recomendada |
|---|---|---|
| `/en`, `/es`, `/fr`, `/de`, `/ru` + seus catálogos + `/sobre`(en) + `/contato` sem H1 | Média-Alta (SEO + acessibilidade) | Redesign deve corrigir conscientemente, não apenas herdar |
| Nenhum `<main>` landmark na home | Média (acessibilidade) | Avaliar no novo design system |
| FontAwesome em SVG font (900KB+) | Média (performance) | Considerar migração pra ícones SVG individuais ou woff2 no redesign |
| Sem `preconnect`/`dns-prefetch` pra flagcdn.com/GTM/Meta | Baixa-Média (performance) | Adicionar no novo `<head>` |
| CSS possivelmente duplicado (4 folhas 2x) | Baixa (a confirmar) | Verificar se é padrão noscript intencional antes de remover |
| 3 `<a></a>` vazias na home | Baixa-Média (acessibilidade) | Inspecionar manualmente |
