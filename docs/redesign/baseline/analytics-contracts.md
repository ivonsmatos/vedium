# Baseline de Analytics — o que não pode quebrar no redesign

> **Fase A (baseline técnico) — 2026-08-24.** Documento read-only. Nenhum evento foi criado, alterado ou removido. Fonte: leitura de código (`vedium_core/`) + `docs/gtm/vedium-gtm-container-import.json` (export do container GTM mantido no repo). Nenhuma chamada à API do GTM/GA4 foi feita — measurement ID e eventos vêm exclusivamente do que está versionado.

## GTM

- **Container ID: `GTM-P6Q2FXLK`** — CONFIRMADO NO CÓDIGO. Único e consistente em todo o site (nenhuma variação por página ou idioma).
- **Forma de carregamento**: snippet padrão (`<script>` assíncrono + `<noscript><iframe>`), com guard de dedupe (`if (d.querySelector('script[src*="'+i+'"]')) return;`).
- **Localização no código — dois padrões coexistindo (achado real, não é bug crítico, mas é inconsistência a limpar no redesign)**:
  - **Padrão principal** (a maioria das ~192 páginas): dentro de `templates/includes/site_footer.html:177-187`, no fim do `<body>` — não no `<head>` como a Google recomenda.
  - **Padrão duplicado** (7 páginas: `www/index.html` + as 5 homes traduzidas `en/es/fr/de/ru/index.html` + `www/curso.html`): têm uma **segunda cópia inline no `<head>`**, além de incluírem `site_footer.html` — o script é deduplicado, mas o `<noscript><iframe>` **não é**, gerando **2 iframes noscript** no HTML dessas 7 páginas.
- Validado por teste automatizado: `tests/test_pure_marketing_pages.py:1878-1906` (verifica o JSON do container) e `:4405-4406` (`assert "GTM-P6Q2FXLK" in html` para todo `www/**/*.html`, `assert "googletagmanager.com/gtag/js" not in html`).

## GA4

- **Não está hardcoded em nenhum template ou controller** — CONFIRMADO (grep de `gtag(`, `analytics.js`, `G-[A-Z0-9]+` em todo `vedium_core` = zero ocorrências fora do JSON do GTM).
- **Measurement ID: `G-TMBTXVRMLE`** — só existe dentro da tag `"GA4 - Base Config"` do container GTM (`docs/gtm/vedium-gtm-container-import.json:26-44,788-798`), disparada no trigger `All Pages`. Ou seja: GA4 roda 100% via GTM, client-side.
- **Perna server-side paralela (achado extra)**: `vedium_core/vedium_core/analytics_events.py:116-157` (`send_ga4_purchase_server_side`) envia o evento `purchase` direto ao GA4 **Measurement Protocol**, disparado por `stripe_billing.py:621-632` logo após confirmação de assinatura Stripe. Usa `frappe.conf.get("GA4_MEASUREMENT_ID")`/`GA4_API_SECRET` (site_config, fora do repo) e o `client_id` do cookie `_ga`.
- **Código morto (achado extra)**: `analytics_events.py` tem outras 4 funções (`track_course_view`, `track_course_enrollment`, `track_lesson_completion`, `send_analytics_event`) que não são chamadas de lugar nenhum — sobras do doc de exemplo `docs/gtm/gtm_examples.html`.

## dataLayer — eventos encontrados

Estrutura pt-BR é a canônica; as variantes en/es/fr/de/ru replicam a mesma lógica/parâmetros (só o texto visível muda, e às vezes o valor de `language`).

### Pageview automático

| Evento | Página/componente | Parâmetros | Criticidade |
|---|---|---|---|
| `view_course` | `www/curso.html` (todo carregamento de página de curso) | `course_name`, `course_category`, `course_price`, `currency` | P2 |

### Teste de nível

