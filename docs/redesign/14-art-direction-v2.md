# 14 — Direção de arte do Design System V2 (Fase B.3 + B.4)

> **Origem**: a Fase B construiu uma base tecnicamente correta (arquitetura Jinja/CSS isolada, acessibilidade, i18n). A revisão visual humana da Fase B.2 **reprovou a direção de arte**: o preview parecia biblioteca técnica de componentes, LMS genérico, dashboard ou marketplace — distante da Vedium. Este documento registra os princípios que guiaram o redesign da Fase B.3 e que qualquer componente novo deve seguir.
>
> **Atualizado na Fase B.4**: a revisão humana da B.3 reprovou de novo — desta vez a *arquitetura* do Presentation Mode (continuava parecendo sequência de componentes, não uma homepage). A B.4 reestruturou o Presentation Mode inteiro para funcionar como protótipo real da Home institucional. Os princípios gerais abaixo continuam válidos; **para a arquitetura específica da Home (ordem de seções, o que foi removido, nova alocação de fotografia, card tipográfico), ver `15-home-v2-art-direction.md`**.

## 1. Princípio central

> PESSOA / AULA / PROFESSOR / CONTEXTO + CONTEÚDO = COMPOSIÇÃO

Fotografia não é decoração nem "mídia opcional" — é parte estrutural da composição, presente desde o primeiro rascunho de um componente, não adicionada depois. Onde a fotografia real ainda não está autorizada (gate de `06-photography-system.md`), o componente assume honestamente o estado "sem mídia" em vez de fingir uma foto (SVG placeholder, avatar com letra, etc.).

A Vedium deve parecer: humana, institucional, contemporânea, sofisticada, editorial, profissional, premium sem ostentação, orientada por fotografia, claramente uma escola de idiomas ao vivo — nunca um SaaS, dashboard, infoproduto ou template ThemeForest genérico.

## 2. O que foi removido/reduzido nesta fase

- Terracota (`--v2-color-accent`) como cor padrão de todo eyebrow/label — virou acento raro (ver seção 5).
- Preço no `CourseCard` (removido do macro, não só condicional) — preço é assunto da seção comercial (`StudyRhythmCard`), nível não é preço.
- `PricingCard` com números inventados — substituída por `StudyRhythmCard`, que descreve frequência/formato sem preço, e usa dado real (`frequency_pricing_rules.py`: 1-5 aulas/semana, desconto de 10% a partir de 2).
- Avatar com letra como fallback "principal" de foto de professor — agora é o mesmo estado "sem mídia" elegante dos demais componentes.
- Badge de nível sobreposto à imagem do `CourseCard` (padrão de e-commerce) — nível virou texto discreto no corpo do card.
- Sombra como recurso decorativo padrão — reservada a elementos que genuinamente flutuam sobre o conteúdo (modal, mega menu).
- ProofBar com números genéricos ("5", "100%", "A1-C1") sem fonte — virou benefício com título + texto.
- SVG "placeholder de dev" fingindo ser foto — virou estado "sem mídia" real do componente (Fase B.1) e, na B.3, fotografia real de fato entrou nos componentes principais (ver seção 6).
- Bandeira remota (`flagcdn.com`) no seletor de idioma — única dependência de asset externo do sistema; virou rótulo textual.

## 3. Escala

Ver `docs/redesign/10-design-system-v2-implementation.md` seção 3 para os tokens exatos. Resumo:

- Container principal: 1180px (`--v2-container-content`), grids/hero até 1280px (`--v2-container-wide`).
- Seção: `clamp(56px, ..., 128px)` de padding vertical — bem mais presença que a Fase B (48-96px).
- Hero: `min-height` institucional (~30rem/480px no bloco de mídia, seção inteira com respiro) só a partir de 992px — em mobile o hero encolhe pro conteúdo real, nunca força altura artificial numa tela pequena.
- H1 ~38px→72px, H2 ~30px→48px, H3 24px→32px, corpo 16px→19px (todos fluidos via `clamp()`, não saltos abruptos por breakpoint).
- Botões/inputs: 48px de altura padrão (`--v2-control-height`), 44px só nos `compact`.
- Linhas de texto de corpo: `.v2-measure`/`__lead`/`__content` limitam a ~34-42rem (aprox. 65-75 caracteres por linha), consistente com `04-design-system-plan.md`.

