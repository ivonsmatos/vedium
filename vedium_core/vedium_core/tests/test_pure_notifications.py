from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_teacher_application_notifies_ops_immediately():
    careers = _read("careers.py")
    notifications = _read("notifications.py")

    assert "notify_teacher_application(doc)" in careers
    assert "frappe.sendmail" in notifications
    assert "delayed=True" in notifications
    assert "Nova candidatura de professor" in notifications
    assert "contato@vediums.com" in notifications


def test_scheduling_hooks_notify_teacher():
    hooks = _read("hooks.py")
    notifications = _read("notifications.py")

    assert '"LMS Certificate Request"' in hooks
    assert "vedium_core.notifications.notify_lms_certificate_request" in hooks
    assert '"Lesson Slot"' in hooks
    assert "vedium_core.notifications.notify_lesson_slot_booked" in hooks
    assert "Novo agendamento" in notifications
    assert "_user_email(evaluator)" in notifications
