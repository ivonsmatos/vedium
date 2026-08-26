# 22 — Ajuste de densidade, transições e escala editorial (Fase B.6D)

> **Origem**: com a direção visual de B.6B (`20-bain-editorial-rhythm.md`) e a mídia de B.6C (`21-course-media-selection.md`) aprovadas, a missão B.6D pediu um refinamento puramente visual **abaixo do Hero** (Hero permanece **congelado**, nenhuma linha de `.v2-editorial-hero*` tocada): corrigir um degrau estrutural entre Pathfinder e VediumMethod, reduzir vazios não-funcionais, e aumentar a escala tipográfica em VediumMethod e nos 5 blocos de Cursos, que estavam pequenos demais para o espaço disponível. Referência de princípios: bain.com (só lógica de composição, nunca código/identidade).

## 1. Bug real corrigido: degrau visual entre Pathfinder e VediumMethod

**Causa-raiz**: Pathfinder usava `grid-template-columns: 42fr 58fr` enquanto VediumMethod (a seção seguinte) usava `40fr 60fr` — a linha de corte entre o painel azul e a área clara saltava 2% da largura do container entre as duas seções empilhadas, criando um "degrau" visível exatamente como descrito na missão. Além disso, cada seção pintava o fundo em **dois divs filhos independentes** em vez de um único fundo no container pai, o que (somado ao `min-height:44rem` forçado no Pathfinder, além do necessário pro conteúdo) arriscava desalinhamento adicional.

**Correção** (padrão sugerido pela missão, aplicado às duas seções por consistência):
- Fundo movido para `linear-gradient(90deg, var(--v2-color-brand-700) 0%, var(--v2-color-brand-700) 42%, <cor-B> 42%, <cor-B> 100%)` no **container do grid** (não mais nos filhos).
- `grid-template-columns` do VediumMethod alterado de `40fr 60fr` para `42fr 58fr`, igualando ao Pathfinder.
- `min-height: 44rem` removido do Pathfinder — altura passa a ser ditada pelo conteúdo.

**Verificação**: screenshot dedicado (últimos 150px do Pathfinder + primeiros 150px do VediumMethod, 1440px e 390px) confirma linha de corte agora contínua e reta, sem degrau. Ver `transition_1440.png` / `transition_390.png`.

## 2. Pathfinder — altura ajustada

`padding-block` do painel e do form-wrap aumentado de `--v2-space-16` (64px) para `--v2-space-20` (80px) — dentro da faixa pedida (72-96px desktop) — e o `min-height:44rem` removido (item 1) já eliminou o espaço vazio não-funcional abaixo do botão do form. Sem uso de `min-height` rígido adicional — a altura das duas colunas agora é dada pelo próprio conteúdo, com `align-items:stretch` do grid mantendo as duas metades niveladas.

## 3. VediumMethod — escala tipográfica aumentada

| Elemento | Antes | Depois |
|---|---|---|
| `grid-template-columns` | `40fr 60fr` | `42fr 58fr` (alinhado ao Pathfinder) |
| `padding-block` (painel e lista) | `--v2-space-16` (64px) | `--v2-space-24` (96px) |
| `.v2-vedium-method__intro-inner` `max-width` | `26rem` | `29rem` (ver bug do item 4) |
| `.v2-vedium-method__title` | escala `v2-h2` padrão (herdada) | `clamp(2.25rem, 1.8rem + 2vw, 3.75rem)`, `line-height:1.06` |
| `.v2-vedium-method__list` `gap` | `--v2-space-8 --v2-space-10` | `--v2-space-10 --v2-space-10` (mais denso) |
| `.v2-vedium-method__item-num` | `clamp(1.75rem, 1.5rem + 1vw, 2.25rem)` (28-36px) | `clamp(2.125rem, 1.8rem + 1.4vw, 2.625rem)` (34-42px) |
| `.v2-vedium-method__item-label` | `--v2-text-lg` | `clamp(1.25rem, 1.1rem + 0.6vw, 1.4375rem)` (20-23px) |
| `.v2-vedium-method__item-text` | corpo padrão (sem tamanho explícito, ~16-17px) | `clamp(1.0625rem, 1rem + 0.3vw, 1.1875rem)` (17-19px), `line-height:1.55` |

