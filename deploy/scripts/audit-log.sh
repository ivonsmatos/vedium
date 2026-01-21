#!/bin/bash
# Vedium LMS - Sistema de Auditoria LGPD/GDPR Compliant
# Author: Vedium Global Education
# Last Updated: 2026-01-21

AUDIT_DIR="/var/log/vedium-audit"
mkdir -p "$AUDIT_DIR"

echo "=== Configurando Sistema de Auditoria Vedium ==="

# ===========================================
# 1. Configure log rotation
# ===========================================
cat > /etc/logrotate.d/vedium << 'LOGROTATE'
# Vedium Application Logs
/var/log/vedium*.log {
    daily
    rotate 365
    compress
    delaycompress
    missingok
    notifempty
    create 640 root root
    dateext
    dateformat -%Y-%m-%d
}

# Vedium Audit Logs (LGPD/GDPR - 5 years retention)
/var/log/vedium-audit/*.log {
    daily
    rotate 1825
    compress
    delaycompress
    missingok
    notifempty
    create 640 root root
    dateext
    dateformat -%Y-%m-%d
}

# NGINX Logs for Vedium
/var/log/nginx/vediums.com*.log
/var/log/nginx/app.vediums.com*.log {
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
    create 640 www-data adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 $(cat /var/run/nginx.pid)
    endscript
}
LOGROTATE

echo "✅ Logrotate configurado"

# ===========================================
# 2. Configure audit rules (if auditd is installed)
# ===========================================
if command -v auditctl &> /dev/null; then
    cat > /etc/audit/rules.d/vedium.rules << 'AUDIT_RULES'
# Vedium LMS Audit Rules

# Monitor docker-compose changes
-w /opt/vedium/docker-compose.yml -p wa -k vedium_config

# Monitor NGINX config changes
-w /etc/nginx/sites-available/vediums.com -p wa -k vedium_nginx

# Monitor SSL certificate access
-w /etc/letsencrypt/live/vediums.com/ -p r -k vedium_ssl

# Monitor backup scripts
-w /opt/vedium/scripts/ -p wa -k vedium_scripts

# Monitor user authentication
-w /var/log/auth.log -p wa -k vedium_auth

# Monitor sudo usage
-w /var/log/sudo.log -p wa -k vedium_sudo
AUDIT_RULES

    auditctl -R /etc/audit/rules.d/vedium.rules 2>/dev/null
    echo "✅ Regras de auditoria configuradas"
else
    echo "⚠️ auditd não instalado, pulando configuração de audit rules"
fi

# ===========================================
# 3. Create audit log structure
# ===========================================
mkdir -p "$AUDIT_DIR"/{access,data-access,admin-actions,security-events}

cat > "$AUDIT_DIR/README.md" << 'README'
# Vedium Audit Logs

Este diretório contém logs de auditoria para conformidade LGPD/GDPR.

## Estrutura

- `access/` - Logs de acesso ao sistema
- `data-access/` - Logs de acesso a dados pessoais
- `admin-actions/` - Ações administrativas
- `security-events/` - Eventos de segurança

## Retenção

- Logs de auditoria: 5 anos (LGPD/GDPR)
- Logs de aplicação: 1 ano
- Logs de acesso web: 90 dias

## Conformidade

- LGPD (Brasil)
- GDPR (Europa)
- ISO 27001

Última atualização: $(date +%Y-%m-%d)
README

echo "✅ Estrutura de logs de auditoria criada"

# ===========================================
# 4. Configure syslog for Vedium
# ===========================================
if [ -f /etc/rsyslog.d/50-default.conf ]; then
    cat > /etc/rsyslog.d/vedium.conf << 'RSYSLOG'
# Vedium LMS Syslog Configuration
local0.*    /var/log/vedium-audit/access/access.log
local1.*    /var/log/vedium-audit/data-access/data.log
local2.*    /var/log/vedium-audit/admin-actions/admin.log
local3.*    /var/log/vedium-audit/security-events/security.log
RSYSLOG

    systemctl restart rsyslog 2>/dev/null || true
    echo "✅ Rsyslog configurado"
fi

# ===========================================
# 5. Set permissions
# ===========================================
chmod -R 640 "$AUDIT_DIR"
chmod 750 "$AUDIT_DIR"
chown -R root:root "$AUDIT_DIR"

echo ""
echo "=== Configuração de Auditoria Concluída ==="
echo "Logs em: $AUDIT_DIR"
echo "Retenção: 5 anos (1825 dias)"
