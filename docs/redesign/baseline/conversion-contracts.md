# Baseline de Conversão — cadeia CTA → sistema, por criticidade

> **Fase A (baseline técnico) — 2026-08-24.** Documento read-only. Classificação de criticidade conforme pedido pela missão: **P0** = quebra impede conversão/matrícula; **P1** = quebra compromete geração de lead; **P2** = quebra compromete mensuração/UX; **P3** = secundário.

## P0 — quebra impede conversão/matrícula

| CTA visível | Componente/template | Evento/dataLayer | Destino | Sistema posterior |
|---|---|---|---|---|
| "Matricular agora" (mensal) | `www/curso.html` (sidebar de preço) | `course_enrollment_intent_click` (`billing_period: monthly`) | `vedium_core.api.start_course_checkout` → Stripe Checkout hospedado (BRL) | Stripe → webhook assinado → LMS Enrollment (CONFIRMADO NO CÓDIGO via `checkout_base_url` em `curso.py`; fluxo completo de webhook não relido nesta auditoria — ver `billing-e2e-tester` para prova ponta a ponta) |
| "Pagar anual" | `www/curso.html` (sidebar de preço) | `course_enrollment_intent_click` (`billing_period: annual`) | mesmo endpoint de checkout, período anual | idem |
| "Acessar curso" (aluno já matriculado) | `www/curso.html` | `course_platform_click` | `https://app.vediums.com/lms/courses/<course_name>?source=public_course&intent=enrollment` | LMS nativo (Frappe LMS) |
| "Continuar na plataforma" | `www/matricula.html` (+6 idiomas) | `enrollment_intent_click` | link `#vd-platform-link` (destino exato NÃO relido nesta auditoria — provável `app.vediums.com`) | LMS / checkout |
| Login | Header + footer (todo o site) | nenhum evento confirmado | `https://app.vediums.com/login` | Frappe LMS (auth) |
| Registro | Header (todo o site) | nenhum evento confirmado | `https://app.vediums.com/login#signup` | Frappe LMS (auth) |
| CTA de teste de nível em página de curso Iorubá/Espanhol/Hebraico | `www/curso.html` (via override) | — | `/contato` (rótulo vira "Fale conosco") | Formulário de contato → CRM (INFERIDO, ver P1) |

**Ponto crítico transversal (P0)**: a lógica DINÂMICA do CTA de teste de nível (`vd_level_test_url_override`/`vd_level_test_contact_override`, ver `ui-contracts.md`) — se o redesign perder essa propagação de contexto, todo curso de Iorubá/Espanhol/Hebraico volta a oferecer um "teste de nível" que não existe para esses cursos, em vez de direcionar pra contato.

## P1 — quebra compromete geração de lead

| CTA visível | Componente/template | Evento/dataLayer | Destino | Sistema posterior |
|---|---|---|---|---|
| Teste de nível (5 variantes: PT geral, PT inglês, EN/ES/FR/DE de PLE) | `www/teste-de-nivel*.html` | `level_test_completed`, `level_test_whatsapp_click` | Cálculo client-side + WhatsApp/CRM | `public_funnel.save_placement_result` (só versão EN gera captura de e-mail) |
| Diagnóstico — agendamento | `www/aula-diagnostica.html` (+6 idiomas) | `diagnostic_schedule_click`, `diagnostic_slot_click` | WhatsApp com horário pré-selecionado | `public_funnel.get_available_diagnostic_slots` → Appointment (doctype nativo) → `appointment_events.py` (emite eventos Brevo A05/A06, per memória do projeto) |
| Formulário de interesse — Comunidade | `templates/includes/public_intent_page*.html` | `public_intent_submit` (`intent: 'comunidade'`) | `public_funnel.submit_public_intent` | CRM Lead (doc_events → Brevo, ver `hooks.py: CRM Lead.after_insert`) |
| Formulário de interesse — B2B | `www/empresas.html` (+6 idiomas) | `public_intent_submit` (`intent: 'b2b'` ou `page_intent`) | mesma função | CRM Lead → Brevo |
| CTAs WhatsApp (header, footer, landings, páginas institucionais) | dezenas de templates | `public_cta_click` (duplicado — ver drift em `analytics-contracts.md`) | `wa.me/5511911293075` | Atendimento manual (WhatsApp Business) — sem integração automática de CRM confirmada nesta leitura |
| Programa de indicação | `www/programa-de-indicacao.html` (+6 idiomas) | `referral_platform_click` | plataforma (link exato não relido) | LMS / sistema de indicação |

