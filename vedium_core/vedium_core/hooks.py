app_name = "vedium_core"
app_title = "Vedium Core"
app_publisher = "Vedium"
app_description = "Sistema Inteligente de Gestão - Raízes de Luxo"
app_email = "contato@vediums.com"
app_license = "MIT"

# =============================================================================
# Roteamento do site
# =============================================================================
LANGUAGE_ROUTE_PREFIXES = (
    "pt-br",
    "en",
    "en-us",
    "en-au",
    "es",
    "es-ar",
    "es-co",
    "fr",
    "fr-ca",
    "de",
    "ru",
    "zh-cn",
)

PUBLIC_LANGUAGE_ROUTES = (
    "catalogo",
    # Alias canônico do catálogo em PT. Versões antigas do seletor regional
    # preservavam este slug ao trocar só o prefixo e geravam, por exemplo,
    # /en-us/cursos-de-idiomas-online (404). Mantê-lo na matriz permite
    # redirecionar qualquer variante regional ao /<idioma>/catalogo real.
    "cursos-de-idiomas-online",
    "sobre",
    "como-funciona",
    "aula-diagnostica",
    "planos",
    "matricula",
    "certificado",
    "comunidade",
    "programa-de-indicacao",
    "empresas",
    "pratica-diaria",
    "faq",
    "teste-de-nivel",
    "teste-de-nivel-ingles",
    "contato",
    "carreiras",
    "termos",
    "privacidade",
    "curso-de-ingles-online",
    "ingles-para-entrevista",
    "ingles-para-programadores",
    "ingles-executivo",
    "ingles-para-viagens",
    "ingles-para-atendimento-ao-cliente",
    "curso-de-ioruba-online",
    "ioruba-para-iniciantes",
    "ioruba-cultura-e-ancestralidade",
    "portugues-para-estrangeiros",
    "portugues-para-executivos",
    "curso-de-espanhol-online",
    "curso-de-hebraico-online",
    "preparatorio-celpe-bras",
)

# Cada prefixo de rota mapeia pra um código de idioma "de família" —
# en/en-us/en-au são todos "en" (mesmo conteúdo, só a bandeira regional
# muda); es/es-ar/es-co são todos "es"; fr/fr-ca são todos "fr". Precisa
# bater com o código usado em LANDINGS[...]["alt"] (ex.: "es", não "es-AR").
# Definido ANTES de LANGUAGE_ROUTE_RULES (que agora depende dela via
# _has_same_slug_translation) — ver uso mais abaixo também em
# _build_language_prefix_redirects().
LANGUAGE_PREFIX_FAMILY = {
    "en": "en", "en-us": "en", "en-au": "en",
    "es-ar": "es", "es-co": "es", "es": "es",
    "fr-ca": "fr", "fr": "fr",
    "de": "de",
    "ru": "ru",
    "zh-cn": "zh-cn",
}

# Prefixos de idioma que já têm home PRÓPRIA traduzida (www/<family>/index.html),
# não mais um placeholder que cai no controller PT. Cada agente de tradução
# (.claude/agents/translator-*.md) adiciona o código de família aqui ao
# publicar www/<family>/index.html — ver LANGUAGE_ROUTE_RULES e
# _build_language_prefix_redirects() logo abaixo, que já leem este set.
LANGUAGES_WITH_OWN_HOME = {"en", "es", "fr", "de", "ru"}

