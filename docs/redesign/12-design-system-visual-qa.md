# 12. QA Visual, Marca e Responsividade — Design System V2 (Fase B.1)

> **Escopo desta fase:** QA e correção SOMENTE de arquivos da Fase B (`vedium_core/vedium_core/public/css/v2/`, `public/js/v2/`, `templates/includes/v2/`, `www/design_system_v2.py`/`.html`, `docs/redesign/10-design-system-v2-implementation.md`). Nenhum arquivo público de produção fora de `v2/` foi tocado. Nenhuma página real (Home, cursos) foi migrada. Nenhum deploy foi feito. Nenhum commit foi feito automaticamente — ver relatório final ao usuário.
>
> Metodologia: sem acesso a `bench` real nem a ferramenta de automação de navegador (Playwright/Puppeteer não estão configurados neste projeto — confirmado por busca no `package.json` e no filesystem; por instrução explícita, nenhuma ferramenta nova foi instalada só para isso). A QA visual foi feita por **auditoria de código** (CSS/Jinja renderizado via `jinja2.Environment` + `FileSystemLoader`, reproduzindo o parser/render Jinja padrão fora do bench) e por **cálculo direto** (contraste WCAG via fórmula de luminância relativa, contagem de landmarks/aria, contagem de breakpoints). Isso está sinalizado como limitação em cada seção onde se aplica.

## 1. Viewports testados (auditoria de código, não screenshot)

Breakpoints reais definidos no CSS (`foundations.css`, `components-editorial.css`, `header-footer.css`): `576px`, `768px`, `992px`, `1200px`. Os 8 viewports pedidos mapeiam assim:

| Viewport | Tier de CSS aplicado | Resultado da auditoria |
|---|---|---|
| 360px | mobile-first (sem breakpoint) | grids em coluna única, botões full-width onde aplicável, sem overflow horizontal detectado no CSS (nenhum `width` fixo maior que o container em componentes editoriais) |
| 375px | mobile-first | idem 360px |
| 390px | mobile-first | idem 360px |
| 430px | mobile-first | idem 360px; testado especificamente contra o card de `LanguageCard`/`CourseCard` com textos longos (seção "Conteúdo extremo" do preview) — sem quebra de layout no CSS |
| 768px | primeiro breakpoint (`min-width:768px`) ativa em `foundations.css`, `components-editorial.css`, `header-footer.css` | grids passam de 1 para 2 colunas; Header v2 permanece em modo mobile até 992px (menu hambúrguer) |
| 1024px | entre `992px` e `1200px` — tier de 992px ativo | Header v2 muda para modo desktop (nav horizontal) em 992px; grids de cards em 2-3 colunas |
| 1280px | tier de `1200px` ativo | largura máxima do `.v2-container--content`/`--wide` passa a limitar o conteúdo, evitando linhas de texto excessivamente longas |
| 1440px | tier de `1200px` ativo | idêntico a 1280px — `max-width` do container impede crescimento indefinido |

**Limitação:** isso é leitura de regras `@media` e valores de `max-width`, não uma renderização visual real. Não há garantia de que não existam sobreposições ou cortes visuais sutis que só um navegador real revelaria. Recomendado no doc 10 (seção 13) como próximo passo.

## 2. Componentes testados

Todos os 22 nomeados na missão + Header v2 + Footer v2, cobertos pelas seções do preview (`www/design_system_v2.html`): Typography, Colors, Buttons, Forms, Misc (Badge/Breadcrumb/Alert/Modal), Heroes (Split/FullBleed/Centered), ProofBar, LanguageCard, CourseCard, LevelTimeline, TeacherCard, StepList, FeatureMedia/VideoSection, Testimonials, PricingCard, FAQ, BlogCard, CTA, Conteúdo extremo (seção nova da B.1), Header, Footer.

Render final verificado via `jinja2.Environment(FileSystemLoader(...))`:
- **1** `<h1>` (único, na faixa fixa de preview — corrige o bug de 4×`<h1>` da Fase B)
- **21** ocorrências de `.v2-media-empty` (estado "sem mídia" correto em todos os pontos onde a imagem é omitida na demo)
- **0** `src=""` (nenhuma imagem quebrada)
- **0** tags Jinja não renderizadas (`{{`/`{%` residuais)

## 3. Problemas encontrados e corrigidos nesta fase (B.1)

