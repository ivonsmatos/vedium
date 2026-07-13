#!/bin/bash
# =============================================================
# Vedium — Script de Restore via restic
# Author: Vedium Global Education
# Última revisão: 2026-05-25 (P0.2 Sprint)
#
# USO:
#   ./restore.sh                          # Restaura último snapshot
#   ./restore.sh --snapshot <ID>          # Restaura snapshot específico
#   ./restore.sh --list                   # Lista snapshots disponíveis
#   ./restore.sh --dry-run                # Simula sem restaurar dados
#
# Variáveis de ambiente necessárias:
#   RESTIC_REPOSITORY  — mesmo que backup.sh
#   RESTIC_PASSWORD    — mesmo que backup.sh
#   AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
#   As credenciais do banco são lidas do site_config.json do Frappe.
# =============================================================
set -euo pipefail

LOG_FILE="${LOG_FILE:-/var/log/vedium-restore.log}"
COMPOSE_DIR="${COMPOSE_DIR:-/opt/vedium}"
RESTORE_TMP="/tmp/vedium-restore"
SNAPSHOT_ID="latest"
DRY_RUN=false
SITE_CONFIG_PATH="${SITE_CONFIG_PATH:-/var/lib/docker/volumes/vedium_vedium-sites/_data/${FRAPPE_SITE_NAME:-app.vediums.com}/site_config.json}"

# ------------------------------------------------------------------
# Funções utilitárias
# ------------------------------------------------------------------
log()  { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [RESTORE] $*" | tee -a "$LOG_FILE"; }
err()  { echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] [ERROR]   $*" | tee -a "$LOG_FILE" >&2; }
die()  { err "$*"; exit 1; }

usage() {
    cat <<EOF
Uso: $0 [opções]

Opções:
  --snapshot <ID>   Restaurar snapshot específico (padrão: latest)
  --list            Listar snapshots disponíveis e sair
  --dry-run         Simular restore sem alterar dados
  -h, --help        Exibir esta ajuda

Exemplos:
  $0                          # Restaura último snapshot
  $0 --snapshot abc12345      # Restaura snapshot específico
  $0 --list                   # Lista snapshots
  $0 --dry-run                # Testa sem alterar dados

Variáveis necessárias:
  RESTIC_REPOSITORY, RESTIC_PASSWORD
EOF
}

# ------------------------------------------------------------------
# Parsear argumentos
# ------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        --snapshot)   SNAPSHOT_ID="$2"; shift 2 ;;
        --list)
            echo "=== Snapshots restic disponíveis ==="
            restic snapshots --tag "vedium" --group-by tags
            exit 0 ;;
        --dry-run)    DRY_RUN=true; shift ;;
        -h|--help)    usage; exit 0 ;;
        *) die "Argumento desconhecido: $1. Use --help para ajuda." ;;
    esac
done

# ------------------------------------------------------------------
# Validar dependências e variáveis
# ------------------------------------------------------------------
for cmd in restic docker python3; do
    command -v "$cmd" >/dev/null 2>&1 || die "Dependência ausente: $cmd"
done

for var in RESTIC_REPOSITORY RESTIC_PASSWORD; do
    [[ -n "${!var:-}" ]] || die "Variável de ambiente ausente: $var"
done

[[ -r "${SITE_CONFIG_PATH}" ]] || die "site_config.json não encontrado: ${SITE_CONFIG_PATH}"
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
[[ -n "${DB_NAME}" && -n "${DB_PASSWORD}" ]] || die "Credenciais do banco ausentes"

# ------------------------------------------------------------------
# Confirmação interativa (pular se --dry-run)
# ------------------------------------------------------------------
if [[ "${DRY_RUN}" == false ]]; then
    log "⚠️  ATENÇÃO: Este procedimento irá sobrescrever dados de PRODUÇÃO."
    log "    Snapshot alvo: ${SNAPSHOT_ID}"
    log "    Destino: ${COMPOSE_DIR}"
    read -r -p "    Digite 'CONFIRMAR' para prosseguir: " CONFIRM
    [[ "${CONFIRM}" == "CONFIRMAR" ]] || die "Restore cancelado pelo usuário."
fi

log "=== Iniciando restore Vedium (snapshot: ${SNAPSHOT_ID}) ==="
[[ "${DRY_RUN}" == true ]] && log "[DRY-RUN] Nenhum dado será alterado."

# ------------------------------------------------------------------
# 1. Baixar snapshot para diretório temporário
# ------------------------------------------------------------------
rm -rf "${RESTORE_TMP}"
mkdir -p "${RESTORE_TMP}"

log "Extraindo snapshot ${SNAPSHOT_ID} para ${RESTORE_TMP}..."
if [[ "${DRY_RUN}" == true ]]; then
    # Versões anteriores do Restic não oferecem `restore --dry-run`.
    # Listar a árvore valida acesso, senha, snapshot e metadados sem gravar dados.
    restic ls "${SNAPSHOT_ID}" >/dev/null
    log "[DRY-RUN] Snapshot acessível e árvore validada. Nenhum dado alterado."
    exit 0
