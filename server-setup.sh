#!/bin/bash
# =====================================================
# COMANDOS PARA PREPARAR O SERVIDOR DE PRODUÇÃO
# Domínio: vediums.com
# Pré-requisitos:
#   - Servidor Ubuntu/Debian recém-provisionado
#   - Acesso SSH por chave (não usar senha)
#   - Usuário com sudo (não usar root direto)
# =====================================================

set -euo pipefail

DOMAIN="vediums.com"

echo "======================================================"
echo "🚀 VEDIUM SETUP - SERVIDOR DE PRODUÇÃO ($DOMAIN)"
echo "======================================================"

# 1. Atualizar sistema e instalar dependências
echo "📦 Instalando dependências..."
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y \
    nginx \
    docker.io docker-compose-v2 \
    certbot python3-certbot-nginx \
    ufw fail2ban \
    unattended-upgrades

# 2. Configurar Docker
echo "🐳 Configurando Docker..."
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"

# 3. Criar estrutura de diretórios
echo "📁 Criando diretórios..."
sudo mkdir -p /opt/vedium/{nginx,site,site/css,backups,logs}
sudo chown -R "$USER:$USER" /opt/vedium

# 4. Remover configuração padrão nginx
echo "🗑️ Removendo configuração padrão..."
sudo rm -f /etc/nginx/sites-enabled/default

# 5. Hardening SSH
echo "🔒 Aplicando hardening SSH..."
sudo sed -i \
    -e 's/^#\?PermitRootLogin .*/PermitRootLogin no/' \
    -e 's/^#\?PasswordAuthentication .*/PasswordAuthentication no/' \
    -e 's/^#\?PubkeyAuthentication .*/PubkeyAuthentication yes/' \
    /etc/ssh/sshd_config
sudo systemctl restart sshd

# 6. Firewall
echo "🔥 Configurando firewall..."
sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# 7. Fail2ban
echo "🛡️ Habilitando fail2ban..."
sudo systemctl enable --now fail2ban

# 8. Atualizações automáticas
echo "🔁 Habilitando unattended-upgrades..."
sudo dpkg-reconfigure -fnoninteractive unattended-upgrades

echo ""
echo "✅ SERVIDOR PREPARADO!"
echo "======================================================"
echo "📋 PRÓXIMAS ETAPAS:"
echo ""
echo "1. TRANSFERIR ARQUIVOS (use deploy-vedium.sh ou .ps1):"
echo "   • deploy/nginx/${DOMAIN}.conf  → /etc/nginx/sites-available/${DOMAIN}"
echo "   • deploy/docker-compose.yml    → /opt/vedium/docker-compose.yml"
echo "   • deploy/.env.example          → /opt/vedium/.env (e preencher!)"
echo "   • deploy/site/index.html       → /opt/vedium/site/index.html"
echo "   • vedium_core/.../vedium.css   → /opt/vedium/site/css/vedium.css"
echo ""
echo "2. ATIVAR NGINX:"
echo "   sudo ln -sf /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/${DOMAIN}"
echo "   sudo nginx -t && sudo systemctl restart nginx"
echo ""
echo "3. SUBIR CONTAINERS:"
echo "   cd /opt/vedium && docker compose up -d"
echo ""
echo "4. CONFIGURAR DNS:"
echo "   ${DOMAIN}     → IP_DESTE_SERVIDOR"
echo "   www.${DOMAIN} → IP_DESTE_SERVIDOR"
echo "   app.${DOMAIN} → IP_DESTE_SERVIDOR"
echo ""
echo "5. CONFIGURAR SSL (APÓS DNS PROPAGAR):"
echo "   sudo certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} -d app.${DOMAIN}"
echo "   sudo systemctl reload nginx"
echo "   sudo systemctl enable --now certbot.timer  # auto-renovação"
echo ""
echo "📊 VERIFICAÇÕES:"
echo "   systemctl status nginx docker"
echo "   docker compose ps"
echo "   curl -I https://${DOMAIN}"
echo "======================================================"
