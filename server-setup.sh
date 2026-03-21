#!/bin/bash
# =====================================================
# COMANDOS PARA EXECUTAR NO SERVIDOR (45.151.122.234)
# Execute como root após conectar via SSH
# =====================================================

set -e

echo "======================================================"
echo "🚀 VEDIUM SETUP - SERVIDOR DE PRODUÇÃO"
echo "======================================================"

# ETAPA 1: Atualizar sistema e instalar dependências
echo "📦 Instalando dependências..."
apt-get update && apt-get upgrade -y
apt-get install -y nginx docker.io docker-compose-v2 certbot python3-certbot-nginx ufw fail2ban

# ETAPA 2: Configurar Docker
echo "🐳 Configurando Docker..."
systemctl start docker
systemctl enable docker
usermod -aG docker root

# ETAPA 3: Criar estrutura de diretórios
echo "📁 Criando diretórios..."
mkdir -p /opt/vedium/{nginx,site,site/css,backups,logs}
chown -R root:root /opt/vedium

# ETAPA 4: Backup nginx atual (se existir)
echo "💾 Backup configuração atual..."
if [ -f /etc/nginx/sites-available/vedium.com ]; then
    cp /etc/nginx/sites-available/vedium.com /opt/vedium/backups/vedium.com.conf.backup-$(date +%Y%m%d-%H%M%S)
fi

# ETAPA 5: Remover configuração padrão nginx
echo "🗑️ Removendo configuração padrão..."
rm -f /etc/nginx/sites-enabled/default

# ETAPA 6: Configurar firewall básico
echo "🔥 Configurando firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8005/tcp  # Temporário para LMS

# ETAPA 7: Configurar fail2ban
echo "🛡️ Configurando fail2ban..."
systemctl start fail2ban
systemctl enable fail2ban

echo ""
echo "✅ SERVIDOR PREPARADO!"
echo "======================================================"
echo "📋 PRÓXIMAS ETAPAS MANUAIS:"
echo ""
echo "1. TRANSFERIR ARQUIVOS:"
echo "   • deploy/nginx/vedium.com.conf → /etc/nginx/sites-available/vedium.com"
echo "   • deploy/docker-compose.yml → /opt/vedium/docker-compose.yml" 
echo "   • deploy/site/index.html → /opt/vedium/site/index.html"
echo "   • vedium_core/vedium_core/public/css/vedium.css → /opt/vedium/site/css/vedium.css"
echo ""
echo "2. EXECUTAR APÓS TRANSFERIR ARQUIVOS:"
echo "   ln -sf /etc/nginx/sites-available/vedium.com /etc/nginx/sites-enabled/vedium.com"
echo "   nginx -t && systemctl restart nginx"
echo "   cd /opt/vedium && docker compose up -d"
echo ""
echo "3. CONFIGURAR DNS:"
echo "   vedium.com → 45.151.122.234"
echo "   www.vedium.com → 45.151.122.234"  
echo "   app.vedium.com → 45.151.122.234"
echo ""
echo "4. CONFIGURAR SSL (APÓS DNS):"
echo "   certbot --nginx -d vedium.com -d www.vedium.com -d app.vedium.com"
echo "   systemctl restart nginx"
echo ""
echo "📊 VERIFICAÇÕES:"
echo "   systemctl status nginx"
echo "   systemctl status docker"
echo "   docker compose ps"
echo "   curl -I http://vedium.com"
echo ""
echo "🌐 TESTES FINAIS:"
echo "   http://vedium.com"
echo "   http://app.vedium.com:8005"
echo "   https://vedium.com (após SSL)"
echo "   https://app.vedium.com (após SSL)"
echo "======================================================"