"""Testes puros para melhorias públicas de marketing.

Estes testes rodam sem Frappe/bench e protegem o pacote seguro de produção:
não validam banco, Stripe, LMS, professores, alunos ou assinaturas.
"""
import json
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
    "faq",
]


def read_public_text():
    files = list(WWW.glob("*.html")) + list(TPL.glob("*.html")) + [WWW / "llms.txt"]
    return "\n".join(p.read_text(encoding="utf-8") for p in files if p.exists())


def test_seo_objective_pages_exist_and_link_to_existing_funnel():
    template = (TPL / "marketing_landing.html").read_text(encoding="utf-8")
    assert "O que você vai aprender" in template
    assert "Perguntas frequentes" in template
    assert "seo_landing_test_click" in template
    assert "seo_landing_whatsapp_click" in template

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


def test_public_level_test_exists_without_backend_dependency():
    html_path = WWW / "teste-de-nivel.html"
    py_path = WWW / "teste-de-nivel.py"
    assert html_path.exists()
    assert py_path.exists()
    html = html_path.read_text(encoding="utf-8")
    assert "https://vediums.com/teste-de-nivel" in html
    assert "Teste de Nível Gratuito" in html
    assert "level_test_completed" in html
    assert "Diagnóstico:" in html
    assert "Recomendação:" in html
    assert "recommendation" in html
    assert "wa.me/5511911293075" in html
    assert "A1" in html and "C1" in html
    assert "/api/method" not in html
    assert "stripe" not in html.lower()


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
    ]
    for item in forbidden:
        assert item not in text
    assert not (WWW / "mentores.html").exists()


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
    for slug in SEO_SLUGS + COMMERCIAL_SLUGS + ["teste-de-nivel"]:
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


def test_public_language_selector_and_gtm_import_are_available():
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    lang_js = (PUBLIC_JS / "vedium-language.js").read_text(encoding="utf-8")
    theme_css = (PUBLIC_CSS / "luxo_theme.css").read_text(encoding="utf-8")
    for locale in ["pt-br", "en-us", "es-ar", "fr", "de", "ru", "zh-cn"]:
        assert f'data-vd-locale="{locale}"' in navbar
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
    assert "api.whatsapp.com/send?phone=5511911293075" in footer
    assert "data-vd-location=\"floating_whatsapp\"" in footer
    assert "navigator.language" in lang_js
    assert "language_selected" in lang_js
    assert "vedium_preferred_locale" in lang_js
    assert "window.location.assign(buildLocaleUrl(locale))" in lang_js
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
    assert "CE - public_cta_click" in triggers
    assert "CE - language_selected" in triggers
