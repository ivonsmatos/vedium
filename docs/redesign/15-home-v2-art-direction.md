# 15 — Direção de arte da Home V2 (Fase B.4)

> **Origem**: a Fase B.3 redesenhou os componentes, mas a revisão humana reprovou de novo — o Presentation Mode continuava parecendo uma sequência de componentes de biblioteca, não uma homepage institucional. A Fase B.4 reestruturou SOMENTE o Presentation Mode de `/design_system_v2` para funcionar como protótipo real da Home Vedium. Ver `14-art-direction-v2.md` para os princípios visuais gerais (ainda válidos); este documento é específico da arquitetura da Home.
>
> **Atualizado na Fase B.5**: a revisão humana aprovou a arquitetura (ordem de seções, ausência de professor/preço/FAQ), mas reprovou o TOM — a Home ainda parecia conceitual/publicitária/genérica, sem autoridade acadêmica. A B.5 foi um reset de linguagem institucional (copy, tipografia, tom), não uma mudança de arquitetura. Este documento continua descrevendo a estrutura (seções 2-6, 8 ainda válidas, exceto onde indicado); **para o reset de tom/copy/confiança institucional, ver `16-home-v2-authority-trust.md`**.
>
> **⚠️ Arquitetura substituída na Fase B.6 (reset Bain-inspired)**: a ordem de seções da seção 2 abaixo **não é mais a ordem real da Home** — foi reestruturada (Hero sem foto + VediumPathfinder, "Cursos" virou blocos grandes alternados em vez de mosaico, Trust Strip fundida em "O que define a Vedium", "Como começar" saiu da sequência). Este documento fica como registro histórico da B.4/B.5. **Para a arquitetura atual, ver `18-bain-inspired-direction.md`** (e `17-home-v2-proof-system.md` para as melhorias de componente da B.6 que sobreviveram à mudança de arquitetura).

## 1. Regra central: Home ≠ página de curso

A Home apresenta a Vedium, sua experiência, os idiomas (como categorias, não fichas técnicas), o método, B2B, conteúdo editorial e o próximo passo. Ela **não** apresenta: professor individual, preço, nível específico (CEFR completo), grade de aulas, depoimento, ficha de curso. Isso tudo pertence às páginas internas (`/professores`, `/curso-de-*`, `/faq`).

## 2. Arquitetura aprovada — ordem exata do Presentation Mode

> **Atualizado na Fase B.5**: a revisão aprovou esta arquitetura, mas pediu 2 seções institucionais novas ("Como a Vedium ensina" e "Institucional Vedium") para reforçar autoridade acadêmica — ver `16-home-v2-authority-trust.md` seção 2 para a ordem final de 13 seções.

1. Header v2
2. Hero institucional
3. Institutional Proof Strip (**Trust Strip** na B.5)
4. Language Showcase (mosaico editorial → **grade uniforme de catálogo** na B.5, ver `16-home-v2-authority-trust.md`)
5. Live Experience
6. How Vedium Works
7. Progressão/Método (institucional, sem CEFR)
8. B2B
9. Knowledge/Blog
10. CTA final
11. Footer

Nada além disso no modo padrão. FAQ foi removido da Home nesta fase.

## 3. Componentes usados na Home

`HeroSplit`, `ProofBar` (variante `on_dark`), `LanguageMosaic`/`LanguageCard` (incl. variante `typographic`, nova nesta fase), `LiveClassExperience` (variante sem mídia, nova nesta fase), `ProcessSteps`, `ProgressionFlow` (**novo componente**, substitui o uso do `LevelJourney` específico de Inglês na Home), `FeatureMedia` (para B2B), `BlogCard` (featured + regular), `CTASection` (variante `brand`), Footer v2.

## 4. Componentes PROIBIDOS na Home (mas mantidos na biblioteca, `?debug=1`)

| Componente | Onde ficou |
|---|---|
| `TeacherFeature`, `TeacherCard`, `TeacherProfileSummary` (incl. a foto real do Prof. Almir) | `#lib-teachers` |
| `StudyRhythmCard` (preço/frequência) | `#lib-pricing` |
| `CourseCard`, `TestimonialCard` | `#lib-course-testimonial` |
| `FAQAccordion` | `#lib-faq` |
| `LevelJourney` (A1–C1 específico de Inglês) | `#lib-levels`, junto com `LevelCard`/`LevelTimeline` atômicos |

Nenhum desses foi excluído do código — todos continuam demonstrados no Component Library, só não fazem parte da composição institucional da Home.

## 5. Fotografia — nova alocação (Home ≠ Fase B.3)

A Fase B.3 usava E07 (videoconferência) no Hero — a revisão apontou que "parece reunião corporativa e não aprendizado de idioma". Realocado:

