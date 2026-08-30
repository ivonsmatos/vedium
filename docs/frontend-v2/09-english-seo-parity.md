# 09 — SEO Parity: `/curso-de-ingles-online` (CURRENT Frappe vs Next local)

Mesmo método do doc 08 (Iorubá): snapshot do HTML real de produção,
comparado campo a campo com `frontend/src/app/curso-de-ingles-online/
page.tsx`. Rota Next só existe localmente.

## Metadados

| Campo | CURRENT | NEXT | Status |
|---|---|---|---|
| URL | `/curso-de-ingles-online` | mesma | ✅ |
| `<title>` | "Curso de Inglês Online ao Vivo do A1 ao C1 \| Vedium" | idêntico | ✅ |
| description | "Aulas de inglês online ao vivo, turmas pequenas e progressão do A1 ao C1. Faça o teste de nível grátis." | idêntica | ✅ |
| canonical | `https://vediums.com/curso-de-ingles-online` | idêntico | ✅ |
| robots | `index, follow, max-image-preview:large` | idêntico | ✅ |
| hreflang | pt-br(self), en, es, fr, de, ru, x-default — **5 locales completos** (diferente de Iorubá, que não tem fr/de) | mesmos 7 entries, mesmos destinos | ✅ |
| OG/Twitter | mesmos textos, mesma imagem (logo quadrada) | idênticos | ✅ |

## H1

- **CURRENT**: "Curso de inglês online ao vivo do A1 ao C1"
- **NEXT**: "Inglês para avançar com segurança." — copy nova dada
  literalmente pela missão da Fase D.2. Mesma lógica já aplicada ao
  Iorubá: title/description (campos de meta) recuperados literalmente;
  H1 (conteúdo visível) é decisão de design já determinada pela missão.
- H1 único confirmado no HTML renderizado.

## Achado real: divergência B1 vs B1+ vs A2+

`vedium_core/vedium_core/course_urls.py` (`ENGLISH_COURSE_LEVELS`,
`ENGLISH_COURSE_NAV_LABELS`) rotula o curso interno
`ingl-s-pr-intermedi-rio` como **A2+**. Já
`vedium_core/vedium_core/catalog_registry.py` (usado só para
IDs comerciais/preço Stripe) rotula o MESMO curso interno como **"Inglês
B1+"** (`commercial_id: "ingles-b1-plus"`) — inclusive com um comentário
deixado no próprio código (`# Note: I found this missing in oneshots...
Actually I didn't grep it well earlier`) que sugere que esse dado nunca foi
verificado com confiança.

**Resolução**: fetch direto da página real
(`https://vediums.com/curso/ingles-pre-intermediario`) confirmou
`<title>Inglês A2+ Pré-Intermediário Online | Vedium</title>` e
`<h1>Inglês Online ao Vivo A2+ – Pré-Intermediário</h1>` — **A2+ é o rótulo
público real e vigente**, não B1 nem B1+. A trilha usada no Next
(`src/content/languages/english.ts`) segue **A1 / A2 / A2+ / B1 / B2 / C1**
— os 6 níveis confirmados contra o HTML ao vivo de cada uma das 6 páginas
de curso, não contra o dict divergente. Nenhum ID, slug ou URL foi
renomeado — só a leitura correta de qual rótulo já é o real.

## Schema (JSON-LD)

| Schema | CURRENT | NEXT | Status |
|---|---|---|---|
| `Course` | name, description, url, provider, `educationalLevel: "A1 a C1 (CEFR)"`, inLanguage | campos idênticos | ✅ |
| `BreadcrumbList` | Início → Cursos de Idiomas → Inglês | idêntico | ✅ |
| `FAQPage` | 13 perguntas (inclui 1 com preço "R$ 240/mês" e 1 sobre aula particular com resposta condicional) | 8 perguntas — as 8 mais fortes e factuais das 13, **nenhuma inventada**; excluídas deliberadamente a de preço (design system não mistura preço em componente editorial, mesma regra de `v2_course_card`) e a de aula particular (resposta incerta/"deve ser confirmado", FAQ fraca) | ✅ (cobertura mantida, 2 exclusões justificadas) |

## Internal links (todos testados HTTP nesta sessão, todos 200)

- 6 níveis: `/curso/ingles-{basico-a1, elementar-a2, pre-intermediario, intermediario-b1, intermediario-superior-b2, avancado-c1}`
- `/teste-de-nivel-ingles` (CTA principal do Hero e do CTA final — **não** é o `/teste-de-nivel` genérico; `course_urls.get_course_level_destination()` confirma que cursos `ingles-*` usam essa rota específica)
- 4 objetivos reais: `/ingles-executivo`, `/ingles-para-entrevista`, `/ingles-para-viagens`, `/ingles-para-programadores`
- `/cursos-de-idiomas-online` (breadcrumb), `/blog/ingles/...` (3 artigos reais)

A sugestão da missão incluía também "Comunicação cotidiana" e "Estudos"
como objetivos — nenhuma das duas tem página própria confirmada
(`/ingles-para-estudos` etc. não existe); não incluídas, conforme regra
"não inventar página".

## Veredito

**SEO PARITY: PASS.** Todos os campos de metadata mecânicos preservados.
Achado real de divergência de dado interno (A2+ vs B1+) resolvido a favor
do HTML de produção ao vivo, sem renomear nenhum ID/slug/URL — documentado
aqui para quem for mexer em `catalog_registry.py` no futuro.