# Páginas de PUBLIC_LANGUAGE_ROUTES que ganharam tradução real MANTENDO O
# MESMO slug (ex.: /en/catalogo -> www/en/catalogo.html, não um slug de SEO
# diferente como as landings usam). {route: {family, ...}}. Quando uma
# página ganha tradução com slug DIFERENTE (o caso comum, ex. curso-de-
# ingles-online), ela não entra aqui — isso é resolvido via LANDINGS[...]["alt"]
# dentro de _build_language_prefix_redirects(), não aqui.
SAME_SLUG_TRANSLATIONS = {
    "catalogo": {"en", "es", "fr", "de", "ru"},
    "sobre": {"en", "es", "fr", "de", "ru"},
    "como-funciona": {"en", "es", "fr", "de", "ru"},
    "faq": {"en", "es", "fr", "de", "ru"},
    "contato": {"en", "es", "fr", "de", "ru"},
    "planos": {"en", "es", "fr", "de", "ru"},
    "matricula": {"en", "es", "fr", "de", "ru"},
    "aula-diagnostica": {"en", "es", "fr", "de", "ru"},
    "certificado": {"en", "es", "fr", "de", "ru"},
    "comunidade": {"en", "es", "fr", "de", "ru"},
    "empresas": {"en", "es", "fr", "de", "ru"},
    "programa-de-indicacao": {"en", "es", "fr", "de", "ru"},
    "carreiras": {"en", "es", "fr", "de", "ru"},
    "diferenciais": {"en", "es", "fr", "de", "ru"},
    "metodologia": {"en", "es", "fr", "de", "ru"},
}


def _has_same_slug_translation(prefix, route):
    family = LANGUAGE_PREFIX_FAMILY.get(prefix, prefix)
    return family in SAME_SLUG_TRANSLATIONS.get(route, set())


LANGUAGE_ROUTE_RULES = (
    # Prefixos com home própria (ver LANGUAGES_WITH_OWN_HOME) ficam de fora:
    # www/<family>/index.html é uma home real traduzida (não mais um
    # placeholder) — deixa a resolução de pasta padrão do Frappe
    # (www/<family>/index.html -> rota "<family>") servir, em vez de forçar
    # pro controller index (PT) como os demais prefixos ainda sem home própria.
    [
        {"from_route": f"/{prefix}", "to_route": "index"}
        for prefix in LANGUAGE_ROUTE_PREFIXES
        if LANGUAGE_PREFIX_FAMILY.get(prefix, prefix) not in LANGUAGES_WITH_OWN_HOME
    ]
    + [
        {"from_route": f"/{prefix}/{route}", "to_route": route}
        for prefix in LANGUAGE_ROUTE_PREFIXES
        for route in PUBLIC_LANGUAGE_ROUTES
        # Mesmo motivo do "en" acima: se existe página real sob o mesmo
        # slug (www/<family>/<route>.html), não força pro controller PT —
        # deixa a resolução de pasta do Frappe servir a tradução real.
        if not _has_same_slug_translation(prefix, route)
    ]
    + [
        {"from_route": f"/{prefix}/curso/<course>", "to_route": "curso"}
        for prefix in LANGUAGE_ROUTE_PREFIXES
    ]
)


