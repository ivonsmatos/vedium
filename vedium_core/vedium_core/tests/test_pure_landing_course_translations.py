from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_translated_landing_grid_uses_page_language_translation():
    source = (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")

    assert "translation = COURSE_TRANSLATIONS.get(course.name, {}).get(lang)" in source
    assert "course.url = get_course_url(course.name, lang)" in source
    assert "course.level_badge = COURSE_LEVEL_BADGE_I18N.get(lang, {}).get(" in source
    assert 'COURSE_TRANSLATIONS[course.name]["title"]' not in source
    assert 'COURSE_TRANSLATIONS[course.name]["short_introduction"]' not in source
