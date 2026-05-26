#!/bin/bash
# Vedium — Deploy via git pull + rsync + bench migrate
# Uso: /opt/vedium/scripts/app-deploy.sh [--no-migrate]
#
# Pré-requisitos:
#   - Repositório clonado em /opt/vedium-src via deploy key SSH
#   - SSH config: Host github-vedium → IdentityFile ~/.ssh/vedium_deploy
#
set -euo pipefail

REPO_DIR="/opt/vedium-src"
APP_SRC="$REPO_DIR/vedium_core"
APP_DEST="/var/lib/docker/volumes/vedium_frappe-bench-data/_data/apps/vedium_core"
SITE="app.vediums.com"
COMPOSE_DIR="/opt/vedium"
LOG="/var/log/vedium-app-deploy.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

log "=== Iniciando deploy ==="

# 1. Git pull
log "Atualizando código do repositório..."
git -C "$REPO_DIR" fetch origin main
git -C "$REPO_DIR" reset --hard origin/main
COMMIT=$(git -C "$REPO_DIR" log --oneline -1)
log "Commit: $COMMIT"

# 2. Rsync app para o volume Docker
log "Sincronizando vedium_core para o volume..."
rsync -av --delete \
  --exclude="__pycache__" \
  --exclude="*.pyc" \
  --exclude=".git" \
  "$APP_SRC/" "$APP_DEST/"
log "Rsync concluído."

# 3. Bench migrate (a não ser que --no-migrate seja passado)
if [[ "${1:-}" != "--no-migrate" ]]; then
  log "Executando bench migrate..."
  cd "$COMPOSE_DIR"
  docker compose exec -T vedium-frappe bench --site "$SITE" migrate 2>&1 | tail -5
  log "Migrate concluído."
fi

log "=== Deploy finalizado com sucesso ==="
