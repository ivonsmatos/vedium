# Procedimento de Restauração

Este documento descreve as etapas para restaurar o Vedium LMS a partir de um backup.

## Pré-requisitos

- Acesso ao servidor via SSH.
- Privilégios de `root` ou `sudo`.
- A chave de criptografia usada para backups (Variável `BACKUP_ENCRYPTION_KEY`).

## Passos para Restauração

### 1. Localizar Backup

Os backups são armazenados em `/opt/vedium/backups/`. Encontre o diretório com a data que deseja restaurar.

```bash
cd /opt/vedium/backups/YYYY-MM-DD_HH-MM-SS
```

### 2. Restaurar Banco de Dados

O backup do banco de dados é criptografado. Você precisa descriptografá-lo antes de restaurar.

```bash
# Descriptografar e restaurar
openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:"$BACKUP_ENCRYPTION_KEY" -in mariadb_backup.sql.gz.enc | \
gunzip | \
docker exec -i vedium-mariadb mysql -u root -p"$MYSQL_ROOT_PASSWORD"
```

### 3. Restaurar Arquivos

Restaure os volumes do Docker.

```bash
# Pare os containers primeiro
cd /opt/vedium
docker-compose down

# Restaurar volumes
docker run --rm \
    -v vedium_frappe-bench-data:/data \
    -v $(pwd):/backup \
    alpine tar xzf /backup/frappe-bench-data.tar.gz -C /data
```

### 4. Restaurar Configurações

Se necessário, restaure os arquivos de configuração.

```bash
tar xzf configs.tar.gz -C /
```

### 5. Reiniciar Serviços

```bash
docker-compose up -d
```

## Validação

Após a restauração, verifique:

1. Faça login na aplicação.
2. Verifique dados recentes (usuários, cursos).
3. Verifique logs do site para erros.
