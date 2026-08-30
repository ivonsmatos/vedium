# 10 — SEO Parity: `/portugues-para-estrangeiros` (PLE) — CURRENT vs Next local

Mesmo método dos docs 08/09: snapshot do HTML real de produção, comparado
campo a campo com `frontend/src/app/portugues-para-estrangeiros/page.tsx`.
Rota Next só existe localmente.

## 1. Rota — auditoria ANTES de construir

- **URL atual confirmada**: `/portugues-para-estrangeiros` (sem prefixo de
  idioma) — **preservada**, nenhum slug novo criado.
- **Redirects**: nenhum redirect encontrado apontando para esta URL nem
  saindo dela — é a canônica direta.
- **Sitemap**: página indexável (`robots: index, follow`), faz parte do
  sitemap padrão de cursos de idioma.
- **Backlinks internos**: linkada pelo hub `/cursos-de-idiomas-online`, pelo
  card "Português para Estrangeiros" da Home (`home_course_collection.py`)
  e pelo Pathfinder (`PATHFINDER_MATRIX["Português para Estrangeiros"]`).
- **hreflang**: ver seção 3 abaixo — achado importante.

## 2. Metadados

| Campo | CURRENT | NEXT | Status |
|---|---|---|---|
| `<title>` | "Português para Estrangeiros \| Vedium" | idêntico | ✅ |
| description | "Português para estrangeiros com aulas ao vivo para morar, trabalhar, estudar e se comunicar melhor no Brasil." | idêntica | ✅ |
| canonical | `https://vediums.com/portugues-para-estrangeiros` | idêntico | ✅ |
| robots | `index, follow, max-image-preview:large` | idêntico | ✅ |
| OG/Twitter | mesmos textos, mesma imagem | idênticos | ✅ |

## 3. Achado real — `x-default` aponta para EN, não pt-BR

Diferente de Iorubá e Inglês (onde `x-default` aponta para a própria
página pt-BR), a página de PLE em produção tem:

```
hreflang="x-default" href="https://vediums.com/en/learn-portuguese-brazil"
```

Ou seja, **a versão canônica "global" desta família já é a inglesa em
produção** — decisão real, coerente com o propósito estratégico da própria
missão (seção 3: "para aquisição internacional, a versão em inglês é
estrategicamente importante"). O Next preserva esse comportamento
literalmente (`hreflang["x-default"]` aponta pra `/en/learn-portuguese-brazil`,
não para `ple.seo.canonical`). O `canonical` da própria página, por outro
lado, continua autorreferente (pt-BR) — `canonical` e `x-default` são
mecanismos diferentes; não há conflito em um apontar pra si mesmo e o outro
sinalizar qual versão é o fallback.

Todos os 5 locales (en/es/fr/de/ru) têm hreflang real e existente — nenhum
locale fake foi criado; nenhum hreflang aponta pra tradução inexistente.

## 4. H1

- **CURRENT**: "Português para estrangeiros com foco em vida real no Brasil"
- **NEXT**: "Português para viver, trabalhar e se comunicar no Brasil." —
  copy nova dada literalmente pela missão da Fase D.3 (mesma lógica já
  aplicada a Iorubá/Inglês: title/description recuperados, H1 é decisão de
  design). H1 único confirmado no HTML renderizado.

## 5. Achado real — sem conteúdo de blog em pt-BR para este tema

`blog_content.py` não tem NENHUM post em pt-BR marcado para português para
estrangeiros. O único conteúdo real do tema existe em **EN** (2 posts,
categoria "Brazilian Portuguese": "What to expect from a structured
Portuguese course for foreigners" e "Portuguese for Brazil: a realistic
study path from A1 to B1") e **FR** (1 post). A seção "Conhecimento
Vedium" foi **deliberadamente omitida** da versão pt-BR — usar os artigos
em inglês misturaria idioma dentro de uma página pt-BR (proibido pela
própria missão, seção 3) e preencher com posts de outro idioma/curso
(Inglês, Iorubá) também é proibido pela regra geral de insights. Quando a
versão `/en/learn-portuguese-brazil` for construída no Next, os 2 artigos
EM INGLÊS reais devem ser usados lá.

## 6. Níveis

`course_urls.py` (`PLE_COURSE_TRACK` + `PLE_COURSE_NAV_I18N`) confirma
**3 níveis sequenciais** (Básico/Intermediário/Avançado) — NÃO uma trilha
CEFR granular por nível (o Course schema real usa só uma faixa agregada,
"A1 a B2"). URLs reais, testadas HTTP 200 nesta sessão:
`/curso/portugues-para-estrangeiros-{basico,intermediario,avancado}`.

**Teste de nível**: PLE não tem teste próprio em português —
`PLE_LEVEL_TEST_URLS` só define rotas específicas para en/es/fr/de; em
pt-BR cai no `/teste-de-nivel` genérico (`course_urls.get_course_level_
destination()`, confirmado). O CTA do Hero usa "Conheça o curso" (âncora
`#niveis`), não "Descubra seu nível" — não inventamos um teste que não
existe no locale pt-BR.

## 7. Schema (JSON-LD)

| Schema | CURRENT | NEXT | Status |
|---|---|---|---|
| `Course` | `educationalLevel: "A1 a B2"`, demais campos padrão | idêntico | ✅ |
| `BreadcrumbList` | Início → Cursos de Idiomas → Português para Estrangeiros | idêntico | ✅ |
| `FAQPage` | 4 perguntas reais | 8 perguntas — as 4 reais preservadas por completo (inclui "As aulas podem ter apoio em inglês?", a pergunta que resolve diretamente site-locale ≠ course-language) + 4 construídas só com fatos já confirmados em outras seções desta mesma página | ✅ superado |

## 8. Internal links (todos testados HTTP 200 nesta sessão)

`/curso/portugues-para-estrangeiros-{basico,intermediario,avancado}`,
`/teste-de-nivel`, `/cursos-de-idiomas-online`, `/como-funciona`.

## Veredito

**SEO PARITY: PASS.** Metadados mecânicos recuperados literalmente. Dois
achados reais documentados e resolvidos sem inventar dado: hreflang
x-default→EN (preservado, não "corrigido" para pt-BR) e ausência de blog
pt-BR (seção omitida, não preenchida com conteúdo de outro idioma).