def _build_language_prefix_redirects():
    """As regras acima (LANGUAGE_ROUTE_RULES) servem a MESMA página em
    português sob um prefixo de outro idioma — isso dependia do JS
    vedium-language.min.js traduzir o texto na hora. Esse JS foi desligado
    (localizePage() virou no-op, travava o navegador) e nunca teve suporte
    pra espanhol/francês/alemão/russo/chinês. Resultado: /en-us/contato,
    /en/curso-de-ioruba-online etc. prometiam outro idioma na URL e
    entregavam português puro — achado pelo usuário em produção
    (2026-07-03), com screenshot de /en-us/portuguese-for-executives (que
    nem existe nesse sistema antigo) e /en-us/contato (que existe, mas em
    português).

    frappe.website.path_resolver.resolve_redirect() roda ANTES da
    resolução de website_route_rules — então basta ADICIONAR redirects
    aqui; não precisa remover LANGUAGE_ROUTE_RULES (essas rotas continuam
    existindo pra quem não tiver o redirect correspondente, mas na prática
    o redirect sempre intercepta primeiro pros casos abaixo).

    Regra: se existe tradução REAL (LANDINGS[...]["alt"][<lang>], pra
    QUALQUER idioma — não só inglês —, ou a lista manual abaixo pra
    páginas fora do dict LANDINGS), redireciona pra ela; senão, redireciona
    pro canônico em português. Nunca mais serve conteúdo desalinhado do
    idioma prometido pela URL. 100% dirigido pelo conteúdo real que existe
    — conforme agentes de tradução (.claude/agents/translator-*.md)
    publicam páginas novas em es/fr/de/ru/zh, elas entram automaticamente
    aqui sem precisar editar hooks.py de novo.
    """
    from vedium_core.marketing_landing_content import LANDINGS

    # {"teste-de-nivel": {"en": "portuguese-placement-test"}, ...} —
    # páginas com tradução real que não são entradas em LANDINGS
    # (controllers próprios, não landing pages).
    pt_to_lang_slug = {
        "cursos-de-idiomas-online": {
            "en": "catalogo",
            "es": "catalogo",
            "fr": "catalogo",
            "de": "catalogo",
            "ru": "catalogo",
        },
        "teste-de-nivel": {
            "en": "portuguese-placement-test",
            "es": "prueba-de-nivel-de-portugues",
            "fr": "test-de-niveau-de-portugais",
            "de": "portugiesisch-einstufungstest",
        },
    }
    for slug, landing in LANDINGS.items():
        alt = landing.get("alt") or {}
        if alt.get("pt-BR") != slug:
            continue
        for lang, alt_slug in alt.items():
            if lang == "pt-BR" or not alt_slug:
                continue
            pt_to_lang_slug.setdefault(slug, {})[lang] = alt_slug

    # Páginas traduzidas mantendo o MESMO slug (ex.: /en/catalogo) —
    # ver SAME_SLUG_TRANSLATIONS logo acima de LANGUAGE_ROUTE_RULES.
    for route, families in SAME_SLUG_TRANSLATIONS.items():
        for family in families:
            pt_to_lang_slug.setdefault(route, {})[family] = route

    redirects = []
    for prefix in LANGUAGE_ROUTE_PREFIXES:
        if prefix == "pt-br":
            continue
        family = LANGUAGE_PREFIX_FAMILY.get(prefix, prefix)
        # Home do idioma: só famílias em LANGUAGES_WITH_OWN_HOME têm home
        # traduzida de verdade (www/<family>/index.html) — prefixos da mesma
        # família (en-us/en-au, es-ar/es-co) também caem nela; os demais
        # idiomas sem home própria ainda voltam pro PT.
        home_target = f"/{family}" if family in LANGUAGES_WITH_OWN_HOME else "/"
        # Evita redirect /en -> /en (self-redirect): "en"/"es" já são
        # servidos direto por www/<family>/index.html via resolução de pasta
        # do Frappe, não precisa de entrada aqui (só os prefixos regionais da
        # mesma família, ex. en-us/en-au/es-ar/es-co, precisam do redirect
        # pra cair na home real).
        if f"/{prefix}" != home_target:
            redirects.append({"source": f"/{prefix}", "target": home_target})
        for route in PUBLIC_LANGUAGE_ROUTES:
            translated_slug = pt_to_lang_slug.get(route, {}).get(family)
            target = f"/{family}/{translated_slug}" if translated_slug else f"/{route}"
            source = f"/{prefix}/{route}"
            # Evita self-redirect (ex.: /en/catalogo -> /en/catalogo quando
            # a tradução mantém o mesmo slug) — nesse caso a página real já
            # existe em www/<family>/<slug>.html e é servida direto.
            if source == target:
                continue
            redirects.append({"source": source, "target": target})
        # en/es/fr/de/ru/curso/<slug> já tem rota + tradução de verdade
        # (curso.py, via course_translations.COURSE_TRANSLATIONS) — só os
        # OUTROS prefixos (zh-cn etc.) precisam cair de volta pro curso
        # em PT. curso.py já trata, por curso individual, o caso de um
        # desses 5 idiomas pedir um slug sem tradução (redireciona pro PT
        # dentro do próprio controller — ver "req_lang not in
        # translations_for_course" em www/curso.py).
        if family not in ("en", "es", "fr", "de", "ru"):
            redirects.append({
                "source": rf"/{prefix}/curso/(.*)",
                "target": r"/curso/\1",
            })
    return redirects


