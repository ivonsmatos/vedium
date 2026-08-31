# Production Deploy Runbook (G.3)
**Data:** 2026-08-30

## 1. Visão Geral
Este runbook documenta os passos necessários para realizar deploys subsequentes no novo ambiente frontend (Next.js) em produção sem causar indisponibilidade no backend (Frappe).

## 2. Deploy Steps

O deploy é ativado através do envio das modificações do código para a máquina real. Nenhum github token exposto será necessário. Utiliza-se chave SSH.

### Passo 1: Build Local (Opcional se Github Actions estiver configurado)
No ambiente CI, garantir que:
```bash
cd frontend && npm install && npm run build
```
Não apresenta erros. (O Dockerfile multi-stage faz isso sozinho no VPS, porém, validar antes no CI poupa recursos do VPS).

### Passo 2: Executar o Script de Deploy Modificado
O script original `deploy-vedium.sh` precisará ser executado para enviar as atualizações.

### Passo 3: Recriar Container Next.js
Logado no VPS via SSH (ou remotamente via comando SSH):
```bash
cd /opt/vedium
# Reconstrói e reinicia apenas o frontend sem afetar o Frappe
docker compose -f deploy/docker-compose.yml up -d --build --no-deps vedium-next
```

## 3. Rollback
Se a nova versão falhar (Next.js crashar ou healthcheck falhar):
```bash
docker compose -f deploy/docker-compose.yml stop vedium-next
```
O Rollback de roteamento no Nginx (Voltar tudo para o Frappe / Site antigo estático):
```bash
sudo cp /opt/vedium/backups/vediums.com.conf.backup-<DATA> /etc/nginx/sites-available/vediums.com
sudo nginx -t
sudo systemctl reload nginx
```
Nenhuma alteração de banco de dados é feita pelo Frontend, portanto Rollbacks são "Stateless" e imediatos.

## 4. Troubleshooting Logs
Para verificar os logs de produção do Next.js:
```bash
docker logs -f vedium-next
```
Para os logs do Nginx:
```bash
tail -f /var/log/nginx/vediums.com.error.log
```
