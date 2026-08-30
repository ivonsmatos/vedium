# 12 — SEO Parity: `/curso-de-hebraico-online` (CURRENT vs Next local)

Mesmo método dos docs 08-11: snapshot do HTML real de produção, comparado
campo a campo com `frontend/src/app/curso-de-hebraico-online/page.tsx`.
Rota Next só existe localmente.

## 1. Rota — auditoria ANTES de construir

- **URL atual confirmada**: `/curso-de-hebraico-online` — já é a oficial,
  **preservada**.
- **Páginas filhas**: todas as 5 auditadas e confirmadas HTTP 200 nesta
  sessão — `/curso/hebraico-a0-alfabetizacao`,
  `/curso/hebraico-moderno-a1`, `/curso/hebraico-moderno-a2-b1`,
  `/curso/hebraico-biblico-leitura-guiada`, `/curso/hebraico-particular`.
- **Redirects**: nenhum encontrado.
- **hreflang**: só pt-br(self) + x-default(self) — mesmo contrato mínimo
  do Espanhol, nenhum locale inventado.

## 2. ACHADO CRÍTICO — a página-pilar atual está desatualizada frente ao catálogo real

O FAQPage ao vivo da página atual responde à pergunta "Existe hebraico
bíblico na Vedium?" com:

> "Ainda não; o piloto atual é só Hebraico Moderno A1. Uma trilha de
> Hebraico Bíblico pode abrir depois, conforme demanda."

Mas as 5 páginas de curso listadas acima estão **todas live, completas e
reais** — cada uma com title/H1/description próprios, sem nenhum indício
de placeholder. `course_urls.py` (`COURSE_PUBLIC_SLUGS`,
`_CATALOG_TRACK_COURSE_IDS["hebrew"]`) também já trata os 5 como produtos
distintos e existentes. Ou seja: **a página-pilar nunca foi atualizada
depois que o catálogo de Hebraico cresceu** de "só o piloto Moderno A1"
para as 5 trilhas atuais.

O Next reflete o **catálogo real confirmado por HTTP**, não o FAQ
desatualizado — isso é uma correção documentada, não uma invenção: toda
trilha usada nesta página tem uma URL própria, ao vivo, testada nesta
sessão. A pergunta "Existe hebraico bíblico?" foi mantida no FAQ (é uma
pergunta real e valiosa), mas a **resposta foi atualizada** para refletir
a realidade atual. Recomendação: atualizar o FAQ da página de produção
Frappe também (fora do escopo desta tarefa — não fazemos deploy nem
alteramos Frappe).

## 3. Metadados

| Campo | CURRENT | NEXT | Status |
|---|---|---|---|
| `<title>` | "Curso de Hebraico Online ao Vivo (com Alfabetização) \| Vedium" | idêntico | ✅ |
| description/OG | "...alfabetização incluída...A partir de R$ 397/mês" (preço é metadado, não UI — mesma regra já aplicada em Espanhol) | idêntica | ✅ |
| canonical | `https://vediums.com/curso-de-hebraico-online` | idêntico | ✅ |
| robots | `index, follow, max-image-preview:large` | idêntico | ✅ |

**Nota**: title/description recuperados literalmente mencionam só
"Alfabetização" (não Bíblico/Particular) — preservados assim mesmo,
seguindo a mesma lógica já usada nas páginas anteriores (meta recuperado
literalmente; H1 e conteúdo visível é que trazem a cobertura completa).

## 4. H1

- **CURRENT**: "Aprenda hebraico moderno online, com alfabetização e
  professor ao vivo"
- **NEXT**: "Hebraico para diferentes percursos de estudo." — copy nova
  dada literalmente pela missão da Fase D.5, que amplia intencionalmente o
  escopo do H1 para cobrir os 5 percursos reais (não só Moderno). H1 único
  confirmado no HTML renderizado.

## 5. Estrutura de níveis — NÃO sequencial

Diferente de Iorubá/Inglês/PLE/Espanhol (uma trilha sequencial única),
Hebraico é **5 produtos distintos**, confirmado em `course_urls.py`
(`_SEQUENTIAL_LANGUAGES` explicitamente NÃO inclui hebrew; docstring:
"Hebrew includes different products... need their own approved labels"):

| Percurso | Sequencial? | URL |
|---|---|---|
| A0 (Alfabetização) | Sim, alimenta o Moderno | `/curso/hebraico-a0-alfabetizacao` |
| Moderno A1 | Sim | `/curso/hebraico-moderno-a1` |
| Moderno A2/B1 | Sim | `/curso/hebraico-moderno-a2-b1` |
| Bíblico — Leitura Guiada | Não, percurso paralelo | `/curso/hebraico-biblico-leitura-guiada` |
| Particular | Não, percurso paralelo | `/curso/hebraico-particular` |

O `ProgressionTimeline` (`ProgressionFlow`) só representa a progressão
sequencial real A0→A1→A2/B1; Bíblico e Particular aparecem em seções
próprias, não como "próximo nível" depois do A2/B1. O tipo genérico
`LanguagePillarContent.tracks` (`EditorialRow[]` com `href`/`ctaLabel`
opcionais) foi adicionado ao contrato compartilhado (`src/types/
language.ts`) especificamente para representar percursos não-sequenciais
de forma reutilizável — não é um tipo acoplado a "hebraico".

## 6. Schema (JSON-LD)

| Schema | CURRENT | NEXT | Status |
|---|---|---|---|
| `Course` | `educationalLevel: "Alfabetização + A1 (iniciante)"` | `"Alfabetização a A2/B1 (Moderno); Leitura Guiada (Bíblico)"` — reflete o catálogo real de 5 percursos | ✅ superado |
| `BreadcrumbList` | Início → Cursos de Idiomas → Curso de Hebraico Online | idêntico | ✅ |
| `FAQPage` | 5 perguntas (1 cita preço, 1 desatualizada sobre Bíblico) | 8 perguntas — 3 das 5 reais preservadas por completo (alfabetização inclusa, curso não é religioso, aulas ao vivo); a de Bíblico **corrigida** (ver achado acima); a de preço excluída (mesma regra já aplicada); +4 construídas só com fatos confirmados nesta mesma página | ✅ cobertura superada |

Nenhum schema de religião foi criado — `Course`/`BreadcrumbList`/`FAQPage`
somente, todos semanticamente corretos para um curso de idioma.

## 7. RTL inline

Único trecho em escrita hebraica real da página: "אלף־בית" (nome do
próprio alfabeto, alef-bet), na seção "Hebraico Moderno". Marcado como
`<span lang="he" dir="rtl">` **só nesse span** — confirmado no HTML
renderizado (`lang="he"` presente, página inteira continua `<html
lang="pt-BR">`, sem `dir="rtl"` em nenhum ancestral). Nenhum outro texto
em escrita hebraica na página.

## 8. Internal links (todos testados HTTP 200 nesta sessão)

Todos os 5 `/curso/hebraico-*`, `/cursos-de-idiomas-online`,
`/blog/hebraico/como-funciona-a-alfabetizacao-em-hebraico-do-zero`,
`/blog/hebraico/hebraico-moderno-x-hebraico-biblico-entenda-a-diferenca`.

## Veredito

**SEO PARITY: PASS**, com uma correção documentada e superior ao dado
atual (FAQ de Hebraico Bíblico desatualizado na produção Frappe, corrigido
no Next com base no catálogo real confirmado por HTTP — nenhum link
inventado, nenhuma trilha fabricada).
