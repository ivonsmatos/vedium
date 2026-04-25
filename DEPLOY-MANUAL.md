# 🚀 Deploy Manual — Vedium (vediums.com)

> **Atenção:** este documento NÃO contém credenciais. Senhas, IPs e tokens
> ficam apenas em `.env` (não versionado), no GitHub Secrets ou no gerenciador
> de senhas da equipe.

## Variáveis necessárias (definir no servidor antes do deploy)

| Nome              | Onde usar                       |
| ----------------- | ------------------------------- |
| `DEPLOY_HOST`     | IP/hostname do servidor         |
| `DEPLOY_USER`     | Usuário SSH (não-root)          |
| `SSH_PRIVATE_KEY` | Chave SSH (no GitHub Secrets)   |
| `SSH_KNOWN_HOSTS` | `ssh-keyscan vediums.com`       |
| `MYSQL_ROOT_PASSWORD` | Gerar: `openssl rand -base64 32` |
| `MYSQL_PASSWORD`  | Gerar: `openssl rand -base64 32` |
| `FRAPPE_ADMIN_PASSWORD` | Gerar: `openssl rand -base64 32` |

## Conectar ao servidor

```bash
ssh $DEPLOY_USER@$DEPLOY_HOST   # autenticação SOMENTE por chave SSH
```

## Etapa 1 — Preparar servidor (uma vez)

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y nginx docker.io docker-compose-v2 certbot python3-certbot-nginx ufw fail2ban
sudo systemctl enable --now docker

# Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Diretórios
sudo mkdir -p /opt/vedium/{nginx,site,site/css,backups}
sudo chown -R $USER:$USER /opt/vedium
```

## Etapa 2 — Hardening SSH

```bash
# Em /etc/ssh/sshd_config:
#   PermitRootLogin no
#   PasswordAuthentication no
#   PubkeyAuthentication yes
sudo systemctl restart sshd
```

## Etapa 3 — NGINX

Copiar:

- `deploy/nginx/vediums.com.conf` → `/etc/nginx/sites-available/vediums.com`
- `deploy/docker-compose.yml`     → `/opt/vedium/docker-compose.yml`
- `deploy/site/index.html`        → `/opt/vedium/site/index.html`
- `vedium_core/vedium_core/public/css/vedium.css` → `/opt/vedium/site/css/vedium.css`

```bash
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/vediums.com /etc/nginx/sites-enabled/vediums.com
sudo nginx -t
sudo systemctl restart nginx
```

## Etapa 4 — Docker

```bash
cd /opt/vedium
cp .env.example .env
nano .env   # preencher com as senhas geradas
docker compose up -d
docker compose ps
```

## Etapa 5 — SSL (após DNS apontar para o IP)

```bash
sudo certbot --nginx -d vediums.com -d www.vediums.com -d app.vediums.com
sudo systemctl reload nginx

# Auto-renovação
sudo systemctl enable --now certbot.timer
```

## Verificações

```bash
sudo systemctl status nginx docker
docker compose ps
sudo journalctl -u nginx -f
docker compose logs -f
```

## Testes finais

- https://vediums.com (site principal)
- https://app.vediums.com (LMS)
- https://www.vediums.com (deve redirecionar para vediums.com)
- `curl -I https://vediums.com` (deve retornar 200 + headers HSTS, X-Frame-Options)
- https://www.ssllabs.com/ssltest/analyze.html?d=vediums.com (alvo: A+)
