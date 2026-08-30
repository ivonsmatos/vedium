# 16 — SEO Parity: `/como-funciona` (CURRENT vs Next local)

Mesmo método dos docs 08-15: snapshot do HTML real de produção, comparado
campo a campo com `frontend/src/app/como-funciona/page.tsx`. Rota Next só
existe localmente.

## 1. Rota — auditoria ANTES de construir

Confirmado por HTTP nesta sessão (`Invoke-WebRequest`):

| URL | Status |
|---|---|
| `/como-funciona` | **200** |
| `/metodologia` | **200** |
| `/como-funciona-a-vedium` | 404 |
| `/teste-de-nivel` | 200 |
| `/teste-de-nivel-ingles` | 200 |
| `/teste-de-nivel-espanhol` | 404 |
| `/teste-de-nivel-hebraico` | 404 |
| `/teste-de-nivel-ioruba` | 404 |
| `/teste-de-nivel-portugues` | 404 |
| `/cursos-de-idiomas-online` | 200 |

## 2. ACHADO CRÍTICO — duas páginas de produção cobrem terreno parecido

A produção Frappe hoje tem **duas páginas distintas**, não uma:

| Campo | `/como-funciona` | `/metodologia` |
|---|---|---|
| `<title>` | "Como funciona - Vedium" | "Metodologia - Vedium" |
| H1 | "Da dúvida ao plano de estudo" | "Aula ao vivo, conversação real e evolução por nível" |
| Foco | Onboarding: teste de nível, aula diagnóstica, plano de estudo | Método de ensino: aula ao vivo, conversação, evolução por nível |
| description | "Entenda em 3 passos como estudar idiomas online ao vivo na Vedium: teste de nivel, aula diagnostica e plano de estudo." | "Conheça a metodologia da Vedium: aulas ao vivo em turma compatível com seu nível, foco em conversação real desde a primeira aula e evolução por níveis, do básico ao avançado." |

A missão F.1 pede uma única página que responde "como eu estudo na
Vedium?", cobrindo as duas frentes (onboarding + metodologia) na mesma
página. Por isso o Next **consolida as duas em uma só**, na URL
`/como-funciona` — que já é a rota para a qual `Header.tsx` (nav
desktop e mobile), `content/site/footer.ts` e
`content/home/liveClass.ts` apontam nesta base de código local (todos
esses links estavam quebrados/404 localmente até esta fase, porque a
rota Next não existia ainda).

**Não foi criada rota para `/metodologia`** — isso seria exatamente o
"dois caminhos concorrentes para a mesma intenção" que a missão proíbe
(seção 1). Recomendação para quando este build for promovido a produção:
`/metodologia` deveria redirecionar (301) para `/como-funciona` — fora
do escopo desta tarefa (sem deploy, sem alteração no Frappe).

## 3. ACHADO CRÍTICO — não existe teste de nível universal

`/teste-de-nivel` (sem sufixo) **não é um teste genérico**: o HTML real
tem título "Teste de Nível de Português para Estrangeiros" e H1
"Descubra seu nível de português antes de começar as aulas" — é o teste
de PLE. O único outro teste real é `/teste-de-nivel-ingles` (Inglês).
Testado por HTTP nesta sessão: `/teste-de-nivel-espanhol`,
`/teste-de-nivel-hebraico`, `/teste-de-nivel-ioruba`,
`/teste-de-nivel-portugues` — todos 404.

Consequência direta na página (missão seção 6, aviso explícito): o CTA
secundário do Hero **não** promete um teste universal. Usa "Fale com a
Vedium" (WhatsApp), o mesmo padrão já usado no Hero de toda página de
idioma. A seção "01 Ponto de Partida" descreve o teste de nível como
possibilidade só para Português para Estrangeiros e Inglês, nunca como
regra para os 5 idiomas.

## 4. Metadados

| Campo | Next (`/como-funciona`) |
|---|---|
| `<title>` | "Como Funciona a Vedium \| Aulas de Idiomas Online ao Vivo" |
| description | "Entenda como funciona a Vedium: aulas ao vivo com professor, ponto de partida por idioma, progressão por nível e acompanhamento ao longo do percurso." |
| canonical | `https://vediums.com/como-funciona` |
| robots | `index, follow, max-image-preview:large` |

Título/description são **novos** (não uma cópia literal de nenhuma das
duas páginas atuais), porque a página Next consolida o escopo das duas
— preservar literalmente o title de só uma delas subrepresentaria a
outra metade do conteúdo.

## 5. Hreflang

Produção tem hreflang completo em `/como-funciona` (pt-br, en, es, fr,
de, x-default) — mas nenhuma dessas traduções existe nesta base de
código Next (o rollout de i18n do projeto, ver
`project_i18n_n_language_rollout` na memória, ainda não chegou a esta
página institucional). Por isso o Next usa o mesmo contrato mínimo já
aprovado em Espanhol/Hebraico: só `pt-br` (self) + `x-default` (self).
Nenhum locale inventado.

## 6. H1

Único H1 confirmado no HTML renderizado: "Um percurso claro para
aprender, praticar e avançar." — copy literal da missão (seção 6).

## 7. Schema (JSON-LD)

| Schema | Conteúdo |
|---|---|
| `Organization` | `{ name: "Vedium", url: "https://vediums.com" }` — mesmo contrato global já usado como `provider` em todas as páginas de curso |
| `BreadcrumbList` | Início → Como Funciona (2 níveis) |
| `FAQPage` | 8 perguntas, todas com fatos confirmados nesta sessão |

Nenhum schema `Course` (a missão seção 27 pede explicitamente para não
usar `Course` nesta página institucional — não é um curso específico).

## 8. Internal links (testados nesta sessão)

Confirmados via interaction-check (`scripts/interaction-check-how-it-works.mjs`):
os 5 `/curso-de-*` e `/portugues-para-estrangeiros`, `/empresas`,
`/curso/hebraico-particular`, WhatsApp oficial
(`https://wa.me/5511911293075...`), 6 âncoras internas
(`#ponto-de-partida`, `#percurso`, `#aulas-ao-vivo`, `#professor`,
`#idioma-e-contexto`, `#acompanhamento`) — todas rolam para a seção
correta. Os 4 links `#niveis` para Inglês/Espanhol/PLE/Iorubá apontam
para âncoras já existentes e confirmadas nessas páginas
(`id="niveis"` presente nos 4 `page.tsx`); o link para Hebraico aponta
para `#percursos`, a âncora real usada na própria página de Hebraico
(Hebraico não tem `#niveis` porque não é sequencial — ver
`12-hebrew-seo-parity.md`).

## Veredito

**SEO PARITY: PASS.** Consolidação de 2 páginas de produção em 1
documentada e justificada; achado crítico sobre o teste de nível não
ser universal tratado com uma correção real de CTA (nenhuma promessa
fabricada); hreflang mínimo e verdadeiro; nenhum link inventado.