| Evento | Gatilho | Página/componente | Parâmetros | Criticidade |
|---|---|---|---|---|
| `level_test_completed` | submit do formulário | `/teste-de-nivel`, `/teste-de-nivel-ingles`, `/en/portuguese-placement-test`, `/es/prueba-de-nivel-de-portugues`, `/fr/test-de-niveau-de-portugais`, `/de/portugiesisch-einstufungstest` | `language`, `level`, `score`, `total_questions`, `focus`, `open_answers_filled` | **P0** — mede conclusão do funil de diagnóstico |
| `level_test_whatsapp_click` | onclick no CTA de resultado | mesmas 6 páginas | `language` | P1 |
| `level_test_plan_click` | onclick "Ver planos" | **só** `/teste-de-nivel` e `/teste-de-nivel-ingles` (ausente nas 4 variantes de PLE em outros idiomas — gap real, não corrigir aqui, só registrar) | `language` | P1 |
| `level_test_catalog_click` | onclick "Escolher curso" | idem acima | `language` | P1 |
| `level_test_email_capture` | callback de sucesso do fetch pra `public_funnel.save_placement_result` | **só** `/teste-de-nivel-ingles` (único teste com captura de e-mail) | `language: 'english_learners'`, `level` | P0 — único ponto de captação de lead do teste de inglês |

### WhatsApp / contato

| Evento | Gatilho | Página/componente | Parâmetros | Criticidade |
|---|---|---|---|---|
| `public_cta_click` (genérico, delegação global) | listener global de clique (`vedium-language.js:773-782`, capture phase, `document`) em **qualquer** link `wa.me/`/`api.whatsapp.com/` | site inteiro (via `web_include_js`) | `location` (`data-vd-location` do link, ou `'whatsapp_link'`), `cta: 'whatsapp'` | P1 |
| `public_cta_click` (explícito por página) | onclick inline | dezenas de páginas: home (4 CTAs), como-funciona, faq, diferenciais, metodologia, matricula, planos, parcerias, quanto-custa, aulas-ao-vivo, aula-diagnostica, `public_intent_page*` | `location` (slug da seção), `cta` | P1 |
| `diagnostic_schedule_click` | onclick nos 3 cards de agendamento | `/aula-diagnostica` + 6 idiomas | `language`, `location: 'aula_diagnostica'` | P1 |
| `diagnostic_slot_click` | onclick em horário real (gerado via fetch a `get_available_diagnostic_slots`) | `/aula-diagnostica` + 6 idiomas | `slot` | P1 |
| `public_intent_submit` | callback de sucesso do form (`submit_public_intent`) | Comunidade (`public_intent_page*.html`) e `/empresas` + 6 idiomas | `intent`, `location` | **P0/P1** — geração de lead |

⚠️ **Gap confirmado**: `contato.html` (o formulário de contato em si) **não dispara nenhum evento dataLayer** — nem pageview custom nem submit. Ver seção "componentes com dependência funcional" em `ui-contracts.md`.

### Matrícula / checkout / curso

| Evento | Gatilho | Página/componente | Parâmetros | Criticidade |
|---|---|---|---|---|
| `enrollment_intent_click` | click em "Continuar na plataforma" | `/matricula` + 6 idiomas | `course`, `plan`, `goal`, `location: 'matricula'` | **P0** |
| `enrollment_whatsapp_click` | click no CTA de dúvida | `/matricula` + 6 idiomas | `course`, `plan`, `goal`, `location: 'matricula'` | P1 |
| `course_platform_click` | onclick "Acessar" (aluno já matriculado) | `www/curso.html` | `course`, `location: 'course_detail'` | **P0** |
| `course_enrollment_intent_click` | onclick nos botões de matricular (mensal/anual) | `www/curso.html` — **e também** `public/js/course_checkout_override.js` (2 fontes potenciais do mesmo evento — verificar duplicidade no redesign) | `course`, `billing_period`, `location: 'course_detail'` (+ `classes_per_week` na versão do JS) | **P0** |
| `plan_select_click` | onclick nos 3 cards de plano | `/planos` + 6 idiomas | `plan`, `location: 'planos'` | P1 |
| `plan_platform_click` | onclick "Escolher curso e seguir" | `/planos` + 6 idiomas | `location: 'planos'` | P1 |
| `referral_platform_click` | onclick "Pegar meu código" | `/programa-de-indicacao` + 6 idiomas | `location: 'programa_de_indicacao'` | P2 |