## 4. Tipografia

Poppins (headings/interface) + Inter (corpo/microcopy) + Arial (fallback, ativo hoje — Poppins/Inter ainda não auto-hospedadas) + Playfair Display (uso editorial seletivo: citação/testimonial, mensagem institucional do footer — **nunca** H1 principal de página real). O exemplo antigo "Aprenda com quem já viveu" em Playfair grande na Fase B não representa mais a direção principal — hoje só aparece no Component Library (debug) como demonstração isolada da família, não como um H1 de verdade.

## 5. Paleta

Hierarquia de uso (não de token — os valores continuam os de `04-design-system-plan.md`):

| Papel | Token | Uso |
|---|---|---|
| Estrutura e confiança | `brand-700`/`brand-800` (azul institucional/petróleo) | Header active state, footer, CTA institucional, mega menu |
| Superfície e apoio | `brand-300` | Números do ProcessSteps/LevelJourney (baixa opacidade visual), badge do timeline atual |
| Respiro | `surface-0`/`surface-50` | Fundo padrão, alternância de seção |
| Estrutura editorial | `ink-900/700/500`, `surface-warm` | Texto, testimonial/CTA em fundo quente |
| Ação e destaque | `accent-700`/`accent-600` (terracota) | **Um** CTA primário por seção, badge "mais escolhido"; nunca em todo eyebrow/label/badge pequeno |

Regra prática aplicada: se ao contar os usos de terracota numa seção o número passar de 1-2, é sinal de que voltou o padrão antigo — reduzir.

## 6. Fotografia

Ver `docs/redesign/06-photography-system.md` (regras completas) e `10-design-system-v2-implementation.md` seção 11 (o que foi implementado). Resumo prático desta fase:

- 4 derivados locais de stock já aprovado (E02/E06/E07/E10), gerados com Pillow já presente no bench, nunca commitados (`.git/info/exclude`).
- Alocação segue `08-page-media-map.md`: E07 → Home hero + B2B; E02 → Inglês; E06 → PLE; E10 → LiveClassExperience + Blog.
- **Iorubá, Espanhol e Hebraico não têm foto** no `LanguageMosaic` desta fase — gate de governança (nenhum stock atual é autorizado como hero/prova de Iorubá; não há asset estático aprovado para Espanhol; evitar repetir a mesma pessoa como se representasse vários cursos cobriu Hebraico também). Isso é uma decisão de disciplina, não uma lacuna esquecida — documentada visivelmente no próprio Presentation mode.
- `LiveClassExperience` não usa stock para simular "aula ao vivo real" (esse é um gate P0 — REAL VEDIUM REQUIRED em `08-page-media-map.md`): a imagem ali é apoio ambiental, o texto descreve o processo pedagógico em geral, nunca afirma "isto é uma aula Vedium".
- `object-position` diferenciado por imagem quando o crop recomendado por `06-photography-system.md` não é o centro (ex.: E07 → `right center`, preserva rosto/mãos conforme a tabela da seção 8 daquele documento).

## 7. Cards e componentes de seção

- `LanguageCard`: fotografia 4:5, nome grande (`--v2-text-2xl`, ~28px), tese curta, nível/trilha como texto simples, CTA textual ("Conheça a trilha →").
- `LanguageMosaic`: ritmo editorial — card grande (Inglês), médios (PLE/Iorubá), pequenos (Espanhol/Hebraico), bloco institucional B2B separado com fundo azul sólido. Em mobile, tudo empilha uniforme.
- `CourseCard`: imagem 4:3 maior, nível como texto discreto (não badge), sem preço.
- `TeacherFeature`: composição 50/50, foto grande, nome como heading real (`<h2>`), bio só quando há fato verificado (nunca inventada).
- `LevelJourney`: timeline grande (tablist ARIA) + painel do nível selecionado com descrição/competências/CTA — substitui a apresentação "dashboard" pequena da `LevelTimeline` isolada (que continua existindo como peça atômica, ver Component Library).
- `ProcessSteps`: números grandes com baixa opacidade (Playfair), não círculo preenchido pequeno.
- `LiveClassExperience`: lista editorial (rótulo + texto), nunca 5 cards.
- `StudyRhythmCard`: frequência/formato como estrutura, nunca preço inventado.

