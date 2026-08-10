"""Testes puros da UI do gerador de aulas ao vivo (P2, 2026-08-10)."""
from pathlib import Path

CORE = Path(__file__).resolve().parents[1]
SCHED = (CORE / "live_class_scheduler.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")
JS = (CORE / "public" / "js" / "lms_batch.js").read_text(encoding="utf-8")


def test_whitelisted_generator_is_staff_only():
    assert "def generate_live_classes_for_batch(" in SCHED
    block = SCHED.split("def generate_live_classes_for_batch(", 1)[1].split("def _find", 1)[0]
    assert "@frappe.whitelist()" in SCHED
    assert "frappe.get_roles()" in block and "frappe.PermissionError" in block
    # aceita weekdays como lista/JSON/CSV e default host = 1o instrutor
    assert "json.loads(weekdays)" in block
    assert 'rows[0].instructor' in block


def test_button_wired_in_doctype_js():
    assert '"LMS Batch": "public/js/lms_batch.js"' in HOOKS
    assert "generate_live_classes_for_batch" in JS
    assert 'frm.add_custom_button("Gerar aulas ao vivo"' in JS
    assert "MultiCheck" in JS
