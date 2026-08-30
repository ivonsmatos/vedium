# 11 — SEO Parity: `/curso-de-espanhol-online` (CURRENT vs Next local)

Mesmo método dos docs 08/09/10: snapshot do HTML real de produção,
comparado campo a campo com
`frontend/src/app/curso-de-espanhol-online/page.tsx`. Rota Next só existe
localmente.

## 1. Rota — auditoria ANTES de construir

- **URL atual confirmada**: `/curso-de-espanhol-online` — já é a oficial,
  **preservada**, nenhum slug novo criado.
- **Redirects**: nenhum encontrado; é a canônica direta.
- **Sitemap**: indexável (`robots: index, follow`).
- **Backlinks internos**: hub `/cursos-de-idiomas-online`, card "Espanhol"
  da Home, Pathfinder (`PATHFINDER_MATRIX["Espanhol"]`).
- **hreflang**: ver achado na seção 3.

## 2. Metadados

| Campo | CURRENT | NEXT | Status |
|---|---|---|---|
| `<title>` | "Curso de Espanhol Online ao Vivo (Básico ao Avançado) \| Vedium" | idêntico | ✅ |
| description/OG | inclui preço ("A partir de R$ 297/mês") | idêntica, preço incluso | ✅ |
| canonical | `https://vediums.com/curso-de-espanhol-online` | idêntico | ✅ |
| robots | `index, follow, max-image-preview:large` | idêntico | ✅ |

**Nota sobre preço no description**: diferente das FAQs visíveis (onde
preço foi excluído em Inglês/PLE/Espanhol, mesma regra do design system
"preço não entra em componente editorial"), o `<meta name="description">`
e `og:description` são metadados de crawler/SERP, não conteúdo renderizado
na página — recuperá-los literalmente (com preço incluso) segue a regra
de SEO parity ("recuperados ou superados") sem violar a regra de UI.

## 3. Achado real — hreflang é só pt-br + x-default (sem outros locales)

Diferente de Iorubá/Inglês/PLE (que têm 5-6 locales reais), a página de
Espanhol em produção tem **hreflang mínimo**:

```
hreflang="pt-br" (self)
hreflang="x-default" (self)
```

Nenhuma versão localizada de Espanhol existe hoje. O Next reproduz
exatamente esse contrato — **nenhum locale foi inventado** (regra
explícita da missão, seção 26: "não adicionar traduções inexistentes").

## 4. H1

- **CURRENT**: "Curso de espanhol online ao vivo, com professor de verdade"
- **NEXT**: "Espanhol para comunicar com mais precisão." — copy nova dada
  literalmente pela missão da Fase D.4 (mesma lógica já aplicada às 3
  páginas anteriores). H1 único confirmado no HTML renderizado.

## 5. Níveis

`catalog_registry.py` + `course_urls.py` confirmam **3 níveis
sequenciais** (Básico/Intermediário/Avançado) com faixa CEFR real por
nível — **não inventada**, recuperada do HTML ao vivo de cada página:

| Nível público | Faixa CEFR real | URL (HTTP 200 testado) |
|---|---|---|
| Básico | A1-A2 | `/curso/espanhol-basico` |
| Intermediário | B1-B2.1 | `/curso/espanhol-intermediario` |
| Avançado | B2.2-C1 | `/curso/espanhol-avancado` |

Preço (R$ 297/397/497 por nível, `catalog_registry.py`) confirma os mesmos
3 cursos — não usado na página (preço fora de componente editorial).

## 6. Achado real — só 2 artigos de blog existem para Espanhol

`/blog/espanhol` lista **2 artigos reais** (não 3): "Falsos cognatos em
espanhol que mais confundem brasileiros" (2/abr/2025, mais recente) e
"Por que brasileiro entende espanhol, mas trava para falar" (24/fev/2025).
A seção "Conhecimento Vedium" mostra os 2 — **não inventa um terceiro**
(regra explícita da missão, seção 17: "se houver poucos artigos, mostrar
menos"). `InsightsEditorial.secondaryB` foi tornado opcional no componente
compartilhado para suportar esse caso real sem quebrar as páginas que já
têm 3 artigos (Home/Iorubá/Inglês, verificado sem regressão nesta sessão).

## 7. Schema (JSON-LD)

| Schema | CURRENT | NEXT | Status |
|---|---|---|---|
| `Course` | `educationalLevel: "Básico ao Avançado (A1 a C1)"` | idêntico | ✅ |
| `BreadcrumbList` | Início → Cursos de Idiomas → Curso de Espanhol Online | idêntico | ✅ |
| `FAQPage` | 5 perguntas reais (1 cita preço) | 8 perguntas — as 4 não-comerciais das 5 reais preservadas por completo (inclui a pergunta central sobre correção de portunhol) + 4 construídas só com fatos já confirmados em outras seções da própria página; excluída só a de preço (mesma regra já aplicada em Inglês/PLE) | ✅ cobertura mantida |

## 8. Internal links (todos testados HTTP 200 nesta sessão)

`/curso/espanhol-{basico,intermediario,avancado}`, `/cursos-de-idiomas-online`,
`/blog/espanhol/falsos-cognatos-em-espanhol-que-mais-confundem-brasileiros`,
`/blog/espanhol/por-que-brasileiro-entende-espanhol-mas-trava-para-falar`.

## Veredito

**SEO PARITY: PASS.** Metadados mecânicos recuperados literalmente
(incluindo preço no `<meta description>`, que é metadado, não UI). Dois
achados reais documentados sem inventar dado: hreflang mínimo (preservado
tal como está, não expandido) e apenas 2 artigos de blog reais (mostrados
os 2, sem terceiro fabricado).
