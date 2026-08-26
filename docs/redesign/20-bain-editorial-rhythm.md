# 20 — Ritmo editorial e credibilidade abaixo do Hero (Fase B.6B)

> **Origem**: o Hero full-bleed em carousel da Fase B.6A (`19-editorial-hero-carousel.md`) foi aprovado e ficou **congelado** nesta fase — nenhuma linha de `.v2-editorial-hero*` foi tocada (confirmado por hash MD5 idêntico do HTML renderizado e por diff de pixel controlado, ver seção 10). A missão pediu que o resto da Home (abaixo do Hero) ganhasse a mesma disciplina editorial do Bain.com: ocupação inteligente do espaço, alternância de fundos com função, fotografia grande, blocos assimétricos, escala tipográfica, autoridade institucional — sem copiar código/identidade do Bain, só a lógica de composição.
>
> **Atualização B.6D** (`22-density-and-transition-refinement.md`): o mismatch de proporção Pathfinder 42/58 vs VediumMethod 40/60 (visível na tabela da seção 11 abaixo) foi identificado como a causa-raiz do "degrau" visual entre as duas seções e corrigido — ambas agora usam 42/58 com fundo pintado no container do grid (`linear-gradient` com parada dura em 42%), não mais em dois divs independentes. Hero reverificado byte-idêntico (`1acd805606a5cd559f92969de0437315`, mesmo hash desta seção) depois da correção. Ver doc 22 para o detalhamento completo.

## 1. Problema identificado

Abaixo do Hero, duas seções tinham grandes áreas brancas sem função: o VediumPathfinder (um card branco estreito boiando num mar de branco) e "O que define a Vedium" (4 colunas iguais, sem protagonismo). Outras seções (Aula ao vivo, CTA final) tinham espaço vazio sem propósito editorial claro.

## 2. VediumPathfinder — de card a seção full-width

**Antes**: `<section class="v2-section v2-section--tight"><div class="v2-container">{{ v2_pathfinder(...) }}</div></section>` — um card branco (`padding`, `border`, `border-radius`, `max-width:44rem`) sozinho numa seção de fundo branco.

**Depois**: `v2_pathfinder_section` — split 42/58 full-bleed (fundo de cada metade sangra até a viewport, conteúdo alinhado ao container de 1280px via `padding-inline-start/end: max(space-10, calc((100vw - container-wide)/2 + space-6))`, mesmo truque de alinhamento já usado nas seções `--brand` desta página):

- **Painel esquerdo (42%, azul institucional)**: eyebrow "Encontre seu ponto de partida", H2 "Um curso para o seu idioma e o seu objetivo.", lead, uma linha terracota de 3px como acento, e "01 IDIOMA / 02 OBJETIVO" como elemento gráfico (número grande e translúcido + rótulo em caixa alta) — não um texto solto, um dispositivo visual reaproveitado depois em Cursos e Progressão.
- **Painel direito (58%, branco)**: o próprio `v2_pathfinder` (form) virou a interface — sem card, sem borda, sem `max-width` de card. Perguntas prefixadas com "01"/"02" (ecoando o painel), tipografia da pergunta ampliada para 26-32px, opções maiores (min-height 52px) com seleção por borda inferior + fundo suave em vez do antigo "chip"/pill, CTA compacto alinhado à esquerda (não mais um botão full-width).

Nenhuma lógica do componente mudou — continua sem CRM, sem alterar o teste de nível real, funcional sem JS (só o slide 1 do Hero e a estrutura dos `<fieldset>` nativos garantem isso; testado via `Input.dispatchKeyEvent` real: `ArrowDown` move foco E seleção dentro do grupo, `Tab` avança pro próximo grupo sem prender foco).

## 3. "O que define a Vedium" → VediumMethod

Renomeado para "O que você encontra na Vedium" / H2 "Ao vivo não é apenas o formato. É parte do método." Trocado de `v2_proof_bar` (4 colunas iguais) para `v2_vedium_method`: split 40/60, mesmo padrão de sangria da seção acima — painel azul (eyebrow + H2 + texto institucional curto) à esquerda, os 4 diferenciais em lista editorial 2×2 à direita (número grande + rótulo em caixa alta + texto, linha fina separando linhas — nunca card/ícone/radius/shadow). O painel azul repete deliberadamente o motivo visual do Pathfinder logo acima, criando uma transição Hero → Pathfinder → Method costurada pela mesma cor institucional, exatamente o que a missão pediu ("escolher a opção que melhor conecta visualmente").

