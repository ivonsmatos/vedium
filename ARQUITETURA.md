# Arquitetura do Sistema Vedium

Este documento descreve a arquitetura técnica do projeto Vedium, detalhando seus componentes, fluxos de dados e integrações.

## 🏗️ Visão Geral

O Vedium é construído sobre o **Frappe Framework**, uma estrutura full-stack meta-driven em Python e JavaScript. Ele estende as funcionalidades nativas através de um Custom App chamado `vedium_core`, integrando o **ERPNext** e um sistema de gestão de aprendizado (**LMS**).

A interface visual é modernizada utilizando **Tailwind CSS**, seguindo o Design System **"Raízes de Luxo"** (Dark Mode, paleta de cores específica).

### 📐 Princípios de Engenharia e Workflow

1. **No Forks**: Nunca modificar apps originais (`lms`, `erpnext`). Todas as mudanças residem em `vedium_core`.
2. **Git Workflow**: Branch `main` estável. Novas features em `feat/nome` e correções em `fix/nome`. Review obrigatório no PR.
3. **Definition of Done (DoD)**:
   - Código mergeado na main.
   - CSS compilado e responsivo.
   - Migrações rodadas (`bench migrate`).
   - UI Check visual aprovado.
4. **High-End UI**: Uso estrito do design system "Raízes de Luxo".

```mermaid
graph TD
    User[Usuário] -->|HTTP/HTTPS| Nginx[Proxy / Router]
    Nginx -->|Web Request| Frappe[Frappe Application Server]
    Frappe -->|Read/Write| MariaDB[(MariaDB Database)]
    Frappe -->|Cache/Queue| Redis[(Redis)]
    
    subgraph "Vedium Core App"
        Hooks[Hooks.py]
        DocTypes[DocTypes (Models)]
        API[API Controllers]
        Templates[Jinja2 Templates]
        Tailwind[Tailwind CSS Assets]
    end
    
    Frappe --> VediumCore[Carrega vedium_core]
```

## 🧩 Componentes Principais

### 1. Docker Services (`docker-compose.yml`)

O ambiente é containerizado para garantir consistência.

- **frappe**: Container principal da aplicação (Python/Gunicorn/JS).
- **mariadb**: Banco de dados relacional para armazenar todos os dados do sistema e metadados (DocTypes).
- **redis-cache**: Cache de sessão e dados voláteis.
- **redis-queue**: Gerenciamento de filas de tarefas em background (Background Jobs).
- **redis-socketio**: Comunicação em tempo real (Websockets).

### 2. Vedium Core (`vedium_core/`)

É o coração da personalização do projeto.

- **`hooks.py`**: Ponto de entrada das configurações. Define:
  - Apps necessários.
  - Scripts globais (CSS/JS) injetados nas páginas.
  - Configurações de PWA (Manifest, cores).
  - Agendamento de tarefas (Cron).
- **`input.css`**: Arquivo fonte do Tailwind CSS. Onde são definidas as diretivas `@tailwind` e estilos customizados.
- **`vedium_core/public/`**: Diretório para assets estáticos servidos diretamente (CSS compilado, imagens, JS).

### 3. Frontend & Estilização

Diferente de um app Frappe padrão, o Vedium investe em uma UI diferenciada:

- **Tailwind CSS v3**: Utilizado para estilização utilitária.
- **Build Process**: O comando `npm run build-css` (definido no `package.json`) processa o `input.css` e gera o `vedium.css` final na pasta pública.
- **Integração**: O arquivo CSS gerado é injetado automaticamente em todas as páginas através da configuração `app_include_css` no `hooks.py`.

## 🔄 Fluxos e Processos

### Inicialização

1. O script `init.sh` prepara o ambiente `bench` do Frappe.
2. O script `install_apps.sh` baixa as dependências críticas:
   - `payments`
   - `erpnext`
   - `lms`
   - `builder` (Frappe Builder)
3. Um novo site (`vedium.localhost`) é criado e os apps são instalados nele.

### Customizações (Hooks)

O arquivo `hooks.py` intercepta eventos do sistema:

- **Web Context**: Injeta variáveis globais como `pwa_enabled` e cores de tema para o template Jinja.
- **Startup**: Define funções executadas no boot (`boot_session`).

## 📱 PWA (Progressive Web App)

O projeto possui configurações explícitas para funcionar como PWA:

- **Manifest**: Localizado em `/assets/vedium_core/manifest.json`.
- **Service Workers**: Scripts de registro em `/assets/vedium_core/js/pwa-register.js`.