LANGUAGE_PREFIX_REDIRECTS = _build_language_prefix_redirects()

from vedium_core.course_urls import legacy_course_redirects
from vedium_core.blog_content import legacy_blog_redirects

website_route_rules = [
    *LANGUAGE_ROUTE_RULES,
    {"from_route": "/sw.js", "to_route": "sw"},
    # Mesmo padrão do /sw.js: serve o manifest.json na raiz (escopo exigido
    # pelo PWA) via Frappe, contornando o nginx (achado do QA 2026-07-01: o
    # nginx tinha um alias fixo para /opt/vedium/pwa/manifest.json, pasta que
    # nunca existiu no host — 404 sempre. Ver docs/plataforma/pendente-pwa-marketing-404.md
    # para o que ainda falta corrigir na config do nginx, fora deste repo).
    {"from_route": "/manifest.json", "to_route": "manifest"},
    # /courses é interceptado pelo LMS app — garante que /catalogo seja a rota do site
    {"from_route": "/trilhas", "to_route": "catalogo"},
    {"from_route": "/cursos", "to_route": "catalogo"},
    {"from_route": "/cursos-de-idiomas-online", "to_route": "catalogo"},
    # Páginas de curso server-rendered (SEO + Schema) — /curso/<slug>
    {"from_route": "/curso/<course>", "to_route": "curso"},
    # Mesma página de curso, versão em inglês (mesmo controller: curso.py
    # detecta o prefixo /en/ e sobrepõe título/descrição via
    # course_translations.COURSE_TRANSLATIONS — só existe para Iorubá e PLE,
    # que têm público que não fala PT). Sem isso, /en/curso/<slug> 404 antes
    # de chegar no controller.
    {"from_route": "/en/curso/<course>", "to_route": "curso"},
    {"from_route": "/es/curso/<course>", "to_route": "curso"},
    {"from_route": "/fr/curso/<course>", "to_route": "curso"},
    {"from_route": "/de/curso/<course>", "to_route": "curso"},
    # Mesmo padrão acima, agora para russo (COURSE_TRANSLATIONS ganhou
    # entradas "ru" pros cursos de Iorubá e PLE no rollout de tradução ru).
    {"from_route": "/ru/curso/<course>", "to_route": "curso"},
    # Post de blog dinâmico — busca no doctype Vedium Blog Post (painel) e,
    # se não achar, no dict de código (blog_content.BLOG_POSTS). Route rules
    # do Frappe têm prioridade sobre arquivos www/ estáticos, então TODOS os
    # posts (inclusive os antigos) passam por aqui agora — não há mais
    # www/blog/<slug>.html individuais.
    {"from_route": "/blog/<slug>", "to_route": "blog_post"},
    # Estrutura por categoria (2026-07-14, ver blog_content.CATEGORY_PAGES):
    # /blog/<slug> acima também serve as páginas de categoria PT (ingles,
    # ioruba, hebraico, espanhol — blog_post.py detecta pelo nome reservado).
    # Artigos NOVOS (publicados depois da reestruturação) ficam aninhados
    # sob a categoria: /blog/<categoria>/<slug>.
    {"from_route": "/blog/<category>/<slug>", "to_route": "blog_post"},
    # Blog PLE (Português para Estrangeiros) com prefixo de idioma ANTES de
    # /blog — ver www/blog.py e www/blog_post.py, que detectam o prefixo via
    # frappe.local.path (mesmo padrão do /en/curso/<course> acima). Hoje só
    # en/es têm conteúdo real planejado no calendário editorial; fr/de/ru/
    # zh-cn entram aqui quando ganharem posts.
    {"from_route": "/en/blog", "to_route": "blog"},
    {"from_route": "/es/blog", "to_route": "blog"},
    {"from_route": "/en/blog/<category>", "to_route": "blog_post"},
    {"from_route": "/es/blog/<category>", "to_route": "blog_post"},
    {"from_route": "/en/blog/<category>/<slug>", "to_route": "blog_post"},
    {"from_route": "/es/blog/<category>/<slug>", "to_route": "blog_post"},
]