| # | Problema | Correção |
|---|---|---|
| 1 | Fontes Google Fonts carregadas via `<link>`/`<preconnect>` remoto no `<head>` do preview | Removidas; substituídas por `@font-face` local (só Playfair Display, ver seção 5) |
| 2 | `v2_placeholder_img` (SVG genérico) usado como substituto de foto real em Hero/CourseCard/FeatureMedia/VideoSection — padrão "placeholder de marketplace", risco de humanização ruim | 5 macros (`v2_hero_split`, `v2_hero_full_bleed`, `v2_course_card`, `v2_feature_media`, `v2_video_section`) tiveram `image_src`/`poster_src` tornados genuinamente opcionais, com novo estado `.v2-media-empty` (ícone neutro + fundo `surface-alt`) quando não há imagem — sem fingir foto |
| 3 | Badge de nível sobreposto à imagem do `CourseCard` (`position:absolute`) — padrão visual de app/marketplace | Badge movido para o corpo do card (antes do título), variante trocada de `brand` para `neutral`; regra de `position:relative`/`absolute` removida do CSS |
| 4 | Conteúdo genérico no preview ("Lorem"-like) não representava a marca real | Substituído por copy real fornecida pela missão para Hero (genérico/B2B/Inglês) e para os 4 `LanguageCard` (Inglês/Iorubá/PLE/Espanhol) |
| 5 | Sem teste de conteúdo extremo (título curto/longo, sem eyebrow, sem imagem, grids de 1/2/3/5/6 cards) | Nova seção `#extreme` no preview cobrindo todos esses casos |
| 6 | Sem teste multilíngue de quebra de linha/RTL além de texto solto | Novo bloco com colunas estreitas (320px) em PT/DE/Hebraico com palavras longas + um par real de `v2_feature_card` renderizado em `dir="rtl" lang="he"` |
| 7 | `direction:rtl` usado como hack de inversão visual em `.v2-feature-media--reverse` (Fase B) | Trocado por `order` do CSS Grid — não corrompe semântica RTL real |
| 8 | Página do preview com múltiplos `<h1>` (bug de acessibilidade, Fase B) | `heading_level` parametrizado nos 3 macros de Hero; único `<h1>` real fica na faixa fixa do topo do preview |

## 4. Problemas pendentes (não corrigidos nesta fase — motivo documentado)

- **Poppins/Inter não auto-hospedadas.** Verificado que os arquivos `.woff2` não existem localmente no repositório; por instrução explícita ("não baixe fontes automaticamente"), não foram baixadas. Fallback ativo: Arial. Playfair Display já está auto-hospedada (arquivos pré-existentes no repo).
- **Crop de rosto/mãos com foto real não validado.** O asset mais próximo disponível no inventário de fotografia (E06) tem 29,4 MB — grande demais para uso web e sem ferramenta de processamento de imagem (PIL/Pillow) instalada no ambiente. Por instrução explícita de não instalar ferramenta nova só para isso, a validação de `object-position`/safe-area/crop foi feita apenas com SVGs abstratos de referência de proporção (4:5 e 4:3), rotulados como "referência técnica", nunca como foto real. Pendente: obter um asset real em tamanho web.
- **Sem teste em navegador/dispositivo real.** Nenhuma ferramenta de automação de navegador está configurada no projeto; não foi instalada nova. QA feita por auditoria de código (seção 1).
- **Sem auditoria de acessibilidade com ferramenta real** (axe, WAVE, leitor de tela). Ver seção 6 para o que foi possível verificar sem ferramenta.

## 5. Tipografia — decisão final (Fase B.1)

- **Aprovadas:** Poppins (títulos/interface), Inter (corpo/UI), Arial (fallback), Playfair Display (uso editorial seletivo — hero/citações).
- **Rejeitada como fonte principal:** Kumbh Sans (estava proposta em `04-design-system-plan.md`; decisão humana explícita na Fase B.1 a descartou).
- **Hebraico:** nem Poppins nem Inter cobrem o alfabeto hebraico — pilha dedicada via seletor `:lang(he)` (`Noto Sans Hebrew`/`Arial Hebrew`/`David`/Arial).
- **Iorubá:** Latim estendido (diacríticos, dígrafos gb/kp) — Poppins/Inter cobrem Latin Extended-A; verificação foi contra as marcas usadas no material de Iorubá revisado nesta sessão, não uma auditoria glifo-a-glifo completa.
- **Estado de hospedagem:** Playfair Display 700 auto-hospedada localmente (3 subsets: latin, latin-ext, cyrillic, com `unicode-range` e `font-display: swap`). Poppins/Inter ainda não existem localmente — caem no fallback Arial até serem providenciadas (ver doc 10, seção 13).
- Nenhum `@import` remoto de fonte permanece no código da Fase B.1.

## 6. Contraste (WCAG) — recalculado nesta fase

Fórmula de luminância relativa (WCAG 2.x) aplicada aos pares de cor realmente usados nos componentes:

| Par | Razão | AA texto normal (4.5:1) | AA texto grande/UI (3:1) |
|---|---|---|---|
| ink-900 sobre surface-0 | 18.51:1 | PASSA | PASSA |
| ink-700 (muted) sobre surface-0 | 10.59:1 | PASSA | PASSA |
| ink-500 (subtle) sobre surface-0 | 4.98:1 | PASSA | PASSA |
| brand-600 (link) sobre surface-0 | 5.47:1 | PASSA | PASSA |
| texto branco sobre accent-700 (botão primário) | 8.75:1 | PASSA | PASSA |
| texto branco sobre accent-600 (hover) | 7.22:1 | PASSA | PASSA |
| texto branco sobre brand-700 | 7.87:1 | PASSA | PASSA |
| border-strong sobre surface-0 (borda funcional) | 3.65:1 | FALHA (não se aplica — não é texto) | PASSA (uso correto: só bordas/UI) |
| border decorativo sobre surface-0 | 1.35:1 | FALHA | FALHA — **por design**: token marcado como "decorativo apenas", nunca usado em borda funcional |
| success/warning/danger sobre branco | 5.31–6.57:1 | PASSA | PASSA |
| focus sobre branco | 4.93:1 | PASSA | PASSA |
| ink-900 sobre surface-warm | 16.49:1 | PASSA | PASSA |
| branco sobre brand-800 (hero on-dark) | 10.30:1 | PASSA | PASSA |

