# 34 — Arquitetura de roteamento híbrido Next/Frappe (Fase G.2, Parte B)

Nenhuma configuração de produção foi alterada. Este documento é
arquitetura + exemplo dry-run, não execução.

## 1. Achado crítico que muda a premissa deste documento

Antes de desenhar qualquer proxy, é preciso saber o que existe hoje de
verdade -- e a resposta, já documentada numa fase anterior deste mesmo
projeto (`docs/redesign/baseline/infrastructure-gap.md`,
`docs/redesign/01-current-stack-audit.md`), é desconfortável:

- **A configuração Nginx ativa em produção NÃO ESTÁ VERSIONADA NESTE
  REPOSITÓRIO.** Os dois arquivos existentes (`deploy/nginx/
  vediums.com.conf`, `deploy/vediums.com.nginx`) descrevem `vediums.com`
  como site **estático** (`root /opt/vedium/site; try_files ...`) --
  isso é **incompatível** com a produção real, que serve `vediums.com`
  a partir do MESMO Frappe que serve `app.vediums.com`, via um
  mecanismo de **host-rewrite** (o Nginx real força `Host:
  app.vediums.com` nas requisições que chegam em `vediums.com`,
  confirmado por `X-Page-Name` e cookies de sessão Frappe na home
  pública, e pelo incidente real de 2026-06-02 documentado em memória de
  projeto). Os 2 arquivos `deploy/nginx/*` já foram classificados como
  "hipótese desatualizada, não config ativa" numa auditoria anterior.
- Isso significa: **eu não posso escrever um patch realista em cima da
  config real**, porque a config real não está neste repositório. O que
  segue abaixo é um **exemplo NOVO, construído a partir do mecanismo
  conhecido** (proxy reverso + host-rewrite pro Frappe), não uma edição
  do arquivo legado -- e continua sendo só um dry-run, não uma
  configuração pronta pra aplicar.
- **Pré-requisito real, não desta fase, mas bloqueador do cutover**:
  exportar a config Nginx ativa do servidor pro Git antes de qualquer
  corte de tráfego real. Sem isso, ninguém consegue revisar o diff real
  entre "antes" e "depois" -- só a intenção documentada aqui.

## 2. Regra arquitetural (missão, seção 15)

Nada de swap completo. `vediums.com` continua respondendo pelas MESMAS
~336 URLs que responde hoje; só uma allowlist pequena passa a ser
respondida pelo Next, tudo o resto continua exatamente como está:

```
                         PUBLIC DOMAIN
                         vediums.com
                              |
                    Cloudflare (inalterado)
                              |
                     Nginx (proxy reverso)
                    /                      \
        rota bate na allowlist      qualquer outra rota
         (ver 33-first-cutover-        (comportamento
          route-map.csv)                ATUAL, inalterado)
                |                              |
        Next origin (a decidir,        Frappe, via o MESMO
        ver seção 12)                  host-rewrite que já
                                        existe hoje
```

## 3. O que NÃO muda (missão, seções 16-18)

- **`app.vediums.com` inteiro** (login, LMS, checkout, Desk/CRM/
  Helpdesk, APIs) -- zero mudança. Nenhuma rota deste host entra na
  allowlist.
