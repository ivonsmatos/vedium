# **VEDIUM DEVELOPMENT WORKFLOW**

Este documento define o ciclo de vida de desenvolvimento do projeto Vedium, desde a concepção visual até à entrada em produção.  
Objetivo: Garantir alta velocidade de entrega com estabilidade (Zero Downtime).

## **1\. ESTRATÉGIA GIT (Git Workflow)**

Utilizamos o modelo **Feature Branch Workflow**. O código na branch main deve estar sempre pronto para produção (deployable).

### **As Branches**

* **main**: Produção. Código estável. **Bloqueada para commits diretos.** Só aceita alterações via Pull Request (PR).  
* **staging**: (Opcional) Branch de homologação. Espelho do ambiente de produção para testes finais.  
* **feat/nome-da-funcionalidade**: Para novas features (ex: feat/chat-groq, feat/dark-mode-header).  
* **fix/nome-do-bug**: Para correção de erros (ex: fix/mobile-menu-scroll).  
* **chore/manutencao**: Para ajustes de configuração, docs ou dependências.

### **O Fluxo Diário**

1. Atualize o seu local: git checkout main \-\> git pull origin main.  
2. Crie a branch: git checkout \-b feat/nova-tela-login.  
3. Desenvolva e commite (Atomic Commits).  
4. Suba para o GitHub: git push origin feat/nova-tela-login.  
5. Abra um **Pull Request (PR)** para a main.

## **2\. PROCESSO DE UI/UX (Design System)**

Antes de escrever código frontend, o design deve ser validado.

1. **Conceção:** O design deve seguir o padrão "Raízes de Luxo" (Dark Mode, Tailwind).  
2. **Prototipagem (Figma/Sketch):**  
   * Definir layout Mobile (PWA) primeiro.  
   * Definir layout Desktop.  
3. **Handoff:** O desenvolvedor deve ter acesso às cores exatas e espaçamentos.  
4. **Implementação:**  
   * Usar classes utilitárias do Tailwind no input.css ou diretamente no HTML.  
   * **NUNCA** usar CSS inline (style="...") salvo exceções estritas.  
   * Rodar npm run build-css para gerar os artefactos.

## **3\. GARANTIA DE QUALIDADE (QA & Testing)**

O QA é responsabilidade de todos, não apenas de um testador dedicado.

### **Nível 1: Testes do Desenvolvedor (Local)**

Antes de abrir o PR, o desenvolvedor deve garantir:

* \[ \] O código roda sem erros no terminal (bench start).  
* \[ \] O build do Tailwind passa sem avisos.  
* \[ \] A funcionalidade foi testada em **Mobile** (Redimensionar navegador) e **Desktop**.  
* \[ \] Não existem print() ou console.log() de debug esquecidos.

### **Nível 2: Code Review (No Pull Request)**

Outro desenvolvedor (ou Tech Lead) deve rever o código no GitHub:

* \[ \] A lógica de negócio está segura? (Ex: Permissões de utilizador verificadas).  
* \[ \] O código segue o padrão do SKILL.md?  
* \[ \] Existem chaves de API expostas? (CRÍTICO: Rejeitar imediatamente).

### **Nível 3: Staging (Homologação)**

Após o merge, o sistema é testado num ambiente idêntico ao de produção:

* Testar fluxo crítico: Login \-\> Ver Aula \-\> Chat IA \-\> Logout.  
* Verificar performance (tempo de carregamento).

## **4\. DEFINITION OF DONE (DoD)**

Uma tarefa só é considerada "Pronta" quando:

1. O código está mergeado na main.  
2. O CSS está compilado e responsivo.  
3. As migrações de banco de dados (bench migrate) foram testadas.  
4. A funcionalidade foi aprovada visualmente (UI Check).

## **5\. COMANDOS ÚTEIS NO WORKFLOW**

**Para Frontend:**

\# Enquanto desenvolve (Watch Mode)  
cd apps/vedium\_core  
npm run watch-css

\# Antes do Commit (Build Final)  
npm run build-css

**Para Backend/Geral:**

\# Atualizar ambiente após um git pull  
bench migrate  
bench clear-cache

\# Reiniciar processos (se alterou Python)  
bench restart  
