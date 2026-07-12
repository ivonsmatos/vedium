# 14 — Atendimento ao Aluno e Tutor IA

**Atualizado em:** 2026-07-12.  
**Base:** texto de decisão do anexo + documentação oficial Frappe revisada nesta
sessão + código local (`ai_controller.py`, `ai_service.py`).

## Decisão

Sim, a Vedium consegue oferecer suporte, dúvidas e acompanhamento dentro do
ecossistema Frappe. A fronteira importante:

- **Dúvida humana / comunidade / fórum:** usar recursos nativos do Frappe
  Learning primeiro.
- **Suporte operacional:** usar fluxo de chamados, hoje simples; Helpdesk
  nativo quando houver volume/equipe.
- **Tutor IA tipo professor particular:** removido/descontinuado no `vedium_core`.
  Não vender "Tutor Vedium 24h" e não reativar widget LLM sem uma nova decisão
  explícita de produto, base de conhecimento, política LGPD e validação real.

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
| Tutor IA pedagógico | — | 🔴 Removido | Removido em 2026-07-12 porque travava a área do aluno e não havia produto estável. |

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

O Tutor IA foi removido do `vedium_core` em 2026-07-12:

- a página custom de progresso foi removida junto com o widget;
- o backend `ai_tutor.py` foi removido;
- a dependência Groq foi removida do app;
- o `after_migrate` limpa campos/DocTypes antigos (`AI Tutor Session`,
  `AI Tutor Message`, chave/modelo Groq em `System Settings`) quando existirem.

A decisão atual é não implementar tutor LLM. Para dúvidas pedagógicas e
operacionais, usar LMS/Raven/Helpdesk e atendimento humano.

## O que não construir agora

- Fórum custom se as discussões nativas do LMS resolvem a dúvida.
- Chat pedagógico em WhatsApp como fonte principal de ensino.
- Tutor IA na home pública ou na área autenticada.
- Tutor IA sem base de conhecimento, validação pedagógica, fallback humano e
  política de privacidade/LGPD.
- Áudio/speaking como promessa pública enquanto `AIService` ainda retorna mock.

## Mensagem comercial correta

Não vender "Tutor Vedium 24h". A mensagem correta é:

> A Vedium usa Frappe Learning para aulas, discussões, tarefas, turmas e
> acompanhamento, com suporte humano por canais oficiais.

## Fontes externas revisadas

- Frappe Learning: https://docs.frappe.io/learning/introduction
- Create a Batch: https://docs.frappe.io/learning/create-a-batch
- Create a Live Class: https://docs.frappe.io/learning/create-a-live-class
- Frappe Helpdesk: https://docs.frappe.io/helpdesk/your-first-steps-with-frappe-helpdesk
- Frappe CRM WhatsApp: https://docs.frappe.io/crm/whatsapp
- Frappe REST API: https://docs.frappe.io/framework/user/en/api/rest
- Frappe Realtime: https://docs.frappe.io/framework/user/en/api/realtime
