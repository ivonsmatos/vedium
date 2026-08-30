# 38 — Fase G.2: Relatório Final (GTM real + Roteamento híbrido)

DEPLOY: NOT PERFORMED. Nenhuma mudança de DNS, Cloudflare, Nginx de
produção, Stripe ou Frappe foi executada nesta fase -- só código local
do Next, documentação e verificação empírica via Playwright contra o
dev server.

## O que foi resolvido dos 2 bloqueios da Fase G.1

1. **GTM real não integrado ao Next** -- RESOLVIDO. Container
   `GTM-P6Q2FXLK` + Consent Mode v2 + barra de cookies (antes
   inexistente no Next) implementados e verificados empiricamente (não
   só lidos no código) via Playwright: default antes do GTM, Aceitar/
   Recusar/Gerenciar, persistência entre reload e navegação, 0 eventos
   duplicados de WhatsApp em 5 pontos de contato reais. Detalhe completo
   em `35-gtm-next-contract.md`.
2. **Cutover precisava ser parcial por rota** -- RESOLVIDO
   arquiteturalmente. `34-hybrid-routing-architecture.md` define a regra
   (allowlist exata, fallback pro Frappe por padrão, nunca wildcard),
   com exemplo Nginx dry-run, e documenta honestamente um achado crítico
   novo: a config Nginx ativa de produção não está versionada neste
   repositório (achado herdado de uma auditoria anterior do projeto,
   não desta fase) -- isso vira um pré-requisito explícito de infra
   antes de qualquer execução real, não um bloqueador de arquitetura.

## Gate

| Campo | Resultado |
|---|---|
| GTM CONTAINER | PASS |
| CONSENT MODE | PASS -- default/accept/reject/manage, todos verificados empiricamente |
| CONSENT CROSS-BACKEND CONTRACT | PASS -- mesmas chaves de `localStorage`, mesmos eventos, scripts vendorizados byte-a-byte dos arquivos reais de produção |
| DATALAYER | PASS -- camada central (`lib/analytics/`), nenhum componente monta payload arbitrário |
| DUPLICATE EVENTS | 0 |
| WHATSAPP TRACKING | PASS -- 5/5 pontos de contato testados (Header, Footer, pilar de curso, B2B, Contato), 1 clique = 1 evento em todos |
| NEXT ROUTE ALLOWLIST | PASS -- 13 rotas mapeadas com evidência (`33-first-cutover-route-map.csv`), regra "allowlist exata, nunca wildcard" documentada |
| FRAPPE FALLBACK | PASS -- regra "fora da allowlist = Frappe" documentada e implementada no exemplo dry-run |
| BLOG REMAINS FRAPPE | PASS -- deliberadamente fora da allowlist desta etapa, mesmo o hub Next já existindo |
| LEVELS REMAIN FRAPPE | PASS -- páginas de nível nunca fizeram parte do escopo, links cross-backend documentados |
| ASSET ROUTING | PASS -- `/_next/*` mapeado; `/assets/vedium_core/*` mantido servido pelo Frappe (caminho já compartilhado, evita duplicar upload de imagem) |
| CANONICAL HYBRID | PASS -- já garantido por construção (`metadataBase`), confirmado nos crawls da Fase G.1, nenhuma mudança necessária |
| SITEMAP HYBRID STRATEGY | PASS -- decisão registrada: Frappe continua dono do sitemap/robots público nesta etapa (o do Next é 15 URLs contra ~336 reais; trocar agora seria regressão) |
| ROLLBACK | PASS -- mecanismo simples (remover blocos `location` da allowlist + `nginx -s reload`), sem restauração de banco |
| STAGING PLAN | PASS -- requisitos e matriz de smoke test documentados (`37-staging-smoke-plan.md`); ambiente em si não criado (decisão de infraestrutura fora do escopo) |
| SECURITY | PASS -- nenhum dado pessoal no `dataLayer` (auditado especificamente pro formulário de contato); nenhum segredo novo introduzido |
| CONSOLE ERRORS | 0 (varredura completa das 15 rotas, depois de todas as mudanças desta fase) |

## Regressão (componentes compartilhados alterados: Header, Footer, Button, TextLink)

`check-overflow-global.mjs` rerodado depois das mudanças: `{
totalChecks: 90, overflowsFound: 0 }` -- nenhuma regressão visual.
Capturas de tela da barra de cookies (desktop/mobile, estado inicial e
painel aberto) conferem visualmente contra o padrão de produção.

## O que ainda fica como pré-requisito de infraestrutura (não desta fase)

Nenhum destes bloqueia a arquitetura ou o código -- bloqueiam só a
EXECUÇÃO real do cutover, e nenhum é responsabilidade de código:

1. Exportar a config Nginx ativa do servidor pro Git (achado herdado,
   não desta fase -- `34-hybrid-routing-architecture.md`, seção 1).
2. Decidir onde o Next roda em produção (`NEXT HOSTING`/`NEXT ORIGIN`
   -- seção 13 do mesmo documento).
3. Criar o ambiente de staging/preview descrito em
   `37-staging-smoke-plan.md` (explicitamente fora do escopo: "não
   criar DNS nesta tarefa").
4. Confirmar com quem administra o GTM que as tags do container
   respeitam os 4 sinais de consentimento corretamente (o código
   garante que os sinais chegam certos -- o comportamento De CADA TAG
   dentro do container é responsabilidade de quem o administra, fora
   deste repositório, ver `docs/redesign/45-consent-remediation-
   result.md`, seção 9).

## CUTOVER READINESS: READY

Os 2 motivos que geraram `NOT READY` na Fase G.1 estão resolvidos com
evidência (código implementado + verificação empírica, não só
documentação). O que resta são pré-requisitos de infraestrutura fora do
escopo de qualquer fase de código (acesso SSH ao servidor, decisão de
hosting, criação de DNS) -- explicitamente registrados, não escondidos,
e nenhum deles exige nova arquitetura ou redesenho: são passos
operacionais de quem administra a infraestrutura, a serem executados
na fase de implementação real (não nesta, de arquitetura).

DEPLOY: NOT PERFORMED.

## Próximo passo

PARE. Não executar staging, deploy, DNS, Cloudflare ou Nginx de
produção sem autorização humana explícita -- conforme pedido no
fechamento da missão G.2.