Todos os pares usados para texto/ícone funcional passam AA. O único par que falha (`border` decorativo, 1.35:1) é usado exclusivamente como decoração visual, nunca como indicador funcional — o token `color-border-strong` (3.6:1) existe especificamente para preencher essa lacuna em bordas com significado (input, card interativo).

## 7. Acessibilidade — verificações possíveis sem ferramenta dedicada

- Único `<h1>` por página de preview (corrigido nesta fase).
- Todos os `<button>`/`<a>` de ícone-apenas (fechar modal, etc.) têm `aria-label`.
- `v2_field` associa `label`/`for`, `aria-describedby` para hint/erro, `aria-required` quando aplicável.
- `v2_modal` usa `role="dialog" aria-modal="true" aria-labelledby`.
- `v2_alert` usa `role="alert"` (warning/danger) ou `role="status"` (info/success).
- `prefers-reduced-motion` respeitado tanto via zeramento de tokens de duração quanto via regra `@media` global.
- Ícones decorativos usam `aria-hidden="true" focusable="false"`; ícones com significado próprio aceitam `decorative=false` + `label`.

**Não verificado** (requer ferramenta real): navegação por teclado ponta a ponta, ordem de foco, comportamento de leitor de tela, zoom 200%/reflow 320px, contraste de estados `:hover`/`:focus-visible` renderizados (só os tokens base foram calculados).

## 8. Mídia — sistema de fotografia

- Estado "sem mídia" (`.v2-media-empty`) agora é o comportamento padrão genuíno de 5 componentes quando nenhuma imagem é passada — não há mais SVG fingindo ser foto.
- Único exemplo de foto real da marca usada em qualquer lugar do sistema: a foto do Prof. Almir Soares da Silva (adicionada na missão anterior, fora do escopo desta fase, mantida como está).
- Duas imagens SVG abstratas (proporção 4:5 e 4:3) existem **somente** dentro da seção "Conteúdo extremo" do preview, claramente comentadas como "referência técnica de proporção", nunca apresentadas como aluno/professor/turma real.
- Crop de rosto/mãos com asset real: **não validado** nesta fase (ver seção 4 — asset de 29,4 MB, sem ferramenta de resize).

## 9. RTL e multilíngue

- Bloco de estresse com colunas de 320px em PT/DE/Hebraico testando quebra de palavra longa e `line-height`.
- Par real de `v2_feature_card` renderizado em `dir="rtl" lang="he"` — valida que as propriedades lógicas de CSS (`margin-inline`, `padding-inline`, `inset-inline-*`) já usadas nos componentes se comportam corretamente sem stylesheet RTL separado.
- `.v2-feature-media--reverse` corrigido para usar `order` em vez de `direction:rtl` (ver seção 3, item 7) — elimina o risco de corromper semântica RTL real ao combinar com conteúdo hebraico de verdade.

## 10. Screenshots gerados

**Nenhum.** Não há ferramenta de automação de navegador disponível neste ambiente/projeto, e a instrução explícita da missão foi não instalar uma nova só para isso. Toda a QA visual desta fase foi feita por auditoria de código (CSS renderizado + regras `@media` + render Jinja real via `jinja2.Environment`), não por captura de tela. Isso está registrado como limitação recorrente nas seções 1, 4 e 13 do doc 10.

## 11. Limitações do ambiente (resumo)

- Sem Playwright/Puppeteer/navegador automatizável configurado — não instalado por instrução explícita.
- Sem PIL/Pillow para processar imagem — não instalado por instrução explícita.
- Sem ambiente `bench` real disponível — render validado via `jinja2.Environment` + `FileSystemLoader`, que reproduz o parser Jinja mas não o contexto/hooks completo do Frappe.
- Sem ferramenta de auditoria de acessibilidade (axe/WAVE) nem leitor de tela.
- Asset fotográfico real disponível (E06) grande demais (29,4 MB) para validação de crop sem ferramenta de resize.

## 12. Testes e verificação executados

- `pytest -q vedium_core/vedium_core/tests/test_pure_*.py vedium_core/vedium_core/tests/test_course_urls.py` → **326 passed**
- `flake8 vedium_core/vedium_core/www/design_system_v2.py --max-line-length=120` → limpo, sem achados
- Render completo do preview via `jinja2.Environment` → OK, 77.037 caracteres, 1×`<h1>`, 21×`.v2-media-empty`, 0×`src=""`, 0 tags Jinja residuais
- `git status --porcelain` → confirma que só arquivos novos/isolados em `v2/` e `docs/redesign/` foram tocados; nenhum arquivo de produção fora do escopo alterado
