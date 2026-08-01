"""Pure/static tests for the optional Frappe -> Brevo integration."""

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"
BREVO = (CORE / "brevo.py").read_text(encoding="utf-8")
COMMUNICATION = (CORE / "communication.py").read_text(encoding="utf-8")
TRIAL = (CORE / "trial.py").read_text(encoding="utf-8")


def test_brevo_module_is_valid_python_and_has_no_hardcoded_secret():
    ast.parse(BREVO)
    assert "xkeysib-..." in BREVO  # documentation placeholder only
    assert "BREVO_API_KEY" in BREVO
    assert '"api-key": _api_key()' in BREVO
    assert "COLE_AQUI" not in BREVO


def test_brevo_uses_contact_upsert_and_custom_events():
    assert '"POST", "/contacts"' in BREVO
    assert '"updateEnabled": True' in BREVO
    assert '"POST", "/events"' in BREVO
    assert '"identifiers": {"email_id": email}' in BREVO
    for event_name in (
        "enrollment_created",
        "trial_started",
        "payment_failed",
        "payment_recovered",
        "enrollment_suspended",
        "enrollment_cancelled",
    ):
        assert event_name in BREVO


def test_enrollment_hook_queues_brevo_even_without_raven():
    function = COMMUNICATION.split("def sync_enrollment", 1)[1].split(
        "def sync_new_professor", 1
    )[0]
    assert "queue_brevo_sync(doc, method)" in function
    assert function.index("queue_brevo_sync(doc, method)") < function.index(
        "if not raven_available()"
    )


def test_trial_expiry_runs_document_hooks():
    expire_block = TRIAL.split("def expire_trials", 1)[1].split(
        "def _send_trial_welcome", 1
    )[0]
    assert 'frappe.get_doc("LMS Enrollment", e.name)' in expire_block
    assert "enrollment.save(ignore_permissions=True)" in expire_block
    assert "frappe.db.set_value" not in expire_block


def test_brevo_outbound_events_are_idempotent_and_backgrounded():
    assert 'integration_request_service": "Brevo API"' in BREVO
    assert "hashlib.sha256" in BREVO
    assert 'queue="short"' in BREVO
    assert "enqueue_after_commit=True" in BREVO
