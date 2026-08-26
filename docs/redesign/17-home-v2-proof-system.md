# 17 — Autoridade visual e sistema de prova (Fase B.6, primeira passada)

> **Origem**: depois do reset de tom da B.5 (`16-home-v2-authority-trust.md`), a missão "AUTORIDADE VISUAL E PROVA INSTITUCIONAL" pediu melhorias visuais **dentro da arquitetura existente** (não mudar ordem/seções): Trust Strip maior, sistema visual unificado de cards de curso, grade sem espaço vazio, cards tipográficos que não parecem "imagem faltando", "Aula ao vivo" preparada para mídia futura, rail de progressão que não parece breadcrumb, e 3 gates formais de mídia (`HOME_MEDIA_GATE`).
>
> **Interrompida e substituída em arquitetura pela Fase B.6 "RESET VISUAL BAIN-INSPIRED"** (ver `18-bain-inspired-direction.md`), que muda a referência visual pra Bain.com e reestrutura a Home (Hero sem foto, VediumPathfinder, "grandes blocos alternados" em vez de mosaico). Este documento registra o que foi implementado nesta primeira passada e **o que sobreviveu** à mudança de direção — a maior parte das mudanças aqui é de componente/CSS de baixo nível, compatível com as duas arquiteturas.

## 1. O que sobreviveu para a Fase B.6-v2 (Bain-inspired)

Tudo abaixo continua em uso depois do reset de arquitetura da seção 2 de `18-bain-inspired-direction.md`:

- Unificação de raio (`--v2-radius-md`/`--v2-radius-media`/`--v2-radius-lg`, seção 3 abaixo)
- Rail de progressão (`.v2-progression`, seção 5 abaixo) — a Bain-inspired manteve o mesmo padrão visual, só trocou os rótulos dos passos
- Correção de padding do card tipográfico + linha decorativa (seção 4 abaixo) — o `LanguageCard`/`LanguageMosaic` em si foi descontinuado da Home na B.6-v2 (ver `18-bain-inspired-direction.md` §3), mas o componente continua na biblioteca de debug e a correção vale para qualquer reaproveitamento futuro
- Peso tipográfico maior do `ProofBar` (`font-weight:700` no título, era 600)

## 2. O que foi descartado/substituído na Fase B.6-v2

- **Trust Strip como seção própria em fundo navy** (`.v2-proofbar--lg` on_dark): a B.6-v2 fundiu Trust Strip + "Como a Vedium ensina" + parte do Institucional numa única seção "O que define a Vedium", em fundo **claro** (não navy) — parte da regra de proporção de cor 70/20/10 (navy vira raro). A classe `.v2-proofbar--lg` continua existindo e é reaproveitada nessa seção nova, só sem `on_dark`.
- **LanguageMosaic/LanguageCard como grade de 5 posições**: substituído por `CourseFeature` ("grandes blocos alternados", um bloco de escala de seção por curso) — ver `18-bain-inspired-direction.md` §3.
- **"Como começar"/ProcessSteps como seção da Home**: a ordem de seção 20 da missão Bain-inspired não inclui mais esse passo a passo (o VediumPathfinder no Hero assume o papel de orientação inicial). O componente continua demonstrado em `?debug=1#lib-process`.

## 3. Unificação de raio (`tokens.css`)

Antes desta fase, o raio variava por componente sem regra clara. Unificado em 3 níveis, conforme a missão ("Hero 12-16px, Cards 8-12px, CTA 12-16px"):

| Token | Valor | Uso |
|---|---|---|
| `--v2-radius-md` | 12px | Cards (`LanguageCard`, `CourseCard__media`, `TeacherCard__photo`, `BlogCard__media`) |
| `--v2-radius-media` | 14px | Mídia de escala de seção (Hero, `TeacherFeature__media`, `FeatureMedia__media`, `LiveClass__media`, `Video`, `CourseFeature__media`) |
| `--v2-radius-lg` | 16px | Blocos de CTA/modal, blocos tonais do `CourseFeature` sem foto |

