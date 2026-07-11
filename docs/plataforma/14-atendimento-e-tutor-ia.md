# 14 — Atendimento ao Aluno e Tutor IA

**Atualizado em:** 2026-07-08.  
**Base:** texto de decisão do anexo + documentação oficial Frappe revisada nesta
sessão + código local (`ai_controller.py`, `ai_service.py`).

## Decisão

Sim, a Vedium consegue oferecer suporte, dúvidas e acompanhamento dentro do
ecossistema Frappe. A fronteira importante:

- **Dúvida humana / comunidade / fórum:** usar recursos nativos do Frappe
  Learning primeiro.
- **Suporte operacional:** usar fluxo de chamados, hoje simples; Helpdesk
  nativo quando houver volume/equipe.
- **Tutor IA tipo professor particular:** não é recurso nativo pronto do
  Frappe Learning. Precisa ser produto custom em `vedium_core`, integrado aos
  cursos e com fallback humano.

Não vender "Tutor Vedium 24h" como pronto até ele cumprir a definição de pronto
no fim deste documento.

## Camadas de atendimento

| Necessidade | Caminho recomendado | Status Vedium | Observação |
|---|---|---|---|
| Dúvida sobre aula, lição ou exercício | Discussões nativas do LMS | 🟢 Ligado | `LMS Settings.show_discussions = 1`, ver [doc 04](04-ecossistema-frappe-oficial.md). |
| Dúvida dentro de uma turma | `LMS Batch` + aba de discussões | 🟡 Piloto criado | `PLE Básico - Turma Agosto/2026`, ainda em rascunho. |
| Aula ao vivo em turma | `LMS Live Class` via Google Meet/Zoom | 🟡 Piloto criado | 9 aulas ao vivo criadas para a turma PLE Básico, com links Google Meet. |
| Tarefa com feedback do professor | Assignments nativos do LMS | 🟢 Nativo | Usar quando o curso tiver atividades corrigidas. |
| Progresso do aluno | Progresso nativo do LMS | 🟢 Nativo | Custom só para vitrine/resumo, ver [doc 05](05-fluxo-jornada-do-aluno.md). |
| Acesso, pagamento, certificado, remarcação | Frappe Helpdesk (`HD Ticket`) | 🟢 Configurado | `Vedium Support` + agente Ivon; falta só IMAP `suporte@` para entrada por e-mail. |
| WhatsApp comercial/admin | Link manual hoje; CRM WhatsApp no futuro | 🔴 Não integrado | `frappe_whatsapp` não instalado, ver [doc 04](04-ecossistema-frappe-oficial.md). |
| Tutor IA pedagógico | Produto custom | ⚪ Previsto/parcial | Existe código parcial, mas faltam DocTypes, UX, base de conhecimento e validação. |

## Como usar o que já existe

Para uma escola de idiomas, a jornada operacional recomendada é:

1. **Curso gravado:** conteúdo, quiz, assignment e progresso no Frappe Learning.
2. **Turma ao vivo:** `LMS Batch` com `LMS Live Class` quando houver cohortes.
3. **Dúvidas:** discussões do LMS por curso/lição/turma.
4. **Feedback docente:** professor responde discussões e corrige assignments.
5. **Suporte administrativo:** chamado/WhatsApp para acesso, pagamento e agenda.

Exemplo de produto:

| Peça | Exemplo |
|---|---|
| Curso | Inglês para Brasileiros A1 |
| Turma | A1 - Agosto/2026 |
| Conteúdo | módulos semanais gravados |
| Ao vivo | 1 ou 2 encontros por semana |
| Discussões | dúvidas de gramática, pronúncia e exercícios |
| Assignments | redação, áudio, tradução e interpretação |
| Feedback | comentário do professor e recomendação de revisão |

## Tutor IA Vedium

O tutor IA deve ser tratado como uma camada custom de produto, não como
configuração nativa do LMS.

### Estado atual do código