⚠️ **Gap confirmado**: `www/contato.html` (o formulário de contato "oficial", destino do CTA de teste de nível pra Iorubá/Espanhol/Hebraico) **não dispara nenhum evento dataLayer** hoje — mensuração do funil de contato depende só do pageview automático. Isto é uma lacuna PRÉ-EXISTENTE, não algo introduzido por esta auditoria; registrar como candidato a correção, não corrigir agora (fora do escopo desta Fase A).

## P2 — quebra compromete mensuração/UX

| CTA visível | Componente/template | Evento/dataLayer | Destino | Sistema posterior |
|---|---|---|---|---|
| "Ver planos" / "Escolher curso" (só PT/EN) | `www/teste-de-nivel.html`, `www/teste-de-nivel-ingles.html` | `level_test_plan_click`, `level_test_catalog_click` | `/planos` ou catálogo | — |
| Cards de plano | `www/planos.html` (+6 idiomas) | `plan_select_click` | — (seleção visual) | — |
| "Escolher curso e seguir" | `www/planos.html` (+6 idiomas) | `plan_platform_click` | plataforma | — |
| Cards de curso em landing SEO | `templates/includes/marketing_landing.html` | `seo_landing_course_grid_click` | `/curso/<slug>` do idioma da landing | — |
| CTA WhatsApp de landing SEO (hero/preço/rodapé) | `marketing_landing.html` (3 posições) | `seo_landing_whatsapp_click`, `seo_landing_price_whatsapp_click`, `seo_landing_bottom_whatsapp_click` | `wa.me/...` | — |
| `view_course` (pageview de curso) | `www/curso.html` | `view_course` | — (medição, não é CTA) | GA4 |

## P3 — secundário

| CTA visível | Componente/template | Evento/dataLayer | Destino |
|---|---|---|---|
| Prática diária (próxima frase / ouvir / falar) | `www/pratica-diaria.html` | `daily_practice_next`, `daily_practice_listen`, `daily_practice_speak` | interação in-page, sem navegação |
| Verificar certificado | Footer + `www/certificado.html` | nenhum evento confirmado | formulário de verificação (LMS Certificate) |

## Integrações mapeadas (visão consolidada)

| Integração | Ponto de entrada no site | Confirmação |
|---|---|---|
| **WhatsApp** | 3 links fixos (header, footer social, footer support) + CTAs contextuais em ~15 páginas | CONFIRMADO NO CÓDIGO (número e texto), NÃO CONFIRMADO se há automação além do link `wa.me/` |
| **Teste de nível** | 5 páginas dedicadas + CTA dinâmico em toda página de curso | CONFIRMADO NO CÓDIGO |
| **CRM (CRM Lead nativo)** | Formulários de intenção (Comunidade, B2B) via `public_funnel.submit_public_intent` | CONFIRMADO NO CÓDIGO: `hooks.py` doc_event `CRM Lead.after_insert` dispara `brevo.on_crm_lead` + `crm_pipeline.on_lead_created` |
| **Brevo** | Via CRM Lead (acima) e via appointment_events/retention_events/attendance_events (ciclo de vida) | CONFIRMADO NO CÓDIGO (hooks.py, scheduler_events + doc_events) — mecanismo já documentado em memória de projeto anterior ("kit Brevo A01-A20") |
| **Frappe (site institucional)** | Todo o site vediums.com | CONFIRMADO |
| **app.vediums.com (LMS)** | Login, Registro, "Acessar curso", "Continuar na plataforma" | CONFIRMADO NO CÓDIGO (URLs fixas), fora do escopo de código desta auditoria |
| **Stripe** | Checkout de matrícula (`start_course_checkout`) | CONFIRMADO NO CÓDIGO (endpoint), fluxo completo de webhook NÃO relido nesta auditoria — ver agente `billing-e2e-tester` para prova ponta a ponta já feita em sessão anterior |
| **Formulários (genéricos)** | `public_funnel.py` (endpoint único reaproveitado por Comunidade, B2B, diagnóstico) | CONFIRMADO NO CÓDIGO como padrão comum |

## Nota metodológica

Este documento cobre os pontos de conversão **confirmados no código-fonte**. Não foi feita nenhuma tentativa de disparar esses eventos em produção nem de inspecionar o GTM Preview/GA4 DebugView (fora do escopo de acesso desta auditoria — ver `baseline-summary.md`, seção "exige acesso externo").
