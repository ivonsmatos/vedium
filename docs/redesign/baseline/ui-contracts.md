# Baseline de UI — Header, Footer e componentes com lógica

> **Fase A (baseline técnico) — 2026-08-24.** Documento read-only. Fonte: leitura completa de `templates/includes/site_navbar.html`, `templates/includes/site_footer.html` e `public/js/vedium-language.js` (versão não minificada; `.min.js` é o build servido em produção). Marcado **CONFIRMADO NO CÓDIGO** quando lido diretamente nesses arquivos.

## Header (`site_navbar.html`)

Template único e responsivo (não há markup mobile separado — o menu mobile é o mesmo `.main-menu__list` clonado em runtime por JS, ver seção "mobile" abaixo).

### Estrutura
- Barra superior: logo (sempre linka `/`, não respeita idioma atual), ícones sociais (Instagram/LinkedIn/WhatsApp), botão do seletor de idioma, bloco de contato (telefone/e-mail).
- Barra inferior: menu principal + bloco de login/registro/teste de nível.
- Modal do seletor de idioma (fora da tag `<header>`, mas dentro deste include).

### Menu principal e destinos (por idioma)

| Item | pt-BR | en | es | fr | de | ru |
|---|---|---|---|---|---|---|
| Início | `/` | `/en/` | `/es/` | `/fr/` | `/de/` | `/ru/` |
| Como funciona | `/como-funciona` | `/en/como-funciona` | `/es/como-funciona` | `/fr/como-funciona` | `/de/como-funciona` | `/ru/como-funciona` |
| Sobre | `/sobre` | `/en/sobre` | `/es/sobre` | `/fr/sobre` | `/de/sobre` | `/ru/sobre` |
| Cursos (dropdown) | `/cursos-de-idiomas-online` | `/en/catalogo` | `/es/catalogo` | `/fr/catalogo` | `/de/catalogo` | `/ru/catalogo` |
| Blog | `/blog` | `/blog` | `/blog` | `/blog` | `/blog` | `/blog` |
| FAQ | `/faq` | `/en/faq` | `/es/faq` | `/fr/faq` | `/de/faq` | `/ru/faq` |
| Contato | `/contato` | `/en/contato` | `/es/contato` | `/fr/contato` | `/de/contato` | `/ru/contato` |

Nota: Blog **nunca** traduz a URL (sempre `/blog`) — decisão consciente documentada no próprio código, não bug.

### Dropdown "Cursos" (por idioma)

| Curso | pt-br | en | es | fr | de | ru |
|---|---|---|---|---|---|---|
| Inglês | `/curso-de-ingles-online` | `/en/learn-english-online` | `/es/curso-de-ingles-online-en-vivo` | `/fr/cours-anglais-en-ligne-en-direct` | `/de/englischkurs-online-live` | `/ru/kurs-angliyskogo-online` |
| Iorubá | `/curso-de-ioruba-online` | `/en/learn-yoruba-online` | `/es/curso-de-yoruba-online` | *(cai no catálogo do idioma)* | *(idem)* | `/ru/kurs-yoruba-online` |
| Português (PLE) | `/portugues-para-estrangeiros` | `/en/learn-portuguese-brazil` | `/es/portugues-para-extranjeros` | `/fr/portugais-pour-etrangers` | `/de/portugiesisch-fuer-auslaender` | `/ru/portugalskiy-dlya-inostrantsev` |
| Espanhol | `/curso-de-espanhol-online` | *(catálogo)* | *(idem)* | *(idem)* | *(idem)* | *(idem)* |
| Hebraico | `/curso-de-hebraico-online` | *(catálogo)* | *(idem)* | *(idem)* | *(idem)* | *(idem)* |

Fallback: se o idioma atual não tem entrada pra aquele curso, o link cai no catálogo daquele idioma — nunca gera URL inventada.

### Login / Registro / Plataforma

- **Login**: `https://app.vediums.com/login` — domínio externo fixo, mesmo em qualquer idioma.
- **Registro**: `https://app.vediums.com/login#signup` — mesma rota, fragmento `#signup`.
- Repetido no footer ("Entrar na plataforma" → mesma URL de login).

### CTA "Teste de nível" — DINÂMICO, ponto crítico

Não é uma URL fixa por idioma. Resolução:
```
url   = vd_level_test_url_override (se definida)  ELSE  default do idioma
label = "Fale conosco" (se vd_level_test_contact_override)  ELSE  "Teste de nível grátis"
```
- **Default por idioma**: pt-br `/teste-de-nivel`; en `/en/portuguese-placement-test`; es `/es/prueba-de-nivel-de-portugues`; fr `/fr/test-de-niveau-de-portugais`; de `/de/portugiesisch-einstufungstest`; **ru `/ru/contato`** (russo não tem teste dedicado, cai direto em contato).
- **Override dinâmico**, setado só em `www/curso.html` a partir de `curso.py`/`get_course_level_destination()` (`course_urls.py`):
  - Curso de **Inglês** → `/teste-de-nivel-ingles`
  - Curso de **PLE** → mapa `PLE_LEVEL_TEST_URLS` por idioma
  - Curso de **Iorubá/Espanhol/Hebraico** → `/contato` (ou `/{lang}/contato`) — **e o rótulo do botão muda para "Fale conosco"**
