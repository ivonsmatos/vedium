# 26 — Home V2 integrada em rota paralela (Fase C)

> **Origem**: com a direção de arte V2 aprovada (Fases 0 a B.6E), esta fase transforma o Presentation Mode em uma Home V2 real, consumindo dados reais do sistema, numa rota paralela não indexável — sem substituir `/`. Regra permanente desta fase: **não redesenhar** nenhuma das áreas já aprovadas (Hero, Pathfinder, VediumMethod, Cursos, Live Class, Progressão, B2B, Conhecimento Vedium, CTA final, Footer) — só integrar dado real, corrigir quebra causada por dado real, e cuidar de acessibilidade/responsividade/performance/integração funcional.

## 1. Rota

**`/_home_v2`** — não `/_home-v2` como a missão sugeria conceitualmente.

**Motivo real (não escolha estética)**: o Frappe converte hífen→underscore ao montar o nome do MÓDULO Python a partir do nome do arquivo `www/<slug>.py`. Um controller cujo arquivo tem hífen no nome nunca roda de verdade (bug silencioso — a página renderiza vazia ou quebra, mascarando a causa). Este exato padrão já foi encontrado e corrigido em ~20 controllers deste app em fase anterior (ver memória do projeto: "Controller www = underscore SEMPRE"). `_home_v2.py`/`.html` evita o problema de origem.

Verificado sem conflito antes de criar: nenhum arquivo/rota `_home-v2`/`_home_v2` existia; nenhuma `website_route_rule` em `hooks.py` reclama esse nome.

## 2. Arquitetura — "não duplicar o HTML inteiro do preview"

Extraído um include compartilhado **`templates/includes/v2/home_body.html`** contendo as 9 seções aprovadas (Hero até Conhecimento Vedium) — consumido tanto por `www/design_system_v2.html` (biblioteca/QA, mantido) quanto por `www/_home_v2.html` (Home V2 real). As duas páginas agora renderizam **exatamente o mesmo corpo**, com os mesmos dados reais — CTA final e Footer ficam fora do include (cada página os chama separadamente), mas usam os mesmos macros já aprovados.

Novo módulo Python **`vedium_core/vedium_core/v2_home_data.py`** (arquivo novo, isolado — não modifica nenhum arquivo de produção compartilhado) concentra a camada de dados reais usada pelos dois controllers:
- `get_insights_selection()` — seleção real de artigos de blog (seção 4).
- `to_insight_macro_dict()` — adaptação de formato pro macro `v2_insights_editorial`.
- `PATHFINDER_MATRIX` — matriz de encaminhamento do Pathfinder (seção 5), espelhada em JS.

## 3. Cursos — por que os 5 blocos continuam curados, não gerados de `get_published_courses()`

Achado real ao investigar: **este ambiente de dev local só tem cursos de Inglês cadastrados no LMS** (`Inglês - Beginner` até `Inglês - Avançado`, mais um `TestPayCourse`) — Iorubá, PLE, Espanhol e Hebraico não existem como registros `LMS Course` aqui. Além disso, mesmo em produção, os 5 blocos-idioma da Home são **copy editorial curada por idioma** (headline/descrição escritas à mão), não uma renderização direta de registro de curso — `LMS Course.category` é por NÍVEL individual ("Inglês - Beginner"), não por idioma agregado; não existe hoje uma função que agregue "todos os cursos de Iorubá" num card único de idioma.

**Decisão desta fase**: manter os 5 blocos com o mesmo texto editorial já aprovado (nenhuma mudança visual), mas:
- Todas as 5 URLs de curso confirmadas reais e HTTP 200 nesta fase (ver `27-home-v2-link-contract.md`).
- Faixa de nível do Inglês ("Do A1 ao C1") confirmada contra a fonte real `course_urls.py` (`ENGLISH_COURSE_LEVELS`): **A1, A2, A2+, B1, B2, C1**. Achado real: a "identidade oficial" citada na missão desta fase menciona "B1+", mas o código real usa **"A2+"** — não existe nível "B1+" no sistema. Documentado aqui como a correção; o texto do card ("Do A1 ao C1", uma faixa, não uma lista) já é compatível com o valor real e não precisou mudar.
- **Gate registrado para fase futura** (não implementado agora, "documentar e parar"): criar uma função de agregação real "cursos por idioma" (com fallback claro quando o idioma não tem curso LMS cadastrado, caso de Iorubá/Espanhol/Hebraico neste ambiente) antes de tentar tornar os 5 blocos 100% dinâmicos.

## 4. Conhecimento Vedium — seleção dinâmica real

`get_insights_selection()`:
1. Tenta `blog_content.list_blog_posts()` (combina posts de código `BLOG_POSTS` + posts publicados pelo painel, doctype "Vedium Blog Post") — comportamento correto e completo em produção.
2. **Achado real**: neste ambiente de dev local, a doctype "Vedium Blog Post" não está migrada (`DoesNotExistError` confirmado via `bench console`) — `list_blog_posts()` falha. Cai então só para `BLOG_POSTS` (97 posts reais de código, não fabricados) via `try/except`. Em produção (doctype presente), a função real roda sem cair no fallback.
3. Filtra `lang == "pt-BR"`, `date`/`url`/`title` válidos (nunca rascunho).
4. Ordena por data decrescente. **Featured** = mais recente. **2 secundários** = próximos mais recentes com **tag diferente** do featured (regra determinística simples de variedade — não é algoritmo de recomendação); se não houver 2 tags diferentes suficientes, completa pelos próximos mais recentes de qualquer tag.