## 4. Cursos — mais densidade, número editorial nos blocos tipográficos

- `.v2-course-feature-stack` gap reduzido de `--v2-space-20` (80px) para `--v2-space-16` (64px) — mais denso sem perder a separação entre blocos.
- Blocos sem foto (Iorubá, Espanhol, Hebraico) ganharam um número editorial grande e translúcido no canto (02/04/05, refletindo a posição real de cada curso na sequência de 5) — mesma linguagem de "número como dispositivo de autoridade" já usada no Pathfinder/Method, reforçando que o bloco de cor sólida é uma escolha de design deliberada, não "faltou imagem" (pedido explícito da missão, seção 15).

## 5. Bug real corrigido: contraste em blocos navy (Iorubá/Hebraico)

`.v2-heading` fixa `color: var(--v2-color-text)` (tinta escura) como padrão — essa declaração explícita sempre vence herança de cor do elemento pai. O bloco `tone="brand"` (Iorubá, Hebraico) definia `color: var(--v2-color-surface-0)` no container, mas isso nunca chegava ao `<h3 class="v2-heading ...">` dentro dele — o título renderizava quase preto sobre fundo navy. Confirmado lendo o CSS antes mesmo de tirar um screenshot (a mesma causa-raiz já documentada para `.v2-section--brand` em `foundations.css`, só que essa variante é um *bloco* dentro de uma seção comum, não uma seção `--brand` inteira). Corrigido com `.v2-course-feature--tone-brand .v2-heading { color: inherit; }` — e o **mesmo padrão de bug foi encontrado de novo, de forma independente**, no painel do VediumPathfinder (H2 do painel azul também renderizava escuro) e corrigido da mesma forma.

## 6. Auditoria de contraste real (não só visual) — todo texto sobre o gradiente navy

A missão pediu validação explícita de contraste em Iorubá/Hebraico. Em vez de confiar só em inspeção visual, computei o contraste WCAG 2.1 real (fórmula de luminância relativa) do texto branco translúcido contra o ponto **mais claro** do gradiente diagonal usado em toda seção navy desta página (`--v2-color-brand-600`, `#2E6DA4` — o pior caso, já que o gradiente vai de `brand-800` escuro a `brand-600` mais claro):

| Elemento | Opacidade antes | Contraste antes | Status | Opacidade depois | Contraste depois |
|---|---|---|---|---|---|
| `.v2-course-feature__level` (tone-brand) | 65% branco | 3.31:1 | ❌ abaixo de AA (4.5:1) | 90% | 4.76:1 |
| `.v2-course-feature__text` (tone-brand) | 85% branco | 4.45:1 | ❌ abaixo por pouco | 90% | 4.76:1 |
| `.v2-pathfinder-section__panel-lead` | 86% branco | 4.53:1 | ⚠️ margem fina demais | 90% | 4.76:1 |
| `.v2-vedium-method__lead` | 86% branco | 4.53:1 | ⚠️ margem fina demais | 90% | 4.76:1 |
| `.v2-live-class__lead` (on-dark, pré-existente) | 82% branco | 4.27:1 | ❌ abaixo de AA | 90% | 4.76:1 |
| `.v2-live-class__list-text` (on-dark, pré-existente) | 75% branco | 3.84:1 | ❌ abaixo de AA | 90% | 4.76:1 |
| `.v2-cta-section__text` (variant brand/brand-full) | 85% branco | 4.45:1 | ❌ abaixo por pouco | 90% | 4.76:1 |

Duas dessas falhas (`live-class__lead`/`live-class__list-text`) eram **pré-existentes** de fases anteriores — nunca tinham sido auditadas matematicamente antes, só aprovadas por inspeção visual. Todas padronizadas para 90% branco (4.76:1, margem confortável acima do mínimo AA de 4.5:1 mesmo no pior ponto do gradiente). O número editorial decorativo (`.v2-course-feature__index`, `aria-hidden`) foi excluído da auditoria — é decoração, não texto de conteúdo.

## 7. Aula ao vivo — "bloco de texto maior" em vez de vazio

