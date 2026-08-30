# 37 — Plano de staging/preview (Fase G.2, Parte B)

Requisitos para a PRÓXIMA fase (implementação real). Nenhum DNS foi
criado nesta fase (missão, seção 37: "Não criar DNS nesta tarefa").

## 1. Requisitos do ambiente

| Requisito | Motivo |
|---|---|
| HTTPS | Mesmo em preview -- GTM/Consent Mode/formulário real (que chama `app.vediums.com`) esperam origem segura; testar em HTTP mascararia bugs de mixed-content |
| `noindex` | `X-Robots-Tag: noindex` no header HTTP (não só meta tag -- cobre também assets/JSON) em TODAS as respostas do ambiente de preview, sem exceção |
| `robots.txt` protegido | `Disallow: /` para qualquer host que não seja `vediums.com` -- já é o comportamento real de `frontend/src/app/robots.ts` (Fase G.1), confirmado funcionando; só precisa continuar assim |
| GTM em modo de teste | Usar o modo "Preview" nativo do próprio GTM (aponta pro mesmo container `GTM-P6Q2FXLK`, sem criar um container separado) -- não inventar um container de teste paralelo, que divergiria do real |
| Next + Frappe coexistindo | O preview precisa reproduzir a MESMA arquitetura de proxy híbrido de `34-hybrid-routing-architecture.md`, não só o Next isolado -- senão o teste não valida o que realmente vai pra produção (links cross-backend, formulário indo pro Frappe real, etc.) |

## 2. Onde

Duas opções, ambas válidas, a decidir por quem administra a
infraestrutura (não decidido aqui):

- **Subdomínio de staging** (ex.: `preview.vediums.com` ou
  `next-staging.vediums.com`) -- exige 1 registro DNS novo + certificado
  TLS, mas testa a URL pública real mais de perto.
- **Porta isolada no mesmo host** (ex.: `https://<IP-do-servidor>:8443`
  atrás de autenticação básica) -- não exige DNS novo, mas o teste de
  Cloudflare/edge fica incompleto (o preview não passaria pelo Cloudflare
  real).

## 3. O formulário de contato em preview

`POST /api/contact` do Next preview aponta, hoje, pra
`https://app.vediums.com/api/method/vedium_core.public_funnel.
submit_public_intent` -- ou seja, **um teste em preview cria um Helpdesk
Ticket e um CRM Lead REAIS em produção**, não um ambiente isolado. Isso
precisa de decisão explícita antes do preview ir ao ar:

- Testar mesmo assim e limpar manualmente os registros de teste depois
  (mesmo padrão já usado pelo agente `billing-e2e-tester` para testes
  ponta-a-ponta em produção controlada), OU
  - Apontar temporariamente o preview pra um ambiente Frappe de
  staging, se existir um (não confirmado nesta fase -- não encontrei
  referência a um site Frappe de staging separado em `deploy/
  docker-compose.yml`).

Não decidido aqui -- fica como pré-requisito explícito antes de ligar o
preview, não como bloqueador desta fase de arquitetura.

## 4. Route Smoke Matrix (missão, seção 38)

Confirma que a decisão de roteamento (allowlist vs fallback) funciona
de fato, não só na teoria:

| Rota | Backend esperado | Como verificar |
|---|---|---|
| `/` | Next | `curl -I` -- checar header/marcador que só o Next emite (ex.: ausência de `X-Frappe-*`, presença de asset `/_next/`) |
| `/curso-de-ingles-online` | Next | idem |
| `/contato` | Next | idem + POST real no formulário (ambiente de teste, ver seção 3) |
| `/blog/<qualquer artigo != o migrado>` | Frappe | idem -- confirma que o fallback NÃO capturou blog por engano |
| `/curso/<slug de nivel>` | Frappe | idem |
| `/teste-de-nivel` | Frappe | idem |
| `/en/` | Frappe | idem |
| `app.vediums.com/login` | Frappe (inalterado) | confirma que o host separado nem passa pela allowlist |

Meta da missão (seção 38): **ROUTING ERRORS: 0** -- nenhuma dessas 8
combinações pode responder do backend errado.

## 5. Gate desta parte

| Campo | Resultado |
|---|---|
| STAGING PLAN | PASS -- requisitos e matriz de smoke test documentados; ambiente em si NÃO criado (decisão de infraestrutura fora do escopo desta fase) |