Resultado real (nesta data, 2026-08-26): featured = "Curso de inglês com professor ao vivo..." (Inglês, 2026-07-15); secundários = "Plano de 30 dias para começar iorubá..." (Iorubá, 2026-07-03) e "Como funciona a alfabetização em hebraico do zero" (Hebraico, 2025-04-23) — mesma variedade Inglês/Iorubá/Hebraico que já estava curada manualmente antes, agora derivada de regra real, não hardcode.

URLs resolvidas são as **canônicas com prefixo de categoria** (`/blog/ingles/...`, `/blog/ioruba/...`, `/blog/hebraico/...`) — achado real: o hardcode anterior usava a URL legada sem prefixo (`/blog/como-funciona-a-alfabetizacao-em-hebraico-do-zero`), que ainda funciona via redirect 301, mas não é mais a canônica. `_post_card()` (função real, reaproveitada) já calcula a forma correta — corrigido automaticamente ao trocar pra dado real.

**Achado ambiental, não corrigido (fora do escopo desta fase)**: `/blog` (o índice) retorna HTTP 403 "Not Permitted" neste ambiente de dev local para usuário Guest — investigado, causa raiz é a mesma doctype "Vedium Blog Post" não migrada (o índice tenta uma permissão sobre ela). Isso não afeta a Home V2 (que chama a função Python diretamente, não faz HTTP pro `/blog`), mas é registrado aqui como algo a confirmar em produção antes do rollout (onde a doctype existe e `/blog` deveria responder 200 normalmente, conforme documentado em `content-contracts.md`).

## 5. Pathfinder — matriz de encaminhamento

Sem JS: `<form method="get" action="/teste-de-nivel">` nativo (inalterado) — fallback seguro e universal.

Com JS (`initPathfinderRouting`, novo, em `design-system-v2.js`): intercepta o submit, resolve idioma+objetivo contra `PATHFINDER_MATRIX` (25 combinações, espelhada em Python e JS — ver seção 2), navega pra URL mais específica quando existe, senão cai na página-pilar do idioma. Nenhuma URL inventada — todas validadas HTTP 200/301 nesta fase (ver `27-home-v2-link-contract.md`). Testado de ponta a ponta via CDP: seleção real de rádio → eventos `dataLayer` corretos → navegação real confirmada (`Iorubá` + `Estudos e cultura` → `/ioruba-cultura-e-ancestralidade`).

## 6. Live Class e mídia dos cursos — DEV/PREVIEW vs PRODUCTION MEDIA

Vídeo (E16) e as 5 fotos de curso (E02/E11/E14/E12/E13) continuam sendo **DEV/PREVIEW MEDIA** — derivados locais de stock Envato já aprovado (`21-course-media-selection.md`), servidos de `public/v2-preview-media/` (gitignored, nunca commitado). **Nenhum copiado pra produção nesta fase.** Copy da seção "Aulas ao vivo" já descreve o CONCEITO de aula ao vivo, nunca afirma ser gravação real da Vedium (mantido desde B.6C). Gate permanente: `REAL_VEDIUM_LIVE_CLASS_MEDIA_REQUIRED` — registrado, não bloqueia a integração técnica desta fase.

## 7. O que NÃO foi alterado (áreas congeladas)

Hero, Pathfinder (visual), VediumMethod, Cursos (visual/mídia), Live Class, Progressão, B2B (visual), Conhecimento Vedium (visual), CTA final, Footer — nenhuma mudança de layout/cor/tipografia/animação. Confirmado por hash MD5 do Hero (`1acd805606a5cd559f92969de0437315`, idêntico ao baseline de B.6B/B.6D/B.6E) e por comparação visual com o Presentation Mode (ver `34-pixel-regression` na seção de testes abaixo).

## 8. Testes e verificação

- `pytest` — 330 passed, 11 skipped (piso de 326 mantido).
- `flake8` limpo em `design_system_v2.py`, `_home_v2.py`, `v2_home_data.py`.
- `/_home_v2` → HTTP 200; `/design_system_v2` → HTTP 200 (sem regressão pós-refatoração do include).
- Único `<h1>` em `/_home_v2` (Hero, slide 1) — confirmado.
- Scan de conteúdo: 0 ocorrências de "exemplo/placeholder/lorem/mock/fake/demo" no HTML visível renderizado.
- 0 overflow horizontal em 1440/390px.
- CRLF: 100% nos arquivos modificados/criados.
- `git status --porcelain`: mudanças isoladas a `vedium_core/vedium_core/{public/js/v2,templates/includes/v2,www/design_system_v2*,www/_home_v2*,v2_home_data.py}` e `docs/redesign/*`.

Ver `27-home-v2-link-contract.md` (matriz de links), `28-home-v2-seo-contract.md` (SEO), `29-home-v2-analytics-contract.md` (analytics) e `30-home-v2-rollout-gates.md` (checklist de rollout).
