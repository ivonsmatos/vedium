import sys
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.course_urls import (  # noqa: E402
    ENGLISH_COURSE_SEO_TITLES,
    get_course_level_destination,
    get_course_navigation,
    get_course_seo_title,
)


ROOT = Path(__file__).resolve().parents[3]
WWW = ROOT / "vedium_core" / "vedium_core" / "www"


def test_english_course_navigation_follows_the_canonical_a1_to_c1_trail():
    navigation = get_course_navigation("ingl-s-elementary")

    assert navigation["previous"] == {
        "label": "Inglês A1 — Iniciante",
        "url": "/curso/ingles-basico-a1",
    }
    assert navigation["next"] == {
        "label": "Inglês A2+ — Pré-Intermediário",
        "url": "/curso/ingles-pre-intermediario",
    }
    assert navigation["pillar"]["url"] == "/curso-de-ingles-online"
    assert navigation["current"]["level"] == "A2"


def test_all_english_level_titles_are_unique_and_fit_the_search_snippet_target():
    assert len(set(ENGLISH_COURSE_SEO_TITLES.values())) == 6
    assert all(len(title) <= 60 for title in ENGLISH_COURSE_SEO_TITLES.values())
    assert get_course_seo_title("ingl-s-beginner", "fallback") == (
        "Inglês A1 Iniciante Online ao Vivo | Vedium"
    )
    assert get_course_seo_title("espanhol-basico", "Espanhol Básico") == (
        "Espanhol Básico — Curso de Idiomas Online ao Vivo | Vedium"
    )
    assert ENGLISH_COURSE_SEO_TITLES["ingl-s-intermedi-rio"].startswith(
        "Inglês B1 Intermediário"
    )


def test_courses_without_an_approved_linear_trail_hide_navigation():
    assert get_course_navigation("hebraico-particular") is None
    assert get_course_navigation("portugues-para-estrangeiros-basico") is None


def test_course_diagnostic_destination_uses_the_taught_language():
    assert get_course_level_destination("ingl-s-beginner") == (
        "/teste-de-nivel-ingles",
        False,
    )
    assert get_course_level_destination(
        "portugues-para-estrangeiros-basico", "en"
    ) == ("/en/portuguese-placement-test", False)
    assert get_course_level_destination("iorub-b-sico", "fr") == (
        "/fr/contato",
        True,
    )
    assert get_course_level_destination("espanhol-basico") == ("/contato", True)
    assert get_course_level_destination("hebraico-particular") == ("/contato", True)


def test_course_template_has_one_semantic_title_and_non_heading_price():
    template = (WWW / "curso.html").read_text(encoding="utf-8")

    assert template.count("<h1>{{ course.title }}</h1>") == 1
    assert '<p class="courses-one__single-content-title">{{ course.title }}</p>' in template
    assert '<p class="course-details__price-amount">' in template
    assert '<h2 class="course-details__price-amount">' not in template
    assert 'class="course-details__trail"' in template
    assert 'href="{{ related_courses.pillar.url }}"' in template
    assert '<meta property="og:title" content="{{ title }}" />' in template
    assert "related_courses.current.level" in template
    assert 'width="1200" height="675"' in template
    assert "{%- set vd_level_test_url =" not in template
    assert "level_test_is_contact" in template
    assert "vd_level_test_url_override = level_test_url" in template
    assert "vd_level_test_contact_override = level_test_is_contact" in template

    controller = (WWW / "curso.py").read_text(encoding="utf-8")
    assert "PUBLIC_ENROLLMENT_COUNT_THRESHOLD = 10" in controller
    assert "context.public_enrollment_count" in controller
    assert "context.level_test_url, context.level_test_is_contact" in controller

    navbar = (
        ROOT
        / "vedium_core"
        / "vedium_core"
        / "templates"
        / "includes"
        / "site_navbar.html"
    ).read_text(encoding="utf-8")
    footer = (
        ROOT
        / "vedium_core"
        / "vedium_core"
        / "templates"
        / "includes"
        / "site_footer.html"
    ).read_text(encoding="utf-8")
    assert "vd_level_test_url_override" in navbar
    assert "vd_menu_free_test_url" in navbar
    assert "vd_level_test_url_override" in footer
    assert "vd_footer_level_test_url" in footer


def test_course_breadcrumb_schema_closes_the_conditional_last_item():
    template = (WWW / "curso.html").read_text(encoding="utf-8")

    assert (
        '"position": 4, "name": {{ related_courses.current.level | tojson }}, '
        '"item": {{ canonical_url | tojson }}}'
    ) in template
    assert (
        '"position": 3, "name": {{ course.title | tojson }}, '
        '"item": {{ canonical_url | tojson }}}'
    ) in template


def test_corporate_english_article_title_does_not_leak_source_extension():
    from vedium_core.blog_content import BLOG_POSTS

    post = BLOG_POSTS[
        "como-escrever-mensagens-curtas-e-claras-em-ingles-corporativo"
    ]
    assert not post["title"].endswith(".md")
    assert not post["h1"].endswith(".md")


def test_guest_course_pages_can_use_frappe_page_cache_without_session_leakage():
    controller = (WWW / "curso.py").read_text(encoding="utf-8")

    assert 'is_guest = frappe.session.user == "Guest"' in controller
    assert "context.no_cache = not is_guest" in controller
    assert "if is_guest:\n        frappe.local.no_cache = False" in controller
    assert 'if frappe.session.user == "Guest":\n        return False' in controller
    assert 'if frappe.session.user == "Guest":\n        return 0' in controller


def test_sitemap_omits_fake_daily_lastmod_from_static_pages():
    controller = (WWW / "sitemap.py").read_text(encoding="utf-8")
    template = (WWW / "sitemap.xml").read_text(encoding="utf-8")

    assert 'url.get("lastmod") or today' not in controller
    assert "from frappe.utils import nowdate" not in controller
    assert "if url.get(\"lastmod\")" in controller
    assert "{%- if link.lastmod %}" in template


def test_approved_lms_level_migration_changes_titles_only():
    migration = (
        ROOT
        / "vedium_core"
        / "vedium_core"
        / "scripts"
        / "migrations"
        / "oneshot"
        / "rename_english_course_levels.py"
    ).read_text(encoding="utf-8")

    assert '"Inglês Online ao Vivo A2 – Elementar"' in migration
    assert '"Inglês Online ao Vivo A2+ – Pré-Intermediário"' in migration
    assert '"Inglês Online ao Vivo B1 – Intermediário"' in migration
    assert '"Inglês Online ao Vivo B2 – Intermediário Superior"' in migration
    assert 'frappe.db.set_value(\n            "LMS Course"' in migration
    assert '"title",\n            target_title' in migration
    assert "frappe.rename_doc" not in migration
    assert "course_price" not in migration
    assert "clear_website_cache()" in migration
