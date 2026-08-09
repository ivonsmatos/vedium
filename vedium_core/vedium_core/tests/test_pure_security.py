"""Testes puros dos fixes de segurança do QA 2026-08-09 (auditoria + auditor).

Travam guards de acesso/PII/SSRF/rate-limit para não regredirem.
"""
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
API = (CORE / "api.py").read_text(encoding="utf-8")
CERT_PDF = (CORE / "certificate_pdf.py").read_text(encoding="utf-8")
WIKI = (CORE / "wiki_import.py").read_text(encoding="utf-8")
PUB_FREQ = (CORE / "public_frequency_checkout.py").read_text(encoding="utf-8")
FREQ = (CORE / "frequency_checkout.py").read_text(encoding="utf-8")
BREVO = (CORE / "brevo.py").read_text(encoding="utf-8")


def _block(src, start, end):
    return src.split(start, 1)[1].split(end, 1)[0]


def test_issue_certificate_checks_ownership():
    block = _block(API, "def issue_certificate(", "def verify_certificate(")
    assert "enrollment.member != frappe.session.user" in block
    assert "frappe.PermissionError" in block


def test_leaderboard_does_not_leak_email():
    block = _block(API, "def get_leaderboard(", "def get_forum_topics(")
    assert "u.full_name AS student" in block
    assert "SELECT member," not in block  # não seleciona o e-mail cru


def test_verify_certificate_public_hides_email():
    block = _block(API, "def verify_certificate(", "def get_payment_history(")
    assert '"student":' in block and "full_name" in block
    # não retorna o dict cru com member (e-mail)
    assert "return cert[0]" not in block


def test_audio_exercises_ratelimited_and_url_validated():
    assert "def _validate_audio_url(" in API
    for fn in ("submit_listening_exercise", "submit_speaking_exercise"):
        block = _block(API, f"def {fn}(", "return")
        assert "rate_limit_by_ip(" in block
        assert "_validate_audio_url(" in block


def test_certificate_pdf_no_name_fallback():
    block = _block(CERT_PDF, "def _get_certificate_data(", "def generate_pdf(")
    # buscava por PK (code posicional) como fallback — removido
    assert '"LMS Certificate",\n                code,' not in block
    assert "verification_code" in block


def test_wiki_import_guarded_and_pathsafe():
    imp = _block(WIKI, "def import_manifest(", "manifest = _load_manifest")
    assert "frappe.get_roles()" in imp and "frappe.PermissionError" in imp
    load = _block(WIKI, "def _load_manifest(", "def ")
    assert "startswith(str(base))" in load  # trava traversal/absoluto


def test_frequency_checkouts_ratelimited():
    assert 'rate_limit_by_ip("checkout"' in PUB_FREQ
    assert 'rate_limit_by_ip("checkout"' in FREQ


def test_brevo_seed_catalog_exists_and_guarded():
    assert "def seed_event_catalog(" in BREVO
    assert "LIFECYCLE_EVENTS" in BREVO
    block = _block(BREVO, "def seed_event_catalog(", "def _event_key(")
    assert "frappe.get_roles()" in block
    assert "enrollment_created" not in block.split("LIFECYCLE_EVENTS", 1)[0]
