# 19 — Hero full-bleed em carousel editorial (Fase B.6A)

> **Origem**: depois do reset Bain-inspired da Home inteira (`18-bain-inspired-direction.md`), a missão pediu uma segunda referência específica só para o **Hero**: o hero atual do Bain.com (full-bleed, carousel editorial, navegação no rodapé). Escopo estritamente limitado ao Hero — nenhuma outra seção da Home foi alterada nesta fase.

## 1. Referência conceitual observada no Bain.com

Acessado `bain.com` (via fetch/leitura de markup) para confirmar a estrutura antes de implementar. O HTML confirma um **carousel de destaques** no topo da home: múltiplos slides, cada um com imagem, headline, texto de apoio e link — a mesma lógica descrita na missão. Não foi possível (nem foi tentado) inspecionar CSS/JS do Bain diretamente pela ferramenta de fetch disponível; a implementação usa o padrão já bem conhecido desse tipo de componente editorial (full-bleed, overlay de leitura, navegação por abas no rodapé com barra de progresso) descrito em detalhe pela própria missão, não uma cópia de arquivo algum do Bain.

**Nunca copiado**: código, CSS, JavaScript, fontes, imagens ou qualquer identidade proprietária do Bain. **Reproduzida só a lógica**: full-bleed, overlay escuro, headline branca grande, header sobreposto, carousel editorial, navegação dos slides no rodapé, movimento sutil, CTA simples com seta.

## 2. Diferenças deliberadas em relação ao Bain

- **Cor**: overlay em navy institucional Vedium (`rgba(29,65,111,...)`, token `--v2-color-brand-800`), nunca o vermelho do Bain.
- **Tipografia**: Poppins (headings)/Inter (corpo), nunca a fonte proprietária do Bain.
- **Conteúdo**: 100% Vedium — cursos, B2B, escola — nunca replica manchetes/relatórios do Bain.
- **CTA**: botão outline secundário com seta (`v2.v2_button(variant="secondary", on_dark=true, icon="arrow-right")`), já existente no design system — não um componente novo copiado de referência externa.

## 3. Componente novo: HeroEditorialCarousel

`v2_hero_editorial_carousel(slides)` em `macros_editorial.html`. Markup: `<section class="v2-editorial-hero">` com `.v2-editorial-hero__slides` (todas as camadas de foto, sempre `position:absolute;inset:0`, crossfade por opacidade), `.v2-editorial-hero__scroll` (indicador "Scroll ↓", só desktop) e `.v2-editorial-hero__nav` (tablist no rodapé, um botão por slide com barra de progresso).

### H1 único

Só o **primeiro slide** renderiza `<h1>`; os demais usam `<p>` com a mesma classe visual. Um carousel não deveria ter vários headings reais competindo pela árvore de acessibilidade, e isso mantém válido o teste já existente do projeto ("um só `<h1>` renderizado no HTML"), sem precisar mudar o método do teste.

### Sem JS

O CSS já deixa só o slide 1 com `opacity:1` (os demais `opacity:0`, `aria-hidden`) — sem JavaScript, o visitante vê um hero estático normal (headline, apoio e CTA reais e funcionais), nunca um carousel quebrado ou uma tela vazia. As abas do rodapé ficam inertes nesse cenário (são `<button>`, sem handler sem JS) — aceitável porque o slide 1 (institucional, Vedium) já é o conteúdo mais importante e continua 100% acessível e navegável.

## 4. Bug real encontrado e corrigido: stacking do crossfade

A primeira versão dava `position:relative` ao slide ativo. Como todo filho dele (`__media`, `__overlay`, `__content`) é `position:absolute`, a altura do slide ativo passava a vir só do **conteúdo de texto em fluxo normal** — bem mais baixo que o Hero inteiro — então a foto/overlay cobriam apenas até a base do texto, não a seção toda. Confirmado por screenshot (a foto cortava logo abaixo do CTA, deixando ~40% do Hero em branco). Corrigido: todo slide fica **sempre** `position:absolute;inset:0` (ativo ou não) — só a opacidade muda no crossfade; a altura vem sempre do `.v2-editorial-hero` (via `.v2-editorial-hero__slides`, também absolute/inset:0).

## 5. Animação e timing

