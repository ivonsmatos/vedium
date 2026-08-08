"""Testes puros do onboarding de professor + turma (P2, 2026-08-08).

Mesmo padrão dos outros test_pure_*: validam o texto-fonte sem Frappe/bench.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

ONBOARDING = (CORE / "teacher_onboarding.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_module_is_valid_python():
    ast.parse(ONBOARDING)


def test_batch_and_professor_handlers_exist():
    assert "def on_batch_created(doc, method=None)" in ONBOARDING
    assert "def on_user_became_professor(doc, method=None)" in ONBOARDING
    assert "def notify_batch_professor(batch_name" in ONBOARDING


def test_handlers_are_wired_in_hooks():
    """Sem o wiring, os handlers nunca rodam."""
    assert '"vedium_core.teacher_onboarding.on_batch_created"' in HOOKS
    assert '"vedium_core.teacher_onboarding.on_user_became_professor"' in HOOKS
    # o handler antigo de professor→Raven continua registrado (lista, não substituição)
    assert '"vedium_core.communication.sync_new_professor"' in HOOKS
    # after_insert de LMS Batch
    batch_block = HOOKS.split('"LMS Batch": {', 1)[1].split("}", 1)[0]
    assert '"after_insert": "vedium_core.teacher_onboarding.on_batch_created"' in batch_block


def test_professor_welcome_is_idempotent_by_role_transition():
    """Boas-vindas do professor dispara UMA vez: detecção por transição de role
    (get_doc_before_save), sem depender de campo/flag persistido."""
    block = ONBOARDING.split("def on_user_became_professor", 1)[1]
    assert "get_doc_before_save" in block
    assert "_user_has_role(before, PROFESSOR_ROLE)" in block
    assert 'PROFESSOR_ROLE = "Vedium Professor"' in ONBOARDING


def test_turma_is_born_complete_and_never_breaks_creation():
    """Turma nova ganha canal Raven + notifica professor; nada disso pode
    derrubar a criação da turma (tudo em try/except com log)."""
    assert "ensure_batch_channel(doc.name)" in ONBOARDING
    assert "notify_batch_professor(doc.name)" in ONBOARDING
    assert ONBOARDING.count("frappe.log_error") >= 3


def test_internal_notifications_use_sendmail_not_brevo():
    """Onboarding de professor/turma é comunicação INTERNA — não é o kit Brevo
    (aluno/lead/B2B). Deve usar frappe.sendmail e não emitir eventos Brevo."""
    assert "frappe.sendmail" in ONBOARDING
    assert "track_event" not in ONBOARDING
    assert "emit_contact_event" not in ONBOARDING
