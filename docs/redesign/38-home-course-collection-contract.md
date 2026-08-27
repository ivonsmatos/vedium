# 38 — Contrato do HomeCourseCollection (Fase C.1.1, Parte B)

## 1. Natureza da coleção — declarado explicitamente

**`HomeCourseCollection` é uma coleção EDITORIAL, curada e versionada em código — não uma agregação dinâmica de catálogo por idioma.** Essa distinção é a exigência central da missão (Parte B, seções 6 e 10) e continua verdadeira nesta fase: o sistema não tem, hoje, uma fonte estruturada de "cursos por idioma" que cubra os 5 idiomas de forma equivalente.

- **Inglês** tem uma fonte estruturada real: `course_urls.py` (`ENGLISH_COURSE_LEVELS`, 6 níveis A1–C1, `ENGLISH_COURSE_NAV_LABELS`, `ENGLISH_COURSE_SEO_TITLES`).
- **Português para Estrangeiros** tem uma trilha estruturada de 3 níveis (`PLE_COURSE_TRACK`, `PLE_COURSE_NAV_I18N`).
- **Iorubá, Espanhol e Hebraico** têm slugs de curso reais em `COURSE_PUBLIC_SLUGS`, mas nenhuma estrutura equivalente de "níveis exibíveis" agregada por idioma (Hebraico em particular não é uma progressão linear — são 5 ofertas distintas: alfabetização, moderno A1, moderno A2-B1, bíblico, particular).

Construir uma agregação dinâmica que cobrisse os 5 de forma uniforme exigiria inventar uma abstração que o resto do sistema não usa — exatamente o que a missão pediu para não fazer ("não criar um sistema excessivamente complexo apenas para dizer que é dinâmico"). A solução adotada, explicitamente permitida pela missão (Parte B, seção 10): **uma única fonte estruturada, testável e versionada, mesmo que o conteúdo dela seja escrito por uma pessoa e não gerado por uma consulta.**

## 2. Onde vive

`vedium_core/vedium_core/home_course_collection.py` — módulo Python novo, isolado (mesmo padrão de `v2_home_data.py`). Duas funções públicas:

- `get_home_course_collection()` — retorna as entradas ativas, ordenadas por `order`, com `media_src` já resolvido (path completo pronto pro template).
- `get_course_index_entries()` — retorna `[{"name", "href"}]` na mesma ordem, para o índice numerado do topo da seção (`v2_course_index_intro`).

Consumida por `templates/includes/v2/home_body.html` (seção 3, "CURSOS") via `context.home_courses`/`context.course_index_entries`, setados tanto em `www/_home_v2.py` quanto em `www/design_system_v2.py` — os dois consumidores desde sempre da mesma fonte real (mesmo padrão já usado para `v2_home_data.get_insights_selection()`).

## 3. Schema (campos reais implementados)

O schema da missão (seção 8) tinha 12 campos mínimos. A implementação real precisou de mais 4 campos de apresentação (`media_alt`, `reverse`, `band_tone`, `object_position`) porque o macro `v2_course_feature` já aprovado (Fase B.6/B.6D) os exige para renderizar sem mudança visual — omiti-los quebraria acessibilidade (alt text) ou mudaria a alternância visual esquerda/direita das seções.

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `slug` | str | sim | Identificador único da entrada (não é o slug de curso do LMS — é o slug da apresentação na Home) |
| `language_key` | str | sim | Chave única do idioma (`ingles`, `ioruba`, `portugues_estrangeiros`, `espanhol`, `hebraico`) |
| `display_name` | str | sim | Nome exibido (também usado como `eyebrow`, ver nota abaixo) |
| `eyebrow` | str | sim | Igual a `display_name` na implementação atual — o macro não distingue os dois hoje; campo mantido separado no schema para permitir divergência futura sem quebrar o contrato |
| `level_summary` | str | sim | Linha de nível/subtítulo (ex. "Do A1 ao C1") |
| `headline` | str | sim | Título de destaque do bloco |
| `description` | str | sim | Parágrafo de apoio |
| `url` | str | sim | Path real do site (validado HTTP 200 desde a Fase C) |
| `cta_label` | str | sim | Texto do link de ação |
| `media_key` | str | sim | Nome do arquivo em `v2-preview-media/` (não o path completo) |
| `media_alt` | str | sim | Texto alternativo real da imagem |
| `order` | int | sim | Posição de exibição (1–5, sequencial, sem furos) |
| `is_active` | bool | sim | Permite desativar uma entrada sem removê-la do código |
| `reverse` | bool | sim | Alternância de layout imagem/texto (visual já aprovado) |
| `band_tone` | str | sim | Tom de fundo da faixa (`white`/`warm`/`alt`) |
| `object_position` | str | sim | CSS `object-position` do crop da imagem |

## 4. Dados oficiais — origem de cada valor

Nenhum copy, URL, nível ou nome de arquivo foi inventado nesta fase. Todos os 5 registros são a migração **byte-a-byte** do que já estava validado desde a Fase C em `templates/includes/v2/home_body.html` (5 chamadas inline de `v2e.v2_course_feature`, ver diff desta fase). Nenhum preço, carga horária, data ou nome de professor aparece na coleção — a Home nunca exibiu esse tipo de dado nestes blocos.

## 5. Testes (`tests/test_pure_home_course_collection.py`)

9 testes novos, sem dependência de Frappe/DB:
- exatamente 5 idiomas ativos;
- todos os campos obrigatórios presentes e não vazios;
- nenhum `language_key`/`slug` duplicado;
- toda `url` é um path absoluto real (não placeholder/lorem/example);
- `order` único e sequencial a partir de 1;
- `get_home_course_collection()` retorna ordenado;
- `media_src` resolvido corretamente a partir de `media_key`;
- `get_course_index_entries()` espelha a coleção;
- o template `home_body.html` de fato consome o loop (não os 5 blocos hardcoded antigos).

## 6. Regressão confirmada

Após a migração, `/design_system_v2` e `/_home_v2` foram recarregados (restart do processo `bench serve`, necessário para módulo Python novo) e o `Content-Length` da resposta ficou **idêntico byte-a-byte** ao medido antes da migração (51.103 bytes em `/_home_v2`) — confirmação de que a mudança de fonte de dado não alterou uma vírgula do HTML renderizado.

## 7. Gate de rollout

`COURSE DATA` = **PASS** — fonte única, testada, sem dado inventado, contrato explícito documentado. O gate de "agregação dinâmica por idioma" (registrado desde a Fase C) continua **não resolvido e fora de escopo** — é uma decisão de produto/arquitetura maior (criar uma fonte estruturada tipo `ENGLISH_COURSE_LEVELS` para os outros 4 idiomas), não um bloqueador para a Home V2 usar curadoria enquanto isso não existe.