A missão ofereceu 2 opções pra coluna esquerda (hoje "muito azul vazio"): reservar área pra mídia futura, ou usar "bloco de texto maior". Optei pela segunda — mais segura, sem risco de parecer um placeholder de imagem quebrada. Título aumentado (`clamp(2.25rem, 1.7rem + 2.4vw, 3.5rem)`, era escala `v2-h2` padrão) e um lead novo adicionado ("Cada encontro acontece com o professor presente, em tempo real. Sem gravação, sem piloto automático.") — afirmação honesta sobre o formato, não uma métrica inventada. Gate de mídia mantido e reforçado: `REAL_VEDIUM_LIVE_CLASS_MEDIA_REQUIRED` registrado no comentário do template, ao lado do `HOME_MEDIA_GATE_02` já existente.

## 8. Progressão, B2B, Insights — mais presença

- **Progressão**: título maior/mais largo (`clamp(1.875rem, 1.5rem+2vw, 3.5rem)`, `max-width:40rem`), rail de 2px para 3px, dot trocado de círculo achatado para halo translúcido + anel sólido + centro vazado ("mais sofisticado"), notas curtas opcionais sob cada etapa (ex.: "Diagnóstico inicial", "Uso real nas aulas") — informação nova, não repetição do rótulo.
- **B2B**: grid de `1.15fr/1fr` para `1fr/1fr` (~50/50), mídia com `min-height:28rem` no desktop (era só `aspect-ratio:4/3`) — imagem maior e mais presente, sem precisar de um hack de sangria que arriscasse quebrar em larguras variadas.
- **Insights/Conhecimento Vedium**: H2 da seção aumentado (`clamp(2rem, 1.6rem+2vw, 3.25rem)`, era `v2-h2` padrão); título do artigo em destaque aumentado e mais pesado (`clamp(1.75rem, 1.4rem+1.6vw, 2.5rem)`, `font-weight:700`, era `--v2-text-h3` 600) — "composição tipográfica forte" (pedido explícito da missão) já que nenhum dos 3 posts reais tem imagem local aprovada.

## 9. CTA final — de card a seção navy de verdade

Antes: `v2_cta_section` renderizava um card (fundo `surface-warm`, `border-radius:lg`, padding próprio) sozinho dentro de uma `<section>` branca — "caixa pequena isolada no meio do branco". Depois: a `<section>` ao redor virou `.v2-section--brand` (mesmo padrão navy full-bleed de "Aula ao vivo"), e um novo variant `brand-full` no componente remove o look de card (`background:none; border-radius:0; padding:0`) — a seção provê o fundo, o componente só organiza título/texto/CTAs. **Bug real pego antes de virar regressão**: o link secundário ("Faça o teste de nível") checava `variant == "brand"` pra decidir se ficava branco — com o novo `variant="brand-full"` essa comparação exata falhava e o link ficaria escuro (ilegível) sobre navy. Corrigido pra `variant in ("brand", "brand-full")` antes do primeiro screenshot.

## 10. Footer — logo e headline não competem mais

O antigo `.v2-footer__message` (Poppins 700, escala `--v2-text-h3`, acima de toda a grade) foi removido — competia visualmente com o logo, posicionado bem abaixo dele. A frase institucional curta ("Escola de idiomas online com aulas ao vivo e progressão por nível.") migrou pra baixo do logo, no lugar da lista de idiomas da Fase B.6A (que já era redundante com a coluna "Cursos" ao lado — removida por duplicar informação, "menos marketing, mais institucional"). O respiro de topo que a antiga headline dava (`padding-block-start` até 96px) migrou pro `.v2-footer__grid` num valor mais contido (64px), já que agora é o logo — não uma headline — o primeiro elemento visual do rodapé.

## 11. Ritmo de cor final

| Seção | Fundo |
|---|---|
| Hero | foto full-bleed (congelado, B.6A) |
| Pathfinder | azul (42%) + branco (58%) |
| VediumMethod | azul (40%) + warm-neutral (60%) |
| Cursos | branco, com blocos tonais azul/warm alternados dentro |
| Aula ao vivo | azul profundo |
| Progressão | warm-neutral |
| B2B | azul profundo (**atualizado na Fase B.6E** — era branco; virou navy pra diferenciar claramente da área B2C ao redor, ver `24-b2b-v2-page-plan.md`) |
| Insights | cinza editorial muito claro (`surface-alt`) |
| CTA final | azul institucional |
| Footer | navy profundo |

