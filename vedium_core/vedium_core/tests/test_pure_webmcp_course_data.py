"""Testes puros do course data service do piloto WebMCP (Fase C.2, secao
24/25 da missao) -- sem dependencia de Frappe/DB, so os modulos Python."""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

# Garante que vedium_core (package) seja localizável a partir da pasta pai
# seja rodando por `pytest` na raiz do repo ou a partir de vedium_core/.
APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

# v2_home_data.py faz `import frappe` no nivel do modulo -- mock antes de
# qualquer import de vedium_core, seguindo o padrao de
# test_pure_catalog_pricing.py / test_pure_catalog_sync.py.
if "frappe" not in sys.modules:
    _frappe_mock = MagicMock()
    _frappe_mock.as_json = lambda x: json.dumps(x)
    _frappe_mock.logger = lambda name="": MagicMock()
    sys.modules["frappe"] = _frappe_mock
    sys.modules["frappe.utils"] = MagicMock()

from vedium_core.webmcp_course_data import (
    LANGUAGE_ENUM_TO_KEY,
    _CATALOG_TRACK_COURSE_IDS,
    get_webmcp_course_data,
)
from vedium_core.v2_home_data import PATHFINDER_MATRIX
from vedium_core.catalog_registry import CATALOG

REAL_PATHFINDER_GOALS = [
    "Trabalho e carreira",
    "Comunicação cotidiana",
    "Viagens",
    "Estudos e cultura",
    "Viver e trabalhar no Brasil",
]

SEQUENTIAL_LANGUAGES = {"english", "portuguese_for_foreigners", "yoruba", "spanish"}


def test_all_five_languages_present_with_required_fields():
    data = get_webmcp_course_data()
    assert set(data["courses"].keys()) == set(LANGUAGE_ENUM_TO_KEY.keys())
    required = [
        "language",
        "course_name",
        "summary",
        "level_summary",
        "delivery_mode",
        "teacher_profile",
        "progression",
        "url",
        "cta_label",
        "levels",
        "levels_are_sequential",
        "next_step",
    ]
    for enum, course in data["courses"].items():
        for field in required:
            assert field in course, f"campo {field} ausente em {enum}"
        assert course["language"] == enum


def test_urls_are_real_public_paths_never_preview_or_local():
    data = get_webmcp_course_data()
    for enum, course in data["courses"].items():
        url = course["url"]
        assert url.startswith("/"), f"URL {url} ({enum}) nao e path absoluto do site"
        assert "_home_v2" not in url
        assert "localhost" not in url and "127.0.0.1" not in url
        assert "C:\\" not in url and "vedium-references" not in url
        for level in course["levels"]:
            assert level["url"].startswith("/"), f"level URL {level['url']} ({enum}) invalida"
        next_step_url = course["next_step"]["url"]
        assert next_step_url.startswith("/"), f"next_step URL {next_step_url} ({enum}) invalida"


def test_levels_non_empty_and_sequential_flag_matches_known_taxonomy():
    data = get_webmcp_course_data()
    for enum, course in data["courses"].items():
        assert len(course["levels"]) > 0, f"{enum} sem niveis"
        expected_sequential = enum in SEQUENTIAL_LANGUAGES
        assert course["levels_are_sequential"] == expected_sequential


def test_hebrew_levels_are_five_distinct_tracks_not_cefr():
    data = get_webmcp_course_data()
    hebrew = data["courses"]["hebrew"]
    assert hebrew["levels_are_sequential"] is False
    labels = [level["label"] for level in hebrew["levels"]]
    assert len(labels) == 5
    assert len(set(labels)) == 5


def test_english_levels_come_from_course_urls_cefr_source():
    data = get_webmcp_course_data()
    english = data["courses"]["english"]
    labels = [level["label"] for level in english["levels"]]
    assert labels == ["A1", "A2", "A2+", "B1", "B2", "C1"]


def test_next_step_kind_matches_real_level_test_availability():
    data = get_webmcp_course_data()
    # Apenas Ingles e PLE tem teste de nivel self-service real hoje --
    # ver course_urls.get_course_level_destination().
    assert data["courses"]["english"]["next_step"]["kind"] == "level_test"
    assert data["courses"]["portuguese_for_foreigners"]["next_step"]["kind"] == "level_test"
    for lang in ("yoruba", "spanish", "hebrew"):
        assert data["courses"][lang]["next_step"]["kind"] == "contact"


def test_pathfinder_matrix_is_the_real_matrix_not_a_copy():
    data = get_webmcp_course_data()
    assert data["pathfinder_matrix_by_display_name"] is PATHFINDER_MATRIX


def test_pathfinder_goals_match_real_taxonomy_used_by_the_ui_form():
    """REAL_PATHFINDER_GOALS acima e o argumento literal passado pro macro
    v2_pathfinder_section() em templates/includes/v2/home_body.html --
    checagem independente pra pegar drift entre UI e o piloto WebMCP."""
    data = get_webmcp_course_data()
    assert data["pathfinder_goals"] == REAL_PATHFINDER_GOALS


def test_language_enum_to_display_name_matches_pathfinder_matrix_keys():
    data = get_webmcp_course_data()
    for enum, display_name in data["language_enum_to_display_name"].items():
        assert display_name in PATHFINDER_MATRIX, f"{display_name} ({enum}) nao existe em PATHFINDER_MATRIX"


def test_catalog_track_course_ids_exist_in_catalog_registry():
    for course_ids in _CATALOG_TRACK_COURSE_IDS.values():
        for course_id in course_ids:
            assert course_id in CATALOG, f"{course_id} nao existe em catalog_registry.CATALOG"


def test_no_price_or_commercial_fields_leak_into_course_data():
    """Secao 5/8 da missao: 'Nao inventar preco' -- garante que nenhum
    campo de preco/produto Stripe do catalog_registry vaza pro data
    service (usamos so o titulo, nunca base_monthly/product_id/etc.)."""
    data = get_webmcp_course_data()
    serialized = json.dumps(data)
    for forbidden in ("base_monthly", "base_annual", "product_id", "custom_annual_prices", "legacy_prices"):
        assert forbidden not in serialized


def test_data_is_plain_json_serializable():
    data = get_webmcp_course_data()
    json.dumps(data)  # nao deve lancar
