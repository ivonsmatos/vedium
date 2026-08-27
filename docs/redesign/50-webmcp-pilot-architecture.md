# 50 — WebMCP piloto: arquitetura (Fase C.2)

> Implementação local. Nenhum deploy, nenhum origin trial ativado, nenhuma
> mudança em produção nesta fase — ver `docs/redesign/49-*` para o último
> estado confirmado de produção (HEALTHY) e `31-webmcp-agentic-web-roadmap.md`
> para o roadmap original (agora parcialmente implementado por este piloto).
>
> **Fase C.2.2 (verificação real):** teste manual realizado em Chrome com
> `chrome://flags/#enable-webmcp-testing` ativo confirmou:
> `document.modelContext` disponível (`typeof` = `"object"`), 4 tools
> descobertas via `getTools()`, `find_course` e `recommend_learning_path`
> executadas com sucesso via `executeTool()`. Resultados registrados em
> `52-webmcp-test-matrix.md` seção 8. Nenhum origin trial ativado;
> produção não alterada.

## Princípio: progressive enhancement, sem segunda base de dados

```
Frappe/Jinja/HTML/JS
        ↓
   site normal (Home V2)
        ↓
document.modelContext disponível?
        ↓
     SIM / NÃO
      ↓      ↓
 registrar   nada muda —
   tools     site 100% funcional
```

Nenhum link, formulário ou navegação humana depende de WebMCP. Confirmado
via teste automatizado (CDP, sem `document.modelContext` mockado): Home
carrega, Pathfinder resolve corretamente, **zero erros de console** — ver
`52-webmcp-test-matrix.md`.

## Course data service — fonte única

A missão explicitamente proíbe uma segunda base de dados WebMCP em
paralelo à Home. A solução adotada:

```
vedium_core/webmcp_course_data.py  (Python, roda no servidor)
        │
        │  reutiliza (nunca duplica):
        │    - home_course_collection.get_home_course_collection()
        │    - course_urls.py (ENGLISH_COURSE_LEVELS, PLE_COURSE_TRACK,
        │      get_course_level_destination — a MESMA lógica que gera a
        │      navegação real em curso.html)
        │    - catalog_registry.CATALOG (só o campo `title`, nunca preço)
        │    - v2_home_data.PATHFINDER_MATRIX (idêntico, não recriado)
        ▼
get_webmcp_course_data() → dict serializável
        │
        │  v2_home_data.build_home_v2_context() (já compartilhada por
        │  `/` e `/_home_v2` desde a Fase C.1.4) adiciona:
        │  context.webmcp_course_data_json = frappe.as_json(...)
        ▼
templates/includes/v2/home_page_content.html
        │
        │  <script type="application/json" id="vedium-webmcp-course-data">
        │  (inerte — nunca executado, só um data island)
        ▼
   ┌────────────────────┬─────────────────────┐
   ▼                    ▼                     
design-system-v2.js   webmcp.js
(Pathfinder humano,    (as 4 tools —
sempre carregado)      só roda se
window.VediumPathfinder document.modelContext
.resolve(lang, goal)   existir)
   │                    │
   └──── MESMA função ──┘
      (recommend_learning_path chama
       window.VediumPathfinder.resolve)
```