### SEO Landing pages (`marketing_landing.html`)

| Evento | Gatilho | Parâmetros | Criticidade |
|---|---|---|---|
| `seo_landing_whatsapp_click` | onclick CTA WhatsApp do hero | `landing: landing.slug` | P1 |
| `seo_landing_course_grid_click` | onclick em card do grid | `landing`, `course` | P1 |
| `seo_landing_price_whatsapp_click` | onclick CTA da seção de preço | `landing` | P1 |
| `seo_landing_bottom_whatsapp_click` | onclick CTA final | `landing` | P1 |

### Prática diária

| Evento | Gatilho | Parâmetros | Criticidade |
|---|---|---|---|
| `daily_practice_next` | click "Próxima frase" | `language`, `level` | P3 |
| `daily_practice_listen` | click "Ouvir" | `language`, `level` | P3 |
| `daily_practice_speak` | click "Falar" | `language`, `level` (INFERIDO por simetria com os 2 acima — parâmetro exato não conferido linha a linha) | P3 |

### Login / registro

**Não há eventos `login`/`sign_up` no repo.** Login e checkout real acontecem em `app.vediums.com` (LMS separado), fora do escopo deste repositório.

## Achados de drift (GTM configurado ≠ código real) — prioridade para o redesign

1. **`language_selected`** — o GTM tem tag+trigger configurados (`vedium-gtm-container-import.json:181-198,546-566`), mas o código que disparava esse evento (`localizePage()` em `vedium-language.js`) foi **desligado** em 2026-07-02 (travava a aba). Trigger morto hoje.
2. **`seo_landing_test_click`** — GTM tem tag+trigger configurados, mas **não existe nenhum `dataLayer.push` com esse nome no código**. O link "fazer teste de nível" da landing (`landing_test_url`) é renderizado sem `onclick`. Trigger órfão, nunca disparado.
3. **Duplicação sistemática de `public_cta_click`**: o listener global (item acima) roda em capture phase sem `stopPropagation()`, e várias páginas TAMBÉM têm `onclick` local nos mesmos links de WhatsApp — **um clique dispara 2 pushes** (um específico + um genérico). Infla a contagem de `public_cta_click` no GA4/GTM em praticamente todo clique de WhatsApp do site hoje.

## Outros pixels de terceiros

| Ferramenta | Status | ID | Localização | Observação |
|---|---|---|---|---|
| **Meta Pixel** | Presente | `1539456614495904` | `public/js/meta-pixel.js`, carregado globalmente | Só `init` + `PageView` automático, nenhum evento custom. **Gated por consentimento LGPD** (`localStorage.vedium_cookie_consent`) — diferente do GTM, que carrega incondicionalmente (achado de compliance a revisar no redesign) |
| LinkedIn Insight Tag | Ausente | — | — | — |
| Hotjar | Ausente | — | — | único match era falso-positivo (ícone FontAwesome) |
| Microsoft Clarity | Ausente | — | — | — |
| TikTok Pixel / Pinterest Tag | Ausente | — | — | — |

## Páginas confirmadas SEM nenhum evento custom (só GA4 base via GTM)

`contato.html`, `aluno.html`, `catalogo.html`, `blog.html`, `blog_post.html`, `blog_category.html`, `sobre.html`, `imprensa.html`, `termos.html`, `cookies.html`, `privacidade.html`, `certificado.html`, `carreiras.html`, `cancelamento-reembolso.html`, `propriedade-intelectual.html`, `gravacao-imagem-voz.html`, `minhas-indicacoes.html`.
