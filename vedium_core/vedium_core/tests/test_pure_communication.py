"""Testes puros da camada Vedium ↔ Raven."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

COMMUNICATION = (CORE / "communication.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_communication_layer_is_optional_until_raven_is_installed():
    assert "def raven_available" in COMMUNICATION
    assert "Raven User" in COMMUNICATION
    assert "return" in COMMUNICATION.split("def sync_enrollment")[1].split("def remove_enrollment_membership")[0]


def test_enrollment_status_is_source_of_truth_for_channel_membership():
    assert 'STATUS_FIELD = "custom_vedium_status"' in COMMUNICATION
    assert 'ACTIVE_STATUSES = {"Active", "Trial"}' in COMMUNICATION
    for status in ["Cancelled", "Ended", "Expired", "Suspended"]:
        assert status in COMMUNICATION
    assert "_remove_channel_member" in COMMUNICATION


def test_raven_channels_are_linked_to_lms_documents():
    assert '"linked_doctype": linked_doctype' in COMMUNICATION
    assert '"linked_document": linked_document' in COMMUNICATION
    assert "ensure_course_channel" in COMMUNICATION
    assert "ensure_batch_channel" in COMMUNICATION


def test_lms_enrollment_hooks_sync_communication():
    enrollment_block = HOOKS.split('"LMS Enrollment": {')[1].split("},", 1)[0]
    assert "vedium_core.communication.sync_enrollment" in enrollment_block
    assert "vedium_core.communication.remove_enrollment_membership" in enrollment_block