# Redirecionamentos 301 (SEO) — URLs antigas/removidas -> destino canônico
website_redirects = [
    *LANGUAGE_PREFIX_REDIRECTS,
    *legacy_course_redirects(),
    *legacy_blog_redirects(),
    {"source": "/course-details", "target": "/cursos-de-idiomas-online"},
    {"source": "/course-details.html", "target": "/cursos-de-idiomas-online"},
    {"source": "/catalogo", "target": "/cursos-de-idiomas-online"},
    {"source": "/index.html", "target": "/"},
    {"source": "/news", "target": "/cursos-de-idiomas-online"},
    {"source": "/news-details", "target": "/cursos-de-idiomas-online"},
    {"source": "/news.html", "target": "/cursos-de-idiomas-online"},
    # URLs em portugues (paginas renomeadas)
    {"source": "/about", "target": "/sobre"},
    {"source": "/sobre.html", "target": "/sobre"},
    {"source": "/contact", "target": "/contato"},
    {"source": "/contact.html", "target": "/contato"},
    {"source": "/teachers-1", "target": "/sobre"},
    {"source": "/mentores", "target": "/sobre"},
    {"source": "/professores", "target": "/sobre"},
    {"source": "/professor-busayo-frank-alonge", "target": "/curso-de-ioruba-online"},
    # Atalhos para fora do www/ precisam ser REDIRECT, não route rule:
    # website_route_rules só resolve templates do próprio www/ — apontar
    # to_route para /lms/... ou /app dava 404 (achado do QA 2026-07-01).
    {"source": "/aluno", "target": "https://app.vediums.com/lms/courses"},
    {"source": "/admin", "target": "https://app.vediums.com/app"},
    {"source": "/rh", "target": "https://app.vediums.com/app/employee"},
    {"source": "/financeiro", "target": "https://app.vediums.com/app/accounts"},
    {"source": "/stripe_checkout", "target": "/catalogo"},
]

# App Logo
app_logo_url = "/assets/vedium_core/images/vedium-logo-reta.svg"

# Website Favicon
website_favicon = "/assets/vedium_core/vedium_assets/images/logos/Icone-color.png"

# Home Page
home_page = "index"

# =============================================================================
# Web Includes - PWA & Tailwind
# =============================================================================

# CSS Includes (loaded on every page)
app_include_css = [
    "/assets/vedium_core/css/vedium.css",
    "/assets/vedium_core/css/luxo_theme.min.css",
]

# JS Includes (loaded on every page)
app_include_js = []

# Website CSS
web_include_css = [
    "/assets/vedium_core/css/vedium.css",
    "/assets/vedium_core/css/luxo_theme.min.css",
]

# Website JS
web_include_js = [
    "/assets/vedium_core/js/pwa-register.min.js?v=static-v4",
    "/assets/vedium_core/js/cookie-consent.min.js?v=mobile-pwa-fix",
    "/assets/vedium_core/js/meta-pixel.min.js?v=consent-lgpd",
    "/assets/vedium_core/js/push-notifications.min.js?v=1",
    "/assets/vedium_core/js/course_checkout_override.js",
]

# =============================================================================
# PWA publico seguro
# O SW antigo cacheava navegacao/API e quebrava o LMS (telas brancas).
# O registro atual fica restrito a vediums.com/www e o SW ignora navegacao,
# /api, /app, /lms, /login e checkout.
# =============================================================================

# Theme Color (barra do navegador mobile) — azul da marca
app_theme_color = "#2E6DA4"

