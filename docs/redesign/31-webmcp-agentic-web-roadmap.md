# 31 — WebMCP / Agentic Web: roadmap (Fase C.2, NÃO implementada)

> **Registro oficial, não implementação.** Esta fase (C.1) só documenta o escopo futuro, por instrução explícita da missão. Nenhum código WebMCP foi escrito. Nenhuma dependência nova foi adicionada ao projeto.

## O que é

WebMCP é a extensão do padrão MCP (Model Context Protocol) para o navegador — permite que um site exponha "ferramentas" (tools) que agentes de IA (assistentes, navegadores agentic) podem chamar diretamente, em vez de só rastrear/interpretar HTML. Para a Vedium, isso significaria um agente conseguir perguntar "quais cursos de inglês vocês têm?" e receber uma resposta estruturada, sem precisar fazer scraping da página.

## Por que registrar agora, sem implementar

A Home V2 já estabelece a base de dados reais (catálogo de cursos, blog, Pathfinder) que uma futura camada WebMCP consumiria — faz sentido registrar o roadmap agora, enquanto o contexto está fresco, mesmo sem implementar nada.

## Escopo inicial proposto (Fase C.2, futura)

| Ferramenta | Função | Fonte de dado real já existente |
|---|---|---|
| `find_course` | Buscar curso por idioma/nível/objetivo | `vedium_core.courses.get_published_courses()` |
| `recommend_learning_path` | Sugerir trilha conforme idioma+objetivo | Mesma lógica do Pathfinder (`v2_home_data.PATHFINDER_MATRIX`), generalizada |
| `get_course_information` | Detalhes de um curso específico | `LMS Course` (via `courses.py`), `course_urls.py` |
| `get_levels` | Níveis/trilha de um idioma | `course_urls.py` (`ENGLISH_COURSE_LEVELS` etc. — hoje só Inglês tem essa estrutura, ver `26-home-v2-integration.md` seção 3) |
| `search_content` | Buscar artigos do blog | `blog_content.list_blog_posts()` (mesma função já usada por `v2_home_data.py`) |
| `get_b2b_information` | Informação institucional B2B | Conteúdo estático de `/empresas` + `v2_b2b_home_feature` |
| `switch_locale` | Trocar idioma da interface | Mesmo contrato de `data-vd-nav-urls`/`vedium-language.js` (ver `25-locale-switcher-contract.md`) |
| `start_level_test` | Iniciar teste de nível | `/teste-de-nivel` (fora do escopo de dado estruturado — é um formulário interativo) |
| `contact_vedium` | Abrir canal de contato | `/contato`, WhatsApp real |

## Excluído da primeira versão (decisão de segurança, não técnica)

- **Pagamento** — nenhuma ferramenta que inicie ou complete cobrança (Stripe).
- **Assinatura** — nenhuma ferramenta que crie/altere assinatura.
- **Matrícula financeira** — nenhuma ferramenta que efetive matrícula paga.
- **Ações destrutivas** — nenhuma ferramenta que apague/cancele dado real (cancelamento de curso, exclusão de conta, etc.).

Justificativa: um agente pode ERRAR de um jeito que um humano não erraria (mal-entendido de intenção, alucinação de parâmetro) — expor ações financeiras/destrutivas a chamadas automatizadas antes de o padrão amadurecer é risco desproporcional ao benefício desta primeira versão.

## Arquitetura: progressive enhancement

Mesmo princípio já usado em toda a V2 (Pathfinder sem JS funciona, carousel sem JS mostra slide 1, etc.): **o site precisa continuar 100% funcional sem suporte a WebMCP** — a camada WebMCP é aditiva, nunca uma dependência. Um navegador/agente sem suporte não perde nenhuma funcionalidade humana existente.

## Pré-requisitos antes de qualquer implementação real

1. Estabilizar a Home V2 (esta fase) e decidir rollout.
2. Resolver o gate de "HomeCourseCollection = CURATED" (`26-home-v2-integration.md` seção 3) — uma ferramenta `find_course` real precisa de uma fonte de dado agregada por idioma que hoje não existe.
3. Avaliar biblioteca/SDK WebMCP madura o suficiente (o padrão ainda está em evolução no momento desta fase).
4. Definir rate limiting / auth para as ferramentas (evitar abuso).

Nenhum destes 4 itens está resolvido ou agendado nesta fase — ficam registrados como pré-condição da futura Fase C.2.
