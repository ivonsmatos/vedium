#!/bin/bash
# Vedium — Ativar Stack de Observabilidade (Prometheus + Grafana + Loki + Uptime Kuma)
#
# Pré-requisito: DNS record criado em Cloudflare:
#   metrics.vediums.com A 45.151.122.234
#
# Uso: bash /opt/vedium/scripts/ativar-observabilidade.sh
#
set -euo pipefail

COMPOSE_DIR="/opt/vedium"
LOG="/var/log/vedium-observability.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

# ---- 1. Atualizar docker-compose com arquivos mais recentes ----
log "Usando arquivos em $COMPOSE_DIR..."
cd "$COMPOSE_DIR"

# ---- 2. Subir stack ----
log "Iniciando containers do perfil observability..."
docker compose --profile observability up -d

log "Aguardando Prometheus (9090) e Grafana (3000) ficarem prontos..."
for svc in prometheus grafana; do
  attempts=0
  until docker compose ps "vedium-$svc" 2>/dev/null | grep -q "running"; do
    attempts=$((attempts + 1))
    if [[ $attempts -ge 30 ]]; then
      log "AVISO: vedium-$svc demorou para iniciar — verifique: docker compose logs vedium-$svc"
      break
    fi
    sleep 2
  done
done

# ---- 3. Nginx config para metrics.vediums.com ----
NGINX_CONF="/etc/nginx/sites-available/metrics.vediums.com"
if [[ ! -f "$NGINX_CONF" ]]; then
  log "Instalando nginx config para metrics.vediums.com..."
  cp "$COMPOSE_DIR/nginx/metrics.vediums.com.conf" "$NGINX_CONF"
  ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/metrics.vediums.com
fi

# ---- 4. SSL com Let's Encrypt ----
if [[ ! -d "/etc/letsencrypt/live/metrics.vediums.com" ]]; then
  log "Obtendo certificado SSL para metrics.vediums.com..."
  # Criar config HTTP temporário para challenge
  cat > /etc/nginx/sites-available/metrics-http-only.conf <<'HTTP_CONF'
server {
    listen 80;
    server_name metrics.vediums.com;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 200 "aguardando cert"; add_header Content-Type text/plain; }
}
HTTP_CONF
  ln -sf /etc/nginx/sites-available/metrics-http-only.conf /etc/nginx/sites-enabled/
  nginx -t && systemctl reload nginx

  certbot certonly --nginx -d metrics.vediums.com \
    --non-interactive --agree-tos --email contato@vediums.com

  rm -f /etc/nginx/sites-enabled/metrics-http-only.conf
  rm -f /etc/nginx/sites-available/metrics-http-only.conf
  log "Certificado obtido."
fi

# ---- 5. Ativar nginx metrics ----
nginx -t && systemctl reload nginx
log "Nginx recarregado."

# ---- 6. Confirmação ----
log "=== Stack de observabilidade ativa! ==="
log "  Grafana:      https://metrics.vediums.com  (host: 3003)"
log "  Prometheus:   http://127.0.0.1:9090  (interno)"
log "  Loki:         http://127.0.0.1:3100  (interno)"
log "  Uptime Kuma:  http://127.0.0.1:3004  (host: 3004)"
log ""
log "  Login Grafana: admin / <GRAFANA_ADMIN_PASSWORD do .env>"
log ""
log "Próximos passos:"
log "  1. Acesse https://metrics.vediums.com e configure o datasource Prometheus"
log "     URL: http://vedium-prometheus:9090"
log "  2. Adicione datasource Loki: http://vedium-loki:3100"
log "  3. Importe dashboard 'Node Exporter' (ID 1860) e 'Nginx' (ID 12559)"
