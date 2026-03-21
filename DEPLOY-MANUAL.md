# =====================================================

# INSTRUÇÕES DE DEPLOY MANUAL - VEDIUM.COM

# =====================================================

# Servidor: ***REDACTED-IP***

# Usuário: root

# Senha: ***REDACTED-PASSWORD***

# =====================================================

## CONECTAR AO SERVIDOR

Abra um terminal SSH (PuTTY, Terminal ou outro cliente SSH):

```
ssh root@***REDACTED-IP***
# Senha: ***REDACTED-PASSWORD***
```

## ETAPA 1: PREPARAR SERVIDOR

```bash
# Atualizar sistema
apt-get update && apt-get upgrade -y

# Instalar dependências
apt-get install -y nginx docker.io docker-compose-v2 certbot python3-certbot-nginx

# Iniciar Docker
systemctl start docker
systemctl enable docker

# Criar diretórios
mkdir -p /opt/vedium/{nginx,site,site/css,backups}
```

## ETAPA 2: CONFIGURAR NGINX

```bash
# Remover configuração padrão
rm -f /etc/nginx/sites-enabled/default

# Backup da configuração atual (se existir)
if [ -f /etc/nginx/sites-available/vedium.com ]; then
    cp /etc/nginx/sites-available/vedium.com /opt/vedium/backups/vedium.com.conf.backup-$(date +%Y%m%d-%H%M%S)
fi
```

## Use os arquivos locais:

- deploy/nginx/vedium.com.conf → /etc/nginx/sites-available/vedium.com
- deploy/docker-compose.yml → /opt/vedium/docker-compose.yml
- deploy/site/index.html → /opt/vedium/site/index.html
- vedium_core/vedium_core/public/css/vedium.css → /opt/vedium/site/css/vedium.css

## ETAPA 3: ATIVAR NGINX

```bash
# Ativar site
ln -sf /etc/nginx/sites-available/vedium.com /etc/nginx/sites-enabled/vedium.com

# Testar configuração
nginx -t

# Reiniciar nginx
systemctl restart nginx
```

## ETAPA 4: INICIAR DOCKER

```bash
cd /opt/vedium
docker compose up -d
docker compose ps
```

## ETAPA 5: CONFIGURAR SSL (DEPOIS DO DNS)

```bash
# Configurar Let's Encrypt
certbot --nginx -d vedium.com -d www.vedium.com -d app.vedium.com

# Reiniciar nginx
systemctl restart nginx
```

## VERIFICAÇÕES

```bash
# Status dos serviços
systemctl status nginx
systemctl status docker

# Logs se houver problemas
journalctl -u nginx -f
docker compose logs -f
```

## PRÓXIMOS PASSOS:

1. ✅ Preparar servidor (execute comandos acima)
2. 🔄 Enviar arquivos (usar SCP ou copiar manualmente)
3. ⚠️ Configurar DNS: vedium.com → ***REDACTED-IP***
4. 🔒 Configurar SSL com certbot
5. 🧪 Testar site final

## TESTES FINAIS:

- http://vedium.com (site principal)
- http://app.vedium.com:8005 (LMS temporário)
- https://vedium.com (após SSL)
- https://app.vedium.com (após SSL)