Efeito colateral desta fase: o antigo espelho hardcoded de
`PATHFINDER_MATRIX` que existia dentro de `design-system-v2.js` (duplicado
manualmente do Python desde a Fase C, com um comentário avisando "qualquer
mudança na matriz real precisa ser replicada nos dois lugares") **foi
removido**. Agora há uma única declaração da matriz (Python,
`v2_home_data.PATHFINDER_MATRIX`), servida ao navegador via o data island.
Isso não é só limpeza — é o que a missão pede explicitamente na seção 7
("Pathfinder humano e recommend_learning_path WebMCP devem usar a MESMA
função de resolução... Não duplicar regras").

## Por que um `<script type="application/json">` e não uma chamada de API

Alternativas descartadas:

- **Segunda estrutura JS hardcoded** (como o antigo `PATHFINDER_MATRIX`
  mirror): exatamente o padrão de duplicação que a missão pede pra
  eliminar.
- **Endpoint REST/whitelisted chamado via `fetch()` a cada `execute()`**:
  adiciona round-trip de rede a toda chamada de tool (contra a seção 27,
  "módulo pequeno... custo praticamente nulo"), e um servidor MCP
  tradicional não é o que a missão pede (seção 27: "WebMCP ≠ MCP Server
  tradicional").

Um data island renderizado pelo MESMO request que já monta a Home
(zero I/O extra, zero dependência nova) e lido de forma síncrona tanto
pelo Pathfinder quanto pelas tools resolve os dois problemas.

## Escopo desta fase (4 tools, somente leitura)

`find_course`, `recommend_learning_path`, `get_course_information`,
`get_levels` — todas `readOnlyHint: true`, nenhuma escreve banco, cria
lead, envia mensagem ou inicia pagamento. Contratos completos em
`51-webmcp-tool-contracts.md`.

Explicitamente fora de escopo (seção 31 da missão): `payment`, `checkout`,
`subscribe`, `enroll`, `send_whatsapp`, `create_lead`, `schedule_class`,
`cancel_subscription`, `update_profile`.

## Onde está registrado

Só nas rotas que renderizam `home_page_content.html`: `/` (Home real,
pt-BR) e `/_home_v2` (rota técnica noindex). Nenhuma outra página
(catálogo, páginas de curso, locales en/es/de/fr/ru) ganhou WebMCP nesta
fase — não pedido pela missão ("NÃO iniciar páginas internas").

## Locale

Section 19 da missão separa "idioma do curso" (o que a tool retorna) de
"locale do site" (em que idioma a página está). Nesta fase, o piloto só
está registrado na Home pt-BR — todo texto de conteúdo retornado
(`summary`, `next_step`, `explanation`) é pt-BR, o mesmo idioma da página
que o serve. Mensagens de erro (`error`) são em inglês, seguindo a
convenção do próprio exemplo da missão (seção 22) e o fato de o consumidor
típico de uma tool WebMCP ser um agente, não um leitor humano da página.
Se uma página em outro locale (en/es/de/fr/ru) ganhar WebMCP no futuro,
o texto de conteúdo deve seguir o locale daquela página — arquitetura já
preparada (o data island é montado por request, então uma versão
localizada só precisa trocar os textos-fonte), mas não implementada agora
(não pedida).

## Origin trial

Nenhum token de origin trial foi adicionado (seção 23 da missão, "NÃO
adicionar token de origin trial automaticamente nesta fase"). Duas
possibilidades documentadas para o futuro:

- **A.** Rodar apenas em browsers/ambientes de teste com suporte nativo
  (ex.: Chrome com a flag experimental, ou uma futura versão estável).
- **B.** Requisitar um origin trial token pro domínio `vediums.com`
  quando/se a Vedium decidir formalmente expor isso a agentes reais em
  produção — decisão de negócio, não técnica, pendente de aprovação
  separada.

## Arquivos

| Arquivo | Papel |
|---|---|
| `vedium_core/vedium_core/webmcp_course_data.py` | Course data service (novo) |
| `vedium_core/vedium_core/v2_home_data.py` | `build_home_v2_context()` agora também popula `webmcp_course_data_json` |
| `vedium_core/vedium_core/templates/includes/v2/home_page_content.html` | Data island + `<script defer src=".../webmcp.js">` |
| `vedium_core/vedium_core/public/js/v2/design-system-v2.js` | Pathfinder lê o data island em vez de matriz hardcoded; expõe `window.VediumPathfinder.resolve` |
| `vedium_core/vedium_core/public/js/v2/webmcp.js` | As 4 tools (novo, isolado) |
| `vedium_core/vedium_core/tests/test_pure_webmcp_course_data.py` | Testes puros do data service (novo) |
| `vedium_core/vedium_core/tests/test_pure_home_v2.py` | Teste de paridade Python/JS atualizado (a duplicação que ele checava deixou de existir por design) |