## 4. Bug real encontrado durante a própria verificação: headline quebrando em 5 linhas

Depois de aumentar `.v2-vedium-method__title`, o primeiro screenshot (`vediummethod_full.png`) mostrou a headline "Ao vivo não é apenas o formato. É parte do método." quebrando em **5 linhas** dentro do `max-width:26rem` da coluna azul — violação direta da regra explícita da missão ("não quebrar em cinco linhas se houver largura disponível"). Corrigido alargando `.v2-vedium-method__intro-inner` de `26rem` para `29rem`; novo screenshot (`vediummethod_fix.png`) confirmou quebra em exatamente 4 linhas.

## 5. Nova seção: abertura de Cursos com índice funcional (substituindo vazio decorativo)

A abertura de "Nossos cursos" tinha um vazio grande entre o headline e o primeiro bloco de curso, e um vazio grande à direita. Em vez de preencher com uma imagem decorativa (a missão pediu para documentar antes de optar por foto), a escolha foi um **índice de cursos funcional** — mais institucional e mais útil.

- Novo macro `v2_course_index_intro(eyebrow, title, lead, courses)` em `macros_editorial.html`, renderizando uma seção `.v2-course-intro` com grid 55/45 (`.v2-course-intro__copy` + `.v2-course-index`).
- Coluna esquerda: eyebrow "NOSSOS CURSOS", novo headline mais curto (item 6), lead curto de uma frase.
- Coluna direita: lista `<ol>` de 5 links reais (`01 Inglês` … `05 Hebraico`, cada um apontando pro `/curso-de-*` real), separadores horizontais discretos (`border-block-end`), hover = seta desloca 4px + nome muda pra `brand-700`. Sem cards, sem ícones, sem fundo por linha — número 14-16px, nome 20-24px (`clamp(1.25rem, 1.1rem+0.6vw, 1.5rem)`), padding-block 16px por item.

## 6. Novo headline de Cursos

Trocado "Cinco idiomas. Percursos organizados para diferentes objetivos." por **"Cinco idiomas. Cursos organizados por nível e objetivo."** — mais curto, quebra em 2 linhas em telas largas (confirmado no screenshot 1440px) sem precisar reduzir o tamanho da fonte pra forçar a quebra. `font-size: clamp(2.25rem, 1.7rem + 2.4vw, 4rem)`, `max-width:46rem`.

## 7. Blocos de curso (5 idiomas) — tipografia aumentada uniformemente

| Elemento | Antes | Depois |
|---|---|---|
| `.v2-course-feature-band` `padding-block` (992px+) | `--v2-space-16` (64px, 128px combinado entre blocos) | `--v2-space-10` (40px, 80px combinado) |
| `.v2-course-feature__index` | herdado (sem tamanho explícito) | `1.0625rem` (~17px) |
| `.v2-course-feature__level` | `--v2-text-lg` | `clamp(1.25rem, 1.15rem + 0.4vw, 1.375rem)` (20-22px) |
| `.v2-course-feature__headline` | escala `v2-h3` herdada (~24-32px) | `clamp(2.125rem, 1.7rem + 1.8vw, 2.625rem)` (34-42px), `line-height:1.14` |
| `.v2-course-feature__text` | corpo padrão (~16-17px) | `clamp(1.125rem, 1.05rem + 0.3vw, 1.25rem)` (18-20px), `line-height:1.55` |

Imagens (seleção, crop e `object-position` de B.6C) e alternância de lado (Inglês esquerda / Iorubá direita / PLE esquerda / Espanhol direita / Hebraico esquerda) **mantidas sem alteração** — só a proporção imagem/conteúdo (`1.1fr 1fr`, ~52/48%) e o gap entre blocos foram tocados (reduzido junto com o `padding-block` acima).

