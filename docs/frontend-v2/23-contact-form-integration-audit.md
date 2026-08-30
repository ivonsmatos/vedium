# 23 — Contact Form Integration Audit

Auditoria feita ANTES de implementar (missão F.3 seções 10-13), lendo o
código-fonte real do backend, não assumindo nada.

## CURRENT FORM

Existe um padrão de captura de interesse já em produção, usado em
várias landing pages internas (`/aula-diagnostica`, `/matricula`, etc.),
via o template compartilhado
`vedium_core/vedium_core/templates/includes/public_intent_page.html`
(e variantes `_en`/`_es`/`_fr`/`_de`/`_ru`). Campos: nome, e-mail,
WhatsApp, mensagem. JavaScript inline (`fetch` + `dataLayer.push`), sem
framework de formulário.

Este padrão **não existe ainda em nenhuma página Next** — nem no
Contato, nem em nenhuma das 9 páginas já construídas.

## CURRENT DESTINATION

```
POST /api/method/vedium_core.public_funnel.submit_public_intent
```

Lido em `vedium_core/vedium_core/public_funnel.py` (linhas 176-237).
Método Frappe `@frappe.whitelist(allow_guest=True)` — real, ativo,
público, sem autenticação necessária.

Corpo aceito (JSON ou form-encoded): `intent`, `name`, `email`, `phone`,
`course`, `plan`, `goal`, `company`, `team_size`, `source`, `message`.

`intent` precisa ser um dos valores de `ALLOWED_INTENTS`: `lead`,
`diagnostic`, `community`, `referral`, `b2b`, `review`. Não existe um
intent "contact" ou "particular" dedicado — a página de Contato usa
`lead` como intent padrão para a maioria dos assuntos e `b2b` para
Empresas (o único assunto com intent próprio e resolução de CRM Lead
Source/Status específica), carregando o assunto real (aulas
particulares, PLE, etc.) no campo `goal`, que vai para o ticket e para o
comentário do CRM Lead.

Validação server-side real: `name` e `email` obrigatórios; e-mail
validado por regex; senão `frappe.throw` com mensagem clara.

## CRM

**CONFIRMADO.** `_upsert_crm_lead_from_public_intent()` cria (ou
comenta em, se já existir por e-mail) um **CRM Lead**, só se o DocType
"CRM Lead" existir no site (checagem defensiva — não quebra se não
existir). Usa `vedium_core.crm_pipeline.resolve_lead_source`/
`resolve_lead_status` para popular `source`/`status` corretamente
(evita o bug histórico documentado no próprio código: "Website
&lt;intent&gt;" não existia como registro válido e o lead era perdido
silenciosamente). Também cria um `Contact` (Frappe core) via
`ensure_contact()`, unificando a identidade entre Helpdesk/CRM.

## BREVO

**NÃO CONFIRMADO nesta função especificamente.** `ensure_contact()` só
cria um `Contact` Frappe core — não chama a ponte Brevo diretamente
neste arquivo. A ponte Frappe→Brevo existe no projeto (kit A01-A20, ver
memória `project_email_lifecycle_brevo`), mas se ela é disparada por um
hook de `doc_events` no `CRM Lead`/`Contact` criado por este funil
específico não foi verificado nesta sessão — fora do escopo de leitura
desta auditoria (exigiria mapear todos os `doc_events` registrados no
`hooks.py`, não só este endpoint). Tratado como não confirmado — o
formulário do Contato **não depende** dessa confirmação para funcionar
(o ticket humano e o e-mail de confirmação já são reais e suficientes).

## EMAIL DESTINATION

**CONFIRMADO por código-fonte.** `_create_ticket()` (linhas 124-170):

- E-mail interno para **contato@vediums.com** (mesmo endereço já
  confirmado por HTTP na produção de `/contato`) com o resumo do
  ticket.
- E-mail de confirmação automático para o e-mail informado pelo
  próprio usuário, com o texto: "Recebemos seu interesse na Vedium...
  Se preferir atendimento imediato, fale pelo WhatsApp."
- Ambos via `frappe.sendmail`, com captura de exceção e
  `frappe.log_error` em caso de falha (não quebra a submissão se o
  e-mail falhar — o ticket/lead já foram criados antes).

## SPAM PROTECTION

**CONFIRMADO — real, ativo, server-side.**
`vedium_core.api.rate_limit_by_ip("public_intent", limit=8,
window_sec=3600)`: no máximo 8 submissões por IP por hora, com janela
fixa (expira sozinha, nunca bloqueia um IP para sempre por erro de
implementação). Ao exceder, `frappe.throw` com "Muitas tentativas.
Aguarde alguns minutos e tente novamente."

Camada adicional no lado Next (não existia antes, adicionada nesta
fase): **honeypot** — um campo invisível (`company_website`, fora da
tab order, `aria-hidden`) que, se preenchido, faz o formulário reportar
sucesso ao bot sem de fato submeter nada ao backend. Nenhum serviço
externo (Turnstile/CAPTCHA) foi introduzido — o rate-limit server-side
já é uma proteção real e o honeypot cobre a maioria dos bots simples,
consistente com "não introduzir CAPTCHA pesado sem necessidade" (missão
seção 15).

## LGPD

**Gap identificado na produção atual**: o formulário Jinja existente
(`public_intent_page.html`) não tem nenhum aviso de LGPD nem link para
a política de privacidade visível no HTML lido nesta sessão.

**Corrigido no Next**: o formulário do Contato inclui uma linha curta
próxima ao botão de envio, explicando o uso dos dados, com link real
para `/privacidade` (confirmado 200 nesta sessão). Nenhum checkbox
"aceito receber marketing" como condição obrigatória de envio — consentimento
comercial, se algum dia for necessário, precisa ser um campo separado
(missão seção 14).

## RECOMMENDED IMPLEMENTATION

Arquitetura implementada nesta fase, seguindo o diagrama conceitual da
missão (seção 12) — nunca React → DocType Frappe diretamente:

```
ContactForm (Client Component isolado, src/components/editorial/ContactForm.tsx)
  ↓ fetch POST /api/contact (mesma origem do Next, sem CORS)
Next Route Handler (src/app/api/contact/route.ts, roda no servidor)
  ↓ valida campos obrigatórios + honeypot, monta payload
  ↓ fetch server-to-server POST
https://app.vediums.com/api/method/vedium_core.public_funnel.submit_public_intent
  ↓ (Frappe: valida, rate-limita, cria ticket + CRM Lead, envia e-mails)
```

O Route Handler nunca expõe credenciais (não há credenciais — o
endpoint é `allow_guest=True`, mas ficar no servidor evita expor o host
`app.vediums.com` e a forma exata da chamada no bundle do cliente, e
permite adicionar validação/normalização própria antes de repassar).
Estados de formulário implementados: `idle` → `loading` → `success` /
`validation-error` (campo específico, texto do próprio Frappe quando
disponível) / `server-error` (mensagem genérica com fallback para
WhatsApp, mesma UX já usada no formulário Jinja). Em erro recuperável,
os dados digitados **não são apagados** (missão seção 16).

Como esta sessão não faz deploy, `https://app.vediums.com/...` não é
alcançável a partir do ambiente local (`localhost:3000` → produção
real) durante o teste automatizado — os testes desta fase cobrem os
estados de validação client-side (campo vazio, e-mail inválido,
honeypot) e a UI de loading/erro via mock, documentado explicitamente
no QA da página. A chamada real ao endpoint de produção só será exercida
após o deploy (fora do escopo desta tarefa).
