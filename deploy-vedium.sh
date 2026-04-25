#!/bin/bash
# =====================================================
# Vedium Production Deploy Script (Linux/WSL)
# =====================================================
#
# Variáveis necessárias (export antes de rodar, ou em ~/.vedium-deploy.env):
#   VEDIUM_SERVER=ip-ou-hostname
#   VEDIUM_USER=usuario-ssh-nao-root
# A autenticação é feita por chave SSH (configure ~/.ssh/config ou agente).
# =====================================================

set -euo pipefail

if [ -f "${HOME}/.vedium-deploy.env" ]; then
    # shellcheck disable=SC1090
    source "${HOME}/.vedium-deploy.env"
fi

SERVER="${VEDIUM_SERVER:?Defina VEDIUM_SERVER (export ou ~/.vedium-deploy.env)}"
USER="${VEDIUM_USER:?Defina VEDIUM_USER}"
DOMAIN="vediums.com"

echo "====================================================="
echo "       VEDIUM PRODUCTION DEPLOY"
echo "====================================================="
echo "Servidor: $SERVER"
echo "Domínio: $DOMAIN"
echo "====================================================="

echo "🔍 Verificando arquivos locais..."
REQUIRED_FILES=(
    "deploy/nginx/vediums.com.conf"
    "deploy/docker-compose.yml"
    "deploy/site/index.html"
    "vedium_core/vedium_core/public/css/vedium.css"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Arquivo não encontrado: $file"
        exit 1
    fi
done
echo "✅ Todos os arquivos encontrados"

ssh_exec() {
    local cmd="$1"
    local desc="$2"
    echo "🔄 $desc"
    ssh "$USER@$SERVER" "$cmd"
    echo "✅ Sucesso!"
}

send_file() {
    local local_path="$1"
    local remote_path="$2"
    local desc="$3"
    echo "📤 $desc ($local_path → $remote_path)"
    scp "$local_path" "$USER@$SERVER:$remote_path"
    echo "✅ Arquivo enviado!"
}

echo ""
echo "🛠️  ETAPA 1: PREPARAÇÃO DO SERVIDOR"
echo "==========================================="
ssh_exec "sudo mkdir -p /opt/vedium/{nginx,site,site/css,backups} && sudo chown -R $USER:$USER /opt/vedium" "Criando diretórios"
ssh_exec "sudo apt-get update && sudo apt-get install -y nginx docker.io docker-compose-v2 certbot python3-certbot-nginx" "Instalando dependências"
ssh_exec "sudo systemctl enable --now docker" "Habilitando Docker"

echo ""
echo "📦 ETAPA 2: ENVIO DE ARQUIVOS"
echo "==========================================="
ssh_exec "[ -f /etc/nginx/sites-available/$DOMAIN ] && sudo cp /etc/nginx/sites-available/$DOMAIN /opt/vedium/backups/${DOMAIN}.conf.backup-\$(date +%Y%m%d-%H%M%S) || true" "Backup nginx"
send_file "deploy/nginx/${DOMAIN}.conf"   "/opt/vedium/nginx/${DOMAIN}.conf"  "Configuração nginx"
send_file "deploy/docker-compose.yml"     "/opt/vedium/docker-compose.yml"    "Docker compose"
send_file "deploy/site/index.html"        "/opt/vedium/site/index.html"       "Site principal"
send_file "vedium_core/vedium_core/public/css/vedium.css" "/opt/vedium/site/css/vedium.css" "CSS compilado"

echo ""
echo "🌐 ETAPA 3: CONFIGURAÇÃO NGINX"
echo "==========================================="
ssh_exec "sudo cp /opt/vedium/nginx/${DOMAIN}.conf /etc/nginx/sites-available/${DOMAIN}" "Configurando nginx"
ssh_exec "sudo ln -sf /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/${DOMAIN}" "Habilitando site"
ssh_exec "sudo rm -f /etc/nginx/sites-enabled/default" "Removendo default"
ssh_exec "sudo nginx -t" "Testando nginx"
ssh_exec "sudo systemctl restart nginx" "Reiniciando nginx"

echo ""
echo "🐳 ETAPA 4: DOCKER CONTAINERS"
echo "==========================================="
ssh_exec "cd /opt/vedium && docker compose up -d" "Iniciando containers"
ssh_exec "cd /opt/vedium && docker compose ps" "Status containers"

echo ""
echo "✅ DEPLOY CONCLUÍDO!"
echo "==========================================="
echo "Site: http://${DOMAIN} (sem SSL ainda)"
echo "LMS: http://app.${DOMAIN}:8005"
echo ""
echo "⚠️  PRÓXIMOS PASSOS MANUAIS:"
echo "1. Configure DNS: ${DOMAIN} -> $SERVER"
echo "2. Execute: sudo certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} -d app.${DOMAIN}"
echo "3. Teste:   https://${DOMAIN}"