# =============================================================================
# Website Context - Bottom Navigation & PWA
# =============================================================================

website_context = {
    "favicon": "/assets/vedium_core/vedium_assets/images/logos/Icone-color.png",
    "splash_image": "/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
    "brand_html": (
        '<img alt="Vedium" src="/assets/vedium_core/images/vedium-logo-reta.svg" '
        'style="height:28px;">'
    ),
}

# =============================================================================
# Jinja Customizations
# =============================================================================


# Add custom context to all web pages
def get_web_context(context):
    context.pwa_enabled = True
    context.theme_color = "#2E6DA4"
    context.background_color = "#0f1419"
    # Website Settings ainda contém um caminho legado inexistente
    # (/images/vedium-logo.png). Força o asset versionado em toda página
    # que usa templates/web.html, como Carreiras.
    context.brand_html = website_context["brand_html"]
    context.splash_image = website_context["splash_image"]
    return context


# =============================================================================
# Override Templates
# =============================================================================

# Override Standard Templates
override_doctype_templates = {}

# Jinja Environment Customization
jinja = {
    "methods": [
        "vedium_core.marketing_landing_content.get_marketing_landing",
        "vedium_core.blog_content.get_blog_post",
        "vedium_core.blog_content.list_blog_posts",
        "vedium_core.utils.jinja_methods",
    ]
}

# =============================================================================
# Scheduled Tasks
# =============================================================================

scheduler_events = {
    "cron": {
        # Segunda-feira 11:00 UTC = 08:00 BRT — resumo semanal de operação
        "0 11 * * 1": ["vedium_core.reports.send_weekly_digest"],
    },
    # Trial de 7 dias: expira matrículas Trial vencidas
    "daily": [
        "vedium_core.trial.expire_trials",
        "vedium_core.stripe_billing.suspend_overdue_enrollments",
        "vedium_core.stripe_billing.send_dunning_reminders",
        # Onboarding/ativação: quem matriculou e não começou o curso recebe um
        # empurrão (e emite o evento student_not_activated pro Brevo A08/A09).
        "vedium_core.student_onboarding.detect_inactive_students",
        "vedium_core.vedium_core.doctype.registro_de_aula_vedium.registro_de_aula_vedium.remind_draft_records",
    ],
    # LGPD: auditoria semanal de solicitações pendentes há mais de 15 dias
    "weekly": [
        "vedium_core.lgpd._audit_pending_requests",
    ],
}

# =============================================================================
# Document Events
# =============================================================================

