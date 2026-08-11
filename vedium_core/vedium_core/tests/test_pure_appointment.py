"""Testes puros do encontro pré-venda (fluxos A05/A06 do kit Brevo, 2026-08).

O agendamento é NATIVO (Appointment Booking do Frappe); aqui validamos só a ponte
de eventos pro Brevo (meeting_booked/attended/no_show), a detecção HÍBRIDA de
no-show e que o setup liga o nativo em vez de criar página custom.
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"

EVENTS = (CORE / "appointment_events.py").read_text(encoding="utf-8")
SETUP = (CORE / "appointment_setup.py").read_text(encoding="utf-8")
BREVO = (CORE / "brevo.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")
INSTALL = (CORE / "install.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")


def test_modules_are_valid_python():
    ast.parse(EVENTS)
    ast.parse(SETUP)


def test_uses_native_booking_not_a_custom_page():
    """Regra de ouro: usa o Appointment Booking NATIVO (config), não uma página
    custom que duplicaria a função."""
    assert "Appointment Booking Settings" in SETUP
    assert "enable_scheduling" in SETUP
    assert "/book_appointment" in EVENTS  # aponta pro fluxo nativo


def test_three_lifecycle_events_are_emitted_and_seeded():
    for ev in ("meeting_booked", "meeting_attended", "meeting_no_show"):
        assert ev in EVENTS
        assert ev in BREVO  # entra no LIFECYCLE_EVENTS (seed do dropdown)


def test_hybrid_no_show_detection():
    """Equipe marca FALTA (exceção); o job assume 'compareceu' para o resto."""
    # mapa marcação -> evento (função pura)
    assert 'OUTCOME_ATTENDED = "Compareceu"' in EVENTS
    assert 'OUTCOME_NO_SHOW = "Faltou"' in EVENTS
    assert 'OUTCOME_ATTENDED: "meeting_attended"' in EVENTS
    assert 'OUTCOME_NO_SHOW: "meeting_no_show"' in EVENTS
    # o job de fecho assume attended quando ninguém marcou falta
    assert "def finalize_past_appointments" in EVENTS
    assert 'or "meeting_attended"' in EVENTS
    assert "custom_attendance_outcome" in CUSTOM_SETUP


def test_events_are_idempotent_by_markers():
    for marker in ("custom_booked_event_on", "custom_outcome_event_on"):
        assert marker in EVENTS
        assert marker in CUSTOM_SETUP


def test_meet_link_is_best_effort_from_event():
    """meeting_url vem do google_meet_link do Event vinculado (best-effort)."""
    assert "google_meet_link" in EVENTS
    assert "add_video_conferencing" in EVENTS


def test_hooks_and_scheduler_registered():
    assert "vedium_core.appointment_events.on_appointment_after_insert" in HOOKS
    assert "vedium_core.appointment_events.on_appointment_outcome" in HOOKS
    assert "vedium_core.appointment_events.finalize_past_appointments" in HOOKS
    assert "vedium_core.appointment_setup" in INSTALL
    assert "ensure_appointment_booking" in INSTALL


def test_setup_is_idempotent_and_non_destructive():
    """Só liga se estiver desligado; não sobrescreve a agenda já ajustada."""
    assert 'return {"skipped": "already_enabled"}' in SETUP
    assert 'not settings.get("availability_of_slots")' in SETUP


def test_setup_needs_agent_and_uses_flags():
    """Não chuta o dono da agenda (pula sem VEDIUM_APPOINTMENT_AGENT) e usa
    flags.ignore_permissions (o save() do nativo não aceita o kwarg)."""
    assert 'return {"skipped": "needs_agent"}' in SETUP
    assert "vedium_appointment_agent" in SETUP
    assert "settings.flags.ignore_permissions = True" in SETUP
    assert "ignore_permissions=True)" not in SETUP  # não usa o kwarg quebrado
