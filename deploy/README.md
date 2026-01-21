# Vedium LMS - Deploy

Este diretório contém toda a configuração necessária para deploy do Vedium LMS em produção.

## 📁 Estrutura

```
deploy/
├── docker-compose.yml      # Orquestração de containers
├── nginx/
│   └── vediums.com.conf    # Configuração NGINX completa
├── scripts/
│   ├── backup.sh           # Backup automático criptografado
│   ├── deploy.sh           # Script de deploy
│   ├── security-monitor.sh # Monitoramento de segurança
│   ├── audit-log.sh        # Configuração de auditoria LGPD
│   └── ativar-ssl.sh       # Ativação SSL Let's Encrypt
├── site/                   # Site estático institucional
│   ├── index.html
│   ├── sobre.html
│   ├── css/vedium.css
│   ├── images/
│   ├── manifest.json
│   └── sw.js
├── SECURITY.md             # Documentação de segurança
├── .env.example            # Template de variáveis de ambiente
└── README.md               # Este arquivo
```

## 🚀 Deploy Rápido

### 1. Preparação do Servidor

```bash
# Conecte ao servidor
ssh root@45.151.122.234

# Clone ou copie o repositório
git clone https://github.com/vedium-global/vedium.git /opt/vedium
# OU
scp -r . root@45.151.122.234:/opt/vedium/
```

### 2. Configuração

```bash
cd /opt/vedium

# Copie e edite o arquivo de ambiente
cp deploy/.env.example deploy/.env
nano deploy/.env

# Copie a configuração NGINX
cp deploy/nginx/vediums.com.conf /etc/nginx/sites-available/vediums.com
ln -sf /etc/nginx/sites-available/vediums.com /etc/nginx/sites-enabled/

# Teste e recarregue NGINX
nginx -t && systemctl reload nginx
```

### 3. Docker Containers

```bash
cd /opt/vedium

# Inicie os containers
docker-compose -f deploy/docker-compose.yml up -d

# Verifique status
docker ps --filter "name=vedium"
```

### 4. SSL Certificate

```bash
# Certifique-se que o DNS está apontando para o servidor
./deploy/scripts/ativar-ssl.sh
```

### 5. Site Estático

```bash
# Copie os arquivos do site
cp -r deploy/site/* /opt/vedium/site/
```

## 🔄 GitHub Actions CI/CD

### Secrets Necessários

Configure em `Settings > Secrets and variables > Actions`:

| Secret            | Descrição               | Exemplo                 |
| ----------------- | ----------------------- | ----------------------- |
| `SSH_PRIVATE_KEY` | Chave SSH privada       | `-----BEGIN OPENSSH...` |
| `SSH_KNOWN_HOSTS` | Fingerprint do servidor | `ssh-keyscan output`    |
| `DEPLOY_USER`     | Usuário SSH             | `root`                  |
| `DEPLOY_HOST`     | IP/hostname do servidor | `45.151.122.234`        |

### Gerar SSH Key

```bash
# No seu computador local
ssh-keygen -t ed25519 -C "github-actions@vediums.com" -f vedium-deploy-key

# Copie a chave pública para o servidor
ssh-copy-id -i vedium-deploy-key.pub root@45.151.122.234

# Use o conteúdo de vedium-deploy-key (privada) como SSH_PRIVATE_KEY
cat vedium-deploy-key

# Gere SSH_KNOWN_HOSTS
ssh-keyscan 45.151.122.234
```

### Workflows Disponíveis

| Workflow             | Trigger         | Descrição                |
| -------------------- | --------------- | ------------------------ |
| `deploy.yml`         | Push to main    | Deploy automático        |
| `security-check.yml` | Daily 06:00 UTC | Verificação de segurança |
| `backup.yml`         | Daily 02:00 UTC | Backup automático        |

## 📊 Containers Docker

| Container             | Imagem               | Porta      | Descrição      |
| --------------------- | -------------------- | ---------- | -------------- |
| vedium-frappe         | frappe/bench:v5.22.6 | 8005, 9005 | Backend Frappe |
| vedium-mariadb        | mariadb:10.6         | 3307       | Banco de dados |
| vedium-redis-cache    | redis:7-alpine       | -          | Cache          |
| vedium-redis-queue    | redis:7-alpine       | -          | Fila de jobs   |
| vedium-redis-socketio | redis:7-alpine       | -          | WebSocket      |

## 🔒 Segurança

Veja [SECURITY.md](SECURITY.md) para:

- Configuração SSL/TLS
- Rate limiting
- Fail2ban
- Backups criptografados
- Compliance LGPD/GDPR

## 📝 Scripts

### backup.sh

```bash
# Backup completo (banco + arquivos)
./scripts/backup.sh

# Backups são salvos em /opt/vedium/backups/
# Retenção: 30 dias
# Criptografia: AES-256-CBC
```

### security-monitor.sh

```bash
# Executa verificação de segurança
./scripts/security-monitor.sh

# Verifica:
# - Status dos containers
# - Uso de disco/memória
# - Tentativas de login SSH
# - Validade do certificado SSL
# - Atualizações pendentes
```

### deploy.sh

```bash
# Deploy completo (backup + pull + restart)
sudo ./scripts/deploy.sh
```

## 🌐 URLs

| URL                     | Destino                             |
| ----------------------- | ----------------------------------- |
| https://vediums.com     | Site institucional (NGINX estático) |
| https://www.vediums.com | Redirect → vediums.com              |
| https://app.vediums.com | Frappe LMS (proxy port 8005)        |

## 📱 Credenciais Padrão

⚠️ **ALTERE IMEDIATAMENTE após deploy!**

| Serviço      | Usuário       | Senha         |
| ------------ | ------------- | ------------- |
| Frappe Admin | Administrator | `Vedium@2024` |
| MariaDB      | root          | Ver `.env`    |

## 🆘 Troubleshooting

### Containers não iniciam

```bash
docker-compose -f deploy/docker-compose.yml logs -f
```

### NGINX erro 502

```bash
# Verifique se Frappe está rodando
curl http://localhost:8005

# Verifique logs
docker logs vedium-frappe
```

### SSL não funciona

```bash
# Verifique DNS
dig vediums.com A

# Verifique certificado
ls -la /etc/letsencrypt/live/vediums.com/

# Renove manualmente
certbot renew --force-renewal
```

---

**Última atualização**: 2026-01-21
