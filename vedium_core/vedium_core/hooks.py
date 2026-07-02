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
    "sobre",
    "como-funciona",
    "aula-diagnostica",
    "planos",
    "matricula",
    "meu-progresso",
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
    "preparatorio-celpe-bras",
)

LANGUAGE_ROUTE_RULES = (
    [{"from_route": f"/{prefix}", "to_route": "index"} for prefix in LANGUAGE_ROUTE_PREFIXES]
    + [
        {"from_route": f"/{prefix}/{route}", "to_route": route}
        for prefix in LANGUAGE_ROUTE_PREFIXES
        for route in PUBLIC_LANGUAGE_ROUTES
    ]
    + [
        {"from_route": f"/{prefix}/curso/<course>", "to_route": "curso"}
        for prefix in LANGUAGE_ROUTE_PREFIXES
    ]
)

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
    {"from_route": "/trilhas", "to_route": "/catalogo"},
    {"from_route": "/cursos", "to_route": "/catalogo"},
    # Páginas de curso server-rendered (SEO + Schema) — /curso/<slug>
    {"from_route": "/curso/<course>", "to_route": "curso"},
    # Post de blog dinâmico — busca no doctype Vedium Blog Post (painel) e,
    # se não achar, no dict de código (blog_content.BLOG_POSTS). Route rules
    # do Frappe têm prioridade sobre arquivos www/ estáticos, então TODOS os
    # posts (inclusive os antigos) passam por aqui agora — não há mais
    # www/blog/<slug>.html individuais.
    {"from_route": "/blog/<slug>", "to_route": "blog_post"},
]

# Redirecionamentos 301 (SEO) — URLs antigas/removidas -> destino canônico
website_redirects = [
    {"source": "/course-details", "target": "/catalogo"},
    {"source": "/course-details.html", "target": "/catalogo"},
    {"source": "/index.html", "target": "/"},
    {"source": "/news", "target": "/catalogo"},
    {"source": "/news-details", "target": "/catalogo"},
    {"source": "/news.html", "target": "/catalogo"},
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
]

# App Logo
app_logo_url = "/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png"

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
    "/assets/vedium_core/css/luxo_theme.css",
]

# JS Includes (loaded on every page)
app_include_js = []

# Website CSS
web_include_css = [
    "/assets/vedium_core/css/vedium.css",
    "/assets/vedium_core/css/luxo_theme.css",
]

# Website JS
web_include_js = [
    "/assets/vedium_core/js/pwa-register.js?v=static-v4",
    "/assets/vedium_core/js/cookie-consent.js?v=mobile-pwa-fix",
    "/assets/vedium_core/js/meta-pixel.js?v=consent-lgpd",
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
}

# =============================================================================
# Jinja Customizations
# =============================================================================


# Add custom context to all web pages
def get_web_context(context):
    context.pwa_enabled = True
    context.theme_color = "#2E6DA4"
    context.background_color = "#0f1419"
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
    }
}

# =============================================================================
# Document Events
# =============================================================================

doc_events = {
    "LMS Course Progress": {
        "on_update": "vedium_core.gamification.Gamification.handle_lesson_completion"
    },
    "LMS Enrollment": {
        "after_insert": "vedium_core.integrations.on_enrollment"
    },
}

# =============================================================================
# Permissions
# =============================================================================

has_permission = {
    # "DocType": "vedium_core.permissions.has_permission"
}

# =============================================================================
# Installation
# =============================================================================

before_install = "vedium_core.install.before_install"
after_install = "vedium_core.install.after_install"
after_migrate = "vedium_core.install.after_migrate"
