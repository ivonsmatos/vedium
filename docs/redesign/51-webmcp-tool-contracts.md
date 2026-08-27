# 51 — WebMCP piloto: contratos das 4 tools (Fase C.2)

API real usada: `document.modelContext.registerTool(config)` (Chrome,
flag experimental, `document.modelContext` — não `navigator.modelContext`,
depreciada). Verificado nesta fase contra a documentação oficial:
[Imperative API](https://developer.chrome.com/docs/ai/webmcp/imperative-api),
[Tool security](https://developer.chrome.com/docs/ai/webmcp/secure-tools).

> **Fase C.2.2 — confirmação de runtime real:** contratos executados no
> Chrome com `chrome://flags/#enable-webmcp-testing` ativo. `find_course`
> e `recommend_learning_path` executadas via `document.modelContext.executeTool()`
> com resultados conformes aos contratos abaixo. `get_course_information` e
> `get_levels` passaram na suíte automatizada; não reexecutadas manualmente
> (sem blocker para o commit). Ver `52-webmcp-test-matrix.md` seção 8.

## Decisão de contrato: `execute` retorna STRING

A documentação oficial confirma: `execute` é `async` e **retorna uma
string** (ou `null` em navegação) — não um objeto estruturado livre. Por
isso as 4 tools deste piloto retornam `JSON.stringify(...)` de uma
estrutura pequena e factual (seção 14 da missão: "Preferir objeto
estruturado quando API/consumer suportar adequadamente... Caso o contrato
atual exija texto: usar texto determinístico e conciso. Documentar
decisão." — esta é a decisão documentada).

## Decisão de contrato: erros retornam STRING JSON, não `throw`

A documentação oficial não especifica o contrato de erro de
`registerTool` (verificado nesta fase — ver `50-webmcp-pilot-architecture.md`
e a pesquisa feita antes da implementação). Optamos por **nunca lançar
exceção** dentro de `execute`: entradas inválidas ou dado indisponível
retornam `JSON.stringify({error: "..."})`, sempre uma string parseável.
Isso evita depender de um comportamento de captura de erro não documentado
e evita expor stack trace ao agente (seção 22 da missão). Mensagens de
erro são em inglês (ver `50-*`, seção "Locale").

## Anotações

Todas as 4 tools: `annotations: { readOnlyHint: true }` — nenhuma escreve
banco, cria lead, envia mensagem, matricula ou inicia pagamento (seção 15
da missão).

## AbortController

Não usado neste piloto. As 4 tools são lookups síncronos (leitura de um
objeto JS já carregado, sem I/O de rede) — não há trabalho cancelável, e
os tools vivem pelo tempo de vida da página (não há gatilho de
desregistro nesta fase). Se uma tool futura fizer I/O de rede (fora do
escopo deste piloto), `AbortController`/`signal` deve ser reavaliado.

---

## 1. `find_course`

| | |
|---|---|
| **Objetivo** | Encontrar o curso publicado de um idioma. |
| **Input** | `{ language: enum }` |
| **Enum de idioma** | `english`, `yoruba`, `portuguese_for_foreigners`, `spanish`, `hebrew` |
| **Fonte de dado** | `webmcp_course_data.py` → `HomeCourseCollection` |
| **Efeito colateral** | Nenhum (read-only) |
| **Locale** | Conteúdo em pt-BR (mesmo locale da página) |

**Output (sucesso):**
```json
{
  "language": "yoruba",
  "course_name": "Iorubá",
  "level_summary": "Básico ao avançado",
  "url": "/curso-de-ioruba-online",
  "next_step": "O próximo passo recomendado é entrar em contato para uma avaliação inicial."
}
```

**Output (erro — idioma inválido):**
```json
{"error": "No published course information is available for that language."}
```

**Não inclui:** preço, turma, professor, disponibilidade (seção 5 da
missão, "Não inventar preço/turma/professor/disponibilidade").

---

## 2. `recommend_learning_path`

| | |
|---|---|
| **Objetivo** | Versão agentic do Pathfinder — recomenda curso+URL a partir de idioma+objetivo. |
| **Input** | `{ language: enum, goal: enum }` |
| **Enum de objetivo** | Derivado em runtime das chaves reais de `PATHFINDER_MATRIX` (nunca uma lista nova) — hoje: `"Trabalho e carreira"`, `"Comunicação cotidiana"`, `"Viagens"`, `"Estudos e cultura"`, `"Viver e trabalhar no Brasil"` |
| **Fonte de dado** | `window.VediumPathfinder.resolve(displayName, goal)` — **a mesma função** que o Pathfinder humano chama |
| **Equivalência** | Testada para as 25 combinações (5×5) — ver `52-webmcp-test-matrix.md`, 0 divergências |

**Output (sucesso):**
```json
{
  "language": "hebrew",
  "goal": "Viagens",
  "course_recommended": "Hebraico",
  "url": "/curso-de-hebraico-online",
  "next_step": "O próximo passo recomendado é entrar em contato para uma avaliação inicial.",
  "next_step_url": null,
  "explanation": "Curso e percurso indicados a partir do idioma e do objetivo informados; não substitui uma avaliação de nível."
}
```

`next_step_url` só é preenchido quando o próximo passo é um teste de nível
self-service (`next_step_url` = URL do teste); quando o próximo passo é
contato, fica `null` (o `url` do curso já é o destino relevante).

**Output (erro — objetivo inválido):**
```json
{"error": "No published learning path is available for that goal."}
```

**Nunca afirma** "este é definitivamente seu nível" (proibido pela missão,
seção 6) — a `explanation` é deliberadamente qualificada.

---

## 3. `get_course_information`

| | |
|---|---|
| **Objetivo** | Detalhes factuais e já publicados de um curso. |
| **Input** | `{ language: enum }` |
| **Fonte de dado** | `HomeCourseCollection.description`/`level_summary` (copy já aprovado, o mesmo exibido na Home) |

**Output (sucesso):**
```json
{
  "course_name": "Espanhol",
  "language": "spanish",
  "summary": "Espanhol para quem quer sair do português misturado com espanhol e comunicar com clareza e confiança.",
  "level_summary": "Comunicação com precisão",
  "delivery_mode": "Aulas ao vivo, online, com professor.",
  "teacher_profile": "Professores nativos e/ou especialistas, conforme o idioma.",
  "progression": "Comunicação com precisão",
  "url": "/curso-de-espanhol-online"
}
```

`delivery_mode` e `teacher_profile` reutilizam copy institucional já
aprovado e exibido globalmente na Home ("Aprenda ao vivo... Professores
nativos e especialistas, aulas em tempo real e progressão organizada por
nível" — Hero da Home V2) — não são um dado novo por curso, são a mesma
afirmação sitewide já publicada. **Não inclui** fluência, prazo,
disponibilidade ou resultado garantido (seção 8 da missão).

---

## 4. `get_levels`

| | |
|---|---|
| **Objetivo** | Níveis ou trilhas reais publicadas de um idioma. |
| **Input** | `{ language: enum }` |
| **Fonte de dado** | Inglês/PLE: `course_urls.py` (`ENGLISH_COURSE_LEVELS`, `PLE_COURSE_TRACK` — a mesma estrutura que gera a navegação real em `curso.html`). Iorubá/Espanhol/Hebraico: `catalog_registry.CATALOG` (campo `title`, único dado reaproveitado desse catálogo — nunca preço). |

**Output — Inglês (trilha sequencial CEFR):**
```json
{
  "language": "english",
  "is_sequential": true,
  "levels": [
    {"label": "A1", "url": "/curso/ingles-basico-a1"},
    {"label": "A2", "url": "/curso/ingles-elementar-a2"},
    {"label": "A2+", "url": "/curso/ingles-pre-intermediario"},
    {"label": "B1", "url": "/curso/ingles-intermediario-b1"},
    {"label": "B2", "url": "/curso/ingles-intermediario-superior-b2"},
    {"label": "C1", "url": "/curso/ingles-avancado-c1"}
  ]
}
```

**Output — Hebraico (trilhas distintas, NÃO sequenciais):**
```json
{
  "language": "hebrew",
  "is_sequential": false,
  "levels": [
    {"label": "Hebraico A0", "url": "/curso/hebraico-a0-alfabetizacao"},
    {"label": "Hebraico Moderno A1", "url": "/curso/hebraico-moderno-a1"},
    {"label": "Hebraico Moderno A2/B1", "url": "/curso/hebraico-moderno-a2-b1"},
    {"label": "Hebraico Bíblico", "url": "/curso/hebraico-biblico-leitura-guiada"},
    {"label": "Hebraico Particular", "url": "/curso/hebraico-particular"}
  ]
}
```

`is_sequential: false` existe especificamente porque o Hebraico não segue
CEFR — são 5 produtos distintos (Alfabetização, Moderno A1, Moderno A2/B1,
Bíblico, Particular), confirmado no código (`course_urls.get_course_navigation()`
docstring: "Hebrew includes different products... need their own approved
labels before they can safely share this pattern"). A tool nunca infere
uma ordem de pré-requisito que não existe (seção 9 da missão, "Não
inferir CEFR onde não for aplicável").

**Achado real desta fase:** `course_urls.py` (`ENGLISH_COURSE_LEVELS`) e
`catalog_registry.py` (`CATALOG[...]["title"]`) **discordam** sobre o
rótulo de 2 níveis de Inglês — `course_urls.py` chama
`ingl-s-pr-intermedi-rio`/`ingl-s-intermedi-rio` de "A2+"/"B1", enquanto
`catalog_registry.py` (dicionário comercial/Stripe) os chama de
"B1"/"B1+". Esta tool usa **exclusivamente `course_urls.py`** para os
rótulos de nível de Inglês, porque é a mesma fonte que já gera a
navegação real (anterior/próximo) mostrada nas páginas de curso — não
`catalog_registry.py`, que é um dicionário comercial (nomeação de produto
Stripe), não uma fonte de nomenclatura pedagógica. Divergência
pré-existente, não introduzida por este piloto; registrada aqui por
transparência (seção 9 da missão: "Não confiar apenas em
memória/documentação antiga. Verificar no código/config atual antes.").
