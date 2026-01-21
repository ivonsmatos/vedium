# Git Workflow - vedium_core

Este documento contém os comandos Git necessários para conectar o app `vedium_core` ao repositório GitHub.

## Pré-requisitos

- O script `init.sh` foi executado com sucesso
- O app `vedium_core` foi criado dentro de `vedium-bench/apps/`

---

## Comandos Git para vedium_core

### 1. Navegar até a pasta do app

```bash
cd vedium-bench/apps/vedium_core
```

### 2. Inicializar o Git (se ainda não estiver inicializado)

```bash
git init
```

### 3. Adicionar o remote origin

```bash
git remote add origin https://github.com/ivonsmatos/vedium.git
```

### 4. Configurar branch principal

```bash
git branch -M main
```

### 5. Sincronizar com o GitHub

**Se o repositório GitHub NÃO está vazio** (já tem arquivos):

```bash
git pull origin main --allow-unrelated-histories
```

Resolve quaisquer conflitos se necessário, depois:

```bash
git add .
git commit -m "feat: Initial vedium_core app structure"
git push -u origin main
```

**Se o repositório GitHub está VAZIO** (primeiro push):

```bash
git add .
git commit -m "feat: Initial vedium_core app structure"
git push -u origin main
```

---

## Comandos Rápidos (Copiar/Colar)

Para repositório **não vazio**:

```bash
cd vedium-bench/apps/vedium_core
git init
git remote add origin https://github.com/ivonsmatos/vedium.git
git branch -M main
git pull origin main --allow-unrelated-histories
git add .
git commit -m "feat: Initial vedium_core app structure"
git push -u origin main
```

Para repositório **vazio**:

```bash
cd vedium-bench/apps/vedium_core
git init
git remote add origin https://github.com/ivonsmatos/vedium.git
git branch -M main
git add .
git commit -m "feat: Initial vedium_core app structure"
git push -u origin main
```

---

## Verificação

Após o push, verifique em: <https://github.com/ivonsmatos/vedium>

Os arquivos do `vedium_core` devem estar visíveis no repositório.
