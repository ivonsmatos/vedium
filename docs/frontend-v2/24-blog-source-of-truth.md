# 24 — Blog: Current Source of Truth (auditoria real, antes de migrar)

Auditoria feita ANTES de construir qualquer arquitetura nova (missão F.5
seções 2-4), lendo código-fonte real e testando URLs reais por HTTP.
Nada aqui foi assumido.

## 1. Duas fontes de posts (confirmado por código)

`vedium_core/vedium_core/blog_content.py` (docstring literal, linhas
1-18) confirma explicitamente que **existem duas fontes**, ambas
renderizadas pelo mesmo template (`templates/includes/blog_post.html`):

1. **`BLOG_POSTS`** (dict Python, este arquivo): 97 artigos "de código",
   editados via commit/deploy. É de onde vem o conteúdo migrado nesta
   fase.
2. **DocType `Vedium Blog Post`** (`vedium_core/vedium_core/vedium_core/
   doctype/vedium_blog_post/vedium_blog_post.json`): posts publicados
   direto pelo Frappe Desk, sem deploy. **Não verificado nesta sessão**
   se há registros reais nele hoje (exigiria acesso ao Frappe
   Desk/banco, não disponível neste ambiente) — gap explícito para a
   próxima sessão confirmar antes do cutover.

`www/blog_post.py` (lido nesta sessão) resolve cada URL chamando
`get_blog_post_any(slug)`, que checa o DocType primeiro e cai no dict
depois — confirmado por leitura direta do código, não pela docstring.

**Implicação para o Next**: a arquitetura nova (`src/content/blog/`)
espelha hoje só a fonte 1 (dict). Antes de qualquer migração em lote
futura, alguém precisa confirmar quantos posts (se algum) existem só no
DocType, ou eles ficarão de fora do inventário.

## 2. Padrão real de URL (testado por HTTP, não assumido)

`www/blog_post.py` (linhas 33-77) mostra a regra exata: um artigo só
responde na URL que o próprio dict declara como `post["url"]`. Se a URL
pedida for diferente, o Frappe redireciona (301 implícito via
`frappe.Redirect`) para a canônica.

Testado nesta sessão com vários artigos reais:

| Artigo (exemplo) | `/blog/<slug>` (sem categoria) | `/blog/<categoria>/<slug>` |
|---|---|---|
| `alfabeto-ioruba` (sem campo `category` no dict) | 200, fica assim (é a canônica) | não existe |
| `hebraico-moderno-x-hebraico-biblico-entenda-a-diferenca` (tem `category: "hebraico"`) | 200, mas **redireciona** para a categorizada | 200, é a canônica |
| `aula-de-ingles-online-ao-vivo-...` (tem `category: "ingles"`) | 200, redireciona | 200, é a canônica |
| PLE em inglês (`brazilian-portuguese-for-expats-...`) | 200, redireciona | fica em **`/en/blog/brazilian-portuguese/<slug>`** (prefixo de idioma, não `/blog/`) |
| PLE em francês (`portugais-bresilien-pour-expatries-...`) | 200, fica assim (**sem prefixo `/fr/`** — ver seção 4) | `/fr/blog/...` dá erro de conexão, não existe |

**Conclusão real**: não existe UM padrão de URL único. Existem 3
formatos legítimos e simultâneos, cada um determinado pelo que o
próprio registro do artigo declara:

1. `/blog/<slug>` — artigos sem campo `category` no dict (a maioria dos
   mais antigos, e também os 4 mais recentes de Iorubá adicionados no
   topo do arquivo, que ainda não receberam `category`).
2. `/blog/<categoria>/<slug>` — artigos com `category` setado (o padrão
   também usado no plano de 44 artigos futuros da planilha SEO/GEO v3).
3. `/<lang>/blog/<categoria>/<slug>` — só para PLE em inglês e espanhol
   hoje (`LANG_BLOG_PREFIXES = ("en", "es")` em `blog_post.py`).

Isso está refletido em `27-blog-url-migration-map.csv`: cada linha usa a
URL real de cada artigo, não um padrão forçado.

## 3. Rota Next construída nesta fase

`app/blog/[category]/[slug]/page.tsx` cobre o formato 2 (o do artigo
migrado como prova de conceito). Os formatos 1 e 3 **não foram
construídos nesta fase** por não terem nenhum conteúdo real migrado
ainda que precise deles (evita rota morta sem conteúdo, mesma disciplina
de "não adicionar abstração sem necessidade" já seguida o projeto
inteiro) — ver `26-blog-cadence-and-dates.md` para o que falta.

## 4. Achado: fr/de/ru/zh têm conteúdo real mas rota de prefixo ausente

`blog_post.py` linha 15 diz literalmente: `LANG_BLOG_PREFIXES = ("en",
"es")` com o comentário "hoje só en/es têm conteúdo planejado no
calendário editorial". Mas o dict **já tem artigos reais publicados**
em fr-FR, de-DE, ru-RU e zh-CN (confirmado em `Publicados_Auditoria` e
no próprio `blog_content.py`) — eles simplesmente não têm campo
`category`, então continuam respondendo na URL plana `/blog/<slug>`
(testado: `portugais-bresilien-pour-expatries-...` responde 200 direto,
sem prefixo `/fr/`). Não é um link quebrado — é a canônica real desses
artigos hoje. Só documentando para não confundir "sem prefixo de
idioma" com "está quebrado".

## 5. Cluster/pilar: a planilha erra 2 URLs

A aba `Clusters_e_Pilares` da SEO/GEO v3 cita `/para-empresas` (B2B) e
`/en/brazilian-portuguese-course-online` (PLE) como páginas-pilar.
**Nenhuma das duas foi confirmada por HTTP nesta sessão**, e a primeira
diverge do que já está aprovado e construído no Next: B2B real é
`/empresas` (Fase E.1). `scripts/migrate-blog.mjs` usa `/empresas` e
`/curso-de-ingles-online`/`/curso-de-ioruba-online`/`/curso-de-espanhol-
online`/`/curso-de-hebraico-online` (todos já aprovados) como pilar
real; o pilar de PLE em inglês fica marcado `REVIEW` no CSV até alguém
confirmar a URL real por HTTP.

## Veredito

Fonte de dados: 2 sistemas coexistindo (dict confirmado, DocType não
verificado). Padrão de URL: 3 formatos legítimos, nenhum deles forçado
ou inventado — cada um extraído do que o próprio código já faz. Nenhuma
URL migrada para um formato diferente do que já está ao vivo hoje.
