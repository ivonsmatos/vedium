# 01 — Mapa de Capacidades: Nativo vs. Custom

**Objetivo:** para cada necessidade de negócio da Vedium, dizer se ela já é
atendida **nativamente** pela plataforma (Frappe / ERPNext / LMS / apps oficiais)
ou por código **custom** do `vedium_core` — e onde exatamente ela vive.

> **Regra de ouro:** consulte este mapa **antes** de construir. Se há solução
> nativa, use-a. Custom só quando o nativo comprovadamente não atende.

**Verificado em produção:** 2026-07-10 (`app.vediums.com`).
**Apps instalados:** `frappe`, `erpnext`, `payments`, `lms`, `vedium_core`,
`telephony`, `helpdesk`, `crm`, `hrms`, `insights`, `wiki`.

## Legenda

| Marcação | Significado |
|----------|-------------|
| 🟢 **Nativo** | Vem pronto no Frappe/ERPNext/LMS ou app oficial. Não escrever código. |
| 🔵 **Custom** | Código próprio em `vedium_core`. Manutenção é nossa. |
| 🟡 **Híbrido** | Nativo por baixo, com uma camada custom por cima (ex.: página de marketing consumindo dado nativo). |
| ⚪ **Configurável, desligado** | Existe nativo, mas ainda não ativado/configurado. |
| 🔴 **Legado / não usar** | Existe no código mas foi substituído. Não reusar. |

---

## Aprendizado e conteúdo

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Catálogo de cursos | 🟡 Híbrido | Nativo `LMS Course`; vitrine custom em `www/catalogo.html` + `www/curso.html` | A página pública é custom (SEO/marca), mas lê os cursos nativos. |
| Cursos, capítulos, lições | 🟢 Nativo | `LMS Course`, `Course Chapter`, `Course Lesson` | Autoria pelo `/lms` (moderador/instrutor). |
| Quiz / prova dentro do curso | 🟢 Nativo | `LMS Quiz`, `LMS Question` | — |
| Teste de nível público (pré-matrícula) | 🔵 Custom | Doctypes `Placement Test`, `Placement Test Question`; páginas `www/teste-de-nivel*.html` | Separado do quiz nativo por ser público e sem login. |
| Flashcards / revisão | 🔵 Custom | Doctype `LMS Flashcard`; `www/pratica-diaria.html` | Doctype duplicado `Flashcard` (SRS/SM-2, órfão, 0 uso) removido 2026-07-01 — ver [doc 02](02-dicionario-doctypes.md). |
| Tutor de IA pedagógico | 🔴 Removido / não usar | — | Removido em 2026-07-12 porque travava a área do aluno e não havia produto estável. Dúvidas pedagógicas devem ir para LMS/Raven/Helpdesk; ver [doc 14](14-atendimento-e-tutor-ia.md). |

## Matrícula e acesso

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Matrícula no curso | 🟢 Nativo | `LMS Enrollment` | Criada por `api.create_enrollment_if_paid` após pagamento. |
| Turmas / cohortes | 🟢 Nativo | `LMS Batch`, `LMS Batch Timetable` | Base para aula em grupo (Live Class). Piloto PLE Básico Agosto/2026 criado e privado. |
| Painel do aluno | 🟢 Nativo | `/lms` | A página custom `www/meu-progresso.html` foi removida em 2026-07-12. O painel oficial é o LMS. |

## Agendamento de aulas ⭐

