app_name = "vedium_core"
app_title = "Vedium Core"
app_publisher = "Vedium"
app_description = "Sistema Inteligente de Gestão - Raízes de Luxo"
app_email = "contato@vedium.com"
app_license = "MIT"

# =============================================================================
# Frappe Overrides
# =============================================================================

# App Logo
app_logo_url = "/assets/vedium_core/images/vedium-logo.svg"

# Website Favicon
website_favicon = "/assets/vedium_core/images/favicon.svg"

# Home Page
home_page = "home"

# =============================================================================
# Web Includes - PWA & Tailwind
# =============================================================================

# CSS Includes (loaded on every page)
app_include_css = [
    "/assets/vedium_core/css/vedium.css",
    "/assets/vedium_core/css/luxo_theme.css"
]

# JS Includes (loaded on every page)
app_include_js = []

# Website CSS
web_include_css = [
    "/assets/vedium_core/css/vedium.css",
    "/assets/vedium_core/css/luxo_theme.css"
]

# Website JS
web_include_js = [
    "/assets/vedium_core/js/pwa-register.js"
]

# =============================================================================
# PWA Configuration
# =============================================================================

# Web Manifest
web_manifest = "/assets/vedium_core/manifest.json"

# Theme Color for PWA
app_theme_color = "#166534"

# =============================================================================
# Website Context - Bottom Navigation & PWA
# =============================================================================

website_context = {
    "favicon": "/assets/vedium_core/images/favicon.svg",
    "splash_image": "/assets/vedium_core/images/splash.png"
}

# =============================================================================
# Jinja Customizations
# =============================================================================

# Add custom context to all web pages
def get_web_context(context):
    context.pwa_enabled = True
    context.theme_color = "#166534"
    context.background_color = "#0f1419"
    return context

# =============================================================================
# Boot Session
# =============================================================================

boot_session = "vedium_core.startup.boot.boot_session"

# =============================================================================
# Override Templates
# =============================================================================

# Override Standard Templates
override_doctype_templates = {}

# Jinja Environment Customization 
jinja = {
    "methods": [
        "vedium_core.utils.jinja_methods"
    ]
}

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
    }
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
