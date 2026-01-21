# Configuração do Arquivo Hosts

Para acessar o site Vedium localmente usando `vedium.localhost`, você precisa configurar o arquivo hosts do seu sistema.

## Windows

1. Abra o **Bloco de Notas** como **Administrador**
2. Vá em **Arquivo > Abrir** e navegue até:

   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

3. Adicione a seguinte linha no final do arquivo:

   ```
   127.0.0.1    vedium.localhost
   ```

4. Salve o arquivo

## Linux / macOS

1. Abra o terminal e execute:

   ```bash
   sudo nano /etc/hosts
   ```

2. Adicione a seguinte linha no final do arquivo:

   ```
   127.0.0.1    vedium.localhost
   ```

3. Salve com `Ctrl+O` e saia com `Ctrl+X`

## Verificação

Após salvar, teste abrindo o terminal e executando:

```bash
ping vedium.localhost
```

Você deve ver respostas de `127.0.0.1`.

---

## Criando o Site no Frappe

Após a configuração do hosts, dentro do container execute:

```bash
cd vedium-bench
bench new-site vedium.localhost --mariadb-root-password root --admin-password admin
bench --site vedium.localhost install-app vedium_core
bench --site vedium.localhost set-config developer_mode 1
bench start
```

O site estará disponível em: **<http://vedium.localhost:8000>**
