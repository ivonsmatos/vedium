"""Testes puros do HomeCourseCollection (Fase C.1.1, Parte B secao 11 da
missao) -- sem dependencia de Frappe/DB, so o modulo Python + o template
que o consome."""

from pathlib import Path

from vedium_core.home_course_collection import (
    HOME_COURSE_COLLECTION,
    get_course_index_entries,
    get_home_course_collection,
)

ROOT = Path(__file__).resolve().parents[3]
HOME_BODY = ROOT / "vedium_core" / "vedium_core" / "templates" / "includes" / "v2" / "home_body.html"

REQUIRED_FIELDS = [
    "slug",
    "language_key",
    "display_name",
    "eyebrow",
    "level_summary",
    "headline",
    "description",
    "url",
    "cta_label",
    "media_key",
    "media_alt",
    "order",
    "is_active",
]


def test_exactly_five_active_languages():
    active = get_home_course_collection()
    assert len(active) == 5


def test_required_fields_present_and_non_empty():
    for course in HOME_COURSE_COLLECTION:
        for field in REQUIRED_FIELDS:
            assert field in course, f"campo {field} ausente em {course.get('slug')}"
        for text_field in ("display_name", "headline", "description", "url", "cta_label", "media_key"):
            assert str(course[text_field]).strip() != "", f"{text_field} vazio em {course.get('slug')}"


def test_no_duplicate_language_key_or_slug():
    keys = [c["language_key"] for c in HOME_COURSE_COLLECTION]
    slugs = [c["slug"] for c in HOME_COURSE_COLLECTION]
    assert len(keys) == len(set(keys)), "language_key duplicado"
    assert len(slugs) == len(set(slugs)), "slug duplicado"


def test_urls_are_real_site_paths_not_placeholders():
    for course in HOME_COURSE_COLLECTION:
        url = course["url"]
        assert url.startswith("/"), f"URL {url} nao e um path absoluto do site"
        assert "example" not in url and "placeholder" not in url and "lorem" not in url.lower()


def test_order_is_unique_and_sequential_from_one():
    orders = sorted(c["order"] for c in HOME_COURSE_COLLECTION if c["is_active"])
    assert orders == list(range(1, len(orders) + 1))


def test_get_home_course_collection_sorted_by_order():
    active = get_home_course_collection()
    assert [c["order"] for c in active] == sorted(c["order"] for c in active)
    assert active[0]["slug"] == "ingles"


def test_get_home_course_collection_resolves_media_src():
    """Hotfix de producao: media_src resolve pro path definitivo
    (public/v2/media/home/, versionado no Git) -- nao mais
    v2-preview-media/ (era local/gitignorado, nunca chegava a producao,
    causa raiz do 404 encontrado no smoke test pos-deploy)."""
    for course in get_home_course_collection():
        assert course["media_src"] == "/assets/vedium_core/v2/media/home/" + course["media_key"]


def test_get_course_index_entries_matches_collection_order():
    entries = get_course_index_entries()
    active = get_home_course_collection()
    assert len(entries) == len(active)
    for entry, course in zip(entries, active):
        assert entry["name"] == course["display_name"]
        assert entry["href"] == course["url"]


def test_home_media_directory_has_all_referenced_files_committed():
    """Hotfix de producao: garante que os arquivos de media referenciados
    em media_key REALMENTE existem em public/v2/media/home/ E que essa
    pasta NAO esta no .git/info/exclude nem no .gitignore -- a causa raiz
    do 404 em producao foi um path referenciado no codigo apontando pra
    uma pasta que nunca era versionada. Este teste falha se isso se repetir."""
    media_dir = ROOT / "vedium_core" / "vedium_core" / "public" / "v2" / "media" / "home"
    assert media_dir.exists(), f"pasta de midia de producao ausente: {media_dir}"
    for course in HOME_COURSE_COLLECTION:
        asset_path = media_dir / course["media_key"]
        assert asset_path.exists(), f"asset ausente em disco: {asset_path}"
        assert asset_path.stat().st_size > 0, f"asset vazio: {asset_path}"

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "public/v2/media/home" not in gitignore, (
        "public/v2/media/home nao pode estar no .gitignore -- e a pasta de producao"
    )


def test_home_body_template_consumes_collection_not_hardcoded_blocks():
    src = HOME_BODY.read_text(encoding="utf-8")
    assert "for course in home_courses" in src
    assert "course_index_entries" in src
    # Fase C.1.1: a secao Cursos nao deve mais ter os 5 blocos hardcoded
    # de v2_course_feature com nome literal de idioma nos argumentos.
    cursos_section = src.split("================= 3. CURSOS")[1].split("================= 4.")[0]
    assert cursos_section.count('v2e.v2_course_feature(') == 1
    assert '"Iorubá"' not in cursos_section