- **Ken Burns**: `scale(1) → scale(1.06) translate(-0.6%,-0.4%)`, 12s, `ease-out`, reiniciado a cada troca de slide (JS remove/reflow/reaplica o `style.animation` da imagem — truque padrão pra reiniciar uma animação CSS via JS sem duplicar keyframes).
- **Crossfade**: opacidade 1100ms `cubic-bezier(.4,0,.2,1)`; o texto (`.v2-editorial-hero__copy`) recebe o mesmo timing em opacidade + `translateY(18px→0)`.
- **Autoplay**: 9s por slide (`--v2-hero-autoplay`, CSS custom property — fonte única lida tanto pela barra de progresso em CSS quanto pelo timer em JS via `getComputedStyle`). Confirmado por teste real: slide avança de `slide-0` para `slide-1` entre 0s e 9.8s.
- **Progresso**: barra por aba (`.v2-editorial-hero__tab-fill`), `transform:scaleX(0→1)`, mesma duração do autoplay, reinicia a cada troca (manual ou automática).
- **Pausa**: hover sobre o Hero, foco dentro dele, aba do navegador oculta (`document.hidden`) e `prefers-reduced-motion`. Clique numa aba muda o slide imediatamente e reinicia o timer.

## 6. `prefers-reduced-motion`

Testado com `Emulation.setEmulatedMedia({prefers-reduced-motion: reduce})`: depois de 10.5s (mais que um ciclo de autoplay), o slide ativo continuou sendo `slide-0` (autoplay nunca inicia) e `getComputedStyle(img).animationName === "none"` (Ken Burns desligado). CSS também reduz a transição de crossfade a `1ms` e remove o `translateY` de entrada do texto nesse modo — o carousel continua funcional manualmente (cliques nas abas), só sem movimento automático.

## 7. Acessibilidade

- `role="tablist"`/`role="tab"`/`aria-selected`/`aria-controls`/`tabindex` roving (só a aba ativa tem `tabindex="0"`).
- Teclado: `ArrowRight`/`ArrowLeft`/`Home`/`End` movem o foco E trocam o slide (mesmo padrão "ativação automática" já usado no `LevelJourney` do design system).
- Pausa ao receber foco dentro do Hero (`focusin`/`focusout`), sem prender o foco (não é modal).
- CTA de cada slide é um link real (`<a href>`), sempre acessível independente do estado do carousel.
- Slides inativos ficam `aria-hidden="true"` — não anunciados por leitor de tela, não navegáveis por Tab.

## 8. Media gate — slide de Iorubá não ativado

A missão pediu explicitamente: *"não usar fotografia cultural genérica... caso não haja [asset aprovado], não ativar este slide"*. Nenhum dos 4 assets Envato locais aprovados (E02/E06/E07/E10) representa Iorubá — gate cultural em vigor desde a Fase B.3/B.4 (`06-photography-system.md`). O carousel final tem **4 slides** (Vedium/Inglês/Português/Empresas), não os 5 pedidos no rascunho da missão. Registrado como `HOME_HERO_REAL_MEDIA_REQUIRED` (Iorubá) — não fabricado, não usado stock genérico.

**Alocação de imagem** (reaproveita os mesmos 4 assets já usados nas seções abaixo do Hero — não há asset extra disponível): Vedium→E06, Inglês→E02, Português→E10, Empresas→E07. Cada slide do Hero mostra a MESMA foto que a seção correspondente mais abaixo na página (Cursos/B2B) — repetição aceita conscientemente dada a escassez de assets aprovados (só 4 no total), documentada aqui em vez de introduzir stock não aprovado só para variar.

## 9. Performance

- Slide 1: `loading="eager" fetchpriority="high"` (candidato a LCP).
- Slides 2-4: `loading="lazy"`.
- `width`/`height` reais de cada arquivo (2000×1263 para E02, 2000×1333 para E06/E07/E10) — evita CLS, sem inventar proporção.
- Tamanho dos 4 arquivos JPEG locais: E02 298.0K, E06 237.8K, E07 256.6K, E10 221.8K (mesmos derivados já usados no resto da Home, nenhum novo asset processado nesta fase).
- Nenhum WebP/AVIF gerado nesta fase (fora de escopo — registrado como possível otimização futura, não bloqueante pra este protótipo).

## 10. Header overlay (consequência necessária do Hero full-bleed)

O Hero full-bleed exige um header transparente sobreposto (pedido explícito da missão, seção 9). Implementado como variante opt-in (`v2_header_overlay=true`) em `header.html`/`header-footer.css`:

