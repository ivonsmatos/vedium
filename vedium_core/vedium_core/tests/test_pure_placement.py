"""Testes puros da captura do teste de nível -> LEVEL (2026-08-10)."""
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
FUNNEL = (CORE / "public_funnel.py").read_text(encoding="utf-8")
BREVO = (CORE / "brevo.py").read_text(encoding="utf-8")
SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
TEST_EN = (CORE / "www" / "teste-de-nivel-ingles.html").read_text(encoding="utf-8")


def test_placement_endpoint_public_ratelimited_and_stores_level():
    assert "def save_placement_result(" in FUNNEL
    block = FUNNEL.split("def save_placement_result(", 1)[1]
    assert "allow_guest=True" in FUNNEL
    assert 'rate_limit_by_ip("placement"' in block
    assert "EMAIL_RE.match(email)" in block
    assert "custom_nivel" in block
    assert "resolve_lead_source" in block  # origem válida (mesmo fix do funil)


def test_level_synced_to_brevo():
    assert '"LEVEL": snapshot.get("level")' in BREVO
    assert 'getattr(doc, "custom_nivel", None)' in BREVO


def test_custom_nivel_field_registered():
    assert '"custom_nivel"' in SETUP


def test_test_page_captures_email_and_level():
    assert "save_placement_result" in TEST_EN
    assert "vd-lvl-send" in TEST_EN and "result-level" in TEST_EN
    assert "X-Frappe-CSRF-Token" in TEST_EN
