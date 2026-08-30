# 33 — Fase G.1: Relatório Final de QA Global Pré-Cutover

DEPLOY: NOT PERFORMED. Nenhuma mudança de DNS, Cloudflare, Nginx ou
produção foi executada nesta fase -- só código local, documentação e
scripts de verificação.

## Gate

| Campo | Resultado |
|---|---|
| ROUTE PARITY | PASS -- 13 páginas + hub de blog migradas e conferidas 1:1 contra produção (`31-global-route-inventory.csv`); resto do site documentado como fora de escopo desta migração, servindo do Frappe |
| SEO PARITY (title/description/canonical/OG) | PASS nas páginas migradas (auditado fase a fase, F.1-F.5) |
| BLOG 97/97 DECISION COVERAGE | PASS -- todo artigo tem decisão registrada (`27-blog-url-migration-map.csv` + `30-blog-review-queue.md`); 2 itens em MANUAL DECISION REQUIRED (1 revisão de professor de Iorubá, 1 revisão editorial de sobreposição), o que é o comportamento correto, não uma falha |
| PUBLISHED DATE PARITY | PASS -- a única data migrada (`2026-07-13`) bate com `blog_content.py` e a auditoria oficial; regra de nunca usar data de migração como `publishedAt` documentada e seguida (`26-blog-cadence-and-dates.md`) |
| SITEMAP | PASS -- `sitemap.ts` gera URLs reais, sem data fabricada |
| ROBOTS | PASS -- `robots.ts` bloqueia por host, seguro em qualquer ambiente não-produção |
| CANONICAL | PASS nas páginas migradas |
| HREFLANG | N/A nesta fase -- as páginas migradas são todas pt-BR; o rollout i18n é um projeto separado que continua 100% no Frappe (fora do escopo desta migração Next) |
| SCHEMA (JSON-LD) | PASS -- parseável, sem host incorreto, mesma estrutura de produção (`Organization`/`EducationalOrganization`/`Course`/`Article`) |
| SSR | PASS -- todas as páginas migradas são Server Components, sem client-only content crítico para SEO |
| BROKEN LINKS | 0 reais (achados do crawler eram todos URLs legítimas fora de escopo, reclassificadas) |
| BROKEN IMAGES | 0 |
| 404 | PASS -- HTTP 404 real, reaproveita design system |
| FOOTER 768px OVERFLOW | **RESOLVIDO NESTA FASE** -- 3 causas-raiz corrigidas, verificado 0/90 no sweep completo |
| MOBILE OVERFLOW (320-1440px) | PASS -- 0/90 checagens |
| ACCESSIBILITY | PASS COM RESSALVA -- skip link é CSS morto (achado real, não bloqueador, fix documentado em `32-qa-global-findings.md`) |
| PERFORMANCE | NÃO VERIFICÁVEL LOCALMENTE -- Lighthouse/CWV reais exigem host público (item pré-produção, não bloqueador desta fase) |
| ANALYTICS CONTRACT (`public_cta_click`) | PASS -- contrato reaproveitado literalmente, sem duplicidade, escopo controlado |
| CONSENT MODE / GTM | **FAIL -- BLOQUEADOR REAL** -- container `GTM-P6Q2FXLK` não está implementado em nenhuma página Next; cutover sem isso apaga a coleta de analytics/marketing das rotas migradas |
| DUPLICATE EVENT PROTECTION | PASS -- `public_cta_click` implementado uma única vez por CTA, sem handler duplicado |
| CONTACT FORM | PASS -- `Route Handler -> Frappe`, honeypot funcional, erros sanitizados, nunca client -> DocType direto |
| STRIPE SEPARATION | PASS -- nenhuma chamada Stripe no Next; toda cobrança continua 100% Frappe |
| FRAPPE DECOUPLING | PASS -- Next só lê conteúdo estático versionado em código + 1 endpoint de formulário que repassa pro Frappe; nenhuma dependência de sessão/cookie do Frappe |
| SECURITY | PASS -- 0 segredos no bundle cliente, mensagens de erro sanitizadas, honeypot funcional |
| ROLLBACK PLAN | PASS -- documentado em `29-cutover-plan.md` (gatilho, responsável, passos, tempo estimado, preservação do backend) |
| CUTOVER PLAN | PASS -- documentado em `29-cutover-plan.md`; achado crítico registrado: precisa ser parcial (proxy reverso por rota), não swap total de DNS |
| CONSOLE ERRORS | Não coletado sistematicamente nesta fase (nenhum erro observado durante os screenshots/interações das Fases F.1-F.5, mas não houve uma varredura dedicada de console em todas as 15 rotas) -- registrado como lacuna, não como PASS forçado |

## CUTOVER READINESS: **NOT READY**

Dois motivos, ambos concretos e corrigíveis antes de uma nova rodada de
aprovação -- nenhum exige redesenho nem nova arquitetura:

1. **GTM/Consent Mode ausente do Next** (bloqueador real, seção 5 de
   `32-qa-global-findings.md`) -- sem isso, o cutover das 13 páginas
   apagaria a coleta de analytics dessas rotas. Fix: adicionar o
   snippet real do container ao `app/layout.tsx` na fase DEPLOY PREVIEW
   do `29-cutover-plan.md`, depois re-testar `public_cta_click` contra
   duplicidade.
2. **Cutover não pode ser um swap total de DNS** -- teria que ser um
   roteamento parcial por proxy reverso (rota a rota), porque a maioria
   do site (96 de 97 artigos de blog, páginas de nível de curso,
   `/teste-de-nivel`, locale roots, LMS inteiro) continua existindo só
   no Frappe. Isso não é um bloqueador de bug, é uma correção de
   premissa de arquitetura que precisa estar alinhada com quem configura
   o Cloudflare/Nginx antes de qualquer execução.

Tudo o mais auditado nesta fase -- paridade de rotas, SEO, overflow,
segurança, formulário, separação de Stripe/Frappe, decisão dos 97
artigos do blog -- está em **PASS**, incluindo a correção completa do
bug histórico de overflow do Footer que a própria missão pediu para
resolver "agora" (seção 29 da missão G.1).

## Itens que não bloqueiam o cutover, mas precisam de decisão humana antes dele

- 2 artigos do blog em `MANUAL DECISION REQUIRED` (`30-blog-review-
  queue.md`): 1 precisa de revisão de um professor de Iorubá (regra
  cultural já estabelecida), 1 precisa de decisão editorial sobre
  possível sobreposição de conteúdo entre dois artigos de inglês.
- Skip link de acessibilidade (CSS existe, markup não) -- fix pontual
  de ~13 arquivos, documentado, não implementado nesta sessão para
  evitar uma correção parcial/inconsistente.
- Redirect `/metodologia -> /como-funciona` -- decisão já tomada,
  redirect ainda não implementado em produção (correto: implementação
  é passo da fase CUTOVER, não desta fase de QA).

## Próximo passo

PARE. Não executar cutover, DNS, Cloudflare ou Nginx sem autorização
humana explícita -- conforme pedido no fechamento da missão G.1. Depois
de resolvidos os 2 itens de NOT READY (GTM real + confirmação da
arquitetura de proxy parcial com quem administra a infra), esta fase
pode ser re-auditada para virar READY.
