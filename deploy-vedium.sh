#!/bin/bash
# =====================================================
# Vedium Production Deploy Script (Linux/WSL)
# =====================================================

set -e

SERVER="***REDACTED-IP***"
USER="root"
DOMAIN="vedium.com"

echo "====================================================="
echo "       VEDIUM PRODUCTION DEPLOY"
echo "====================================================="
echo "Servidor: $SERVER"
echo "Domínio: $DOMAIN"
echo "====================================================="

# Verificar arquivos necessários
echo "🔍 Verificando arquivos locais..."
REQUIRED_FILES=(
    "deploy/nginx/vedium.com.conf"
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

# Função para executar comandos SSH
ssh_exec() {
    local cmd="$1"
    local desc="$2"
    echo "🔄 $desc"
    echo "Executando: $cmd"
    ssh -o StrictHostKeyChecking=no $USER@$SERVER "$cmd"
    echo "✅ Sucesso!"
}

# Função para enviar arquivos
send_file() {
    local local_path="$1"
    local remote_path="$2" 
    local desc="$3"
    echo "📤 $desc"
    echo "Enviando: $local_path -> $remote_path"
    scp -o StrictHostKeyChecking=no "$local_path" $USER@$SERVER:"$remote_path"
    echo "✅ Arquivo enviado!"
}

echo ""
echo "🛠️  ETAPA 1: PREPARAÇÃO DO SERVIDOR"
echo "==========================================="

# Criar diretórios
ssh_exec "mkdir -p /opt/vedium/{nginx,site,site/css,backups}" "Criando diretórios"

# Instalar dependências
ssh_exec "apt-get update && apt-get install -y nginx docker.io docker-compose-v2 certbot python3-certbot-nginx" "Instalando dependências"

# Iniciar Docker
ssh_exec "systemctl start docker && systemctl enable docker" "Iniciando Docker"

echo ""
echo "📦 ETAPA 2: ENVIO DE ARQUIVOS"  
echo "==========================================="

# Backup atual
ssh_exec "[ -f /etc/nginx/sites-available/vedium.com ] && cp /etc/nginx/sites-available/vedium.com /opt/vedium/backups/vedium.com.conf.backup-\$(date +%Y%m%d-%H%M%S) || true" "Backup nginx"

# Enviar arquivos
send_file "deploy/nginx/vedium.com.conf" "/opt/vedium/nginx/vedium.com.conf" "Configuração nginx"
send_file "deploy/docker-compose.yml" "/opt/vedium/docker-compose.yml" "Docker compose"
send_file "deploy/site/index.html" "/opt/vedium/site/index.html" "Site principal"
send_file "vedium_core/vedium_core/public/css/vedium.css" "/opt/vedium/site/css/vedium.css" "CSS compilado"

echo ""
echo "🌐 ETAPA 3: CONFIGURAÇÃO NGINX"
echo "==========================================="

# Configurar nginx
ssh_exec "cp /opt/vedium/nginx/vedium.com.conf /etc/nginx/sites-available/vedium.com" "Configurando nginx"
ssh_exec "ln -sf /etc/nginx/sites-available/vedium.com /etc/nginx/sites-enabled/vedium.com" "Habilitando site" 
ssh_exec "rm -f /etc/nginx/sites-enabled/default" "Removendo default"

# Testar configuração
ssh_exec "nginx -t" "Testando nginx"
ssh_exec "systemctl restart nginx" "Reiniciando nginx"

echo ""
echo "🐳 ETAPA 4: DOCKER CONTAINERS"
echo "==========================================="

# Iniciar containers
ssh_exec "cd /opt/vedium && docker compose up -d" "Iniciando containers"
ssh_exec "cd /opt/vedium && docker compose ps" "Status containers"

echo ""
echo "✅ DEPLOY CONCLUÍDO!"
echo "==========================================="
echo "Site: http://vedium.com (sem SSL ainda)"
echo "LMS: http://app.vedium.com:8005"
echo ""
echo "⚠️  PRÓXIMOS PASSOS MANUAIS:"
echo "1. Configure DNS: vedium.com -> $SERVER" 
echo "2. Execute: certbot --nginx -d vedium.com -d www.vedium.com -d app.vedium.com"
echo "3. Teste: https://vedium.com"
echo ""
echo "Para configurar SSL, execute no servidor:"
echo "ssh $USER@$SERVER"
echo "certbot --nginx -d vedium.com -d www.vedium.com -d app.vedium.com"