- **Implicação para o redesign**: qualquer novo header/footer precisa continuar aceitando as duas variáveis de contexto (`vd_level_test_url_override`, `vd_level_test_contact_override`), inclusive a troca de rótulo.

### WhatsApp

- Número: **+55 11 91129-3075**, em 3 lugares: ícone social do header, ícone social do footer, e um **CTA de WhatsApp dedicado no footer** (coluna Suporte, com número visível).
- Texto pré-preenchido fixo (não varia por idioma): "Olá, quero falar com a Vedium".
- Mesmo número como `tel:` clicável e `mailto:contato@vediums.com` na barra de contato do header.
- Todo clique em link `wa.me/`/`api.whatsapp.com/` dispara `public_cta_click` via listener global (ver `analytics-contracts.md`).

### Seletor de idioma/locale

Botão no header (bandeira + label atual, ex. "BRASIL | PORTUGUÊS") abre um modal com **12 locales** em 4 grupos:

| Grupo | Locales |
|---|---|
| Global | English (`en` → `/en/`) |
| Américas | Brazil (`pt-br`), United States (`en-us`), Argentina (`es-ar`), Canada (`fr-ca`), Colombia (`es-co`) |
| EMEA | France (`fr`), Germany "DACH Region" (`de`), Spain (`es`), Russia (`ru`) |
| Ásia | China (`zh-cn`), Australia (`en-au`) |

**Mecânica da troca de idioma (`vedium-language.js`, `updateLocaleLinks`)**:
1. O `<header>` expõe `data-vd-nav-urls` (JSON) e `data-vd-nav-current`, calculados no **servidor** (Jinja) a partir de `landing.alternates` / `post.alt` / `alt_langs` da página atual.
2. Ao clicar numa bandeira, o JS busca a URL REAL daquela família de idioma no mapa; nunca troca prefixo cegamente.
3. Sem tradução real, cai em `en`, depois em `pt-br`.
4. Só faz o fallback antigo (trocar prefixo no path atual) se não houver mapa nenhum pra página atual.
5. Locales "irmãos" (en/en-us/en-au, es/es-ar/es-co, fr/fr-ca) preservam a bandeira regional escolhida via querystring `?locale=`, **sem localStorage** (removido deliberadamente).
6. **Bug real de produção corrigido em 2026-07-03**, documentado no próprio código: antes deste mecanismo, clicar na bandeira dos EUA em `/en/portuguese-for-executives` gerava 404 (`/en-us/portuguese-for-executives` nunca existiu) — o JS só trocava prefixo sem checar existência do slug.
7. `localizePage()` (tradução automática de texto solto via JS) está **DESLIGADA** desde 2026-07-02 (travava a aba). Hoje só os rótulos vindos do Jinja mudam de idioma.

### Mobile

Sem markup próprio — `vedium.js` clona `.main-menu__list` para dentro de `.mobile-nav__container` em runtime. Mesmos links, mesmo dropdown, nenhum CTA/WhatsApp exclusivo do mobile.

---

## Footer (`site_footer.html`)

Footer rico, com i18n próprio (`vd_footer_lang`, calculado independente do navbar).

### Colunas
1. **Logo/marca** — logo, tagline, ícones sociais (Instagram, LinkedIn, WhatsApp).
2. **Cursos de Idiomas** — catálogo + 5 clusters de idioma (mesmos destinos i18n do dropdown do header).
3. **Objetivos** — inglês para viagens/atendimento, português executivos, Celpe-Bras, iorubá cultura + **link de teste de nível** (mesma lógica dinâmica do header).
4. **Vedium (institucional)** — como funciona, metodologia, diferenciais, aulas ao vivo, sobre, planos, aula diagnóstica, programa de indicação, empresas.
5. **Suporte** — FAQ, Contato, **Termos/Privacidade/Cookies/Cancelamento (hardcoded, sempre PT, sem tradução em nenhum idioma)**, verificar certificado, "Entrar na plataforma" (login), **CTA WhatsApp dedicado**.

### Seções extras
- "Vedium online para você" — 8 links de nicho SEO.
- "Conteúdos gratuitos" — Blog, post iorubá, `/quanto-custa-curso-de-idiomas` e `/teste-de-nivel-ingles` (ambos **hardcoded, sem tradução em nenhum idioma**).
- "Conteúdos e oportunidades" — indicação, parcerias, carreiras, empresas, comunidade, matrícula.

