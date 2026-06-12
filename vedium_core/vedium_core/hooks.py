app_name = "vedium_core"
app_title = "Vedium Core"
app_publisher = "Vedium"
app_description = "Sistema Inteligente de Gestão - Raízes de Luxo"
app_email = "contato@vediums.com"
app_license = "MIT"

# =============================================================================
# Roteamento do site
# =============================================================================
website_route_rules = [
    # /courses é interceptado pelo LMS app — garante que /catalogo seja a rota do site
    {"from_route": "/trilhas", "to_route": "/catalogo"},
    {"from_route": "/cursos", "to_route": "/catalogo"},
    # Páginas de curso server-rendered (SEO + Schema) — /curso/<slug>
    {"from_route": "/curso/<course>", "to_route": "curso"},
    # Atalhos amigáveis para ferramentas integradas
    {"from_route": "/aluno", "to_route": "/lms/courses"},
    {"from_route": "/admin", "to_route": "/app"},
    {"from_route": "/rh", "to_route": "/app/employee"},
    {"from_route": "/financeiro", "to_route": "/app/accounts"},
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
    {"source": "/teachers-1", "target": "/mentores"},
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
web_include_js = ["/assets/vedium_core/js/pwa-register.js", "/assets/vedium_core/js/cookie-consent.js"]

# =============================================================================
# PWA — DESATIVADO (ver pwa-register.js, que desregistra service workers)
# O SW antigo cacheava respostas 404 de API e quebrava o LMS (telas brancas).
# NÃO reativar sem estratégia network-first para /api/*.
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
    context.pwa_enabled = False  # PWA desativado — ver comentário acima
    context.theme_color = "#2E6DA4"
    context.background_color = "#0f1419"
    return context


# =============================================================================
# Override Templates
# =============================================================================

# Override Standard Templates
override_doctype_templates = {}

# Jinja Environment Customization
jinja = {"methods": ["vedium_core.utils.jinja_methods"]}

# =============================================================================
# Scheduled Tasks
# =============================================================================

scheduler_events = {
    # "cron": {
    #     "0 0 * * *": [
    #         "vedium_core.tasks.daily"
    #     ]
    # }
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
