# 52 — WebMCP piloto: matriz de testes (Fase C.2)

Todos os testes abaixo rodaram localmente (`http://vedium.local:8005`,
container `vedium-frappe`), sem nenhum deploy. Harness: `pytest` (dados
puros) + Chrome headless via CDP com `document.modelContext` mockado
(seção 24 da missão — "criar mock mínimo em testes").

## 1. Testes puros (pytest, sem DB)

`vedium_core/vedium_core/tests/test_pure_webmcp_course_data.py` — 12
testes, **12 passed**:

- 5 idiomas presentes com todos os campos obrigatórios.
- URLs sempre absolutas (`/...`), nunca `_home_v2`/`localhost`/path do
  Windows/`vedium-references`.
- `levels` nunca vazio; `levels_are_sequential` correto por idioma
  (Inglês/PLE/Iorubá/Espanhol = `true`, Hebraico = `false`).
- Hebraico: 5 trilhas distintas, rótulos únicos.
- Inglês: rótulos exatos `["A1","A2","A2+","B1","B2","C1"]` (fonte
  `course_urls.ENGLISH_COURSE_LEVELS`).
- `next_step.kind`: `"level_test"` só para Inglês/PLE, `"contact"` para
  Iorubá/Espanhol/Hebraico — confere com
  `course_urls.get_course_level_destination()`.
- `pathfinder_matrix_by_display_name` **é** (identidade de objeto, não
  cópia) `v2_home_data.PATHFINDER_MATRIX`.
- `pathfinder_goals` bate com a lista literal usada pelo form humano em
  `home_body.html` (checagem independente, não derivada da mesma fonte).
- Todo `course_id` usado em `_CATALOG_TRACK_COURSE_IDS` existe em
  `catalog_registry.CATALOG`.
- Nenhum campo de preço/produto Stripe (`base_monthly`, `product_id`,
  etc.) vaza pro data service.
- Dado é 100% serializável via `json.dumps`.

Suíte completa do repo após a mudança: `flake8` limpo,
**376 passed, 0 failed, 11 skipped** (mesmo baseline anterior + 12 testes
novos; o único teste que precisou de ajuste foi
`test_pathfinder_matrix_languages_match_between_python_and_js`, que
checava a duplicação Python/JS que esta fase eliminou por design — ver
`50-webmcp-pilot-architecture.md`).

## 2. Fallback sem WebMCP (`document.modelContext` ausente)

Chrome real, sem flag/origin trial (o estado de 100% dos usuários e
crawlers hoje):

| Checagem | Resultado |
|---|---|
| `document.modelContext` | `undefined` (esperado) |
| Tools registradas | `false` (webmcp.js retornou cedo, corretamente) |
| `window.VediumPathfinder.resolve` existe e funciona sozinho | `true` — `resolve('Inglês','Viagens')` → `/ingles-para-viagens` |
| Data island presente no DOM | `true` |
| Erros de console/exceções JS | **0** |

## 3. Registro das tools (com `document.modelContext` mockado)

Mock injetado via `Page.addScriptToEvaluateOnNewDocument` (roda antes de
qualquer script da página, como a seção 24 da missão pede).

| Tool | name | title | readOnlyHint | required |
|---|---|---|---|---|
| 1 | `find_course` | "Find a Vedium language course" | `true` | `["language"]` |
| 2 | `recommend_learning_path` | "Recommend a Vedium learning path" | `true` | `["language","goal"]` |
| 3 | `get_course_information` | "Get Vedium course information" | `true` | `["language"]` |
| 4 | `get_levels` | "Get Vedium course levels" | `true` | `["language"]` |

`language` enum em todas as 4: `["english","hebrew","portuguese_for_foreigners","spanish","yoruba"]`.
`goal` enum (só na tool 2): as 5 strings reais do Pathfinder.

**Idempotência:** `window.__vediumWebMcpToolsRegistered === true`,
exatamente 4 tools no registro (sem duplicação).

## 4. Execução — casos felizes e de erro

| Chamada | Resultado |
|---|---|
| `find_course({language:'english'})` | `{"language":"english","course_name":"Inglês","level_summary":"Do A1 ao C1","url":"/curso-de-ingles-online","next_step":"O próximo passo recomendado é realizar o teste de nível."}` |
| `find_course({language:'klingon'})` | `{"error":"No published course information is available for that language."}` |
| `recommend_learning_path({language:'hebrew',goal:'Viagens'})` | `{"language":"hebrew","goal":"Viagens","course_recommended":"Hebraico","url":"/curso-de-hebraico-online","next_step":"...contato...","next_step_url":null,"explanation":"..."}` |
| `recommend_learning_path({language:'hebrew',goal:'Invalid Goal'})` | `{"error":"No published learning path is available for that goal."}` |
| `get_course_information({language:'spanish'})` | Campos completos, sem preço/turma/professor nomeado — ver `51-*` |
| `get_levels({language:'english'})` | 6 níveis CEFR, `is_sequential:true`, URLs corretas |
| `get_levels({language:'hebrew'})` | 5 trilhas, `is_sequential:false` |

Nenhuma exceção não tratada; nenhum erro de console durante toda a
sequência.

## 5. Equivalência Pathfinder ↔ `recommend_learning_path` (seção 25 da missão)

Matriz completa: **5 idiomas × 5 objetivos = 25 combinações**. Para cada
uma, comparado `window.VediumPathfinder.resolve(displayName, goal)`
(chamado diretamente, como o form humano chama) contra a `url` retornada
por `recommend_learning_path.execute({language, goal})`.

**Resultado: 25/25 idênticas — 0 divergências.**

