# Pendente — 404 do PWA em `vediums.com/sw.js` e `/manifest.json`

**Status:** parcialmente corrigido dentro do repo (2026-07-01). A causa raiz
completa exige editar a config do nginx no servidor, que **não é versionada
em lugar nenhum do repo** — não mexi nela sozinho, conforme a regra de não
tocar infraestrutura sensível fora de código sem aprovação. Este documento
descreve exatamente o que falta mudar e onde.

## Causa raiz confirmada

O nginx do servidor (multi-tenant, serve vários projetos além do Vedium —
`syncrh`, `ecomed`, `vettaboss`, etc.) tem, no arquivo
`/etc/nginx/sites-available/vediums.com` (linkado em
`/etc/nginx/sites-enabled/vediums.com`), dois blocos `location` **em cada um
dos dois `server{}`** (`vediums.com`/`www.vediums.com` e `app.vediums.com`)
que interceptam `/sw.js` e `/manifest.json` **antes** do `location /` que
faz proxy para o Frappe:

```nginx
location = /sw.js {
    alias /opt/vedium/pwa/sw.js;
    add_header Content-Type "application/javascript; charset=utf-8";
    add_header Service-Worker-Allowed "/";
    add_header Cache-Control "no-cache, no-store, must-revalidate";
    expires 0;
}
location = /manifest.json {
    alias /opt/vedium/pwa/manifest.json;
    add_header Content-Type "application/manifest+json; charset=utf-8";
    add_header Cache-Control "no-cache";
}
```

O `alias` aponta para `/opt/vedium/pwa/`, uma pasta que **nunca existiu** no
host (confirmado via SSH: `ls /opt/vedium/pwa/` → `No such file or
directory`). O `/opt/vedium/` real só tem `site/` (publicado pelo
`deploy.yml`, step "Publish marketing site"), não `pwa/`. Resultado: nginx
serve 404 direto, sem nem repassar a requisição para o Frappe — confirmado
com `curl --resolve vediums.com:443:127.0.0.1 https://vediums.com/sw.js` →
`404` (testando a origem real, não edge/CDN).

Isso significa que **mesmo o fix que já existia no repo para `/sw.js` nunca
era alcançado**: existe desde 28/06/2026 um `vedium_core/vedium_core/www/sw.py`
que serve `/sw.js` corretamente via `website_route_rules` do Frappe
(`{"from_route": "/sw.js", "to_route": "sw"}` em `hooks.py`), e ele responde
`200` quando testado direto no gunicorn dentro do container — mas o nginx
intercepta a URL primeiro com o `alias` quebrado e a requisição nunca chega
no Frappe.

## O que já foi corrigido dentro do repo (não depende do nginx para existir,
mas também não resolve o 404 sozinho — ver seção seguinte)

1. **`vedium_core/vedium_core/www/manifest.py`** (novo, 2026-07-01) — mesmo
   padrão do `sw.py` já existente: serve `vedium_core/public/manifest.json`
   (branding correto, ícones corretos, azul `#2E6DA4`) como
   `application/manifest+json` via rota `{"from_route": "/manifest.json",
   "to_route": "manifest"}` em `hooks.py`. Sem isso, nem existia um jeito de
   o Frappe responder `/manifest.json` na raiz — o 404 seria garantido mesmo
   se o nginx fosse corrigido.
2. **`deploy/site/manifest.json`** — tinha branding completamente errado e
   obsoleto ("Vedium - Inteligência Cultural", verde `#166534`, que a marca
   proíbe). Corrigido para o branding atual (nome, descrição, azul
   `#2E6DA4`). Esse arquivo é servido estaticamente só para as duas páginas
   legadas que o nginx roteia com `root /opt/vedium/site` —
   `/termos.html` e `/privacidade.html` — que têm `<link rel="manifest"
   href="/manifest.json">` no `<head>`.
3. Confirmado que a home e as páginas do site principal (Frappe) **não
   dependem** de `/manifest.json` na raiz — usam
   `<link rel="manifest" href="/assets/vedium_core/vedium_assets/images/favicons/site.webmanifest">`,
   que já funciona (200, testado). O `/manifest.json` da raiz só importa hoje
   para as 2 páginas HTML legadas acima e para a instalabilidade "correta"
   do PWA a partir de qualquer rota que não seja a home.

## Por que isso NÃO resolve o 404 sozinho

Mesmo com `www/manifest.py` existindo, o **nginx continua interceptando
`/sw.js` e `/manifest.json` antes do proxy** por causa do `alias` para a
pasta inexistente. Ou seja: o 404 em produção **persiste** até alguém
corrigir a config do nginx no servidor.

## O que precisa mudar no nginx (fora do repo — não versionado em lugar
nenhum, decisão de infraestrutura)

Arquivo: `/etc/nginx/sites-available/vediums.com` no servidor
`45.151.122.234` (linkado em `/etc/nginx/sites-enabled/vediums.com`).

Há dois blocos `server {}` com o mesmo par de `location` problemático — um
para `server_name vediums.com www.vediums.com` (por volta da linha 38-49) e
outro idêntico para `server_name app.vediums.com` (por volta da linha
84-93). Em ambos, remover (ou apontar corretamente) os blocos:

```nginx
location = /sw.js {
    alias /opt/vedium/pwa/sw.js;
    ...
}
location = /manifest.json {
    alias /opt/vedium/pwa/manifest.json;
    ...
}
```

**Opção recomendada (mais simples e já resolve tudo):** apagar os dois
blocos `location = /sw.js` e `location = /manifest.json` inteiros em ambos
os `server{}`. Sem eles, essas URLs caem no `location /` (proxy para
`127.0.0.1:8005`, o Frappe/gunicorn) igual qualquer outra rota — e o Frappe
já sabe responder as duas graças às rotas `www/sw.py` e `www/manifest.py`
descritas acima (ambas já no repo, na branch main a partir deste commit).
Isso também elimina a manutenção de uma pasta `/opt/vedium/pwa/` que nunca
existiu.

**Opção alternativa (se por algum motivo quiserem servir via nginx direto,
sem passar pelo Frappe):** trocar o `alias` para apontar para os arquivos
reais publicados pelo `deploy.yml`, que ficam em `/opt/vedium/site/`:
```nginx
location = /sw.js       { alias /opt/vedium/site/sw.js; ... }
location = /manifest.json { alias /opt/vedium/site/manifest.json; ... }
```
Isso funcionaria porque `deploy/site/sw.js` e `deploy/site/manifest.json`
(corrigidos nesta mesma limpeza) já são publicados ali a cada deploy. Mas a
opção recomendada (deixar o Frappe responder) é preferível: evita duas
fontes de verdade para o mesmo arquivo e usa o padrão que o projeto já
adotou para `/sw.js`.

Depois de aplicar, validar com:
```
nginx -t && systemctl reload nginx
curl -skI https://vediums.com/sw.js
curl -skI https://vediums.com/manifest.json
curl -skI https://app.vediums.com/sw.js
curl -skI https://app.vediums.com/manifest.json
```
Todos devem responder `200`.

## Quem decide

Isso não é uma decisão de produto — é puramente técnico e de baixo risco
(remover um `alias` morto), mas mexe em infraestrutura compartilhada com
outros projetos no mesmo servidor (nginx multi-tenant). Por isso ficou fora
do fluxo normal de commit+push+deploy deste repo. Peço que um humano com
acesso ao servidor aplique a mudança acima (ou peça para eu aplicar, se
autorizado a editar `/etc/nginx/` diretamente).
