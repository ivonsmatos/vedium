# Vedium — Runbook de Operações

> Versão: 1.0 — 2026-05-25  
> Stack: Frappe v15 / ERPNext v15 / Python 3.11 / MariaDB 10.6 / Docker Compose  
> Servidor: 45.151.122.234 (Ubuntu)  
> Acesso: `ssh ubuntu@45.151.122.234`

---

## Índice

1. [Comandos do dia a dia](#1-comandos-do-dia-a-dia)
2. [Deploy de atualização](#2-deploy-de-atualização)
3. [Backup manual](#3-backup-manual)
4. [Restore de emergência](#4-restore-de-emergência)
5. [Diagnóstico de problemas](#5-diagnóstico-de-problemas)
6. [Escalonamento de incidentes](#6-escalonamento-de-incidentes)
7. [Rollback rápido](#7-rollback-rápido)
8. [Reiniciar serviços específicos](#8-reiniciar-serviços-específicos)
9. [Banco de dados](#9-banco-de-dados)
10. [Certificado TLS](#10-certificado-tls)
11. [Checklist de saúde](#11-checklist-de-saúde)

---

## 1. Comandos do dia a dia

```bash
# Conectar ao servidor
ssh ubuntu@45.151.122.234
cd /opt/vedium

# Status rápido
make status

# Ver logs em tempo real
make logs

# Ver apenas workers
make logs-workers

# Acessar shell dentro do container frappe
make shell

# Verificar saúde da API
make health
```

---

## 2. Deploy de atualização

```bash
# No servidor
cd /opt/vedium

# Puxar código novo
git pull origin main

# Rebuild assets Frappe (CSS/JS do vedium_core)
make build-assets

# Executar migrações (se houver mudanças de DocType)
make migrate

# Limpar cache
make clear-cache

# Reiniciar containers
make restart

# Verificar saúde
make health
```

**Dica:** para deployar sem downtime, o gunicorn com `--preload` permite reiniciar workers sem derrubar o process master. Use `docker compose restart vedium-frappe` — não `down/up`.

---

## 3. Backup manual

```bash
# No servidor (requer variáveis RESTIC_* no ambiente)
cd /opt/vedium
make backup

# Listar snapshots
make restore-list

# Ver detalhes do backup (restic direto)
source /opt/vedium/.env && restic snapshots --tag vedium
```

**Verificar cronjob de backup:**

```bash
crontab -l | grep backup
# Deve ter algo como:
# 0 3 * * * /opt/vedium/deploy/scripts/backup.sh >> /var/log/vedium-backup.log 2>&1
```

**Configurar cronjob se não existir:**

```bash
(crontab -l; echo "0 3 * * * bash /opt/vedium/deploy/scripts/backup.sh >> /var/log/vedium-backup.log 2>&1") | crontab -
```

---

## 4. Restore de emergência

> ⚠️ **STOP.** Antes de qualquer restore em produção, certifique-se que:
>
> 1. O incidente justifica sobrescrever dados de produção.
> 2. Um backup de segurança foi feito do estado atual.
> 3. Você comunicou a equipe.

```bash
# Listar snapshots disponíveis
make restore-list

# Restore interativo (último snapshot)
make restore

# Restore de snapshot específico
bash /opt/vedium/deploy/scripts/restore.sh --snapshot <ID>

# Simular sem alterar dados
bash /opt/vedium/deploy/scripts/restore.sh --dry-run
```

O script `restore.sh` cria automaticamente um backup do banco atual antes de sobrescrever.

---

## 5. Diagnóstico de problemas

### Site retorna 502 Bad Gateway

```bash
# 1. Ver status containers
make status
docker ps --filter name=vedium

# 2. Ver logs do frappe
make logs-frappe

# 3. Ver logs nginx
sudo tail -50 /var/log/nginx/app.vediums.com.error.log

# 4. Testar conectividade interna
curl -s http://localhost:8005/api/method/ping

# 5. Reiniciar frappe
docker compose -f deploy/docker-compose.yml restart vedium-frappe
```

### Emails não chegam / Jobs não executam

```bash
# Verificar se workers estão rodando
make workers

# Ver logs dos workers
make logs-workers

# Verificar filas Redis
docker exec vedium-redis-queue redis-cli llen frappe:default
docker exec vedium-redis-queue redis-cli llen frappe:short
docker exec vedium-redis-queue redis-cli llen frappe:long

# Reiniciar workers e scheduler
docker compose -f deploy/docker-compose.yml restart \
    vedium-worker-default vedium-worker-short vedium-worker-long vedium-scheduler
```

### Banco de dados lento

```bash
# Ver queries lentas no MariaDB
docker exec -it vedium-mariadb mysql \
    -u root -p"${MYSQL_ROOT_PASSWORD}" \
    -e "SHOW PROCESSLIST;"

# Ver tamanho das tabelas maiores
docker exec -it vedium-mariadb mysql \
    -u root -p"${MYSQL_ROOT_PASSWORD}" \
    -e "SELECT table_schema, table_name, ROUND(data_length/1024/1024,2) AS 'MB'
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema','mysql','performance_schema')
        ORDER BY data_length DESC LIMIT 20;"
```

### Disco cheio

```bash
# Ver uso do disco
df -h

# Docker — limpar imagens/containers não usados
docker system df
docker system prune -f   # NÃO remove volumes

# Ver snapshots restic
source /opt/vedium/.env && restic snapshots --tag vedium
# Forçar retenção (libera espaço no bucket)
restic forget --keep-daily 7 --keep-monthly 3 --tag vedium --prune
```

### PWA / Service Worker não atualiza no browser do usuário

```bash
# Verificar se /sw.js está sendo servido
curl -I https://app.vediums.com/sw.js
# Deve retornar: Content-Type: application/javascript
#                Service-Worker-Allowed: /
#                Cache-Control: no-cache, no-store, must-revalidate

# Se retornar 404, verificar nginx
sudo nginx -t
sudo systemctl reload nginx
```

---

## 6. Escalonamento de incidentes

| Severidade | Critério                           | Ação                                                     | Contato        |
| ---------- | ---------------------------------- | -------------------------------------------------------- | -------------- |
| P0         | Site fora do ar (502/503 público)  | Verificar containers → reiniciar → restore se necessário | Ivon imediato  |
| P1         | API lenta (>3s) ou workers parados | Verificar logs → reiniciar workers                       | Ivon < 30min   |
| P2         | Funcionalidade específica quebrada | Criar issue no GitHub, agendar fix                       | Próximo sprint |
| P3         | Erro cosmético / UI                | Issue no GitHub                                          | Normal         |

---

## 7. Rollback rápido

```bash
# Ver últimos commits
git log --oneline -10

# Voltar para commit específico (SEM alterar dados do banco)
git checkout <hash>
make build-assets
make restart

# Para voltar para main depois
git checkout main
make build-assets
make restart
```

---

## 8. Reiniciar serviços específicos

```bash
# Reiniciar apenas um serviço
docker compose -f deploy/docker-compose.yml restart vedium-frappe
docker compose -f deploy/docker-compose.yml restart vedium-socketio
docker compose -f deploy/docker-compose.yml restart vedium-scheduler

# Reiniciar banco (⚠️ causa downtime)
docker compose -f deploy/docker-compose.yml restart vedium-mariadb

# Reiniciar Redis cache (limpa cache — pode ser necessário)
docker compose -f deploy/docker-compose.yml restart vedium-redis-cache

# Reiniciar tudo
make restart
```

---

## 9. Banco de dados

### Acesso ao MySQL

```bash
docker exec -it vedium-mariadb mysql \
    -u root -p"${MYSQL_ROOT_PASSWORD}"
```

### Listar databases

```sql
SHOW DATABASES;
USE `app.vediums.com`;
SHOW TABLES;
```

### Verificar integridade

```bash
docker exec vedium-mariadb mysqlcheck \
    -u root -p"${MYSQL_ROOT_PASSWORD}" \
    --all-databases --check --optimize 2>/dev/null
```

---

## 10. Certificado TLS

```bash
# Renovar certificado Let's Encrypt
sudo certbot renew --dry-run   # testar
sudo certbot renew             # renovar

# Após renovar, recarregar nginx
sudo systemctl reload nginx

# Verificar validade
echo | openssl s_client -connect app.vediums.com:443 2>/dev/null | \
    openssl x509 -noout -dates
```

---

## 11. Checklist de saúde

Execute semanalmente:

- [ ] `make health` → API respondendo em <300ms
- [ ] `make workers` → todos os workers rodando
- [ ] `make restore-list` → último snapshot < 24h
- [ ] `df -h` → disco < 80%
- [ ] `sudo certbot renew --dry-run` → certificado OK
- [ ] `docker ps --filter status=exited` → nenhum container parado inesperadamente
- [ ] Verificar alertas no Telegram (se configurado)
- [ ] Abrir `https://app.vediums.com` e fazer login manual

---

_Para dúvidas sobre a arquitetura, consultar [ARQUITETURA_PROPOSTA.md](../ARQUITETURA_PROPOSTA.md)._