| Asset | Fase B.3 | Fase B.4 |
|---|---|---|
| E02 (estudo, fones, notebook, caderno) | Inglês (LanguageCard) + FeatureMedia genérico | **Hero** (match direto com o briefing: "adulto aprendendo, fones, notebook, anotações, concentração") + thumbnail do mega menu |
| E06 (escuta/estudo online) | PLE (LanguageCard) | **Inglês** (LanguageCard, no Language Showcase) |
| E07 (videoconferência em equipe) | Hero + B2B | **B2B apenas** — "parece reunião corporativa" deixou de ser um problema porque agora É literalmente a seção sobre equipes corporativas |
| E10 (fones, notas em casa) | LiveClassExperience + Blog | Blog (featured) apenas — LiveClassExperience virou fundo navy sem foto (ver §6) |

**Card tipográfico (novo nesta fase)**: Iorubá, Espanhol e Hebraico não têm fotografia própria autorizada (gate cultural de Iorubá; sem asset estático aprovado para os outros dois). Em vez do estado "sem mídia" (ícone neutro, usado em componentes onde a foto é estruturalmente esperada), essas 3 posições do mosaico usam um **card tipográfico** — nome do idioma grande em Playfair Display sobre fundo sólido (`tone="brand"` azul ou `tone="warm"` surface-warm, alternados para ritmo). "Um card tipográfico bem desenhado é melhor que um placeholder ou uma foto culturalmente errada" (texto da missão).

**Regra reforçada nesta fase**: nenhum placeholder (caixa cinza + ícone) pode aparecer no Presentation Mode. O `BlogCard` foi corrigido para simplesmente não renderizar bloco de mídia quando não há `image_src` (antes caía no ícone neutro) — achado ao auditar a própria Home contra a regra da missão, não reportado por screenshot.

## 6. Seção por seção

**Hero**: conteúdo à esquerda (48%), imagem à direita (52%) — invertido em relação à Fase B.3, que tinha mídia primeiro no DOM/grid por padrão (bug real: a foto aparecia à esquerda, texto à direita, contrário ao que a missão sempre pediu). Corrigido na própria macro `v2_hero_split` (conteúdo agora vem primeiro no markup).

**Institutional Proof Strip**: fundo azul profundo (`.v2-section--brand`), texto branco, sem caixas, divisores verticais discretos, sem números.

**Language Showcase**: mosaico assimétrico específico de 5 posições via `nth-child` (não um sistema genérico de tamanhos) — Inglês grande (2 linhas), Iorubá+Espanhol empilhados numa coluna estreita, PLE+Hebraico dividindo a linha de baixo. Geometria próxima do diagrama ASCII da missão.

**Live Experience**: fundo azul profundo, sem foto (ver §5) — duas colunas de texto (título/lead + lista editorial de 4 itens + CTA), a "segunda maior seção visual" pedida.

**How Vedium Works**: `ProcessSteps` com números grandes translúcidos, sem ícones, sem caixas fechadas.

**Progressão/Método**: componente novo (`v2_progression_flow`) — linha editorial horizontal "Diagnóstico → Trilha → Prática → Feedback → Próximo nível", sem CEFR, sem caixa, sem número.

**B2B**: `FeatureMedia` com E07, sem preço, sem estatística fictícia.

**Blog/Knowledge**: 1 destaque grande (E10) + 2 menores sem imagem (texto puro, não placeholder).

**CTA final**: fundo azul profundo, título "Descubra qual é o próximo passo para você." (a missão rejeitou "Pronto para começar?" como genérico demais).

**Footer**: mantido, com refino de contraste/tamanho de fonte/espaçamento (ver `14-art-direction-v2.md` §9 e `10-design-system-v2-implementation.md` §8).

## 7. Mobile

Confirmado com screenshot real (Chrome headless + CDP mobile emulation) em 390px: Hero com texto primeiro e foto grande abaixo; Proof Strip em 2×2; Language Showcase em coluna única full-width (mosaico complexo não recriado, exatamente como pedido); Live Experience empilha em coluna única mantendo o fundo navy; How it Works e Progressão em coluna vertical; B2B com imagem+conteúdo empilhados; Blog com destaque + lista; CTA full-width; Footer em colunas empilhadas.

## 8. Diferença Home vs. página de curso

| | Home | Página de curso (`/curso-de-*`) |
|---|---|---|
| Professor | Só menção textual ("professores nativos e especialistas") | Perfil individual com foto/nome/bio (quando aprovado) |
| Preço | Nunca | Sim, quando confirmado |
| Nível | Categoria ampla ("Do A1 ao C1") | Trilha CEFR completa, `LevelJourney` |
| Depoimento | Nunca | Sim, quando real e autorizado |
| CourseCard | Não usado | Usado (grade de níveis/turmas do curso) |
| FAQ | Não | Sim, específico do curso |
| Fotografia | Editorial, institucional, idioma como categoria | Pode incluir professor/aula específica do curso |

## 9. Testes executados

326 testes puros, flake8 limpo, render Jinja (ambos os modos, 0 tags residuais), único `<h1>` em Presentation e Debug mode, `Almir`/`preço`/`depoimento`/FAQ/`CourseCard`/`StudyRhythm`/`LevelJourney` ausentes do HTML de Presentation mode (grep direto no output renderizado, não inspeção visual), 0 ocorrências de `.v2-media-empty` em Presentation mode, screenshots reais em 390px e 1440px (Chrome headless + CDP).