Navy aparece em Pathfinder (parcial), VediumMethod (parcial), Aula ao vivo, **B2B**, CTA e Footer — sempre com função (transição de capítulo, prova, diferenciação B2B, ou fechamento). Insights (cinza claro) separa B2B do CTA final, evitando dois navy consecutivos sem quebra — continua "nunca arco-íris de fundos", pedido original da missão.

## 12. O que foi observado no Bain.com (princípios) vs. o que foi adaptado

**Observado (só lógica de composição, nunca copiado)**: ocupação inteligente do espaço (nada "sobra" sem função), alternância de fundo com propósito de capítulo, fotografia grande quando existe, blocos assimétricos (40/60, 42/58 — nunca grades de 4 colunas iguais), tipografia como principal veículo de hierarquia/autoridade, números como dispositivo editorial recorrente.

**Nunca copiado**: nenhum texto, imagem, CSS ou código do Bain. Cor institucional é o azul/terracota da Vedium, nunca o vermelho do Bain. Como a Vedium ainda não tem números institucionais robustos pra publicar (nenhuma métrica inventada, pedido explícito da missão seção 22), a autoridade vem da estrutura pedagógica em si — cursos, aula ao vivo, progressão, B2B, conteúdo — não de estatística.

## 13. Verificação do Hero congelado (regra absoluta da missão)

1. **Hash MD5 do HTML renderizado**: extraído o `<section class="v2-editorial-hero">...</section>` completo do HTML servido antes e depois de todas as mudanças desta fase — `1acd805606a5cd559f92969de0437315` nos dois casos, **idêntico byte a byte** (8724 bytes).
2. **Nenhuma edição em `.v2-editorial-hero*`, `.v2-hero-editorial*`, `.v2-hdr-utility--overlay`, `.v2-header--overlay`, `.v2-header-overlay-wrap`, ou nas funções `initHeroCarousel`/`initHeaderOverlay` de `design-system-v2.js`** durante toda a Fase B.6B — confirmado revisando cada diff aplicado.
3. **Diff de pixel controlado**: screenshots do Hero antes/depois mostraram uma pequena diferença (`bbox` não vazio) — investigado e confirmado como ruído esperado do próprio Ken Burns/crossfade (a mesma foto muda de escala/posição continuamente): duas capturas do estado **"depois"**, tiradas poucos segundos uma da outra sem nenhuma mudança de código entre elas, mostraram a mesma ordem de grandeza de diferença (delta médio por canal ~0.06/255 no controle "depois vs depois", ~0.35/255 no "antes vs depois" — ambos imperceptíveis, mesma faixa). Confirma que a diferença é 100% timing de animação, não uma regressão de código.
4. **`prefers-reduced-motion: reduce`** testado de novo ao final da fase: autoplay não inicia, Ken Burns desligado (`animationName: "none"`) — comportamento idêntico ao validado na Fase B.6A.

## 14. Testes executados

- 326 testes puros passando, 5 skipped; flake8 limpo em `design_system_v2.py`
- Render Jinja real (Docker), 0 `Traceback`, único `<h1>`
- 0 ocorrências de `.v2-media-empty`, "contexto", travessão (`—`), "professor real", "Título de exemplo" no HTML renderizado
- 0 overflow horizontal em 1440px e 390px (`scrollWidth === clientWidth` nos dois)
- Teclado real no Pathfinder: `ArrowDown` move foco+seleção dentro do grupo de rádio, `Tab` avança sem prender foco
- Contraste WCAG 2.1 calculado matematicamente para todo texto branco translúcido sobre o gradiente navy (seção 6) — 7 casos auditados, 5 falhas reais encontradas e corrigidas (2 delas pré-existentes de fases anteriores, nunca antes auditadas)
- Hero verificado intacto por hash MD5 + diff de pixel controlado + reduced-motion (seção 13)
- CRLF: nenhum arquivo modificado contém `\r`
- `git status --porcelain`: mudanças isoladas a `vedium_core/vedium_core/{public/css/v2,public/js/v2,templates/includes/v2,www/design_system_v2.*}` e `docs/redesign/*`