| Peça | Arquivo | Estado |
|---|---|---|
| Chat Groq/Llama | `vedium_core/controllers/ai_controller.py` | Endpoint existe, exige login, rate limit de 50 mensagens/hora e `persona_id`. |
| Persona e log | `AI Persona`, `AI Interaction Log`, `Vedium Settings` | Citados no código/roadmap, mas não existem em `vedium_core/doctype/`. |
| Áudio/speaking | `vedium_core/services/ai_service.py` | Retorna mock enquanto `OPENAI_API_KEY`/pacote/implementação real não estiverem prontos. |
| Portal do aluno | — | Não há widget/chat de aluno documentado como pronto. |
| Base de conhecimento | — | Não há pipeline documentado para aulas, PDFs, transcrições ou políticas. |

Conclusão: há uma semente técnica, mas ainda não há um tutor IA de produção.

### Arquitetura recomendada

1. **DocTypes custom**
   - `Vedium AI Chat Session`: aluno, curso, lição, idioma, nível CEFR, status.
   - `Vedium AI Chat Message`: sessão, autor, conteúdo, metadados, tokens.
   - `AI Persona`: prompt, idioma, escopo pedagógico, guardrails.
   - `AI Interaction Log`: custo, duração, tokens, erro, versão de modelo.

2. **Widget no portal do aluno**
   - botão "Falar com tutor" dentro da área autenticada;
   - contexto automático de curso/lição;
   - opção "chamar professor" quando a IA não resolver.

3. **Base de conhecimento**
   - aulas, PDFs, transcrições, exercícios e políticas da escola;
   - respostas limitadas ao material do curso quando a pergunta for pedagógica;
   - versionamento por curso para evitar resposta baseada em conteúdo antigo.

4. **Fallback humano**
   - perguntas sensíveis, confusas, fora do escopo ou com baixa confiança viram
     discussão no LMS ou chamado para professor/equipe.

5. **Dados pedagógicos**
   - dúvidas frequentes por curso;
   - tópicos com maior erro;
   - dificuldade recorrente por aluno;
   - recomendação de revisão ou próxima atividade.

## O que não construir agora

- Fórum custom se as discussões nativas do LMS resolvem a dúvida.
- Chat pedagógico em WhatsApp como fonte principal de ensino.
- Tutor IA na home pública; ele pertence à área autenticada do aluno.
- Tutor IA sem log, limite, fallback humano e política de privacidade/LGPD.
- Áudio/speaking como promessa pública enquanto `AIService` ainda retorna mock.

## Definição de pronto para vender "Tutor Vedium 24h"

Antes de usar isso como diferencial comercial, precisa existir:

1. DocTypes criados/migrados e cobertos por teste mínimo.
2. Persona pedagógica por idioma/curso, com guardrails revisados.
3. Widget no portal do aluno com contexto de curso/lição.
4. Histórico por sessão e logs de erro/tokens.
5. Fallback humano para professor/Helpdesk/discussão.
6. Política clara de privacidade e retenção de conversa.
7. Teste com alunos reais em pelo menos um curso piloto.

Até lá, a mensagem correta é:

> A Vedium usa Frappe Learning para aulas, discussões, tarefas, turmas e
> acompanhamento. O Tutor IA Vedium é uma camada custom planejada para evoluir
> o suporte pedagógico 24h com base nos materiais dos cursos.

## Fontes externas revisadas

- Frappe Learning: https://docs.frappe.io/learning/introduction
- Create a Batch: https://docs.frappe.io/learning/create-a-batch
- Create a Live Class: https://docs.frappe.io/learning/create-a-live-class
- Frappe Helpdesk: https://docs.frappe.io/helpdesk/your-first-steps-with-frappe-helpdesk
- Frappe CRM WhatsApp: https://docs.frappe.io/crm/whatsapp
- Frappe REST API: https://docs.frappe.io/framework/user/en/api/rest
- Frappe Realtime: https://docs.frappe.io/framework/user/en/api/realtime
