#!/bin/bash
# Vedium LMS - Deploy Script
# Automated deployment from GitHub to production server
# Author: Vedium Global Education
# Last Updated: 2026-01-21

set -e

# ===========================================
# Configuration
# ===========================================
DEPLOY_DIR="/opt/vedium"
BACKUP_DIR="/opt/vedium/backups"
LOG_FILE="/var/log/vedium-deploy.log"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ===========================================
# Functions
# ===========================================
log() {
    echo -e "${GREEN}[$(date +"%Y-%m-%d %H:%M:%S")]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

# ===========================================
# Pre-deployment checks
# ===========================================
echo "========================================="
echo "   Vedium LMS - Deploy Script"
echo "   $(date)"
echo "========================================="
echo ""

log "Iniciando deploy..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "Execute como root: sudo ./deploy.sh"
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    error "Docker não está rodando!"
fi

# ===========================================
# 1. Backup current state
# ===========================================
log "Criando backup pré-deploy..."
mkdir -p "$BACKUP_DIR/pre-deploy-$TIMESTAMP"

# Backup configs
if [ -f "$DEPLOY_DIR/docker-compose.yml" ]; then
    cp "$DEPLOY_DIR/docker-compose.yml" "$BACKUP_DIR/pre-deploy-$TIMESTAMP/"
fi

# Backup site files
if [ -d "$DEPLOY_DIR/site" ]; then
    tar czf "$BACKUP_DIR/pre-deploy-$TIMESTAMP/site-backup.tar.gz" "$DEPLOY_DIR/site" 2>/dev/null || true
fi

log "✅ Backup criado em: $BACKUP_DIR/pre-deploy-$TIMESTAMP"

# ===========================================
# 2. Pull latest changes via app-deploy script
# ===========================================
if [ -x "/opt/vedium/scripts/app-deploy.sh" ]; then
    log "Atualizando código da aplicação via git pull..."
    /opt/vedium/scripts/app-deploy.sh
    log "✅ Código atualizado e migrate concluído"
elif [ -d "/opt/vedium-src/.git" ]; then
    log "Atualizando do Git (fallback)..."
    git -C /opt/vedium-src fetch origin main
    git -C /opt/vedium-src reset --hard origin/main
    log "✅ Código atualizado"
fi

# ===========================================
# 3. Update Docker containers
# ===========================================
log "Atualizando containers Docker..."
cd "$DEPLOY_DIR"

# Pull new images
docker-compose pull

# Restart containers with new images
docker-compose up -d --remove-orphans

log "✅ Containers atualizados"

# ===========================================
# 4. Update static site files
# ===========================================
if [ -d "$DEPLOY_DIR/deploy/site" ]; then
    log "Atualizando arquivos do site estático..."
    rsync -av --delete "$DEPLOY_DIR/deploy/site/" "$DEPLOY_DIR/site/"
    log "✅ Site estático atualizado"
fi

# ===========================================
# 5. Set permissions
# ===========================================
log "Configurando permissões..."
chown -R root:root "$DEPLOY_DIR"
chmod +x "$DEPLOY_DIR/deploy/scripts/"*.sh 2>/dev/null || true

# ===========================================
# 6. Reload NGINX
# ===========================================
if systemctl is-active --quiet nginx; then
    log "Recarregando NGINX..."
    nginx -t && systemctl reload nginx
    log "✅ NGINX recarregado"
fi

# ===========================================
# 7. Health check
# ===========================================
log "Verificando saúde dos serviços..."
sleep 5

# Check containers
RUNNING=$(docker ps --filter "name=vedium" --format "{{.Names}}" | wc -l)
if [ "$RUNNING" -lt 5 ]; then
    warn "Apenas $RUNNING containers rodando (esperado: 5)"
else
    log "✅ $RUNNING containers rodando"
fi

# Check websites
for URL in "https://vediums.com" "https://app.vediums.com"; do
    HTTP_CODE=$(curl -skI "$URL" -o /dev/null -w '%{http_code}' --max-time 10)
    if [ "$HTTP_CODE" == "200" ]; then
        log "✅ $URL - OK"
    else
        warn "$URL - HTTP $HTTP_CODE"
    fi
done

# ===========================================
# 8. Summary
# ===========================================
echo ""
echo "========================================="
log "✅ DEPLOY CONCLUÍDO COM SUCESSO!"
echo "========================================="
echo ""
echo "📋 Resumo:"
echo "   - Backup: $BACKUP_DIR/pre-deploy-$TIMESTAMP"
echo "   - Containers: $RUNNING rodando"
echo "   - Timestamp: $TIMESTAMP"
echo ""
echo "🔗 URLs:"
echo "   - Site: https://vediums.com"
echo "   - App:  https://app.vediums.com"
echo ""
echo "📜 Logs: $LOG_FILE"
