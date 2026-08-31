# 58 — Auditoria do CSS copiado do Frappe para `frontend/`

## Contexto

`frontend/` é o novo app Next.js (App Router, Server Components por padrão)
que reconstrói Header, Footer e a Home usando o MESMO design system V2 que já
roda em produção em `vediums.com/` (Frappe/Jinja). Os 5 arquivos CSS em
`frontend/src/styles/` são cópia byte-a-byte dos arquivos em
`vedium_core/vedium_core/public/css/v2/` — confirmado via diff antes desta
sessão, sem nenhuma edição.

Esta auditoria classifica cada arquivo/grupo de regras como:

- **KEEP** — reutilizável como está, sem acoplamento a Frappe/Jinja.
- **REFACTOR LATER** — CSS válido e já usado em produção, mas que a Home
  Next ainda não consome (pertence a componentes de páginas futuras:
  Curso, Sobre, Empresas, Blog, FAQ). Fica no lugar; não é dívida técnica.
- **FRAPPE-SPECIFIC / REMOVE** — depende de markup Jinja, JS vanilla
  específico do site Frappe, ou convenção que não faz sentido no Next.

Conclusão geral: o design system V2 já nasceu "isolado" (ver comentários no
topo de cada arquivo fonte — nunca usa seletor de elemento não-escopado,
nunca depende de Bootstrap/jQuery/classes do Desk). Por isso a cópia 1:1
funcionou sem nenhuma reescrita de seletor. Não há necessidade de remoção
agressiva agora — a recomendação abaixo é "manter tudo", com poucos itens
para revisar depois.

## `tokens.css` (249 linhas) — **KEEP** (100%)

Só `:root { --v2-* }`, `@font-face` (Playfair Display, auto-hospedada) e
2 media queries (`prefers-color-scheme`, vazio; `prefers-reduced-motion`).
Zero acoplamento a Frappe. Nota pré-existente (não introduzida por esta
migração): Poppins/Inter ainda não estão auto-hospedadas — cai no fallback
Arial da própria stack (`--v2-font-heading`/`--v2-font-body`), documentado
no próprio arquivo. Mesmo comportamento em produção hoje.

## `foundations.css` (217 linhas) — **KEEP** (100%)

Reset e utilitários, tudo sob `.v2-scope` (aplicado no `<body>` do
`layout.tsx`). `.v2-skip-link` existe na folha mas ainda não tem um link
real usando a classe no Header — **REFACTOR LATER**: adicionar o skip-link
de acessibilidade quando o Header ganhar mais conteúdo antes do `<main>`.

## `components-base.css` (302 linhas) — **KEEP** (100%)

Button, Badge, Breadcrumb, Field/Input/Select, Alert, Modal, Icon wrapper.
A Home usa só Button/Icon hoje (via `<Button>`/`<Icon>` em
`src/components/ui/`). Badge/Breadcrumb/Field/Alert/Modal — **REFACTOR
LATER**: sem uso ainda porque nenhuma página com formulário/modal foi
construída (aula diagnóstica, contato, matrícula); ficam prontos no lugar.

## `header-footer.css` (463 linhas) — **KEEP** (100%)

Utility bar, header principal, mega menu, painel mobile, variante overlay
(hero full-bleed), footer completo (grid, links SEO, bottom bar). Mapeado
1:1 para `Header.tsx`/`Footer.tsx` — mesmos nomes de classe, sem
divergência. Os comentários no arquivo referenciam fases/nomes de arquivo
do lado Frappe (`site_navbar.html`, `design-system-v2.js`) — são só
histórico, não afetam runtime. **REFACTOR LATER** (cosmético, baixa
prioridade): limpar essas referências cruzadas quando o Next deixar de ser
"espelho" e passar a ser fonte própria.

## `components-editorial.css` (1883 linhas) — **misto**

### KEEP — usados pela Home hoje

Hero editorial carousel, Pathfinder (form + section), Vedium Method, Course
Index Intro, Course Feature (+ band), Live Class Experience, Progression
Flow, B2B Home Feature, Insights Editorial, CTA Section, Text Link. Mapeiam
1:1 para `src/components/editorial/*`.

### REFACTOR LATER — CSS válido, sem consumidor Next ainda

Pertencem a páginas fora do escopo desta missão (gate: só Header/Footer/
Home). Nenhum é Frappe-specific — só ainda não têm componente React:

- Language Card / Language Mosaic (`/curso-de-<idioma>`, hub `/catalogo`)
- Teacher Card / Teacher Profile Summary / Teacher Feature (`/professores`)
- Level Card / Level Timeline / **Level Journey** (depende de um padrão
  ARIA tablist com navegação por teclado — precisa de um Client Component
  próprio quando a página de curso for construída, análogo ao que já foi
  feito aqui para o Hero Carousel)
- Process Steps (`/como-funciona`)
- Video Section (poster + play — sem player real acoplado ainda)
- Testimonial Card (sem depoimento aprovado publicável)
- Study Rhythm Card (`/planos`)
- FAQ Accordion (depende de um Client Component próprio para
  abrir/fechar — mesma observação do Level Journey; sem-JS já degrada bem
  via `<details>`/`<noscript>` no macro original, então o componente Next
  também deve preservar esse fallback quando for construído)

### FRAPPE-SPECIFIC / REMOVE

Nenhuma regra de CSS nesta pasta caiu nessa categoria. O único acoplamento
real ao Frappe não está no CSS, e sim em três pontos de *markup/JS* que
esta missão **deliberadamente não portou** para o Next (fora do escopo:
"não consumir API Frappe ainda", "não fazer deploy"):

1. **Snippet GTM inline** (`<script>` no fim de `footer.html` e no
   `<head>` de `www/index.html`, container `GTM-P6Q2FXLK`) — não replicado.
   Decisão de analytics/consentimento é "risco alto" (`05-full-site-
   migration-plan.md`) e não deve entrar como efeito colateral desta
   missão de paridade visual.
2. **`vedium-language.js`** (resolução real de locale via
   `data-vd-nav-urls`/`data-vd-nav-current`) — o `LocaleSwitcher` no Next é
   só a UI (abre/fecha, mesmos hrefs estáticos que o header Jinja já usa:
   `/en/`, `/es/`, etc.); a lógica de fallback `en→pt-br` não foi
   reimplementada porque nenhuma rota localizada existe neste app ainda.
3. **`webmcp.js`** / data island WebMCP — fora do escopo desta missão.

## Resumo

| Arquivo | KEEP | REFACTOR LATER | FRAPPE-SPECIFIC/REMOVE |
|---|---|---|---|
| tokens.css | 100% | — | — |
| foundations.css | ~99% | skip-link sem uso | — |
| components-base.css | ~40% em uso ativo, 100% reutilizável | Badge/Breadcrumb/Field/Alert/Modal sem consumidor ainda | — |
| header-footer.css | 100% | comentários de histórico Frappe (cosmético) | — |
| components-editorial.css | ~35% em uso ativo (Home) | ~55% pronto para páginas futuras | ~10% = 0 regras CSS; acoplamento real está em JS/markup não portado (GTM, locale JS, WebMCP) |

Nenhum arquivo precisa de remoção agora. Primeiro atingir paridade visual
das páginas restantes (Curso, Sobre, Empresas, Blog, FAQ, Planos) — só
depois disso decidir se alguma seção do design system ficou
comprovadamente sem uso em nenhuma página real.