## 8. Verificação de regressão nas seções não tocadas nesta fase

Nenhuma CSS de Aula ao vivo, B2B, Progressão, Insights ou CTA final foi alterada em B.6D (só tokens locais/escopados às classes das seções 3 e 7 acima — nenhum token global em `tokens.css` foi tocado). Confirmado visualmente por screenshot dedicado a cada seção após todas as mudanças:
- **Aula ao vivo**: vídeo com controles, sem autoplay, layout intacto (`liveclass_check.png`).
- **B2B**: imagem + copy intactos (`b2b_check.png`) — nota metodológica: a primeira captura veio sem a imagem porque o script de screenshot ad-hoc usado pra essa verificação (`shot_xpath.js`) não incluía o passo de scroll progressivo necessário pra disparar `loading="lazy"` no Chrome headless (bug de metodologia já documentado em B.6C, reproduzido aqui por um script novo que esqueceu o fix); corrigido no próprio script antes de re-capturar — não é uma regressão do site.
- **Progressão**: rail, dots e notas intactos, sem imagens (`progressao_check.png`).
- **CTA institucional**: navy full-bleed intacto, sem regressão de contraste (`cta_check.png`).

## 9. Hero — reverificação de "congelado"

1. **Diff de fonte**: `git diff` nos arquivos `components-editorial.css`, `design_system_v2.html` e `macros_editorial.html` não retornou nenhuma linha contendo `editorial-hero` — confirma que nenhuma regra ou marcação do Hero foi tocada nesta fase (nem em fases anteriores ainda não commitadas).
2. **Hash MD5 do HTML renderizado**: `1acd805606a5cd559f92969de0437315` — **idêntico** ao hash registrado na Fase B.6B (`20-bain-editorial-rhythm.md`, seção 13). Nota de metodologia: uma primeira tentativa de extração com regex simples (`.*?</section>` + lookahead) deu um hash diferente por não contar corretamente `<section>` aninhadas dentro do carrossel do Hero, capturando 7 bytes a mais/menos do que a seção real; a extração corrigida (contagem de profundidade de tags) reproduziu exatamente os 8724 bytes e o hash de B.6B. Registrado aqui pra não repetir o mesmo erro de extração numa fase futura.

## 10. Viewports testados

- **1440px**: transição Pathfinder→VediumMethod, VediumMethod completo, abertura de Cursos (índice), Inglês, Iorubá, PLE, Espanhol, Hebraico — todos sem overflow (`docScrollWidth <= 1440` confirmado via CDP).
- **1280px**: checagem de overflow (`docScrollWidth:1265 <= 1280`, sem overflow).
- **390px**: transição Pathfinder→VediumMethod, VediumMethod (diferenciais empilhados), abertura de Cursos (índice abaixo do headline), Inglês (imagem-esquerda), Iorubá (imagem-direita) — todos sem overflow (`docScrollWidth:390 == winInnerWidth:390`).

## 11. Testes executados

- `330 passed, 11 skipped` (`pytest apps/vedium_core`, suíte pura sem DB) — sem regressão em relação ao piso de 326 da fase anterior.
- `flake8` limpo em `design_system_v2.py` (`max-line-length=120`).
- CRLF: 100% das linhas com `\r` em todos os arquivos `.py`/`.css`/`.html`/`.js`/`.csv`/`.md` modificados nesta fase (nenhuma linha LF solta).
- `git status --porcelain`: mudanças isoladas a `vedium_core/vedium_core/{public/css/v2,public/js/v2,templates/includes/v2,www/design_system_v2.*}` e `docs/redesign/*` — nenhum arquivo de produção tocado.
- 0 overflow horizontal em 1280/1440/390px.
- Hero verificado intacto por diff de fonte + hash MD5 idêntico ao de B.6B (seção 9).
- Nenhuma seção fora do escopo (Aula ao vivo, B2B, Progressão, Insights, CTA) apresentou regressão visual (seção 8).
