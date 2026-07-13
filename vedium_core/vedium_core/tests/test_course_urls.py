from vedium_core.course_urls import (
    COURSE_PUBLIC_SLUGS,
    get_course_url,
    get_internal_course_name,
    legacy_course_redirects,
)


def test_all_published_course_families_have_stable_public_slugs():
    assert len(COURSE_PUBLIC_SLUGS) == 20
    assert len(set(COURSE_PUBLIC_SLUGS.values())) == 20

    public = set(COURSE_PUBLIC_SLUGS.values())
    assert any(slug.startswith("ingles-") for slug in public)
    assert any(slug.startswith("espanhol-") for slug in public)
    assert any(slug.startswith("hebraico-") for slug in public)
    assert any(slug.startswith("ioruba-") for slug in public)
    assert any(slug.startswith("portugues-para-estrangeiros-") for slug in public)


def test_clean_slug_resolves_to_internal_lms_identifier():
    assert get_internal_course_name("ingles-basico-a1") == "ingl-s-beginner"
    assert get_internal_course_name("ioruba-basico") == "iorub-b-sico"
    assert get_internal_course_name("hebraico-moderno-a1") == "hebraico-moderno-a1"


def test_course_urls_and_legacy_redirects_are_language_aware():
    assert get_course_url("ingl-s-beginner") == "/curso/ingles-basico-a1"
    assert get_course_url("ingl-s-beginner", "en") == "/en/curso/ingles-basico-a1"

    redirects = legacy_course_redirects()
    assert {
        "source": "/curso/ingl-s-beginner",
        "target": "/curso/ingles-basico-a1",
    } in redirects
    assert {
        "source": "/es/curso/iorub-b-sico",
        "target": "/es/curso/ioruba-basico",
    } in redirects
