# Playbook de CRM e Operação — Vedium

> Processo de gestão do funil de vendas e atendimento.
> Criado em 2026-06-12. Ferramentas: Frappe CRM (`app.vediums.com/crm`),
> Helpdesk (`app.vediums.com/helpdesk`), Aluno 360 (`/aluno_360`).

---

## 1. Como o funil funciona (automático)

```
Visitante preenche /contato  ──►  CRM Lead criado (source: Website)
                                   + Contact unificado
                                   + mensagem no histórico do lead
                                   + e-mail para contato@vediums.com

Aluno se matricula (pagou)   ──►  Lead marcado "Converted"
                                   + e-mail de boas-vindas ao aluno

Candidato em /carreiras      ──►  DocType Candidatura + Contact
```

Tudo isso já está implementado no `vedium_core` — nenhuma ação manual
para registrar; a ação humana é **trabalhar** os leads.

## 2. Estágios do lead (usar os nativos do Frappe CRM)

| Estágio | Significado | Ação esperada |
|---|---|---|
| New | Chegou do site, ninguém falou com ele | Responder em **< 4h úteis** |
| Contacted | Primeira resposta enviada | Oferecer aula experimental |
| Qualified | Tem interesse e perfil | Enviar proposta/link de matrícula |
| Nurture | Não é agora, mas tem potencial | Entra na Newsletter Vedium |
| Unqualified / Junk | Sem perfil / spam | Arquivar |
| Converted | Matriculou (automático) | Pós-venda / onboarding |

**SLA sugerido**: lead novo respondido em até 4h úteis. Lead sem resposta
em 48h aparece no resumo semanal — cobrar no checklist.

## 3. Rotina semanal (15 min — segunda-feira)

Um e-mail automático **"[Vedium] Resumo semanal de operação"** chega toda
segunda às 08:00 (BRT) com: leads novos, matrículas, tickets, candidaturas
e erros do sistema. Checklist ao receber:

1. Todos os leads "New" foram respondidos? (`/crm`)
2. Tickets em aberto têm dono? (`/helpdesk`)
3. Matrículas da semana receberam o e-mail de boas-vindas? (automático —
   conferir spam/bounce se aluno reclamar)
4. Erros recorrentes no Error Log? (`/app/error-log`)

## 4. Suporte (Helpdesk) — configuração pendente

O Helpdesk está instalado mas sem entrada automática de e-mail. Para
transformar e-mails em tickets:

1. Criar a caixa `suporte@vediums.com` num provedor com IMAP
   (Zoho Mail free / Google Workspace — o Resend só envia, não recebe).
2. No desk: `/app/email-account/new` → preencher IMAP (entrada) e SMTP
   (saída), marcar **Enable Incoming** e apontar "Append To" = `HD Ticket`.
3. Testar: e-mail para suporte@ deve virar ticket em `/helpdesk`.

## 5. Newsletter (nutrição de leads)

- Email Group **"Newsletter Vedium"** criado na plataforma.
- ⚠️ **LGPD**: NÃO adicionar contatos automaticamente — só quem consentiu
  (checkbox no formulário ou opt-in explícito). Leads em "Nurture" podem
  ser convidados a assinar, não inscritos à força.
- Enviar via `/app/newsletter/new` → escolher o grupo → o Resend (já
  configurado) faz o disparo.

## 6. Alertas do Uptime Kuma — passo pendente (Telegram)

O Kuma monitora site, plataforma, banco, redis e o POST+Origin (regressão
histórica do LMS), mas **sem canal de notificação ninguém fica sabendo**:

1. No Telegram: falar com `@BotFather` → `/newbot` → guardar o token.
2. Falar com `@userinfobot` para obter seu chat ID.
3. No Kuma (porta 3001 do servidor, via túnel SSH:
   `ssh -L 3001:localhost:3001 root@SERVIDOR`) → Settings → Notifications
   → Add → Telegram → colar token + chat ID → marcar "Default" e
   "Apply to all existing monitors".

## 7. Acessos rápidos

| Ferramenta | URL |
|---|---|
| CRM (leads/pipeline) | `app.vediums.com/crm` |
| Helpdesk (tickets) | `app.vediums.com/helpdesk` |
| Aluno 360 (visão unificada) | `app.vediums.com/aluno_360` |
| Desk admin | `app.vediums.com/app` |
| Newsletter | `app.vediums.com/app/newsletter` |
| Candidaturas | `app.vediums.com/app/candidatura` |