fi

restic restore "${SNAPSHOT_ID}" --target "${RESTORE_TMP}" --verbose \
    || die "Falha ao extrair snapshot restic"

log "Snapshot extraído com sucesso em ${RESTORE_TMP}"

# ------------------------------------------------------------------
# 2. Parar containers app/workers (manter banco rodando para restore)
# ------------------------------------------------------------------
log "Parando containers Frappe (mantendo banco online)..."
cd "${COMPOSE_DIR}"
docker compose stop \
    vedium-frappe \
    vedium-socketio \
    vedium-worker-default \
    vedium-worker-short \
    vedium-worker-long \
    vedium-scheduler \
    || log "Aviso: alguns containers já estavam parados"

# ------------------------------------------------------------------
# 3. Restaurar dump MariaDB (se existir no snapshot)
# ------------------------------------------------------------------
DUMP_FILE=$(find "${RESTORE_TMP}/tmp" -name "vedium-mariadb-dump.sql.gz" 2>/dev/null | head -1 || true)

if [[ -f "${DUMP_FILE}" ]]; then
    log "Restaurando banco de dados MariaDB..."

    # Criar backup de segurança do banco atual antes de sobrescrever
    SAFE_DUMP="/tmp/vedium-pre-restore-$(date +%Y%m%d%H%M%S).sql.gz"
    log "Criando backup de segurança do banco atual em ${SAFE_DUMP}..."
    docker exec vedium-mariadb mariadb-dump \
        -u "${DB_NAME}" -p"${DB_PASSWORD}" \
        "${DB_NAME}" --single-transaction 2>/dev/null | gzip > "${SAFE_DUMP}" \
        || log "Aviso: não foi possível criar backup de segurança do banco atual"

    # Restaurar
    zcat "${DUMP_FILE}" | docker exec -i vedium-mariadb mariadb \
        -u "${DB_NAME}" -p"${DB_PASSWORD}" "${DB_NAME}" \
        || die "Falha ao restaurar MariaDB"
    log "Banco restaurado com sucesso"
else
    log "Aviso: dump MariaDB não encontrado no snapshot — banco não alterado"
fi

# ------------------------------------------------------------------
# 4. Restaurar o volume Frappe ativo
# ------------------------------------------------------------------
FRAPPE_BENCH_VOLUME="${FRAPPE_BENCH_VOLUME:-vedium_frappe-bench-v16}"
FRAPPE_BENCH_RESTORE="${RESTORE_TMP}/var/lib/docker/volumes/${FRAPPE_BENCH_VOLUME}/_data"

# Compatibilidade com snapshots produzidos pela versão antiga do backup.
if [[ ! -d "${FRAPPE_BENCH_RESTORE}" ]]; then
    FRAPPE_BENCH_RESTORE="${RESTORE_TMP}/tmp/vedium-frappe-bench"
fi

if [[ -d "${FRAPPE_BENCH_RESTORE}" ]]; then
    log "Restaurando volume ${FRAPPE_BENCH_VOLUME}..."
    docker run --rm \
        -v "${FRAPPE_BENCH_VOLUME}:/data" \
        -v "${FRAPPE_BENCH_RESTORE}":/source:ro \
        alpine sh -c "rm -rf /data/* && cp -a /source/. /data/" \
        || die "Falha ao restaurar volume ${FRAPPE_BENCH_VOLUME}"
    log "Volume ${FRAPPE_BENCH_VOLUME} restaurado"
else
    log "Aviso: diretório frappe-bench não encontrado no snapshot — volume não alterado"
fi

# ------------------------------------------------------------------
# 5. Reiniciar containers
# ------------------------------------------------------------------
log "Reiniciando todos os containers..."
cd "${COMPOSE_DIR}"
docker compose up -d \
    || die "Falha ao iniciar containers após restore"

# ------------------------------------------------------------------
# 6. Verificação de saúde pós-restore
# ------------------------------------------------------------------
log "Aguardando containers ficarem saudáveis (60s)..."
sleep 60

HEALTH_STATUS=$(docker inspect --format='{{.State.Health.Status}}' vedium-frappe 2>/dev/null || echo "unknown")
if [[ "${HEALTH_STATUS}" == "healthy" ]]; then
    log "Container vedium-frappe: healthy ✅"
else
    log "Container vedium-frappe: ${HEALTH_STATUS} ⚠️ — verificar logs com: docker logs vedium-frappe"
fi

# Teste de ping HTTP
if curl -sf http://localhost:8005/api/method/ping >/dev/null 2>&1; then
    log "API respondendo: OK ✅"
else
    log "API não respondendo ainda — pode estar inicializando. Tente em 2 minutos."
fi

# ------------------------------------------------------------------
# 7. Limpeza
# ------------------------------------------------------------------
rm -rf "${RESTORE_TMP}"

log "=== Restore concluído ==="
log "    Snapshot restaurado: ${SNAPSHOT_ID}"
log "    Backup de segurança do banco (pré-restore): ${SAFE_DUMP:-N/A}"
log "    Verifique a aplicação em: https://app.vediums.com"
