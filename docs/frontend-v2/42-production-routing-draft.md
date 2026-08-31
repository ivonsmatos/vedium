# Draft do Roteamento de Produção Híbrido (G.3 / Cutover)
**Data:** 2026-08-30

## 1. Visão Geral

Este documento descreve o draft da configuração final a ser aplicada no arquivo `deploy/nginx/vediums.com.conf` (Produção Real) no dia do **Cutover**.

**O bloco principal `server { server_name vediums.com; ... }` perderá a referência de arquivos estáticos `/opt/vedium/site` e implementará a estratégia testada no Staging.**

## 2. Configuração Nginx (Draft)

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name vediums.com www.vediums.com;

    if ($host = www.vediums.com) { return 301 https://vediums.com$request_uri; }
    # ... SSL e Security Headers padrões ...

    # ------------------------------------------------------------------
    # ASSETS NEXT.JS (Acelerados por Proxy Cache se necessário, imutáveis)
    # ------------------------------------------------------------------
    location /_next/ {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # ------------------------------------------------------------------
    # ASSETS FRAPPE (Imagens de blog, scripts herdados)
    # ------------------------------------------------------------------
    location ~ ^/(assets|files|website_script.js)/ {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host app.vediums.com;
        proxy_hide_header Cache-Control;
        proxy_hide_header Expires;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # ------------------------------------------------------------------
    # LEGACY REDIRECTS (301)
    # ------------------------------------------------------------------
    location /metodologia { return 301 https://vediums.com/sobre.html; }
    location /app { return 301 https://app.vediums.com; }
    location /login { return 301 https://app.vediums.com/login; }
    location /lms { return 301 https://app.vediums.com/lms; }

    # ------------------------------------------------------------------
    # FALLBACK EXPLÍCITO FRAPPE (Páginas Frappe Intactas)
    # ------------------------------------------------------------------
    # Blog, páginas jurídicas, e API.
    location ~ ^/(blog|api/method|sobre.html|privacidade.html|termos.html) {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host app.vediums.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # PWA
    location = /sw.js {
        proxy_pass http://127.0.0.1:8005/assets/vedium_core/js/sw.js;
        proxy_set_header Host app.vediums.com;
        add_header Content-Type "application/javascript; charset=utf-8";
    }

    # ------------------------------------------------------------------
    # NEXT.JS CORE CATCH-ALL
    # ------------------------------------------------------------------
    # Home (/) e Cursos/Idiomas serão roteados para o Node.js.
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }
}
```