## 8. Header

76-88px de altura (era ~72px fixo), logo maior, mega menu de "Cursos" em 2 colunas (idiomas + atalhos institucionais) com uma pequena imagem editorial, seletor de idioma textual (sem bandeira remota). Continua **não ativado em produção** — só o componente isolado.

## 9. Footer

Mantido (já era "a parte mais próxima da direção correta" segundo a missão), com mensagem institucional curta adicionada acima da grade de colunas e mais espaço no topo.

## 10. Mobile

Validado com screenshot real (Chrome headless + CDP, ver `12-design-system-visual-qa.md` seção 0) em 390px: foto grande no topo do hero, headline forte, os dois CTAs do hero em botões full-width empilhados, ProofBar em grid 2×2, cards em largura total, menu hambúrguer abaixo de 992px, `LevelJourney` com timeline em faixa de rolagem horizontal intencional.

## 11. Usos proibidos (reforçado nesta fase)

- Foto de banco de imagens apresentada como professor/aluno/aula/plataforma real da Vedium.
- Qualquer pessoa stock usada para "representar" Iorubá pela aparência.
- Preço inventado em qualquer componente de preview.
- Avatar com letra como solução principal de "sem foto de professor".
- Badge/selo decorativo sem dado real por trás.
- Pose publicitária de stock (sorriso encenado, "apontando para o copy space") — ver seção 12 abaixo, é exatamente o que as referências fazem e que a Vedium evita.
- `direction: rtl` como hack de inversão visual (usar `order`).
- Terracota como cor padrão de todo elemento pequeno (eyebrow/badge/label).

## 12. Decisões em relação a Edumon e EduAll

Ambos foram examinados visualmente nesta fase (screenshots reais em `vedium-references/edumon/documentation/assets/images/screenshot.png` e `vedium-references/eduall/documentation/images/output.png`/`output4.png` — referências de leitura, nunca copiadas literalmente, nenhum arquivo dentro de `edumon`/`eduall` foi modificado).

**Extraído como referência de proporção/composição (usado)**:
- Escala do hero: a foto ocupa quase toda a altura do bloco, não uma miniatura — replicado no `HeroSplit` (mídia com `height:100%` no desktop, não `aspect-ratio` fixo pequeno).
- Assimetria leve do split (o texto e a imagem não são forçosamente 50/50 rígido) — o Hero da Vedium usa ~52/48.
- Eyebrow discreto acima de um H1 grande — mantido, mas sem a cor de destaque em todo lugar (ver seção 5).

**Explicitamente descartado (motivo)**:
- **Cards de estatística flutuando sobre a foto do hero** (Edumon: "28k Total Students"/"529+ Total Courses"; EduAll: "36k+ Enrolled Students"/"20% OFF"/"Online Supports") — exatamente o padrão de número-grande-genérico que a missão pediu para remover do `ProofBar`; sobrepor isso à foto do professor real seria pior ainda (mistura prova genérica com identidade real).
- **Avatar stack** ("24k+ Happy Students" com fotos de rosto empilhadas) — implica prova social sem fonte auditável.
- **Doodles decorativos** (seta desenhada à mão, círculo tracejado, ponto rosa, ícones coloridos de contorno) — ruído visual sem função, contrário à direção "sóbria e institucional" pedida.
- **Pose publicitária de stock** (EduAll/AgileTech: mulher sorrindo, apontando para um espaço vazio ao lado) — é literalmente o que `06-photography-system.md` pede para recusar ("sorriso publicitário ou comemoração encenada", "pessoa apontando para copy space sem contexto").
- **Múltiplas cores de destaque simultâneas** (EduAll usa azul + laranja + roxo + rosa na mesma tela) — a Vedium usa uma paleta contida (azul estrutural + terracota raro).
- **Menu com dropdown de categoria + busca + carrinho + login** (visual de e-commerce/marketplace) — o Header v2 da Vedium é enxuto: Logo, Cursos, Como funciona, Professores, Para empresas, Blog, Entrar, 1 CTA.

A Vedium é deliberadamente mais sóbria e institucional que as duas referências — ambas comunicam "plataforma de cursos genérica"; a direção aqui é "escola de idiomas ao vivo, premium sem ostentação".
