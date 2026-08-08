# 10 — Matriz de Integrações

**Verificado em produção:** 2026-07-03. O quê está conectado, onde vive a
configuração, e o nível de confiança de cada afirmação.

| Integração | Status | Onde configura | Onde é usada | Observação |
|---|---|---|---|---|
| **Google Calendar/Meet** | 🟢 Ativo | `Google Calendar` (nativo) + `LMS Google Meet Settings` | Agendamento 1-a-1 (`Course Evaluator`) e aula em grupo (`LMS Live Class`) | 3 contas: 2 pessoais (Ivon, Almir) + 1 compartilhada "Vedium Aulas ao Vivo" usada pelos 3 professores desde 2026-07-03. Meet é gerado automático pelo job `schedule_evals`, não instantâneo. |
| **Zoom** | ⚪ Não confirmado | `LMS Zoom Settings` | Alternativa a Google Meet pra `LMS Live Class` | Não confirmado se há conta configurada nesta rodada (SSH instável na checagem). A escola prefere Google Meet (decisão do usuário, 2026-07-03) — Zoom não é prioridade. |
| **Stripe** | 🟢 Ativo (principal) | `.env`/Site Config (chaves) + `api.py` (`create_checkout_session`, `stripe_webhook`) | Checkout de matrícula | Preço em R$/US$ conforme curso. Webhook cria `LMS Enrollment` via `create_enrollment_if_paid` (inclui `purchased_certificate=1` desde 2026-07-03). |
| **Cripto** | 🔴 Desativado | `factory` de gateways | — | Desligado deliberadamente (sem verificação HMAC do Coinbase Commerce; decisão de produto em ADR, ver histórico git). |
| **MercadoPago / BaseCommerce** | ⛔ Removidos (2026-08) | — | — | Gateways, funções e webhooks eliminados do código (`get_gateway` só tem `stripe`/`crypto`). Ver histórico git. |
| **E-mail transacional** | 🟢 Ativo | `Email Account` "Vedium" + fila/workers Frappe | Confirmação de matrícula, candidatura de professor, notificação de agendamento, recuperação de senha | Outgoing ligado. Desde 2026-07-08, `vedium_core.notifications` cobre candidatura em `/carreiras`, `LMS Certificate Request` e `Lesson Slot` legado com e-mail enfileirado + `Notification Log` quando possível. |
| **WhatsApp** | 🔴 Não integrado (manual) | — | Botão de link direto (`wa.me/...`) no site e no e-mail de confirmação de lead | Não há automação (lembrete de aula, confirmação de agendamento). `frappe_whatsapp` (app de terceiro, usa WhatsApp Cloud API da Meta direto) resolveria isso — ver [doc 04](04-ecossistema-frappe-oficial.md). Não instalado. |
| **Google Tag Manager (GTM)** | 🟢 Ativo | Injetado no tema do site | Eventos de funil (`view_course`, `course_enrollment_intent_click`, `course_platform_click` etc., ver `curso.py`/`curso.html`) | Confirmado nesta sessão via tráfego de rede real (`googletagmanager.com`, `G-TMBTXVRMLE`) durante teste do fluxo de agendamento. |
| **Tutor IA / LLM** | 🔴 Removido | — | — | Removido em 2026-07-12 porque o widget travava a área do aluno e não havia produto estável. Não existe endpoint Groq/LLM ativo no `vedium_core`; suporte pedagógico deve usar LMS/Raven/Helpdesk. |
| **Kaspersky / extensões de segurança do navegador** | ⚠️ Ruído observado | Lado do cliente (navegador do usuário) | — | Durante teste do fluxo de agendamento nesta sessão, tráfego de `gc.kis.v2.scr.kaspersky-labs.com` e falhas `502`/`503` em `socket.io`/`cloudflareinsights`/`fbevents` apareceram no console — não são bugs da Vedium, são extensões/antivírus do lado do cliente interferindo. Não confundir com erro real da plataforma ao debugar (like aconteceu quando o erro real de permissão do `LMS Course` ficou escondido no meio desse ruído). |

## Como isso foi verificado

Itens 🟢 foram confirmados via SSH (leitura de produção) e/ou teste real no
navegador nesta sessão (2026-07-03). Itens ⚪ são heranças de investigação
anterior ([doc 01](01-mapa-nativo-vs-custom.md)) que não foram
reconfirmadas agora — tratar como hipótese, não fato, até reverificar.
