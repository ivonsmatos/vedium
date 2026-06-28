"""Testes puros para melhorias públicas de marketing.

Estes testes rodam sem Frappe/bench e protegem o pacote seguro de produção:
não validam banco, Stripe, LMS, professores, alunos ou assinaturas.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WWW = ROOT / "vedium_core" / "vedium_core" / "www"
TPL = ROOT / "vedium_core" / "vedium_core" / "templates" / "includes"

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
    for slug in SEO_SLUGS:
        html_path = WWW / f"{slug}.html"
        py_path = WWW / f"{slug}.py"
        assert html_path.exists()
        assert py_path.exists()
        html = html_path.read_text(encoding="utf-8")
        assert f"https://vediums.com/{slug}" in html
        assert "/teste-de-nivel" in html
        assert "schema.org" in html
        assert "wa.me/5511911293075" in html
        assert "dataLayer" in html


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
    ]
    for item in forbidden:
        assert item not in text


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


def test_dynamic_sitemap_lists_public_marketing_pages():
    sitemap = (ROOT / "vedium_core" / "vedium_core" / "seo_utils.py").read_text(
        encoding="utf-8"
    )
    for slug in SEO_SLUGS + COMMERCIAL_SLUGS + ["teste-de-nivel"]:
        assert f'"/{slug}"' in sitemap
