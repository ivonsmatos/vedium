#!/bin/bash
# =============================================================
# Vedium — Script de Backup com restic
# Compliance: LGPD/GDPR
# Author: Vedium Global Education
# Última revisão: 2026-05-25 (P0.2 Sprint)
#
# Dependências no host:
#   - restic >= 0.16  (apt install restic)
#   - docker >= 24
#
# Variáveis de ambiente necessárias (via .env ou systemd):
#   RESTIC_REPOSITORY  — ex: s3:https://s3.us-east-1.wasabisys.com/vedium-backup
#   RESTIC_PASSWORD    — senha de criptografia (gerada com openssl rand -base64 32)
#   AWS_ACCESS_KEY_ID  — credencial do bucket Wasabi/R2
#   AWS_SECRET_ACCESS_KEY
#   As credenciais do banco são lidas do site_config.json do Frappe.
#   TELEGRAM_BOT_TOKEN (opcional) — alertas de falha
#   TELEGRAM_CHAT_ID   (opcional)
# =============================================================
set -euo pipefail

LOG_FILE="${LOG_FILE:-/var/log/vedium-backup.log}"
COMPOSE_DIR="${COMPOSE_DIR:-/opt/vedium}"
SITE_NAME="${FRAPPE_SITE_NAME:-app.vediums.com}"
DUMP_TMP="/tmp/vedium-mariadb-dump.sql.gz"
SITE_CONFIG_PATH="${SITE_CONFIG_PATH:-/var/lib/docker/volumes/vedium_vedium-sites/_data/${SITE_NAME}/site_config.json}"

