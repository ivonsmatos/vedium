#!/bin/bash
# Vedium LMS - Script de Monitoramento de Segurança
# Detecção de Intrusão e Alertas
# Author: Vedium Global Education
# Last Updated: 2026-01-21

LOG_FILE="${LOG_FILE:-/var/log/vedium-security.log}"
ALERT_FILE="${ALERT_FILE:-/var/log/vedium-alerts.log}"

# Logging functions
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" >> "$LOG_FILE"
}

alert() {
    echo "[ALERT $(date +"%Y-%m-%d %H:%M:%S")] $1" >> "$ALERT_FILE"
    echo "[ALERT $(date +"%Y-%m-%d %H:%M:%S")] $1" >> "$LOG_FILE"
    # Add webhook/Slack/email notification here
}

log "=== Verificação de Segurança Iniciada ==="

# ===========================================
# 1. Check Docker containers
# ===========================================
CONTAINERS=$(docker ps --filter "name=vedium" --format "{{.Names}}: {{.Status}}" 2>/dev/null)
if [ -z "$CONTAINERS" ]; then
    alert "CRÍTICO: Containers Vedium não estão rodando!"
else
    log "Containers OK: $(echo "$CONTAINERS" | tr '\n' ', ')"
fi

# Count running containers
RUNNING_COUNT=$(docker ps --filter "name=vedium" --format "{{.Names}}" 2>/dev/null | wc -l)
if [ "$RUNNING_COUNT" -lt 5 ]; then
    alert "AVISO: Apenas $RUNNING_COUNT containers Vedium rodando (esperado: 5)"
fi

# ===========================================
# 2. Check disk usage
# ===========================================
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_USAGE" -gt 90 ]; then
    alert "CRÍTICO: Disco com ${DISK_USAGE}% de uso!"
elif [ "$DISK_USAGE" -gt 85 ]; then
    alert "AVISO: Disco com ${DISK_USAGE}% de uso!"
else
    log "Disco: ${DISK_USAGE}% utilizado"
fi

# ===========================================
# 3. Check memory usage
# ===========================================
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt 95 ]; then
    alert "CRÍTICO: Memória com ${MEM_USAGE}% de uso!"
elif [ "$MEM_USAGE" -gt 90 ]; then
    alert "AVISO: Memória com ${MEM_USAGE}% de uso!"
else
    log "Memória: ${MEM_USAGE}% utilizada"
fi

# ===========================================
# 4. Check SSH failed logins
# ===========================================
if [ -f /var/log/auth.log ]; then
    SSH_FAILS_TODAY=$(grep "Failed password" /var/log/auth.log 2>/dev/null | grep "$(date +%b\ %d)" | wc -l)
    SSH_FAILS_TOTAL=$(grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l)

    if [ "$SSH_FAILS_TODAY" -gt 50 ]; then
        alert "AVISO: $SSH_FAILS_TODAY tentativas SSH falhas hoje!"
    fi
    log "Tentativas SSH falhas: Hoje=$SSH_FAILS_TODAY, Total=$SSH_FAILS_TOTAL"
fi

# ===========================================
# 5. Check Fail2ban status
# ===========================================
if command -v fail2ban-client &> /dev/null; then
    BANNED_SSH=$(fail2ban-client status sshd 2>/dev/null | grep "Currently banned" | awk '{print $NF}')
    log "IPs banidos no SSH: ${BANNED_SSH:-0}"

    # List all jails
    JAILS=$(fail2ban-client status 2>/dev/null | grep "Jail list" | cut -d: -f2 | tr -d ' \t')
    log "Fail2ban jails ativos: $JAILS"
fi

# ===========================================
# 6. Check SSL certificate expiration
# ===========================================
CERT_PATH="/etc/letsencrypt/live/vediums.com/fullchain.pem"
if [ -f "$CERT_PATH" ]; then
    EXPIRY=$(openssl x509 -enddate -noout -in "$CERT_PATH" 2>/dev/null | cut -d= -f2)
    EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s 2>/dev/null || echo 0)
    NOW_EPOCH=$(date +%s)
    DAYS_LEFT=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

    if [ "$DAYS_LEFT" -lt 7 ]; then
        alert "CRÍTICO: Certificado SSL expira em $DAYS_LEFT dias!"
    elif [ "$DAYS_LEFT" -lt 14 ]; then
        alert "AVISO: Certificado SSL expira em $DAYS_LEFT dias!"
    else
        log "Certificado SSL válido por $DAYS_LEFT dias"
    fi
fi

# ===========================================
# 7. Check for security updates
# ===========================================
if command -v apt &> /dev/null; then
    apt update -qq 2>/dev/null
    SECURITY_UPDATES=$(apt list --upgradable 2>/dev/null | grep -i security | wc -l)
    TOTAL_UPDATES=$(apt list --upgradable 2>/dev/null | grep -v "Listing" | wc -l)

    if [ "$SECURITY_UPDATES" -gt 0 ]; then
        alert "INFO: $SECURITY_UPDATES atualizações de segurança pendentes"
    fi
    log "Atualizações pendentes: Total=$TOTAL_UPDATES, Segurança=$SECURITY_UPDATES"
fi

# ===========================================
# 8. Check active connections
# ===========================================
if command -v netstat &> /dev/null; then
    ESTABLISHED=$(netstat -an 2>/dev/null | grep ESTABLISHED | wc -l)
    LISTENING=$(netstat -an 2>/dev/null | grep LISTEN | wc -l)
    log "Conexões: ESTABLISHED=$ESTABLISHED, LISTENING=$LISTENING"
elif command -v ss &> /dev/null; then
    ESTABLISHED=$(ss -t state established 2>/dev/null | wc -l)
    LISTENING=$(ss -t state listening 2>/dev/null | wc -l)
    log "Conexões: ESTABLISHED=$ESTABLISHED, LISTENING=$LISTENING"
fi

# ===========================================
# 9. Check critical file integrity
# ===========================================
DOCKER_COMPOSE="/opt/vedium/docker-compose.yml"
if [ -f "$DOCKER_COMPOSE" ]; then
    HASH=$(sha256sum "$DOCKER_COMPOSE" | awk '{print $1}')
    log "Hash docker-compose.yml: ${HASH:0:16}..."
fi

# ===========================================
# 10. Check website availability
# ===========================================
for URL in "https://vediums.com" "https://app.vediums.com"; do
    HTTP_CODE=$(curl -skI "$URL" -o /dev/null -w '%{http_code}' --max-time 10 2>/dev/null)
    if [ "$HTTP_CODE" != "200" ]; then
        alert "CRÍTICO: $URL retornou HTTP $HTTP_CODE"
    else
        log "Site $URL: HTTP $HTTP_CODE OK"
    fi
done

log "=== Verificação de Segurança Concluída ==="