- **`position:fixed`** (não `absolute`) — decisão deliberada, diferente do que uma leitura literal de "overlay só no Hero" sugeriria. Um header `absolute` sairia do fluxo só durante o Hero e desapareceria (rolaria pra fora) assim que o Hero terminasse, deixando as outras 7 seções da Home sem navegação nenhuma. `fixed` resolve isso E entrega, de graça, a pendência de "sticky header" registrada em `16-home-v2-authority-trust.md` §5 como adiada.
- **Logo dupla** (branca + colorida, cross-fade só em CSS via `opacity`, sem trocar `src` via JS) — `is-solid` alterna qual das duas aparece.
- **`is-solid`**: JS compara `hero.getBoundingClientRect().bottom` com a base do próprio header (via rAF, sem lib de scroll) — confirmado por teste real: depois de `scrollTo(0, 1300)`, `is-solid` vira `true` e o header renderiza fundo branco sólido, logo colorida, texto escuro.
- **Bug real encontrado e corrigido**: a barra do próprio dev-tool de preview (`.dstool-banner`, fora de `.v2-scope`) é `position:sticky;top:0;z-index:500` — como meu header também tentava `top:0`, os dois ocupavam o mesmo retângulo no topo da tela e o dev-banner (z-index maior) escondia a utility bar inteira por baixo dele. Corrigido medindo a altura real do dev-tool em runtime (`initHeaderOverlay`) e aplicando esse valor como `top` do header — nunca hardcoded, porque a barra do dev-tool quebra em mais linhas (e fica mais alta) em telas estreitas.
- **Mesmo valor também encolhe `min-height:100svh` do Hero** (`--v2-devtool-offset`, CSS custom property setada pelo mesmo JS): sem isso, Hero (100svh) + a barra do dev-tool juntos passavam de uma tela, e a navegação de slides do rodapé ficava fora da viewport inicial em telas móveis (onde a barra do dev-tool quebra em até 3 linhas, ~96px). Em produção real (sem dev-tool), a variável nunca é setada, fica `0px`, e `100svh` volta a ser literal.

## 11. Mobile (390px)

Full-screen, mesma lógica do desktop. Conteúdo alinhado à base (`align-items:flex-end`) em vez de centralizado, overlay reforçado (a mesma gradiente radial/linear, só que a coluna de texto ocupa quase toda a largura). Headline reduzida (`clamp(2.625rem, 2rem+3vw, 3.25rem)`, ~42-52px conforme pedido). Navegação dos slides em scroll horizontal (`overflow-x:auto`) quando os 4 rótulos não cabem lado a lado. Confirmado por screenshot real: hero cobre a tela inteira, texto legível, os 4 tabs (Vedium/Inglês/Português/Empresas) visíveis na base, dentro de uma única tela após a correção do `--v2-devtool-offset`.

## 12. O que ficou fora do escopo desta fase (por instrução explícita)

- VediumPathfinder **não** ficou dentro do Hero — foi reposicionado pra sua própria seção logo abaixo (ver comentário em `www/design_system_v2.html`, secao "1B"), sem alterar o componente em si.
- Nenhuma outra seção da Home foi tocada (Cursos, Aula ao vivo, Progressão, B2B, Conhecimento Vedium, CTA, Footer — todas idênticas à Fase B.6/B.6-v2).
- Nenhuma migração da Home real de produção, nenhum deploy, nenhum commit automático.

## 13. Testes executados

- 326 testes puros passando, 5 skipped; flake8 limpo em `design_system_v2.py`.
- Render Jinja real (Docker), Presentation Mode 200/OK, único `<h1>`, 0 `Traceback`.
- 4 slides confirmados no HTML renderizado (`v2-editorial-hero__slide` × 4), 0 ocorrências de "Iorubá" nos rótulos de navegação do Hero (gate de mídia confirmado, não fabricado).
- Interação real via CDP: clique na aba 3 (Português) troca o slide ativo corretamente (`aria-selected`, `id` do slide, crossfade visual confirmado por screenshot).
- Autoplay real: slide avança sozinho entre 0s e 9.8s.
- `prefers-reduced-motion: reduce` real: autoplay não inicia, Ken Burns desligado (`animationName: "none"`), confirmado depois de 10.5s de espera.
- Scroll real: `is-solid` ativa corretamente depois de passar do Hero, header muda pra fundo branco/logo colorida/texto escuro, confirmado por screenshot.
- Screenshots reais em 1440px e 390px (slide 1 estático, slide 3 após clique, header solid após scroll, hero mobile completo com navegação visível).
- CRLF: nenhum arquivo modificado contém `\r`. `git status --porcelain`: mudanças isoladas a `vedium_core/vedium_core/{public/css/v2,public/js/v2,templates/includes/v2,www/design_system_v2.*}` e `docs/redesign/*`.
