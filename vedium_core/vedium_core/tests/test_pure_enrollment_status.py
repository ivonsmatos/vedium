"""Testes puros para extensões Vedium em LMS Enrollment."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
TRIAL = (CORE / "trial.py").read_text(encoding="utf-8")


def test_lms_enrollment_has_vedium_status_custom_fields():
    assert '"LMS Enrollment"' in CUSTOM_SETUP
    for fieldname in [
        "custom_vedium_status",
        "custom_vedium_status_changed_on",
        "custom_vedium_status_reason",
        "custom_trial_start",
        "custom_trial_end",
    ]:
        assert fieldname in CUSTOM_SETUP
    for option in ["Active", "Trial", "Suspended", "Cancelled", "Ended", "Expired"]:
        assert option in CUSTOM_SETUP


def test_trial_uses_custom_vedium_status_not_missing_native_status():
    assert 'STATUS_FIELD = "custom_vedium_status"' in TRIAL
    assert '"status": TRIAL_STATUS' not in TRIAL
    assert 'filters={"status": TRIAL_STATUS}' not in TRIAL
    assert 'frappe.db.set_value("LMS Enrollment", e.name, "status", EXPIRED_STATUS)' not in TRIAL
