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
    assert get_course_navigation("espanhol-basico") is None


def test_ple_course_navigation_follows_the_canonical_basico_to_avancado_trail():
    """PLE (Português para Estrangeiros) got its own linear trail alongside the
    English one — previously get_course_navigation() only knew the English
    track, so PLE pages rendered no "related courses" block at all (see PLE
    cluster SEO mission, item 0.1). It must be language-aware: the old
    category-based get_related_courses() leaked pt-BR links onto the /en/
    course pages, which is the bug this trail replaces.
    """
    navigation = get_course_navigation("portugues-para-estrangeiros-intermediario")

    assert navigation["previous"] == {
        "label": "PLE — Básico",
        "url": "/curso/portugues-para-estrangeiros-basico",
    }
    assert navigation["next"] == {
        "label": "PLE — Avançado",
        "url": "/curso/portugues-para-estrangeiros-avancado",
    }
    assert navigation["pillar"]["url"] == "/portugues-para-estrangeiros"
    assert navigation["current"]["level"] == "Intermediário"

    en_navigation = get_course_navigation("portugues-para-estrangeiros-basico", "en")
    assert en_navigation["current"]["url"] == "/en/curso/portugues-para-estrangeiros-basico"
    assert en_navigation["next"] == {
        "label": "PLE — Intermediate",
        "url": "/en/curso/portugues-para-estrangeiros-intermediario",
    }
    assert en_navigation["previous"] is None
    assert en_navigation["pillar"]["url"] == "/en/learn-portuguese-brazil"
    assert en_navigation["pillar"]["breadcrumb_label"] == "Portuguese for Foreigners"
    assert en_navigation["current"]["level"] == "Basic"

    # Idioma sem chrome próprio (ru) cai pro pt-BR em vez de quebrar.
    ru_navigation = get_course_navigation("portugues-para-estrangeiros-avancado", "ru")
    assert ru_navigation["current"]["level"] == "Avançado"
    assert ru_navigation["pillar"]["url"] == "/portugues-para-estrangeiros"


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
    assert '"offers": {{ course_schema_offer | tojson }}' in template
    assert 'width="1200" height="675"' in template
    assert "{%- set vd_level_test_url =" not in template
    assert "level_test_is_contact" in template
    assert "vd_level_test_url_override = level_test_url" in template
    assert "vd_level_test_contact_override = level_test_is_contact" in template

    controller = (WWW / "curso.py").read_text(encoding="utf-8")
    assert "PUBLIC_ENROLLMENT_COUNT_THRESHOLD = 10" in controller
    assert "context.public_enrollment_count" in controller
    assert "context.level_test_url, context.level_test_is_contact" in controller
    assert '"price": str(context.course.course_price)' in controller
    assert '"priceCurrency": context.course.currency' in controller
    assert "frappe.db.set_value" not in controller

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


def test_ple_course_pages_translate_related_courses_curriculum_and_x_default():
    """PLE cluster SEO mission (2026-08-23), items 0.1, 0.3 and 1.2:
    - related_courses now needs the requested language (0.1: EN course pages
      used to link to pt-BR titles/URLs).
    - chapters_list titles come straight from the DB in pt-BR; PLE has a
      dedicated translation table so /en/curso/... doesn't show a Portuguese
      curriculum on the page selling "for complete beginners" (0.3).
    - PLE's audience doesn't speak Portuguese by definition, so x-default on
      the 3 PLE course pages must resolve to English, not pt-BR (1.2) —
      other clusters (e.g. English) must keep the pt-BR default untouched.
    """
    controller = (WWW / "curso.py").read_text(encoding="utf-8")
    template = (WWW / "curso.html").read_text(encoding="utf-8")

    assert (
        "from vedium_core.course_translations import COURSE_TRANSLATIONS, "
        "PLE_CURRICULUM_TRANSLATIONS"
    ) in controller
    assert "get_course_x_default_lang" in controller
    assert "context.related_courses = get_related_courses(course_name, req_lang)" in controller
    assert "context.x_default_lang = get_course_x_default_lang(course_name)" in controller
    assert "_apply_curriculum_translation(context.course, course_name, req_lang)" in controller
    assert "def _apply_curriculum_translation(course, course_name, req_lang):" in controller

    assert (
        'href="{{ alt_langs.get(x_default_lang, alt_langs.get(\'pt-br\', canonical_url)) }}"'
        in template
    )

    from vedium_core.course_urls import get_course_x_default_lang

    assert get_course_x_default_lang("portugues-para-estrangeiros-basico") == "en"
    assert get_course_x_default_lang("ingl-s-beginner") is None


def test_curso_html_trail_labels_are_translated_for_every_supported_language():
    """The trail heading/labels used to be pt-BR-only text hardcoded for the
    English track ("Continue sua trilha de inglês") while en/es/fr/de were
    missing previous_level/next_level/all_levels entirely (rendered blank).
    Both bugs would have leaked onto PLE pages once they got a trail too.
    """
    template = (WWW / "curso.html").read_text(encoding="utf-8")

    assert "Continue sua trilha de inglês" not in template
    assert "Ver todos os níveis de inglês" not in template
    for lang_line in (
        '"related": "Continue your track", "previous_level": "Previous level", '
        '"next_level": "Next level", "all_levels": "See all levels"',
        '"related": "Continúa tu trayecto", "previous_level": "Nivel anterior", '
        '"next_level": "Siguiente nivel", "all_levels": "Ver todos los niveles"',
        '"related": "Continuez votre parcours", "previous_level": "Niveau précédent", '
        '"next_level": "Niveau suivant", "all_levels": "Voir tous les niveaux"',
        '"related": "Setzen Sie Ihren Kursweg fort", "previous_level": "Vorheriges Niveau", '
        '"next_level": "Nächstes Niveau", "all_levels": "Alle Niveaus ansehen"',
    ):
        assert lang_line in template


def test_course_instructor_card_never_leaks_placeholder_system_accounts():
    """1.3 (E-E-A-T): curso.py used to build instructors_list straight from
    the Course Instructor child table with no filtering. Several course
    creation scripts (e.g. create_ple_courses.py:_default_instructor) fill
    that field with a system account ("Administrator" or the shared support
    inbox) whenever no real teacher is assigned yet, on the assumption the
    front-end never rendered it -- which was true until this card shipped.
    Rendering it unfiltered would show "Administrator" as the teacher on
    every course still waiting for a real one.
    """
    courses_module = (
        ROOT / "vedium_core" / "vedium_core" / "courses.py"
    ).read_text(encoding="utf-8")
    controller = (WWW / "curso.py").read_text(encoding="utf-8")
    template = (WWW / "curso.html").read_text(encoding="utf-8")

    assert 'PLACEHOLDER_INSTRUCTOR_ACCOUNTS = {"Administrator"' in courses_module
    assert "def get_public_instructors(course_name):" in courses_module
    assert "if row.instructor in PLACEHOLDER_INSTRUCTOR_ACCOUNTS:\n            continue" in courses_module

    assert "get_public_instructors" in controller
    assert "instructors_list = get_public_instructors(course.name)" in controller

    assert "{% if course.instructors_list %}" in template
    assert "{{ ui.instructor_label }}" in template
    # Sem foto (caso do professor de PLE hoje -- ver relatório da missão):
    # cai num avatar com a inicial, nunca numa tag <img> com src vazio.
    assert "course-details__instructor-avatar-fallback" in template
    assert '"instructor": [{% for instructor in course.instructors_list %}' in template


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
