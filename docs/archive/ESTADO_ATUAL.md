# Estado Atual do Projeto

Este documento registra o status atual do desenvolvimento do Vedium, incluindo funcionalidades identificadas e a estrutura vigente.

**Data de Atualização**: 24/01/2026 - Triggering Deployment Test

## 🚀 Deployment Test

- **Action**: Testing GitHub Actions Automation.
- **Goal**: Verify if `git pull` runs successfully on the server.

## ✅ Funcionalidades Implementadas

### Infraestrutura

- [x] Ambiente Docker configurado (`docker-compose.yml`) com serviços essenciais (Frappe, MariaDB, Redis).
- [x] Scripts de automação de setup (`init.sh`, `install_apps.sh`).
- [x] Configuração de rede e volumes persistentes.

### Core App (`vedium_core`)

- [x] App criado e estruturado.
- [x] Integração com **Tailwind CSS** configurada (`package.json`, `input.css`).
- [x] **Hooks do Frappe** configurados para:
  - Injeção global de CSS (`vedium.css`).
  - Definição de Favicon e Logo.
  - Contexto de PWA (Tema, Splash Screen).

### Dependências

O projeto está preparado para utilizar os seguintes apps (baseado em `install_apps.sh`):

- **ERPNext v15**: ERP completo.
- **LMS v15**: Sistema de Gestão de Aprendizado.
- **Frappe Builder**: Construtor visual de páginas.
- **Payments**: Módulo de pagamentos.

## 🚧 Em Andamento / Pendências Observadas

### Documentação

- [x] Criação do README inicial.
- [x] Documentação da Arquitetura.
- [ ] Documentação detalhada dos API Endpoints (se houverem customizações complexas).

### Frontend

- O projeto possui `input.css`, mas requer execução manual ou automatizada do build do Tailwind (`npm run build-css`) para gerar o arquivo final se este não for comitado.

### Compliance com Skill "Vedium Architect" & Workflow

- [x] **AI Controller**: Arquivo `ai_controller.py` localizado em `vedium_core/controllers/`.
- [ ] **Design System**: Verificar aplicação do "Raízes de Luxo" nos templates atuais.
- [ ] **Workflow**: Garantir que branches `feat/` estejam sendo usadas para próximos desenvolvimentos.

## ⚠️ Pontos de Atenção

1. **Ambiente de Desenvolvimento**: Certifique-se de que o Node.js está disponível para compilar o CSS, caso faça alterações no design.
2. **Docker**: O container `vedium-frappe` inicia com `sleep infinity` no docker-compose, o que indica que o servidor deve ser iniciado manualmente (`bench start`) ou que o setup é focado em desenvolvimento interativo dentro do container.
