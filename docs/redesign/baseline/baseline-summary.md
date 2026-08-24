# Baseline Summary — Fase A (2026-08-24)

> Documento read-only. Nenhuma alteração de frontend, Python, Jinja, CSS, JS, DocType, banco, redirect, Nginx, Docker, sitemap, robots.txt, GTM/GA4, CRM, Stripe foi feita nesta fase. Fontes: `sitemap.xml`/`robots.txt` ao vivo (2026-08-24), `hooks.py`, `sitemap.py`, `course_urls.py`, `marketing_landing_content.py`, `courses.py`, `templates/includes/site_navbar.html`, `templates/includes/site_footer.html`, `public/js/vedium-language.js`, `docs/gtm/vedium-gtm-container-import.json`, `.github/workflows/deploy.yml`, e o audit paralelo já existente em `docs/redesign/01-current-stack-audit.md`/`02-route-and-seo-map.md` (mesmo dia, tratado como fonte cruzada, não reexecutado).

# Estado atual

## URLs
**336 URLs** no `sitemap.xml` de produção (contagem exata batida contra a expectativa da missão — "~336 URLs já identificadas"). Todas as 336 responderam **HTTP 200 direto, sem redirect** (`--max-redirs 0`, verificado em lote em 2026-08-24). Classificadas em 12 famílias (ver `route-families.csv` e `urls.csv`):

| Família | Contagem |
|---|---|
| blog-article | 77 |
| institutional | 51 |
| level | 50 |
| objective | 50 |
| conversion | 37 |
| blog-category | 26 |
| language-pillar | 18 |
| pt-BR (locale) | 133 |
| en | 64 |
| es | 41 |
| fr | 32 |
| de | 32 |
| ru | 34 |
| homepage / course-hub / legal / b2b | 6 cada |
| blog-hub | 3 |

Existem também rotas públicas **fora do sitemap por desenho** (não são lacunas): `/aluno`, `/aluno_360`, `/onboarding`, `/minhas-indicacoes` (área logada/dashboard, corretamente excluídas), `/catalogo`, `/trilhas`, `/cursos` (aliases que redirecionam pro canônico), `/manifest.json`, `/sw.js` (arquivos de sistema).

## Indexáveis
Da amostra detalhada de 66 URLs (uma por combinação família×idioma, no mínimo): **nenhuma** teve `noindex` no `robots` meta. `robots.txt` de produção permite `Allow: /` geral, com bloqueios explícitos só de `/desk/`, `/app/`, `/api/method/`, `/printview`, `/backups/` — e permissões **explícitas** para crawlers de IA (GPTBot, ChatGPT-User, CCBot, anthropic-ai, Claude-Web, Google-Extended), relevante pra GEO.

## Redirects
Inventário completo em `redirects.csv`: **~19 redirects fixos** confirmados linha a linha no código (`hooks.py:website_redirects` + condicionais em `www/*.py`) + **3 famílias paramétricas grandes** (não expandidas linha a linha, recomendado gerar via bench antes do redesign):
- `legacy_course_redirects()`: exatamente **54 redirects** (9 cursos com slug interno≠público × 6 variantes de idioma).
- `legacy_blog_redirects()`: até **29 redirects** (posts com categoria migrada).
- `_build_language_prefix_redirects()`: o bloco mais volumoso (até 11 prefixos × 33 rotas), existe especificamente por causa de um bug real de produção de 2026-07-03 (URL prometia um idioma, entregava português).

**1 divergência crítica confirmada**: `/pratica-diaria` deveria redirecionar por Host header (código confirma a intenção), mas produção observada (audit paralelo do mesmo dia) responde 200 sem redirecionar — causa raiz não determinada nesta Fase A.

## Idiomas/locales
**12 prefixos de rota** (`pt-br, en, en-us, en-au, es, es-ar, es-co, fr, fr-ca, de, ru, zh-cn`), agrupados em **6 famílias de conteúdo** (pt-BR, en, es, fr, de, ru). Só **5 famílias têm home própria traduzida** (en/es/fr/de/ru — `LANGUAGES_WITH_OWN_HOME`); zh-cn não tem home nem conteúdo dedicado, cai sempre no fallback PT. Seletor de idioma (12 locales no modal) é dirigido por conteúdo real por página (`data-vd-nav-urls`), nunca troca prefixo cegamente — mecanismo corrigido após incidente real de 404 em 2026-07-03.