# ------------------------------------------------------------------
# Funções utilitárias
# ------------------------------------------------------------------
log()   { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [BACKUP] $*" | tee -a "$LOG_FILE"; }
err()   { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [ERROR]  $*" | tee -a "$LOG_FILE" >&2; }
alert() {
    err "$*"
    if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=🔴 [Vedium Backup] $*" \
            --max-time 10 || true
    fi
}
notify_ok() {
    log "$*"
    if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
            --data-urlencode "text=✅ [Vedium Backup] $*" \
            --max-time 10 || true
    fi
}

# Impede dois backups simultâneos (por exemplo, cron + execução manual) e
# garante a remoção do dump temporário mesmo quando o processo é interrompido.
exec 9>/var/lock/vedium-backup.lock
if ! flock -n 9; then
    log "Outro backup já está em execução; encerrando sem iniciar uma cópia concorrente."
    exit 0
fi
trap 'rm -f "${DUMP_TMP}"' EXIT

# ------------------------------------------------------------------
# Validar dependências e variáveis
# ------------------------------------------------------------------
for cmd in restic docker curl python3 flock; do
    command -v "$cmd" >/dev/null 2>&1 || { alert "Dependência ausente: $cmd"; exit 1; }
done

for var in RESTIC_REPOSITORY RESTIC_PASSWORD; do
    [[ -n "${!var:-}" ]] || { alert "Variável de ambiente ausente: $var"; exit 1; }
done

# Inicializar repositório restic se ainda não existir
if ! restic snapshots &>/dev/null; then
    log "Inicializando repositório restic em ${RESTIC_REPOSITORY}..."
    restic init || { alert "Falha ao inicializar repositório restic"; exit 1; }
fi

log "=== Iniciando backup Vedium (restic) ==="
BACKUP_FAILED=0

if [[ ! -r "${SITE_CONFIG_PATH}" ]]; then
    alert "site_config.json não encontrado: ${SITE_CONFIG_PATH}"
    exit 1
fi

mapfile -t DB_CREDENTIALS < <(python3 - "${SITE_CONFIG_PATH}" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    config = json.load(handle)
print(config["db_name"])
print(config["db_password"])
PY
)
DB_NAME="${DB_CREDENTIALS[0]:-}"
DB_PASSWORD="${DB_CREDENTIALS[1]:-}"
[[ -n "${DB_NAME}" && -n "${DB_PASSWORD}" ]] || {
    alert "Credenciais do banco ausentes em ${SITE_CONFIG_PATH}"
    exit 1
}

# ------------------------------------------------------------------
# 1. Dump MariaDB → arquivo temporário (single-transaction: zero downtime)
# ------------------------------------------------------------------
log "Fazendo dump do MariaDB..."
if docker exec vedium-mariadb mariadb-dump \
        -u "${DB_NAME}" \
        -p"${DB_PASSWORD}" \
        "${DB_NAME}" \
        --single-transaction \
        --routines \
        --triggers \
        --events \
        2>/dev/null | gzip > "${DUMP_TMP}"; then
    log "Dump concluído: ${DUMP_TMP}"
else
    alert "Falha no dump do MariaDB"
    BACKUP_FAILED=1
fi

# ------------------------------------------------------------------
# 2. Backup via restic (MariaDB dump + volumes Frappe + configs)
# ------------------------------------------------------------------
log "Enviando para repositório restic: ${RESTIC_REPOSITORY}..."

BACKUP_PATHS=("${DUMP_TMP}")

# O cron roda como root, então o Restic pode ler o volume diretamente.
# Isso evita duplicar vários GB em /tmp antes de cada backup.
FRAPPE_BENCH_VOLUME="${FRAPPE_BENCH_VOLUME:-vedium_frappe-bench-v16}"
FRAPPE_VOLUME_PATH="/var/lib/docker/volumes/${FRAPPE_BENCH_VOLUME}/_data"
if [[ -d "${FRAPPE_VOLUME_PATH}" ]]; then
    BACKUP_PATHS+=("${FRAPPE_VOLUME_PATH}")
else
    alert "Volume Frappe não encontrado: ${FRAPPE_VOLUME_PATH}"
    BACKUP_FAILED=1
fi

# Configs e nginx (se existirem)
[[ -d "${COMPOSE_DIR}" ]]               && BACKUP_PATHS+=("${COMPOSE_DIR}")
[[ -f "/etc/nginx/sites-available/vediums.com" ]] && \
    BACKUP_PATHS+=("/etc/nginx/sites-available/vediums.com")

if restic backup \
        --tag "vedium,daily" \
        --tag "site:${SITE_NAME}" \
        --verbose \
        "${BACKUP_PATHS[@]}"; then
    log "Backup restic concluído com sucesso"
else
    alert "Falha no backup restic"
    BACKUP_FAILED=1
fi

# ------------------------------------------------------------------
# 3. Retenção: manter 30 dias de snapshots diários, 12 mensais
# ------------------------------------------------------------------
log "Aplicando política de retenção..."
restic forget \
    --keep-daily 30 \
    --keep-monthly 12 \
    --tag "vedium" \
    --prune \
    --verbose || {
    alert "Falha na política de retenção restic"
    BACKUP_FAILED=1
}

# ------------------------------------------------------------------
# 4. Verificar integridade do snapshot mais recente
# ------------------------------------------------------------------
log "Verificando integridade do último snapshot..."
restic check --read-data-subset=5% || {
    alert "Verificação de integridade restic falhou — revisar repositório"
    BACKUP_FAILED=1
}

# ------------------------------------------------------------------
# 5. Limpeza de arquivos temporários
# ------------------------------------------------------------------
rm -f "${DUMP_TMP}"

# ------------------------------------------------------------------
# 6. Alerta de espaço em disco
# ------------------------------------------------------------------
DISK_USED_PCT=$(df "${COMPOSE_DIR:-/}" | tail -1 | awk '{print $5}' | tr -d '%')
if [[ "${DISK_USED_PCT}" -gt 85 ]]; then
    alert "Disco em ${DISK_USED_PCT}% de uso no host — atenção imediata necessária"
fi

# ------------------------------------------------------------------
# Resumo final
# ------------------------------------------------------------------
SNAP_COUNT=$(restic snapshots --tag "vedium" --json 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
if [[ "${BACKUP_FAILED}" -eq 0 ]]; then
    notify_ok "Backup diário concluído. Snapshots: ${SNAP_COUNT}. Disco: ${DISK_USED_PCT}% usado."
    exit 0
else
    alert "Backup concluído COM FALHAS. Verificar log: ${LOG_FILE}"
    exit 1
fi
