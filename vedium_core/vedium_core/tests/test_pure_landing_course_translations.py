from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def test_english_landing_grid_uses_nested_english_translation():
    source = (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")

    assert 'COURSE_TRANSLATIONS.get(course.name, {}).get("en")' in source
    assert 'COURSE_TRANSLATIONS[course.name]["title"]' not in source
    assert 'COURSE_TRANSLATIONS[course.name]["short_introduction"]' not in source
