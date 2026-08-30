# 25 — Blog Content Model

Contrato de artigo (`src/types/blog.ts`), o porquê de cada campo, e como
ele mapeia para as fontes reais (produção + planilha SEO/GEO v3).

## Campos e origem

| Campo | Origem | Nota |
|---|---|---|
| `slug`, `category` | `blog_content.py` (chave do dict + campo `category`) | `category` vazio = URL plana `/blog/<slug>` (ver `24-blog-source-of-truth.md`) |
| `title`, `h1`, `description` | `blog_content.py` | Preservados literalmente na migração de prova de conceito |
| `language` | Cruzado com `Publicados_Auditoria` (coluna idioma) quando há correspondência | Idioma do CONTEÚDO, não do locale do site (missão seção 26) |
| `publishedAt`, `publishedAtDisplay` | `blog_content.py`, campo `date`/`date_display` | **Imutável na migração** -- ver `26-blog-cadence-and-dates.md` |
| `updatedAt` | Não usado ainda -- nenhum artigo migrado tem revisão editorial real registrada | Só populado quando houver edição de conteúdo de verdade, nunca por migração técnica |
| `author` | Institucional fixo ("Equipe Vedium") | Nenhuma autoria individual inventada (missão seção 23) -- autoria por professor específico só quando confirmada, fora do escopo desta fase |
| `tag`, `cluster`, `pillarUrl` | `blog_content.py` (`tag`) + aba `Clusters_e_Pilares` da SEO/GEO v3, com pilar substituído pela URL real já aprovada no Next quando diverge da planilha | Ver `24-blog-source-of-truth.md` seção 5 |
| `primaryKeyword`, `secondaryKeywords`, `searchIntent`, `funnelStage` | Preenchidos manualmente para o artigo migrado, seguindo as regras de `Regras_SEO_GEO_v2` (termo-alvo real, não o título) | Não exibidos na UI (missão seção 19: "não necessariamente mostrar") -- ficam no modelo para uso futuro em relatórios/roteamento de conteúdo relacionado |
| `schema` | `Article` para este artigo (informacional/comparativo, sem passo a passo dominante) | Regra de `Regras_SEO_GEO_v2`: HowTo só em passo a passo real, Course em comercial, Article no resto |
| `heroImage` | `blog_content.py` (`hero_image`/`hero_alt`) | Imagem já hospedada (Unsplash) -- mantida como estava, não há guideline de mídia própria ainda aplicada ao blog (diferente das páginas institucionais, que usam `vedium-references/envato-assets`) |
| `sections` | `blog_content.py` (`sections`), HTML preservado literalmente | Corpo controlado por nós, mesma convenção do Frappe |
| `faq` | `blog_content.py` (`faqs`) | Alimenta `FAQPage` |
| `cta` | `blog_content.py` (`cta_title`/`cta_text`/`cta_label`/`cta_url`) | CTA contextual do próprio artigo, não um CTA genérico de curso (missão seção 35) |
| `relatedArticles` | Vazio no artigo migrado | Só 1 artigo migrado nesta fase -- sem irmãos reais ainda para popular (missão seção 16: nunca preencher com outro idioma só por falta de conteúdo) |
| `seo.canonical` | Construído a partir de `category`/`slug`, confirmado por HTTP contra a URL real de produção | |

## Por que não tem mais campos

O modelo NÃO inclui (por decisão consciente, mission seção 20 "não criar
campos sem necessidade"):

- Contagem de views/analytics -- pertence a uma camada de analytics
  separada (ver seção 45 da missão), não ao conteúdo.
- Autor com foto/bio -- não há dado real confirmado para popular isso
  hoje (ver `24-blog-source-of-truth.md`, sem persona fictícia).
- Campos de tradução/hreflang no próprio artigo -- tratados à parte
  (missão seção 27: hreflang só entre pares realmente equivalentes, não
  todo artigo tem um).

## Reuso de componentes (sem Design System novo)

`ArticleTemplate` (`src/components/blog/ArticleTemplate.tsx`) reusa:
`Breadcrumb`, `FAQSection`, `Button`, e a mesma estrutura de markup do
`CtaSection--brand-full` (replicada, não reimportada, porque o CTA do
artigo tem só 1 botão e texto próprio por artigo -- mesma lição
aprendida na Fase F.3 sobre não fatiar classes de um componente sem
reproduzir o wrapper inteiro). Tipografia do corpo usa
`.v2-container--reading` (760px, já documentado no Design System como
"FAQ, artigos, legal") + um bloco novo `.v2-article-body` só para estilo
de elementos HTML puros (h3/p/ul/table) vindos do conteúdo migrado.