> Este é o bloco que causou retrabalho. **É tudo nativo do LMS.** Não existe (mais)
> caminho custom — as páginas `agendar-aula`/`minha-agenda` foram removidas.

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Aula 1-a-1 aluno↔professor por disponibilidade | 🟢 Nativo | `Course Evaluator` + `Evaluator Schedule` + `LMS Certificate Evaluation` | Professor cadastra slots e conecta Google Calendar em `/lms/user/<username>/slots`. Aluno agenda pelo curso/progresso. Gera Google Meet. |
| Aula ao vivo em grupo | 🟢 Nativo | `LMS Live Class` (+ `LMS Batch`) | Via **Zoom** (⚪ Zoom Settings ainda não configurado). Moderador cria da página da turma. |
| Convites de calendário | 🟢 Nativo | Integração Google Calendar | Google Settings **ligado** (client_id presente). Cada professor autoriza o próprio calendário. |
| Slot custom "Lesson Slot" | 🔴 Legado | Doctype `Lesson Slot` (`vedium_core`) | **Não usar.** Substituído pelo nativo. Permanentemente vazio em produção (0 registros). Leituras mortas em `meu_progresso.py` foram removidas 2026-07-01; o único uso restante é `public_funnel.get_available_diagnostic_slots` (aula diagnóstica pública), mantido de propósito e sempre retornando lista vazia até uma decisão de produto sobre portar isso para o Course Evaluator nativo. Doctype não pode ser removido enquanto esse endpoint existir. Ver [doc 02](02-dicionario-doctypes.md). |

## Avaliação e certificação

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Avaliação para certificar | 🟢 Nativo | `enable_certification` no curso + `LMS Certificate Evaluation` | Destrava o agendamento da avaliação para o aluno. |
| Emissão de certificado | 🟢/🔵 ⚠️ | Nativo `LMS Certificate`; **também** doctype custom `LMS Certificate` em `vedium_core` | ⚠️ **Ponto de confusão a reconciliar** — confirmar qual está em uso. Ver [doc 02](02-dicionario-doctypes.md) e [doc 07]. |
| Verificação pública de certificado | 🔵 Custom | `public_funnel.verify_certificate` + `www/certificado.html` | Lê `verification_code`. |

## Pagamentos, cupom e indicação

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| App de pagamentos | 🟢 Nativo (base) | app `payments` | Fornece a base; o fluxo de checkout é custom por cima. |
| Checkout / criação de sessão | 🔵 Custom | `api.create_checkout` (Stripe) | Custom para controlar preço, cupom e moeda (R$/US$). |
| Confirmação → matrícula | 🔵 Custom | `api.create_enrollment_if_paid` (webhook) | Cria `LMS Enrollment`, consome cupom, dispara indicação e e-mail. |
| Cupom de desconto | 🔵 Custom | Doctype `Coupon` | `used_count` incrementado atomicamente no webhook. |
| Programa de indicação | 🔵 Custom | `referrals.py` + doctypes `Referral`, `Referral Conversion`; `www/minhas-indicacoes` | Reaproveita o campo `coupon_code` do checkout. Ver [doc 06]. |
| Pagamento cripto | 🔴 Desativado | Gateway crypto | Desabilitado na factory (decisão ADR). |

## Engajamento e operação

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Gamificação (pontos, emblemas) | 🔵 Custom | `gamification.py`, campo `User.vedium_points`, doctype `LMS Badge Log` | `add_points` usa UPDATE atômico. |
| Comunidade / fórum | 🟢 Nativo | Discussões do LMS | Custom só a landing `www/comunidade`. É o canal recomendado para dúvidas pedagógicas humanas; ver [doc 14](14-atendimento-e-tutor-ia.md). |
| Suporte / chamados | 🟡 Híbrido | Nativo `HD Ticket` (helpdesk); fallback técnico `Support Ticket` (`vedium_core`) | Consolidado em 2026-07-08: fluxos públicos e `open_support_ticket()` criam `HD Ticket` via `vedium_core.helpdesk.create_ticket`; `Support Ticket` fica só como fallback se Helpdesk não existir. |
| CRM / leads | 🟢 Nativo | `CRM Lead` (app `crm`) | App destravado por patch manual de compatibilidade; funil público ainda não foi migrado para CRM Lead. |
| Sincronizar aluno → CRM | 🔵 Custom | `integrations.py` (`sync_student_to_crm`) | Enfileirado no `after_insert` da matrícula. |

