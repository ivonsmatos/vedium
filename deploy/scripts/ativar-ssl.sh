#!/bin/bash
# Vedium LMS - Script para Ativar SSL
# Author: Vedium Global Education
# Last Updated: 2026-01-21

set -e

# Configuration
DOMAIN="${DOMAIN:-vediums.com}"
SERVER_IP="${SERVER_IP:-45.151.122.234}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@vediums.com}"
WEBROOT="/var/www/certbot"

echo "=== Vedium SSL Activation Script ==="
echo ""

# ===========================================
# 1. Check DNS propagation
# ===========================================
echo "=== Verificando DNS ==="
DNS_OK=true

for subdomain in "" "www." "app."; do
    FULL_DOMAIN="${subdomain}${DOMAIN}"
    IP=$(dig +short "$FULL_DOMAIN" A 2>/dev/null | head -1)

    if [ "$IP" == "$SERVER_IP" ]; then
        echo "✅ $FULL_DOMAIN -> $IP"
    else
        echo "❌ $FULL_DOMAIN -> ${IP:-não resolvido} (esperado: $SERVER_IP)"
        DNS_OK=false
    fi
done

if [ "$DNS_OK" = false ]; then
    echo ""
    echo "⚠️  DNS ainda não propagado. Configure no Cloudflare:"
    echo "   Tipo A | @ | $SERVER_IP | Proxied"
    echo "   Tipo CNAME | www | $DOMAIN | Proxied"
    echo "   Tipo A | app | $SERVER_IP | Proxied"
    echo ""
    echo "Aguarde a propagação (pode levar até 48h) e execute novamente."
    exit 1
fi

# ===========================================
# 2. Create webroot for ACME challenge
# ===========================================
echo ""
echo "=== Preparando ambiente ==="
mkdir -p "$WEBROOT/.well-known/acme-challenge"
chown -R www-data:www-data "$WEBROOT" 2>/dev/null || true

# ===========================================
# 3. Get SSL certificate from Let's Encrypt
# ===========================================
echo ""
echo "=== Obtendo certificado SSL ==="

# Check if certbot is installed
if ! command -v certbot &> /dev/null; then
    echo "Instalando certbot..."
    apt update && apt install -y certbot python3-certbot-nginx
fi

certbot certonly --webroot -w "$WEBROOT" \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" \
    -d "app.$DOMAIN" \
    --non-interactive \
    --agree-tos \
    --email "$ADMIN_EMAIL" \
    --force-renewal

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Certificado obtido com sucesso!"
else
    echo "❌ Erro ao obter certificado. Verifique os logs:"
    echo "   /var/log/letsencrypt/letsencrypt.log"
    exit 1
fi

# ===========================================
# 4. Generate DH parameters (if not exists)
# ===========================================
if [ ! -f /etc/nginx/ssl/dhparam.pem ]; then
    echo ""
    echo "=== Gerando parâmetros DH (pode demorar) ==="
    mkdir -p /etc/nginx/ssl
    openssl dhparam -out /etc/nginx/ssl/dhparam.pem 2048
fi

# ===========================================
# 5. Enable HTTPS configuration
# ===========================================
echo ""
echo "=== Ativando configuração HTTPS ==="

# Test NGINX config
nginx -t
if [ $? -ne 0 ]; then
    echo "❌ Erro na configuração do NGINX"
    exit 1
fi

# Reload NGINX
systemctl reload nginx

# ===========================================
# 6. Setup auto-renewal
# ===========================================
echo ""
echo "=== Configurando renovação automática ==="

# Add to crontab if not exists
if ! crontab -l 2>/dev/null | grep -q "certbot renew"; then
    (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -
    echo "✅ Renovação automática configurada (03:00 diário)"
fi

# ===========================================
# 7. Verify SSL
# ===========================================
echo ""
echo "=== Verificando SSL ==="
sleep 2

for subdomain in "" "app."; do
    FULL_URL="https://${subdomain}${DOMAIN}"
    HTTP_CODE=$(curl -skI "$FULL_URL" -o /dev/null -w '%{http_code}' --max-time 10)

    if [ "$HTTP_CODE" == "200" ]; then
        echo "✅ $FULL_URL - HTTP $HTTP_CODE"
    else
        echo "⚠️ $FULL_URL - HTTP $HTTP_CODE"
    fi
done

# ===========================================
# 8. Summary
# ===========================================
echo ""
echo "========================================="
echo "✅ SSL ATIVADO COM SUCESSO!"
echo "========================================="
echo ""
echo "🌐 Sites seguros:"
echo "   Site: https://$DOMAIN"
echo "   App:  https://app.$DOMAIN"
echo ""
echo "🔒 Certificado válido até:"
openssl x509 -enddate -noout -in "/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
echo ""
echo "📋 Próximos passos:"
echo "   1. Teste os sites no navegador"
echo "   2. Verifique HSTS em https://hstspreload.org"
echo "   3. Teste SSL em https://www.ssllabs.com/ssltest/"