doc_events = {
    "LMS Course Progress": {
        "on_update": "vedium_core.gamification.handle_lesson_completion"
    },
    "LMS Enrollment": {
        "after_insert": [
            "vedium_core.integrations.on_enrollment",
            "vedium_core.communication.sync_enrollment",
            "vedium_core.courses.bump_courses_cache_version",
        ],
        "on_update": [
            "vedium_core.communication.sync_enrollment",
            "vedium_core.courses.bump_courses_cache_version",
        ],
        "on_trash": [
            "vedium_core.communication.remove_enrollment_membership",
            "vedium_core.courses.bump_courses_cache_version",
        ],
    },
    # Espelha Lead do CRM no Brevo (contato + eventos lead_created/
    # lead_updated/lead_status_changed/lead_converted). on_crm_lead enfileira
    # em background (queue "short", after_commit), então falha do Brevo nunca
    # bloqueia a gravação do Lead no CRM.
    "CRM Lead": {
        "after_insert": "vedium_core.brevo.on_crm_lead",
        "on_update": "vedium_core.brevo.on_crm_lead",
    },
    # Invalida o cache de páginas públicas (catálogo, landings, página de
    # curso — ver vedium_core/courses.py) sempre que dados exibidos lá mudam.
    "LMS Course": {
        "after_insert": "vedium_core.courses.bump_courses_cache_version",
        "on_update": [
            "vedium_core.courses.bump_courses_cache_version",
            "vedium_core.course_chapter_override.sync_chapter_ordering",
        ],
        "on_trash": "vedium_core.courses.bump_courses_cache_version",
    },
    "Course Chapter": {
        "after_insert": "vedium_core.courses.bump_courses_cache_version",
        "on_update": "vedium_core.courses.bump_courses_cache_version",
        "on_trash": "vedium_core.courses.bump_courses_cache_version",
    },
    "Course Lesson": {
        "after_insert": "vedium_core.courses.bump_courses_cache_version",
        "on_update": "vedium_core.courses.bump_courses_cache_version",
        "on_trash": "vedium_core.courses.bump_courses_cache_version",
    },
    "LMS Course Review": {
        "after_insert": "vedium_core.courses.bump_courses_cache_version",
        "on_update": "vedium_core.courses.bump_courses_cache_version",
        "on_trash": "vedium_core.courses.bump_courses_cache_version",
    },
    "LMS Certificate Request": {
        "after_insert": "vedium_core.notifications.notify_lms_certificate_request"
    },
    "Lesson Slot": {
        "after_insert": "vedium_core.notifications.notify_lesson_slot_booked",
        "on_update": "vedium_core.notifications.notify_lesson_slot_booked",
    },
    # Gamificação: quiz aprovado (+25 / prova final +100, só na 1ª aprovação)
    "LMS Quiz Submission": {
        "after_insert": "vedium_core.gamification.handle_quiz_submission"
    },
    # Gamificação: certificado emitido (+200 + cupom de desconto pro próximo
    # nível PLE — ver MILESTONE_NEXT_COURSE em gamification.py)
    "LMS Certificate": {
        "after_insert": "vedium_core.gamification.handle_certificate_issued"
    },
    # Professor novo (ganhou a role "Vedium Professor") entra automaticamente
    # no Raven (usuário + membro do workspace) -- ver comunication.sync_new_professor.
    # Não adiciona a nenhum canal específico, isso é manual (admin escolhe).
    "User": {
        "on_update": "vedium_core.communication.sync_new_professor",
    },
    "Discussion Reply": {
        "validate": "vedium_core.access_control.validate_discussion_reply",
    },
}

# =============================================================================
# Desk Client Scripts
# =============================================================================

doctype_js = {
    "Candidatura": "public/js/candidatura.js",
}

# =============================================================================
# Permissions
# =============================================================================

has_permission = {
    # Gate entre níveis do curso PLE (Básico -> Intermediário -> Avançado) —
    # ver vedium_core/ple_gating.py
    "LMS Course": "vedium_core.ple_gating.has_permission",
    "Course Chapter": "vedium_core.ple_gating.has_permission",
    "Course Lesson": "vedium_core.ple_gating.has_permission",
    "LMS Quiz": "vedium_core.ple_gating.has_permission",
    "LMS Batch": "vedium_core.access_control.has_batch_permission",
    "LMS Live Class": "vedium_core.access_control.has_live_class_permission",
    "Registro de Aula Vedium": "vedium_core.vedium_core.doctype.registro_de_aula_vedium.registro_de_aula_vedium.has_permission",
}

# Endpoints upstream que consultam apenas a existência da matrícula precisam
# aplicar também o status financeiro Vedium, evitando bypass do gate DocType.
override_whitelisted_methods = {
    "lms.lms.doctype.course_lesson.course_lesson.save_progress": (
        "vedium_core.access_control.save_progress"
    ),
    "lms.lms.utils.get_discussion_topics": (
        "vedium_core.access_control.get_discussion_topics"
    ),
    "lms.lms.utils.get_discussion_replies": (
        "vedium_core.access_control.get_discussion_replies"
    ),
}

# =============================================================================
# Installation
# =============================================================================

before_install = "vedium_core.install.before_install"
after_install = "vedium_core.install.after_install"
after_migrate = "vedium_core.install.after_migrate"
