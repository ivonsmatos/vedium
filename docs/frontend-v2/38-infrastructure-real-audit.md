# Infraestrutura Real Audit (G.3)
**Data:** 2026-08-30

## 1. Visão Geral Atual (Produção)

A infraestrutura atual hospeda a plataforma LMS (Frappe) e o site institucional de forma monolítica no mesmo servidor, gerenciados pelo Nginx.

### Componentes Chave

*   **Hospedagem:** Servidor (VPS) único (`VEDIUM_SERVER`), gerenciado via SSH por chave.
*   **Docker Compose (`deploy/docker-compose.yml`):**
    *   `vedium-frappe` (Gunicorn na porta local 8000).
    *   `vedium-socketio` (Node na porta local 9000).
    *   `vedium-worker-*` e `vedium-scheduler` (Frappe background jobs).
    *   `vedium-mariadb` (MariaDB 10.6, sem porta exposta ao host).
    *   `vedium-redis-*` (Três instâncias Redis 7, protegidas por senha na rede interna).
*   **Proxy Reverso (Nginx no Host):**
    *   `app.vediums.com`: Proxy reverso para `127.0.0.1:8005` (porta mapeada do Gunicorn) e `/socket.io/` para `127.0.0.1:9000`.
    *   `vediums.com`: Hospedagem puramente estática. O Nginx serve arquivos HTML diretos do diretório `/opt/vedium/site`, sem proxy para o Frappe na raiz. Apenas os Web Manifest e Service Worker PWA (`/manifest.json`, `/sw.js`) fazem proxy para o backend Frappe.
*   **Deploy (CI/CD / Script):**
    *   O deploy é semi-automatizado via script `deploy-vedium.sh` (ou `.ps1`). Ele envia o `docker-compose.yml`, as configurações do Nginx (`vediums.com.conf` e `security-headers.conf`), constrói a imagem Docker `vedium-frappe-raven:v16` e reinicia os containers (`docker compose ... up -d --build`).

## 2. Pontos de Atenção para o Frontend Next.js

1.  **O Site Institucional Atual é Estático:** O Nginx em produção já serve `vediums.com` puramente como arquivos estáticos (`/opt/vedium/site`). O conteúdo dinâmico do site público que desenvolvemos na Fase G.1 (`/cursos`, `_language_ioruba_v2`, etc) estava rodando apenas via rotas do Frappe (ex: `app.vediums.com`).
2.  **Roteamento:** A transição do site estático (atual `vediums.com`) para o aplicativo Next.js (SSR/SSG) exigirá apenas mudar o bloco Nginx do `vediums.com` para realizar um `proxy_pass` para o container Next.js (e não mais servir diretório estático).
3.  **Portas de Rede:**
    *   Frappe usa a porta 8005 no host.
    *   Socket.IO usa a porta 9000 no host.
    *   O Nginx gerencia TLS/SSL via Certbot na porta 443 e faz o bypass HTTP -> HTTPS.
    *   O Next.js poderá rodar na porta 3000 do host, exposta a partir do Docker.

## 3. Conclusão da Auditoria

A infraestrutura Nginx é ideal para a Fase G.3. O Nginx já é o orquestrador do tráfego. Adicionar o roteamento híbrido (Next.js + Frappe) é tão simples quanto adicionar regras `location` explícitas no bloco de configuração do servidor do Nginx para enviar o tráfego de rotas específicas para um novo backend local (Next.js) em vez de `/opt/vedium/site` ou `127.0.0.1:8005`.