## 4. Card tipográfico — bug de padding duplicado + linha decorativa

O card tipográfico (`variant="typographic"`, usado quando não há fotografia autorizada — gate cultural de Iorubá, sem asset aprovado para Espanhol/Hebraico na época) tinha **padding duplicado**: o próprio `.v2-language-card--typographic` aplicava `padding: var(--v2-space-8)` E o `.v2-language-card__body` interno aplicava `padding: var(--v2-space-6)` de novo, resultando em respiro desproporcional em relação aos cards com foto. Corrigido — a variante tipográfica não tem padding próprio, só `gap` no body.

Adicionado `.v2-language-card--typographic::before`: uma linha decorativa (2.5rem × 3px, `opacity:0.55`, `background:currentColor`) acima do nome do idioma, para o card não "parecer imagem faltando" quando não há foto — pedido explícito da missão ("um card tipográfico bem desenhado é melhor que um placeholder").

## 5. Rail de progressão (substituiu o texto+seta inline da B.4)

A missão apontou que a representação anterior (rótulos curtos separados por seta, tipografia pequena) "pode parecer breadcrumb". Redesenhado como um **rail de verdade**: uma linha fina horizontal (`.v2-progression__rail`, absolute, 2px, só desktop) atravessando marcadores — bolinhas sólidas (`.v2-progression__dot`) acima de cada rótulo (`.v2-progression__label`, Poppins 700). Padrão comum de "stepper"/trilho de progresso, visualmente distinto do separador `>` e da tipografia pequena típicos de breadcrumb. Em mobile, os passos empilham em coluna e o rail horizontal não aparece (regra de imagem: um rail vertical de 5 pontos não cabe com clareza em 390px sem virar ruído visual).

## 6. HOME_MEDIA_GATE — gates formais de mídia

Registrados como comentários no código-fonte, marcando onde a Home usa fotografia stock/tonal como estado temporário até haver captação real da Vedium:

- **`HOME_MEDIA_GATE_01`**: Hero — a Fase B.6-v2 removeu a foto do Hero por decisão de design (Bain-inspired não usa foto de impacto no Hero), então este gate ficou sem objeto: não se aplica mais.
- **`HOME_MEDIA_GATE_02`**: "Aula ao vivo" (`LiveClassExperience`) — continua sem foto/vídeo real de aula Vedium com professor visível; os 4 assets locais processados (E02/E06/E07/E10) já estão alocados em Cursos/B2B e nenhum serve como prova de aula ao vivo real (ver `06-photography-system.md`, gate P0). Comentário no template (`www/design_system_v2.html`, seção "4. AULA AO VIVO").
- **`VEDIUM_B2B_REAL_MEDIA_PREFERRED`**: B2B usa E07 (videoconferência em equipe, stock) — funcional mas fotografia/case B2B real da Vedium é preferível antes do rollout. Comentário no template (seção "6. B2B").

## 7. Live Class — proporção preparada para mídia futura (52/48)

A missão pediu que a seção "Aula ao vivo" ficasse preparada para uma futura proporção de mídia 50-55%/45-50% quando a captação real (R01/R02/R05) chegar. O grid mudou de `1fr 1fr` para `1.1fr 1fr` (~52/48) e `min-height` da mídia de 24rem para 26rem. Como a seção continua sem imagem por enquanto (gate 02 acima), essa mudança só terá efeito visual quando `image_src` for passado — o texto/lista ocupam as duas colunas de texto no estado atual (ver `v2_live_class_experience` em `macros_editorial.html`).

## 8. Testes executados

326 testes puros, flake8 limpo, render Jinja sem erro em ambos os modos, único `<h1>`, 0 `.v2-media-empty` em Presentation mode, screenshots reais 390px/1440px confirmando raio/padding/rail — ver `18-bain-inspired-direction.md` §8 para os resultados finais (esta passada foi absorvida pela seguinte antes de uma rodada de screenshot própria ser fechada).