## Comunicação e e-mail

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Envio/recebimento de e-mail | 🟢 Nativo | `Email Account` configuradas no Frappe | Contas transacionais e `suporte@vediums.com` via Microsoft 365 OAuth; suporte recebido pode virar `HD Ticket`. |
| E-mail transacional (matrícula, indicação, agendamento) | 🔵 Custom | `frappe.sendmail` em `api.py`, `referrals.py` | Nativo LMS também manda convite de avaliação/aula. |
| Notificações in-app | 🟢 Nativo | Notificações do Frappe/LMS | — |

## Marketing, SEO e i18n

| Necessidade | Status | Onde vive | Observações |
|---|---|---|---|
| Site institucional (home, sobre, contato) | 🔵 Custom | `www/*.html` + `templates/includes` | Servido em `vediums.com`. |
| Landing pages por objetivo/idioma | 🔵 Custom | `marketing_landing_content.py` (dict `LANDINGS`) + `templates/includes/marketing_landing.html` | Uma fonte central + template compartilhado. |
| Blog | 🔵 Custom | `blog_content.py` + `www/blog/*` | Índice em `/blog`. |
| Sitemap / SEO / GEO | 🔵 Custom | `sitemap.py`, `seo_utils.py`, `geo_endpoints.py`, `llms.txt` | — |
| Páginas EN de SEO internacional | 🔵 Custom | `www/en/*.html` | hreflang. |
| Tradução da plataforma | 🟢 Nativo | Traduções do Frappe | O switcher de idioma do site é custom (`vedium-language.js`). |
| PWA instalável | 🔵 Custom | `pwa-register.js`, manifest, `sw.js` | `/sw.js` e `/manifest.json` na raiz servidos pelo Frappe (`www/sw.py`, `www/manifest.py`) — mas o nginx do servidor ainda intercepta as duas URLs com um `alias` quebrado (pasta `/opt/vedium/pwa/` inexistente) e dá 404 antes de chegar no Frappe. Pendência de infra fora do repo: [pendente-pwa-marketing-404.md](pendente-pwa-marketing-404.md). |

---

## Como decidir: nativo ou custom?

```
Preciso de uma capacidade nova
        │
        ▼
Existe doctype/feature nativo que faz isso?  ──Sim──►  Usar nativo.
  (procurar no LMS, ERPNext, Frappe;                   Configurar, não codar.
   confirmar no servidor)                              Custom só a "casca" de marca/SEO se preciso (🟡).
        │
        Não
        ▼
É regra específica da Vedium que o nativo
não modela (preço/cupom/indicação/SEO)?     ──Sim──►  Custom em vedium_core,
        │                                             reaproveitando o nativo por baixo.
        Não
        ▼
Reavaliar a necessidade — provavelmente é
configuração, não código.
```

**Checklist antes de abrir editor:**
1. Procurei o doctype nativo? (`bench --site ... execute frappe.db.sql` para listar DocTypes que batem com o tema.)
2. Confirmei no servidor se já está instalado/ligado?
3. Este mapa e o [doc 02](02-dicionario-doctypes.md) confirmam que é custom mesmo?

## Pendências que este mapa expôs (a reconciliar)

- ⚠️ **Certificado:** doctype custom `LMS Certificate` vs. nativo — confirmar qual é a fonte da verdade.
- ✅ **Flashcards:** resolvido 2026-07-01 — `Flashcard` era órfão (0 uso no código, 0 registros), removido do repo. `LMS Flashcard` é o canônico.
- ✅ **Suporte:** consolidado em `HD Ticket`; `Support Ticket` é fallback técnico.
- ⚠️ **CRM:** app acessível após patch manual no servidor; risco de `bench update` desfazer o patch até haver correção upstream/commit próprio.
- 🔴 **Lesson Slot legado:** ✅ leituras mortas removidas 2026-07-01 (`meu_progresso.py`). Doctype mantido só porque `public_funnel.get_available_diagnostic_slots` ainda o consulta (sempre vazio); garantir que nada novo o referencie além disso.