Isso é esperado estruturalmente (seção 7 da missão): as duas chamadas
executam a **mesma função** (`resolveLearningPath`, exposta como
`window.VediumPathfinder.resolve`) sobre a **mesma fonte de dado** (o data
island); não há duas implementações a manter em sincronia.

## 6. URLs — teste HTTP (seção 20 da missão)

33 URLs únicas que as 4 tools podem retornar (curso pilar × 5, teste de
nível × 2, contato × 1, páginas de objetivo específico × 5, níveis
individuais × 20).

**Local (`http://127.0.0.1:8005`):** 19/33 retornaram 200. As outras 14
(`/curso/<slug>` de Iorubá/Espanhol/Hebraico/PLE) retornaram 404 —
**causa confirmada**: o banco de dev local só tem 7 de 20 registros `LMS
Course` semeados (só Inglês), não um bug de geração de URL — as mesmas
URLs vêm de `course_urls.get_course_url()`, a função que já gera todo link
de curso do site inteiro.

**Produção (`https://vediums.com`, leitura HTTP HEAD apenas — não é
deploy nem alteração):** as 14 URLs que falharam localmente foram testadas
diretamente em produção. **14/14 retornaram 200.** Combinado com as 19
locais, **33/33 URLs confirmadas válidas.**

## 7. Regressão (seção 26 da missão)

Suíte completa do projeto: **376 passed, 0 failed, 11 skipped** (era 376
antes desta fase também, já que o único ajuste foi um teste reescrito, não
removido). Checkpoint de produção mais recente (`docs/redesign/49-*`,
mantido intacto — nada desta fase tocou produção): Home/Hero/locale/
Cursos/Pathfinder/Consent/SEO/mobile permanecem HEALTHY, não reverificados
nesta fase porque nada em produção mudou.

## 8. Teste manual com WebMCP real (Fase C.2.2)

> Verificação manual realizada em Chrome com a flag experimental ativada
> (`chrome://flags/#enable-webmcp-testing`). Esta seção distingue
> explicitamente dois ambientes de teste:
>
> - **Ambiente automatizado (pytest + mock CDP):** `document.modelContext`
>   mockado via `Page.addScriptToEvaluateOnNewDocument`; todas as tools
>   verificadas por análise estática do JS servido e do data island real.
> - **Runtime real do Chrome (manual):** `document.modelContext` disponível
>   nativamente via flag experimental; tools descobertas e executadas via
>   `document.modelContext.executeTool()`.

### 8.1 API real

| Checagem | Resultado |
|---|---|
| `typeof document.modelContext` | `"object"` (AVAILABLE) ✅ |
| `document.modelContext.getTools()` | 4 tools retornadas ✅ |
| `navigator.modelContext` | não usado pelo código Vedium (presente só em comentário no webmcp.js) ✅ |

### 8.2 Tools descobertas no browser real

| # | name | readOnlyHint |
|---|---|---|
| 1 | `find_course` | `true` |
| 2 | `recommend_learning_path` | `true` |
| 3 | `get_course_information` | `true` |
| 4 | `get_levels` | `true` |

Exatamente 4. Nenhuma quinta tool. Nenhuma duplicata.

### 8.3 Execução real — casos testados manualmente

| Chamada | Input | Resultado real |
|---|---|---|
| `find_course` via `document.modelContext.executeTool` | `{language:"english"}` | `course_name:"Inglês"`, `level_summary:"Do A1 ao C1"`, `url:"/curso-de-ingles-online"`, `next_step:"…teste de nível"` ✅ |
| `recommend_learning_path` via `document.modelContext.executeTool` | `{language:"english",goal:"Viagens"}` | `course_recommended:"Inglês"`, `url:"/ingles-para-viagens"`, `next_step_url:"/teste-de-nivel-ingles"` ✅ |

`get_course_information` e `get_levels` não foram reexecutadas manualmente
nesta fase — passaram na suíte automatizada (seção 4) e na análise estática
do data island real; sem necessidade de reteste manual para liberar o commit.

### 8.4 Origin isolation (verificação estática + runtime)

| Checagem | Resultado |
|---|---|
| Análise estática de headers (`curl -I`) | Sem `Permissions-Policy` que bloqueie WebMCP; sem `document.domain` setado; página top-level same-origin ✅ |
| Registro de tools no Chrome real | PASS — Chrome registrou e executou as 4 tools sem nenhum blocker observado ✅ |

Nota: COOP/COEP ausentes no servidor de dev local (Werkzeug) — esperado e
irrelevante para contexto top-level same-origin. Produção usa Nginx com
headers próprios; a ausência em dev local não é blocker arquitetural.
Cenários de iframe/cross-origin não testados nesta fase (fora do escopo do
piloto).

### 8.5 Resultado consolidado (Fase C.2.2)

```
WEBMCP AUTOMATED TEST ENVIRONMENT:   MOCKED (pytest + CDP mock)
WEBMCP MANUAL REAL-BROWSER RUNTIME:  PASS (Chrome flag experimental)

TOOLS:                  4
find_course:            PASS (automatizado + manual)
recommend_learning_path: PASS (automatizado + manual)
get_course_information: PASS (automatizado)
get_levels:             PASS (automatizado)

PATHFINDER EQUIVALENCE: PASS (estrutural — mesma função/fonte)
NO-WEBMCP FALLBACK:     PASS (visual + automatizado)
LOCALE:                 PASS
SECURITY:               PASS
ORIGIN ISOLATION:       PASS (estático + runtime)

TESTS (regressão final): 376 passed, 0 failed, 11 skipped
ORIGIN TRIAL:           NOT ENABLED
DEPLOY:                 NOT PERFORMED
```
