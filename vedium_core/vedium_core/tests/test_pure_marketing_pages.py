"""Testes puros para melhorias públicas de marketing.

Estes testes rodam sem Frappe/bench e protegem o pacote seguro de produção:
não validam banco, Stripe, LMS, professores, alunos ou assinaturas.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WWW = ROOT / "vedium_core" / "vedium_core" / "www"
TPL = ROOT / "vedium_core" / "vedium_core" / "templates" / "includes"
PUBLIC_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js"
PUBLIC_CSS = ROOT / "vedium_core" / "vedium_core" / "public" / "css"
GTM_IMPORT = ROOT / "docs" / "gtm" / "vedium-gtm-container-import.json"

sys.path.insert(0, str(ROOT / "vedium_core"))
from vedium_core.marketing_landing_content import LANDINGS  # noqa: E402

SEO_SLUGS = [
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
]

COMMERCIAL_SLUGS = [
    "como-funciona",
    "aula-diagnostica",
    "planos",
    "faq",
]


def read_public_text():
    files = list(WWW.glob("*.html")) + list(TPL.glob("*.html")) + [WWW / "llms.txt"]
    return "\n".join(p.read_text(encoding="utf-8") for p in files if p.exists())


def test_seo_objective_pages_exist_and_link_to_existing_funnel():
    template = (TPL / "marketing_landing.html").read_text(encoding="utf-8")
    assert "O que você vai aprender" in template
    assert "Perguntas frequentes" in template
    assert "seo_landing_whatsapp_click" in template
    assert "landing_test_url" in template
    assert "/teste-de-nivel-ingles" in template
    assert 'href="{{ landing_test_url }}" class="thm-btn"' in template
    assert "seo_landing_test_click" not in template

    for slug in SEO_SLUGS:
        html_path = WWW / f"{slug}.html"
        py_path = WWW / f"{slug}.py"
        assert html_path.exists()
        assert py_path.exists()
        html = html_path.read_text(encoding="utf-8")
        py = py_path.read_text(encoding="utf-8")
        landing = LANDINGS[slug]
        assert f'get_marketing_landing("{slug}")' in html
        assert 'marketing_landing.html' in html
        assert slug in py
        assert len(landing["lead"]) > 120
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4


def test_commercial_pages_exist_and_drive_to_public_ctas():
    for slug in COMMERCIAL_SLUGS:
        html_path = WWW / f"{slug}.html"
        py_path = WWW / f"{slug}.py"
        assert html_path.exists()
        assert py_path.exists()
        html = html_path.read_text(encoding="utf-8")
        assert f"https://vediums.com/{slug}" in html
        assert "/teste-de-nivel" in html
        assert "wa.me/5511911293075" in html
        assert "public_cta_click" in html


def test_level_test_ctas_use_native_navigation_only():
    files = [
        WWW / "index.html",
        TPL / "site_navbar.html",
        TPL / "marketing_landing.html",
        WWW / "como-funciona.html",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    assert re.search(r'href="(?:\{\{ landing_test_url \}\}|/teste-de-nivel(?:-ingles)?)"', combined)
    assert not re.search(
        r'href="(?:\{\{ landing_test_url \}\}|/teste-de-nivel(?:-ingles)?)"[^>]*\sonclick=',
        combined,
    )
    assert "seo_landing_test_click" not in combined
    assert "cta:'level_test'" not in combined


def test_public_level_test_exists_without_backend_dependency():
    html_path = WWW / "teste-de-nivel.html"
    english_html_path = WWW / "teste-de-nivel-ingles.html"
    py_path = WWW / "teste-de-nivel.py"
    english_py_path = WWW / "teste-de-nivel-ingles.py"
    assert html_path.exists()
    assert english_html_path.exists()
    assert py_path.exists()
    assert english_py_path.exists()
    html = html_path.read_text(encoding="utf-8")
    english_html = english_html_path.read_text(encoding="utf-8")
    assert "https://vediums.com/teste-de-nivel" in html
    assert "Teste de Nível de Português para Estrangeiros" in html
    assert "portuguese-level-test" in html
    assert html.count("data-correct=") == 15
    assert "/teste-de-nivel-ingles" in html
    assert "Gramática e vocabulário" in html
    assert "Compreensão de leitura" in html
    assert "Compreensão auditiva" in html
    assert "Produção escrita" in html
    assert "Produção oral" in html
    assert "Atenção passageiros" in html
    assert "médico de resgate" in html
    assert "SpeechSynthesisUtterance" in html
    assert "level_test_completed" in html
    assert "level_test_plan_click" in html
    assert "level_test_catalog_click" in html
    assert "/aula-diagnostica" in html
    assert "/planos" in html
    assert "portuguese_foreigners" in html
    assert "Diagnóstico:" in html
    assert "Recomendação:" in html
    assert "recommendation" in html
    assert "wa.me/5511911293075" in html
    assert "A1" in html and "C1" in html
    assert "/api/method" not in html
    assert "stripe" not in html.lower()
    assert "https://vediums.com/teste-de-nivel-ingles" in english_html
    assert "Teste de Nível de Inglês" in english_html
    assert "english-level-test" in english_html
    assert english_html.count("data-correct=") == 15
    assert "/teste-de-nivel" in english_html
    assert "Grammar and vocabulary" in english_html
    assert "Reading comprehension" in english_html
    assert "Listening comprehension" in english_html
    assert "Writing" in english_html
    assert "Speaking" in english_html
    assert "Flight 204 to London" in english_html
    assert "project was successful" in english_html
    assert "SpeechSynthesisUtterance" in english_html
    assert "level_test_completed" in english_html
    assert "level_test_plan_click" in english_html
    assert "level_test_catalog_click" in english_html
    assert "/aula-diagnostica" in english_html
    assert "/planos" in english_html
    assert "english_learners" in english_html
    assert "Diagnóstico:" in english_html
    assert "Recomendação:" in english_html
    assert "wa.me/5511911293075" in english_html
    assert "A1" in english_html and "C1" in english_html
    assert "/api/method" not in english_html
    assert "stripe" not in english_html.lower()


def test_public_pages_do_not_reintroduce_template_residue():
    text = read_public_text()
    forbidden = [
        "Lorem ipsum",
        "Amazing Courses",
        "Kevin Martin",
        "666 888 0000",
        "[email protected]",
        "testimonials-one",
        "Prova Social",
        "Prova social",
        "Ana Oliveira",
        "Dra. Juliana Costa",
        "pravatar.cc",
        "Company-Logos",
        "Who Will You Learn With?",
        'href="/mentores"',
        'href="/professores"',
        'href="/professor-busayo-frank-alonge"',
    ]
    for item in forbidden:
        assert item not in text
    assert not (WWW / "mentores.html").exists()
    assert not (WWW / "professores.html").exists()
    assert not (WWW / "professores.py").exists()
    assert not (WWW / "professor-busayo-frank-alonge.html").exists()
    assert not (WWW / "professor-busayo-frank-alonge.py").exists()


def test_company_legal_data_is_visible_without_touching_checkout():
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    terms = (WWW / "termos.html").read_text(encoding="utf-8")
    privacy = (WWW / "privacidade.html").read_text(encoding="utf-8")
    for text in [footer, terms, privacy]:
        assert "VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA" in text
        assert "58.434.869/0001-24" in text
    assert "Stripe" in terms
    assert "Stripe" in privacy
    assert "Direito de arrependimento" in terms
    assert "7 (sete) dias corridos" in terms
    assert "não altera o checkout" in terms


def test_llms_txt_has_current_course_level_and_objective_pages():
    llms = (WWW / "llms.txt").read_text(encoding="utf-8")
    assert "Upper Intermediário (B2)" in llms
    assert "Upper Intermediário (B1)" not in llms
    for slug in SEO_SLUGS + COMMERCIAL_SLUGS:
        assert f"https://vediums.com/{slug}" in llms
    assert "https://vediums.com/mentores" not in llms


def test_app_domain_redirect_and_catalog_level_guards_are_in_place():
    index_html = (WWW / "index.html").read_text(encoding="utf-8")
    index_py = (WWW / "index.py").read_text(encoding="utf-8")
    catalogo_py = (WWW / "catalogo.py").read_text(encoding="utf-8")
    curso_py = (WWW / "curso.py").read_text(encoding="utf-8")
    static_index = (ROOT / "deploy" / "site" / "index.html").read_text(encoding="utf-8")
    nginx_primary = (ROOT / "deploy" / "nginx" / "vediums.com.conf").read_text(encoding="utf-8")
    nginx_legacy = (ROOT / "deploy" / "vediums.com.nginx").read_text(encoding="utf-8")
    assert "app.vediums.com" in index_py
    assert 'redirect_location = "/login"' in index_py
    assert "raise frappe.Redirect" in index_py
    for html in [index_html, static_index]:
        assert "app.vediums.com" in html
        assert "window.location.replace('/login')" in html
    assert ".main-slider .swiper-slide { display: flex !important; align-items: center !important; pointer-events: none; }" in index_html
    assert ".main-slider .swiper-slide-active { pointer-events: auto; }" in index_html
    for nginx in [nginx_primary, nginx_legacy]:
        assert "location = /" in nginx
        assert "return 302 /login;" in nginx
    assert catalogo_py.index('"Upper Intermediário": "B2"') < catalogo_py.index('"Intermediário": "B1"')
    assert index_py.index('"Upper Intermediário": "B2"') < index_py.index('"Intermediário": "B1"')
    assert "_dedupe_chapters" in curso_py
    assert "_dedupe_lessons" in curso_py
    assert "chapter.lessons = _dedupe_lessons" in curso_py


def test_dynamic_sitemap_lists_public_marketing_pages():
    sitemap = (ROOT / "vedium_core" / "vedium_core" / "seo_utils.py").read_text(
        encoding="utf-8"
    )
    sitemap_page = (WWW / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_context = (WWW / "sitemap.py").read_text(encoding="utf-8")
    robots = (ROOT / "vedium_core" / "vedium_core" / "public" / "robots.txt").read_text(
        encoding="utf-8"
    )
    robots_page = (WWW / "robots.txt").read_text(encoding="utf-8")
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(
        encoding="utf-8"
    )
    for slug in SEO_SLUGS + COMMERCIAL_SLUGS + ["teste-de-nivel", "teste-de-nivel-ingles"]:
        assert f'"/{slug}"' in sitemap
        assert f'"loc": "/{slug}"' in sitemap_context
        assert f'"{slug}"' in hooks
    for prefix in ["pt-br", "en-us", "es-ar", "de", "zh-cn"]:
        assert f'"{prefix}"' in hooks
        assert f'"{prefix}"' in sitemap
        assert f'"{prefix}"' in sitemap_context
    assert '"/mentores"' not in sitemap
    assert "urlset" in sitemap_page
    assert "links" in sitemap_page
    assert "Sitemap: https://vediums.com/sitemap.xml" in robots
    assert "sitemap-courses.xml" not in robots
    assert "sitemap-llm.xml" not in robots
    assert "Sitemap: https://vediums.com/sitemap.xml" in robots_page
    assert "User-agent: *" in robots_page
    assert '{"from_route": "/sw.js", "to_route": "sw"}' in hooks


def test_public_language_selector_and_gtm_import_are_available():
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    lang_js = (PUBLIC_JS / "vedium-language.js").read_text(encoding="utf-8")
    pwa_js = (PUBLIC_JS / "pwa-register.js").read_text(encoding="utf-8")
    sw_js = (PUBLIC_JS / "sw.js").read_text(encoding="utf-8")
    root_sw_js = (WWW / "sw.js").read_text(encoding="utf-8")
    sw_py = (WWW / "sw.py").read_text(encoding="utf-8")
    cookie_js = (PUBLIC_JS / "cookie-consent.js").read_text(encoding="utf-8")
    theme_css = (PUBLIC_CSS / "luxo_theme.css").read_text(encoding="utf-8")
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(
        encoding="utf-8"
    )
    manifest = json.loads(
        (ROOT / "vedium_core" / "vedium_core" / "public" / "vedium_assets" / "images" / "favicons" / "site.webmanifest").read_text(
            encoding="utf-8"
        )
    )
    static_index = (ROOT / "deploy" / "site" / "index.html").read_text(encoding="utf-8")
    static_sw = (ROOT / "deploy" / "site" / "sw.js").read_text(encoding="utf-8")
    for locale in ["pt-br", "en-us", "es-ar", "fr", "de", "ru", "zh-cn"]:
        assert f'data-vd-locale="{locale}"' in navbar
    for href in ["/pt-br/", "/en-us/", "/es-ar/", "/de/", "/zh-cn/"]:
        assert f'href="{href}"' in navbar
    assert "data-vd-language-open" in navbar
    assert "Select your region and language" in navbar
    assert "BRASIL | PORTUGUÊS" in navbar
    assert "vedium-language-chips" not in navbar
    assert ".vedium-language-chips" in theme_css
    assert "display: none !important" in theme_css
    assert "flagcdn.com/w20/br.png" in navbar
    assert "flagcdn.com/w20/us.png" in navbar
    assert "flagcdn.com/w20/cn.png" in navbar
    assert "GTM-P6Q2FXLK" in footer
    assert "vedium-language.js?v=" in footer
    assert "pwa-register.js?v=static-v4" in footer
    assert "/assets/vedium_core/js/pwa-register.js?v=static-v4" in hooks
    assert "/assets/vedium_core/js/cookie-consent.js?v=mobile-pwa-fix" in hooks
    assert "vediumGoToLevelTest" not in footer
    assert "document.addEventListener('touchend'" not in footer
    assert "window.location.href = link.href" not in footer
    assert "api.whatsapp.com/send?phone=5511911293075" in footer
    assert "data-vd-location=\"floating_whatsapp\"" in footer
    assert "navigator.language" not in lang_js
    assert "language_selected" in lang_js
    assert "vedium_preferred_locale" not in lang_js
    assert "window.location.assign" not in lang_js
    assert 'var current = getLocaleFromPath() || "pt-br";' in lang_js
    assert "localeCopy" in lang_js
    assert "translateTextNodes" in lang_js
    assert "updateLocaleLinks" in lang_js
    assert "Take the free placement test" in lang_js
    assert "Kostenlosen Einstufungstest machen" in lang_js
    assert 'prefix: "/pt-br/"' in lang_js
    assert 'prefix: "/es-ar/"' in lang_js
    assert 'prefix: "/de/"' in lang_js
    assert "setModalOpen" in lang_js
    assert "flagcdn.com/w20/br.png" in lang_js
    assert "switchLanguage(detected" not in lang_js
    assert "switchLanguage(" not in lang_js
    assert "translate.google.com" not in lang_js
    assert "loadGoogleTranslate" not in lang_js
    assert "vediumInitGoogleTranslate" not in lang_js
    assert "google_translate_element" not in navbar
    assert "googtrans=" not in lang_js
    assert "target.closest" in lang_js
    assert "navigator.serviceWorker.register('/sw.js'" in pwa_js
    assert "fetch('/sw.js', { method: 'HEAD', cache: 'no-store' })" in pwa_js
    assert "PUBLIC_HOSTS" in pwa_js
    assert "app.vediums.com" not in pwa_js
    assert "request.mode === 'navigate'" in sw_js
    assert "request.mode === 'navigate'" in root_sw_js
    assert "request.mode === 'navigate'" in static_sw
    assert "application/javascript; charset=utf-8" in sw_py
    assert 'frappe.response["type"] = "binary"' in sw_py
    assert "'/api/'" in sw_js
    assert "'/lms'" in sw_js
    assert "'/checkout'" in sw_js
    assert "caches.match('/index.html')" not in sw_js
    assert "caches.match('/index.html')" not in static_sw
    assert "serviceWorker.register('/sw.js')" not in static_index
    assert "@media(max-width:767px)" in cookie_js
    assert "top:12px" in cookie_js
    assert "bottom:auto" in cookie_js
    assert manifest["name"] == "Vedium"
    assert manifest["short_name"] == "Vedium"
    assert manifest["start_url"] == "/"
    assert manifest["icons"][0]["src"].startswith("/assets/vedium_core/")

    gtm = json.loads(GTM_IMPORT.read_text(encoding="utf-8"))
    raw_gtm = GTM_IMPORT.read_text(encoding="utf-8")
    assert '"type": "template"' not in raw_gtm
    assert '"type": "boolean"' not in raw_gtm
    assert '"type": "integer"' not in raw_gtm
    assert '"tagFiringOption": "ONCE_PER_PAGE"' not in raw_gtm
    assert '"tagFiringOption": "oncePerLoad"' not in raw_gtm
    assert '"tagFiringOption": "ONCE_PER_EVENT"' in raw_gtm
    names = {tag["name"] for tag in gtm["containerVersion"]["tag"]}
    triggers = {trigger["name"] for trigger in gtm["containerVersion"]["trigger"]}
    assert "GA4 - Base Config" in names
    assert "GA4 - Event - Public CTA Click" in names
    assert "GA4 - Event - Level Test Completed" in names
    assert "GA4 - Event - Level Test Plan Click" in names
    assert "GA4 - Event - Level Test Catalog Click" in names
    assert "CE - public_cta_click" in triggers
    assert "CE - language_selected" in triggers
    assert "CE - level_test_plan_click" in triggers
    assert "CE - level_test_catalog_click" in triggers
