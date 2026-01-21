# 🔐 Vedium LMS - Documentação de Segurança

## Visão Geral

O Vedium LMS foi configurado seguindo as melhores práticas de segurança para plataformas educacionais, em conformidade com LGPD, GDPR e padrões ISO 27001.

---

## 1. Criptografia de Dados

### SSL/TLS (HTTPS)

- **Protocolos**: TLSv1.2, TLSv1.3 (apenas)
- **Cipher Suites**: Apenas ciphers modernos e seguros
- **HSTS**: Habilitado (max-age=2 anos, includeSubDomains, preload)
- **Certificado**: Let's Encrypt com renovação automática

### Dados em Repouso

- **Backups**: Criptografados com AES-256-CBC
- **Banco de Dados**: Dados sensíveis criptografados
- **Chaves**: Armazenadas de forma segura

---

## 2. Autenticação

### Controles Implementados

- **Rate Limiting**: 5 tentativas/minuto no login
- **Fail2ban**: Ban automático após 3 falhas (24h para SSH)
- **Senhas**: Política de senhas fortes obrigatória
- **Sessões**: Timeout configurado, tokens seguros

### MFA (Multi-Factor Authentication)

- Disponível via Frappe/ERPNext
- Suporte a TOTP (Google Authenticator, etc.)

### SSO (Single Sign-On)

- Suporte a OAuth2, SAML 2.0
- Integração com provedores externos

---

## 3. Controle de Acesso

### Modelo RBAC

- **Administrator**: Acesso total
- **Instructor**: Gerenciar cursos próprios
- **Student**: Acesso a cursos matriculados
- **Guest**: Apenas visualização pública

### Princípio do Menor Privilégio

- Usuários recebem apenas permissões necessárias
- Revisões periódicas de acessos (trimestral)

---

## 4. Infraestrutura

### Firewall (UFW)

```
22/tcp  - SSH
80/tcp  - HTTP (redirect para HTTPS)
443/tcp - HTTPS
```

### Segmentação de Rede

- Containers isolados via Docker networks
- Serviços internos não expostos externamente
- Banco de dados apenas acessível internamente

### Backups

- **Frequência**: Diário às 02:00
- **Retenção**: 30 dias
- **Criptografia**: AES-256
- **Verificação**: Checksums SHA-256
- **Local**: /opt/vedium/backups

---

## 5. Compliance

### LGPD (Brasil)

- ✅ Consentimento para coleta de dados
- ✅ Direito ao esquecimento
- ✅ Portabilidade de dados
- ✅ Logs de auditoria (365 dias)
- ✅ Criptografia de dados pessoais

### GDPR (Europa)

- ✅ Data minimization
- ✅ Right to erasure
- ✅ Data portability
- ✅ Breach notification procedures

### ISO 27001

- ✅ Gestão de riscos documentada
- ✅ Controles de acesso
- ✅ Gestão de incidentes
- ✅ Continuidade de negócios

---

## 6. Monitoramento

### Logs de Atividades

- `/var/log/vedium-security.log` - Eventos de segurança
- `/var/log/vedium-alerts.log` - Alertas críticos
- `/var/log/nginx/vediums.com.access.log` - Acessos web
- `/var/log/vedium-backup.log` - Logs de backup

### Detecção de Intrusão

- Monitoramento a cada 15 minutos
- Alertas automáticos para:
  - Containers parados
  - Disco > 85%
  - Memória > 90%
  - Certificado expirando
  - Atualizações pendentes

### Fail2ban Jails

- sshd: Proteção SSH
- nginx-http-auth: Autenticação HTTP
- nginx-limit-req: Rate limiting
- nginx-botsearch: Proteção contra bots

---

## 7. Atualizações

### Procedimento

1. Verificar atualizações: `apt list --upgradable`
2. Testar em ambiente de homologação
3. Fazer backup antes de atualizar
4. Aplicar atualizações: `apt upgrade`
5. Verificar funcionamento

### Patches de Segurança

- Aplicados imediatamente (< 24h para críticos)
- Monitoramento de CVEs relevantes
- Unattended-upgrades habilitado para patches críticos

---

## 8. Contatos de Segurança

### Em caso de incidente:

1. Documentar o ocorrido
2. Isolar sistema afetado se necessário
3. Notificar equipe de segurança
4. Seguir procedimento de resposta a incidentes

### Contato

- Email: security@vediums.com
- Emergência: Abrir issue no GitHub com label `security`

---

## Comandos Úteis

```bash
# Verificar status de segurança
/opt/vedium/deploy/scripts/security-monitor.sh

# Executar backup manual
/opt/vedium/deploy/scripts/backup.sh

# Ver IPs banidos
sudo fail2ban-client status sshd

# Verificar certificado SSL
openssl x509 -enddate -noout -in /etc/letsencrypt/live/vediums.com/fullchain.pem

# Ver logs de segurança
tail -f /var/log/vedium-security.log

# Ver alertas
cat /var/log/vedium-alerts.log
```

---

**Última atualização**: 2026-01-21
**Versão**: 1.1