## Integrações críticas
GTM (`GTM-P6Q2FXLK`) · GA4 (`G-TMBTXVRMLE`, só via GTM + 1 caminho server-side pro evento `purchase`) · Meta Pixel (`1539456614495904`, gated por consentimento LGPD) · WhatsApp (`+55 11 91129-3075`, 3 posições fixas) · CRM Lead nativo → Brevo (via doc_events) · Stripe Checkout (matrícula) · `app.vediums.com` (LMS/login/registro, fora deste repo) · `public_funnel.py` (endpoint comum de formulários). Ver `analytics-contracts.md` e `conversion-contracts.md`.

## Eventos críticos
**~30 nomes de evento `dataLayer.push` distintos** catalogados (ver `analytics-contracts.md`). 2 achados de drift (eventos configurados no GTM mas mortos/órfãos no código: `language_selected`, `seo_landing_test_click`) e 1 achado de duplicação sistemática (`public_cta_click` disparado 2x por clique de WhatsApp, listener global + handler local).

## Riscos P0
1. **CTA de teste de nível é dinâmico por curso** (`vd_level_test_url_override`/`vd_level_test_contact_override`) — perder essa propagação no redesign quebra silenciosamente o direcionamento pra Iorubá/Espanhol/Hebraico.
2. **Checkout de matrícula** (`course_enrollment_intent_click`, botões mensal/anual) — ponto de conversão financeira; 2 fontes potenciais do mesmo evento (template + JS de override) a reconciliar.
3. **Mecanismo de host-rewrite Nginx** que unifica vediums.com↔app.vediums.com — **não está versionado no Git**, vive só no servidor. Sem exportar essa config antes do corte do redesign, há risco real de repetir o incidente de LMS quebrado já documentado (2026-06-02).
4. **Seletor de idioma** (`data-vd-nav-urls`/`data-vd-nav-current`) — remover/renomear esses atributos reintroduz o bug de 404 de 2026-07-03.
5. **Formulário de contato sem tracking** (`contato.html`) — não é uma quebra do redesign, é uma lacuna pré-existente; registrar pra decisão consciente.

## Riscos P1
1. `/pratica-diaria` não redireciona como o código espera (divergência código↔produção não explicada).
2. Fonte de dados dupla do Blog (`Vedium Blog Post` DocType + `blog_content.BLOG_POSTS` dict) — ferramenta de migração que só olhe o DocType perde posts.
3. 13 URLs confirmadas sem `<h1>` (todas as 5 homes traduzidas, os 5 catálogos traduzidos, `/sobre`, `/en/sobre`, `/contato`).
4. GTM carrega **sem** gate de consentimento LGPD (diferente do Meta Pixel, que é gated) — achado de compliance a revisar.
5. 2 arquivos Nginx versionados no repo (`deploy/nginx/*`) divergem entre si e da produção real — nenhum dos dois deve ser aplicado como está.

## Débitos técnicos
- FontAwesome em formato SVG font legado (900KB+ por arquivo).
- Duplicação de snippet GTM (2 `<noscript>` em 7 páginas: home×6 idiomas + `curso.html`).
- Ausência de `<main>` landmark na home.
- Sem `preconnect`/`dns-prefetch` para domínios de terceiros (flagcdn.com, GTM, Meta).
- Código morto em `analytics_events.py` (4 de 5 funções não são chamadas por nada).
- Inconsistência de parâmetro (`redirect=` vs `redirect-to=`) entre controllers de auth-gate.

## Contratos que o redesign deve preservar
Checklist — ver `ui-contracts.md`, `conversion-contracts.md`, `analytics-contracts.md`, `content-contracts.md` pro detalhe de cada item:
- [x] Login/Registro sempre pra `app.vediums.com/login` (+`#signup`)
- [x] CTA de teste de nível dinâmico por curso (URL **e** rótulo)
- [x] Seletor de idioma dirigido por `data-vd-nav-urls`/`data-vd-nav-current`, nunca por troca cega de prefixo
- [x] WhatsApp com número e texto fixos, mesmo `href` em 3 posições
- [x] Legal (Termos/Privacidade/Cookies/Cancelamento) hardcoded em PT, decisão já tomada
- [x] GTM `GTM-P6Q2FXLK` presente em toda página, GA4 só via GTM
- [x] `curso.html` único servindo todos os 5 clusters × 6 idiomas (mudança aqui é sempre transversal)
- [x] `marketing_landing.html` único servindo pilares e objetivos de todos os idiomas
- [x] hreflang só quando há tradução real (nunca inventar)
- [x] Redirects 301 de `hooks.py` (fixos + as 3 famílias paramétricas)

---

# Redesign Regression Gate

Antes de qualquer rollout futuro deve ser possível confirmar:

- [ ] URLs preservadas (comparar novo sitemap.xml contra as 336 desta baseline)
- [ ] redirects preservados (comparar contra `redirects.csv`)
- [ ] canonicals preservados/corretos (comparar contra `seo-snapshot.csv` e `urls.csv`)
- [ ] sitemap coerente (336 URLs → sem 404/redirect dentro do próprio sitemap)
- [ ] robots coerente (crawlers de IA continuam permitidos; `Disallow` de áreas internas preservado)
- [ ] hreflang preservado (recíproco, só onde há tradução real — não inventar)
- [ ] structured data não degradado (Course, FAQPage, BreadcrumbList, EducationalOrganization, ContactPoint, PostalAddress presentes onde estavam)
- [ ] H1 preservado ou melhorado (linha de base: 53 das 66 amostradas TÊM h1 hoje; as 13 sem H1 são candidatas a melhoria consciente, não a regressão silenciosa)
- [ ] conteúdo crítico presente (ver `content-contracts.md` por família)
- [ ] internal links preservados (header/footer completos, ver `ui-contracts.md`)
- [ ] CTAs funcionando (P0 da tabela em `conversion-contracts.md`)
- [ ] dataLayer funcionando (os ~30 eventos catalogados em `analytics-contracts.md`, sem introduzir NEM remover duplicidade sem decisão consciente)
- [ ] GA4/GTM funcionando (`GTM-P6Q2FXLK` presente, sem duplicar noscript)
- [ ] WhatsApp funcionando (3 posições, mesmo número/texto, tracking sem duplicar)
- [ ] teste de nível funcionando (5 variantes + lógica de override dinâmico por curso)
- [ ] CRM funcionando (`public_intent_submit` → CRM Lead → Brevo)
- [ ] Stripe/checkout funcionando (`course_enrollment_intent_click` → `start_course_checkout`)
- [ ] login funcionando (`app.vediums.com/login`)
- [ ] registro funcionando (`app.vediums.com/login#signup`)
- [ ] app.vediums.com funcionando (fora do escopo de código deste repo, mas destino de múltiplos CTAs)
- [ ] mobile funcional (menu clonado via JS, sem markup próprio hoje — decidir conscientemente se o redesign muda essa estratégia)
- [ ] acessibilidade não degradada (baseline: 13/66 sem H1, 0/66 com H1 duplicado, home sem `<main>`, 1 img sem alt, 3 `<a>` vazias — ver `performance-baseline.md`)
- [ ] performance não degradada (baseline: home 147KB HTML/12 CSS/9 JS/43 img; FontAwesome SVG 900KB+; ver `performance-baseline.md`)

---

# Pendências

**Aguarda decisão do dono / fora do escopo de código:**
- Confirmar se a duplicação de `public_cta_click` (WhatsApp) deve ser corrigida — decisão de arquitetura de tracking, não desta Fase A.
- Decidir se `/pratica-diaria` migra de vez pro LMS ou permanece no site institucional (a divergência de redirect precisa de decisão, não só de fix técnico).

**Exige acesso externo (não disponível nesta sessão):**
- Search Console — relatório "International Targeting" descontinuado em 2022; hreflang validado aqui só por inspeção de código + amostra HTML, não por ferramenta nativa.
- GA4 DebugView / validação ao vivo de eventos.
- Core Web Vitals de campo (CrUX) — `performance-baseline.md` usa só medição sintética via `curl`, sem Lighthouse/PageSpeed.
- Acesso SSH/bench ao servidor de produção — impediu: (1) exportar a config Nginx ativa real, (2) rodar as funções geradoras de redirect paramétrico (`_build_language_prefix_redirects()`, `legacy_course_redirects()`, `legacy_blog_redirects()`) pra expandir `redirects.csv` linha a linha, (3) confirmar campos de acessibilidade que exigem inspeção visual/leitor de tela real.

**Encontrado, mas fora do escopo desta missão (registrar, não corrigir):**
- 4 folhas de CSS aparentemente duplicadas no `<head>` da home (`animate.css`, `custom-animate.css`, `fontawesome/all.min.css`, `jarallax.css`) — pode ser padrão `<noscript>` intencional, não confirmado.
- Ausência de `<main>` landmark na home.
- FontAwesome em formato SVG legado (candidato a otimização de performance no redesign).
- Inconsistência `redirect=` vs `redirect-to=` entre `www/onboarding.py` e os demais controllers de auth-gate.
- Código morto em `analytics_events.py`.
- 2 arquivos Nginx versionados (`deploy/nginx/vediums.com.conf`, `deploy/vediums.com.nginx`) divergem entre si — nenhum reflete a produção real; útil como referência histórica, não como fonte de verdade.