- **Blog** -- mesmo o hub (`/blog`) e 1 artigo já existirem no Next
  (Fase F.5), **nenhuma URL de blog entra na allowlist desta primeira
  etapa** (missão, seção 17, explícito: "mesmo que /blog index já exista
  visualmente no Next, não trocar produção ainda"). Motivo: só 1 dos 97
  artigos foi migrado -- trocar o `/blog` index route agora criaria uma
  experiência incompleta (hub apontando majoritariamente pra artigos que
  só existem no Frappe).
- **Páginas de nível de curso** (`/curso/<slug>`, ~18 URLs) -- o Next
  nunca as construiu; os pilares migrados (`/curso-de-ingles-online`
  etc.) já linkam pra elas normalmente, e esses links continuam
  funcionando como link cross-backend comum (ver seção 8).
- **Teste de nível, locale roots (`/en/` etc.), `/professores`** (já é
  301 pro `/sobre` em produção) -- fora do escopo desta etapa.

## 4. Allowlist do primeiro cutover

Ver `docs/frontend-v2/33-first-cutover-route-map.csv` -- 13 rotas exatas
(Home + 5 pilares de curso + B2B + Como Funciona + Sobre + Contato + 3
páginas legais). Todas com `safe_to_cutover: YES` na análise desta fase.
`/metodologia` fica marcada `NO` até o redirect 301 ser implementado
junto com o cutover (não antes, não depois).

## 5. Fallback (missão, seção 20-21)

Regra única, sem exceção: **se a URL não estiver explicitamente na
allowlist, vai pro Frappe.** Nada de `location / { Next }` com fallback
improvisado -- isso inverteria o risco (qualquer rota nova/esquecida
cairia no backend errado). O Nginx dry-run abaixo implementa a allowlist
como blocos `location =` (exact match) + 5 blocos de pilar de curso,
NUNCA um wildcard `location /` apontando pro Next.

## 6. Exemplo Nginx (dry-run, seção 36 -- NÃO aplicar)

```nginx
# ==========================================================
# EXEMPLO / DRY-RUN -- Fase G.2. NAO e a config ativa (que nao
# esta versionada, ver secao 1). Este bloco assume que ele
# seria inserido DENTRO do server{} real de vediums.com, ANTES
# do location / atual que faz o host-rewrite pro Frappe.
# ==========================================================

# Upstream do Next -- endereco fictício até a decisão de hosting
# (ver secao 12). Trocar quando NEXT_ORIGIN for definido.
upstream vedium_next {
    server 127.0.0.1:3000;
}

# --- Assets do Next (ver secao 7) ---
location /_next/ {
    proxy_pass http://vedium_next;
    proxy_set_header Host $host;
    proxy_cache_valid 200 30d;
    add_header Cache-Control "public, immutable";
}

# --- Allowlist exata (ver 33-first-cutover-route-map.csv) ---
location = / {
    proxy_pass http://vedium_next;
    include /etc/nginx/snippets/vedium-next-headers.conf;
}
location = /curso-de-ingles-online { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /curso-de-ioruba-online { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /portugues-para-estrangeiros { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /curso-de-espanhol-online { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /curso-de-hebraico-online { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /empresas { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /como-funciona { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /sobre { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /contato {
    proxy_pass http://vedium_next;
    include /etc/nginx/snippets/vedium-next-headers.conf;
    # POST /api/contact tambem precisa cair aqui -- e uma rota do
    # proprio Next (Route Handler), nao uma API do Frappe.
}
location = /api/contact { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /api/health { proxy_pass http://vedium_next; access_log off; }
location = /privacidade { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /termos { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }
location = /cancelamento-reembolso { proxy_pass http://vedium_next; include /etc/nginx/snippets/vedium-next-headers.conf; }

# /sitemap.xml e /robots.txt DELIBERADAMENTE FORA da allowlist nesta
# etapa -- o sitemap do Next so tem 15 URLs (14 estaticas + 1 artigo),
# contra as ~336 URLs reais do sitemap Frappe. Trocar agora seria uma
# REGRESSAO de SEO, nao uma melhoria. Ver 36-hybrid-sitemap-strategy.md.

# --- Tudo o mais: comportamento ATUAL, inalterado ---
# (o location / real, com o host-rewrite pro Frappe, continua
# depois destes blocos -- Nginx usa o location mais especifico
# primeiro, entao os `location =` acima sempre ganham da allowlist
# sem precisar tocar no bloco generico existente)
```

`vedium-next-headers.conf` (novo snippet, exemplo):

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_redirect off;
```

Note que este snippet **preserva** `Host: vediums.com` (não faz
host-rewrite) -- diferente do bloco Frappe, o Next não precisa que o
Host seja reescrito pra `app.vediums.com`, porque o Next não é
multi-tenant por host como o Frappe é. Isso é uma simplificação real a
favor do Next, não um risco.

## 7. Assets (missão, seção 22)

`/_next/*` (JS/CSS gerados pelo build), imagens em `/assets/vedium_core/
...` (Next usa os MESMOS caminhos que o Frappe já usa hoje, ver
`frontend/public/assets/vedium_core/`, incluindo os 2 scripts
vendorizados desta fase) e fontes precisam ser servidos pelo Next
origin, nunca pelo Frappe. Como os caminhos de imagem já são
intencionalmente idênticos aos de produção (decisão da Fase D em
diante), é preciso `location /assets/vedium_core/` também apontar pro
Next nas 13 rotas migradas -- ou aceitar que, por ora, essas imagens
sejam servidas 2x (uma cópia no Next, outra no Frappe, cada uma para seu
próprio conjunto de páginas). Recomendação: manter `/assets/
vedium_core/` servido pelo Frappe (como já é hoje) e o Next usando esse
MESMO caminho público (que já funciona, porque é o mesmo domínio) --
evita duplicar upload de imagem em 2 lugares. Só `/_next/` (exclusivo do
build Next) precisa de rota nova.

## 8. Next Link -- rota Next vs rota Frappe (missão, seção 23-24)

`next/link` (usado em `Button`/`TextLink`/navegação interna) faz
client-side navigation quando o destino é uma rota que o próprio Next
Router reconhece; para qualquer `href` que não seja uma rota do app
Next (ex.: `/curso/<slug>`, `/teste-de-nivel`, `/blog/<demais 96>`),
o React Router do Next não tem essa rota registrada -- o clique vira uma
navegação de página inteira (full page load) para essa URL, que o proxy
então encaminha pro Frappe normalmente, exatamente como um `<a href>`
comum funcionaria. Não é preciso nenhum código especial pra isso
funcionar -- é o comportamento padrão de uma SPA parcial dentro do mesmo
domínio. Verificado nesta fase: nenhum componente do Next tenta
`router.push()` para uma URL fora do próprio Next (checado
`PathfinderForm.tsx`, único lugar com `useRouter()` -- só navega pra
URLs da `PATHFINDER_MATRIX`, todas rotas reais do Next).

Sentido contrário (Frappe → Next): os templates Jinja não precisam ser
alterados nesta fase (missão, seção 24) -- como a URL pública não muda
(`/sobre` continua sendo `/sobre`), qualquer link existente no Frappe
que aponte pra uma dessas 13 rotas simplesmente passa a ser respondido
pelo Next depois do cutover, sem precisar editar nenhum `.html` Jinja.

## 9. Canonical (missão, seção 25)

Já garantido por construção, não é uma correção desta fase: todo
`page.tsx` migrado usa metadata gerada a partir de
`metadataBase: new URL("https://vediums.com")` (`app/layout.tsx`) --
nenhuma página emite canonical com host interno, localhost ou porta.
Confirmado nos crawls da Fase G.1 (`32-qa-global-findings.md`).

## 10. Cookies (missão, seção 26)

- **Consentimento** (`vedium_cookie_consent`, `vedium_cookie_preferences`):
  `localStorage`, mesma origem (`vediums.com`) nos dois backends --
  automaticamente compartilhado, sem configuração de proxy necessária
  (ver `35-gtm-next-contract.md`).
- **Sessão Frappe** (`sid`, CSRF): o Next não lê nem grava nenhum cookie
  de sessão Frappe -- as 13 páginas migradas são 100% públicas, sem
  estado de login. Nenhum risco de quebrar sessão do LMS.
- **Cookie domain**: não precisa mudar -- como tudo continua sob
  `vediums.com` (nenhuma migração de subdomínio), o domain do cookie
  (implícito, sem `Domain=` explícito na maioria dos casos) continua
  válido para os dois backends.

## 11. Headers, cache, health check, failure behavior (missão, seções 27-28, 31-32)

- **Headers a preservar**: `X-Forwarded-For`, `X-Forwarded-Proto`,
  `Host`, IP real -- replicados no exemplo da seção 6 (mesmo padrão já
  usado no bloco real de `app.vediums.com` neste mesmo tipo de arquivo).
- **Cache**: `/_next/static/*` pode ter cache longo e imutável (hash no
  nome do arquivo, como o Next já gera). `POST /api/contact` e qualquer
  API **nunca** devem ser cacheadas -- não incluídas em nenhum bloco de
  cache no exemplo acima. Páginas públicas (as 13 da allowlist) podem
  ter cache de borda curto (Cloudflare), mas isso é decisão de quem
  administra o Cloudflare, não implementado aqui.
- **Health checks separados**: `NEXT` -- `GET /api/health`, implementado
  nesta fase (`frontend/src/app/api/health/route.ts`), testado local
  (`200 {"status":"ok"}`, nenhum dado sensível). `FRAPPE` -- `/health`,
  já existe, confirmado no `deploy/nginx/vediums.com.conf` legado
  (`return 200 "OK"`). Nenhum dos dois expõe versão, stack trace ou
  configuração.
- **Failure behavior**: se o Next origin cair e o Frappe continuar de
  pé, a resposta correta é um erro 502/503 visível (ou o Nginx servindo
  uma página de erro estática), **não** um fallback automático
  silencioso pro Frappe pra essas 13 rotas -- porque a versão Frappe
  dessas páginas pode já estar desatualizada/diferente depois do
  cutover (mission, seção 32: "pode devolver versão antiga divergente
  sem controle"). Preferir indisponibilidade visível e rollback manual
  (seção 12) a uma resposta inconsistente sem ninguém perceber.

## 12. Rollback (atualiza `29-cutover-plan.md`)

Mecanismo mais simples possível: comentar/remover os blocos
`location = ...` da allowlist (seção 6) e recarregar o Nginx
(`nginx -s reload`, sem downtime). O `location /` genérico (host-rewrite
pro Frappe) volta a responder essas 13 URLs imediatamente, servindo o
conteúdo que já está lá (o Frappe nunca deixou de ter essas páginas --
elas só pararam de ser a resposta ativa). **Nenhuma restauração de
banco de dados envolvida** -- é puramente uma mudança de roteamento.

## 13. Origin -- decisões pendentes (missão, seção 34)

| Item | Status |
|---|---|
| NEXT HOSTING | **DECISION REQUIRED** -- não existe hoje nenhuma infraestrutura de produção para rodar o Next (`deploy/docker-compose.yml` só tem serviços Frappe/MariaDB/Redis). Precisa de: um processo Node rodando `next start` (ou export estático, a decidir), most provavelmente um novo container Docker no mesmo host/VPC que já roda o Frappe, atrás do mesmo Nginx |
| NEXT ORIGIN | **DECISION REQUIRED** -- endereço fictício usado no exemplo (`127.0.0.1:3000`) até essa decisão ser tomada |
| FRAPPE ORIGIN | **DOCUMENTADO** -- `127.0.0.1:8005` (Gunicorn), confirmado em `deploy/nginx/vediums.com.conf` (bloco de `app.vediums.com`) e consistente com o restante da infraestrutura Docker já documentada em memória de projeto |

## 14. Cloudflare / Nginx (missão, seções 35-36)

Não mudar nada agora. O roteamento por allowlist (seção 6) assume que a
camada que decide Next-vs-Frappe é o **Nginx** (é onde o host-rewrite
já acontece hoje, é o lugar natural para adicionar `location`s novos).
Não foi criado nenhum Cloudflare Worker -- não haveria motivo técnico
para isso quando o Nginx já cumpre esse papel, e criar uma segunda
camada de roteamento (Worker + Nginx) só aumentaria a superfície de
divergência. Antes de qualquer implementação real, a pessoa que
administra o Cloudflare/Nginx precisa (a) confirmar que o mecanismo
real ainda é "Nginx faz host-rewrite" (não mudou desde a última
auditoria) e (b) exportar a config ativa pro Git (seção 1).

## 15. SEO em arquitetura híbrida (missão, seção 42)

Google rastreia Next e Frappe no mesmo domínio sem problema, contanto
que cada URL tenha exatamente UMA resposta (nunca as duas ao mesmo
tempo). A allowlist por `location =` exata (seção 6) garante isso por
construção -- o Nginx só tem uma rota vencedora por URL, nunca as duas
simultaneamente. Nenhuma das 13 URLs migradas continua respondendo
pelo Frappe em paralelo depois do cutover.
