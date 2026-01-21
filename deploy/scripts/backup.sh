#!/bin/bash
# Vedium LMS - Script de Backup Automático
# Compliance: LGPD/GDPR
# Author: Vedium Global Education
# Last Updated: 2026-01-21

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/opt/vedium/backups}"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
RETENTION_DAYS=${RETENTION_DAYS:-30}
LOG_FILE="${LOG_FILE:-/var/log/vedium-backup.log}"
ENCRYPTION_KEY="${BACKUP_ENCRYPTION_KEY:-VediumBackup2026Secure}"

# Logging function
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_FILE"
}

alert() {
    echo "[ALERT $(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_FILE"
    # Add webhook/email notification here if needed
}

log "=== Iniciando backup Vedium LMS ==="

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# 1. Backup MariaDB (encrypted)
log "Backup do banco de dados..."
docker exec vedium-mariadb mysqldump \
    -u root \
    -p"${MYSQL_ROOT_PASSWORD:-root}" \
    --all-databases \
    --single-transaction \
    --routines \
    --triggers \
    2>/dev/null | gzip | openssl enc -aes-256-cbc -salt -pbkdf2 -pass pass:"$ENCRYPTION_KEY" \
    > "$BACKUP_DIR/$DATE/mariadb_backup.sql.gz.enc"

if [ $? -eq 0 ]; then
    log "✅ Backup do banco de dados concluído"
else
    alert "❌ Erro no backup do banco de dados"
fi

# 2. Backup Docker volumes
log "Backup dos volumes Docker..."
docker run --rm \
    -v vedium_frappe-bench-data:/data:ro \
    -v "$BACKUP_DIR/$DATE":/backup \
    alpine tar czf /backup/frappe-bench-data.tar.gz -C /data .

if [ $? -eq 0 ]; then
    log "✅ Backup dos volumes concluído"
else
    alert "❌ Erro no backup dos volumes"
fi

# 3. Backup configurations
log "Backup das configurações..."
tar czf "$BACKUP_DIR/$DATE/configs.tar.gz" \
    /opt/vedium/docker-compose.yml \
    /etc/nginx/sites-available/vediums.com \
    2>/dev/null || true

# 4. Backup site files
log "Backup dos arquivos do site..."
tar czf "$BACKUP_DIR/$DATE/site-files.tar.gz" \
    /opt/vedium/site \
    2>/dev/null || true

# 5. Calculate checksums for integrity
log "Calculando checksums..."
cd "$BACKUP_DIR/$DATE"
sha256sum * > checksums.sha256

# 6. Clean old backups (retention policy)
log "Limpando backups antigos (>${RETENTION_DAYS} dias)..."
find "$BACKUP_DIR" -maxdepth 1 -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \; 2>/dev/null || true

# 7. Check available space
SPACE_LEFT=$(df -h "$BACKUP_DIR" | tail -1 | awk '{print $4}')
SPACE_USED_PCT=$(df "$BACKUP_DIR" | tail -1 | awk '{print $5}' | tr -d '%')

if [ "$SPACE_USED_PCT" -gt 85 ]; then
    alert "⚠️ Disco com ${SPACE_USED_PCT}% de uso! Espaço disponível: $SPACE_LEFT"
fi

log "Espaço disponível: $SPACE_LEFT"

# 8. Summary
BACKUP_SIZE=$(du -sh "$BACKUP_DIR/$DATE" | awk '{print $1}')
log "=== Backup concluído com sucesso ==="
log "Local: $BACKUP_DIR/$DATE"
log "Tamanho total: $BACKUP_SIZE"
log "Arquivos:"
ls -lh "$BACKUP_DIR/$DATE" | tail -n +2 | tee -a "$LOG_FILE"

# Exit success
exit 0
