# 36 — Estratégia de sitemap/robots durante a transição híbrida (Fase G.2, Parte B)

Só estratégia. Nenhuma mudança de `/sitemap.xml` ou `/robots.txt` de
produção foi feita nesta fase.

## 1. Estado real dos dois sitemaps

| | Frappe (produção real) | Next (`app/sitemap.ts`, Fase G.1) |
|---|---|---|
| URLs | ~336 (confirmado por auditoria HTTP anterior, `docs/redesign/baseline/infrastructure-gap.md`) | 15 (14 estáticas + 1 artigo de blog) |
| Cobertura | Site inteiro: institucional, 5 pilares, ~18 páginas de nível, 97 artigos de blog, 6 idiomas, teste de nível, legais | Só as 13 páginas migradas + hub de blog + 1 artigo |
| `lastModified` | Não auditado nesta fase | Só quando existe dado editorial real (nunca data de build) |

## 2. Decisão para esta etapa: Frappe continua dono do sitemap/robots público

Trocar `/sitemap.xml`/`/robots.txt` pro Next agora **seria uma
regressão de SEO real**, não uma melhoria -- o Google perderia de vista
321 URLs que continuam existindo e respondendo normalmente. Por isso,
diferente do que um primeiro rascunho desta fase chegou a colocar no
exemplo de Nginx (corrigido em `34-hybrid-routing-architecture.md`,
seção 6), `/sitemap.xml` e `/robots.txt` **NÃO entram na allowlist**
desta primeira etapa de cutover. Continuam sendo respondidos pelo
Frappe, exatamente como hoje.

Como as 13 URLs migradas **não mudam de endereço** (mesmo path público,
só troca o backend que responde), o sitemap Frappe existente continua
100% válido para elas sem precisar de nenhuma edição -- um `<loc>` no
sitemap não sabe nem precisa saber qual backend respondeu.

## 3. Quando migrar o sitemap de verdade (fora do escopo desta fase)

Só faz sentido quando o Next cobrir uma fração grande o suficiente do
site pra que seu próprio `sitemap.ts` seja mais completo que uma
omissão. Duas rotas possíveis, a decidir numa fase futura própria:

- **Sitemap único gerado pelo Next**, que passa a incluir também as
  URLs que ainda são só-Frappe (exigiria o Next conhecer essa lista --
  hoje ele não tem acesso ao catálogo dinâmico do Frappe/LMS).
- **Sitemap índice** (`sitemap_index.xml`) apontando pra 2 sitemaps
  filhos, um por backend -- mais simples de manter (cada backend só
  declara o que ele mesmo serve), mas exige que ambos os backends
  concordem em nunca listar a mesma URL duas vezes (risco de
  duplicação se alguém esquecer de remover uma URL do sitemap Frappe
  depois de uma migração futura).

Nenhuma das duas foi implementada -- registradas como opção, não como
plano aprovado (missão, seção 43: "não implementar antes de validar").

## 4. robots.txt

Mesma lógica: o `robots.txt` real de produção já permite crawler de IA
(GPTBot, ChatGPT-User, CCBot, anthropic-ai, Claude-Web, Google-Extended)
e aponta pro sitemap real -- nenhum motivo pra trocar por um
`robots.ts` do Next que hoje só existe pra ambiente local (e que,
inclusive, bloqueia (`Disallow: /`) qualquer host que não seja
`vediums.com` -- ver `frontend/src/app/robots.ts`, Fase G.1). Continua
assim até o Next cobrir o suficiente do site pra assumir esse papel.

## 5. Gate desta parte

| Campo | Resultado |
|---|---|
| SITEMAP HYBRID STRATEGY | PASS -- decisão registrada (Frappe continua dono), nenhuma duplicação de URL entre os dois sitemaps nesta etapa (Next simplesmente não expõe o seu em produção) |