### Bloco legal final
Razão social (VEDIUM GLOBAL EDUCAÇÃO E TECNOLOGIA LTDA), CNPJ 58.434.869/0001-24, copyright e link pra agência (Scaledata) — todos **hardcoded, nunca traduzidos**.

### Não existe segunda instância do seletor de idioma no footer.

### Scripts incluídos no footer
1. Snippet GTM (`GTM-P6Q2FXLK`) com guard anti-duplicação.
2. `<noscript>` do GTM.
3. `vedium-language.min.js?v=v11-n-languages`.
4. `pwa-register.min.js?v=static-v5`.

Não há script de cookie-consent incluído no footer nem no header hoje (grep de `cookie-consent`/`CookieConsent` em todo o repo = zero ocorrências, apesar de existir a página institucional `/cookies`).

---

## Componentes com dependência funcional (não são só visuais)

| Componente | Arquivo atual | Função | Dependências | Evento | Destino | Risco de redesign |
|---|---|---|---|---|---|---|
| CTA de teste de nível (header + footer) | `site_navbar.html`, `site_footer.html` | Link dinâmico cujo destino E rótulo mudam por página de curso | `vd_level_test_url_override`, `vd_level_test_contact_override` (contexto Jinja setado só por `curso.html`) | — | Varia (teste dedicado ou `/contato`) | **ALTO** — se o redesign não propagar essas 2 variáveis pra todo template de curso, o botão volta ao default errado silenciosamente |
| Seletor de idioma | `site_navbar.html` + `vedium-language.js` | Troca de locale preservando a tradução REAL da página atual (não troca prefixo cego) | `data-vd-nav-urls`/`data-vd-nav-current` no `<header>`, calculados no servidor por página | — | URL real da tradução, com fallback en→pt-br | **ALTO** — remover/renomear esses atributos reintroduz o bug de 404 de 2026-07-03 |
| Botão WhatsApp (3 instâncias) | `site_navbar.html`, `site_footer.html` (x2) | Deep link `wa.me/` com texto pré-preenchido | Nenhuma (link puro) | `public_cta_click` (2x por clique, ver drift em analytics-contracts.md) | `wa.me/5511911293075` | MÉDIO — reimplementação precisa manter `href` no padrão `wa.me/...` pro tracking global continuar funcionando |
| Formulário de contato | `www/contato.html` (INFERIDO — não lido linha a linha nesta auditoria) | Captação de lead | `public_funnel` (INFERIDO por padrão dos demais formulários) | **NENHUM confirmado** (ver gap em analytics-contracts.md) | — | MÉDIO — sem tracking hoje; qualquer redesign deveria corrigir isso, não apenas preservar |
| Teste de nível (5 variantes) | `www/teste-de-nivel*.html`, `www/en|es|fr|de/*placement*` | Formulário client-side, calcula score sem round-trip ao servidor, depois oferece captura de e-mail (só na versão inglês) | `public_funnel.get_available_diagnostic_slots`, `public_funnel.save_placement_result` | `level_test_completed`, `level_test_whatsapp_click`, (`level_test_plan_click`/`level_test_catalog_click` só PT/EN), `level_test_email_capture` (só EN) | — | **ALTO** — lógica de cálculo de nível é client-side; portar pro redesign sem re-testar cada idioma arrisca quebrar o resultado silenciosamente |
| Cards de curso (grid) | `templates/includes/marketing_landing.html`, `www/catalogo.html` | Renderiza curso ao vivo do LMS (preço, nível, link) | `vedium_core.courses.get_published_courses()` | `seo_landing_course_grid_click` | `/curso/<slug>` do idioma da landing | MÉDIO — dado é sempre live, risco está em preservar filtro/ordenação |
| Pricing/planos | `www/planos.html` | 3 cards de plano (leve/recomendado/intensivo) | Nenhuma chamada dinâmica confirmada (INFERIDO como conteúdo estático) | `plan_select_click`, `plan_platform_click` | `/matricula` | MÉDIO |
| Checkout (botões de matrícula) | `www/curso.html`, `public/js/course_checkout_override.js` | Inicia fluxo de matrícula/checkout Stripe | Ver `conversion-contracts.md` | `course_enrollment_intent_click` (2 fontes potenciais — ver drift em analytics-contracts.md) | Stripe Checkout hospedado | **ALTO** — é o ponto de conversão financeira do site |
| Locale switcher | (mesmo componente do seletor de idioma acima) | — | — | — | — | — |
| Modais | Modal do seletor de idioma (`site_navbar.html:204-238`) | Abre/fecha via `data-vd-language-open` | JS de tema (`vedium.js`) | — | — | BAIXO |
| Login/Registro (header+footer) | `site_navbar.html`, `site_footer.html` | Link fixo pra app externo | Nenhuma | — | `https://app.vediums.com/login` (+`#signup`) | BAIXO tecnicamente, mas é o único ponto de entrada pra plataforma — qualquer erro de digitação na URL quebra 100% do login |
