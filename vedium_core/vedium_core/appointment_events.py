"""Ponte Frappe→Brevo do encontro pré-venda (fluxos A05/A06 do kit).

O AGENDAMENTO em si é NATIVO (Appointment Booking do Frappe + Google Calendar/
Meet — ver appointment_setup.py). Este módulo NÃO recria a página nem o e-mail
de confirmação nativo: ele só EMITE eventos no ciclo de vida do `Appointment`
para o Brevo disparar os modelos:

    meeting_booked   -> A05 (confirmação + lembretes, agendados pelo Brevo a
                        partir de params.meeting_datetime)
    meeting_attended -> A05-04 (resumo pós-encontro)
    meeting_no_show  -> A06 (reagendamento / encerramento respeitoso)

Detecção de no-show = HÍBRIDA (decisão 2026-08): a equipe marca as FALTAS
(exceção) em `custom_attendance_outcome`; um job assume "compareceu" para o
restante após uma tolerância. Assim o meeting_attended nunca depende de marcação
manual, e o meeting_no_show é sempre uma ação deliberada.

Idempotente via `custom_booked_event_on` / `custom_outcome_event_on`. Nunca fatal
(best-effort): um erro aqui não pode derrubar o agendamento. Ver doc 16/19 e
[[project_email_lifecycle_brevo]].
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, cint, format_date, get_time, get_datetime, now_datetime

from vedium_core import brevo

BOOKING_URL = "https://app.vediums.com/book_appointment"
# Tolerância (horas) após o horário para o job assumir "compareceu". A equipe
# deve marcar as faltas dentro dessa janela (idealmente logo após o encontro).
DEFAULT_GRACE_HOURS = 3

OUTCOME_ATTENDED = "Compareceu"
OUTCOME_NO_SHOW = "Faltou"

# Mapa marcação -> evento (função pura: testável sem Frappe).
_OUTCOME_EVENT = {
    OUTCOME_ATTENDED: "meeting_attended",
    OUTCOME_NO_SHOW: "meeting_no_show",
}


def outcome_to_event(outcome: str | None) -> str | None:
    """Puro: traduz a marcação de presença no nome do evento Brevo (ou None)."""
    return _OUTCOME_EVENT.get((outcome or "").strip())


def _grace_hours() -> int:
    return cint(frappe.conf.get("vedium_meeting_grace_hours")) or DEFAULT_GRACE_HOURS


def _has_field(fieldname: str) -> bool:
    try:
        return bool(frappe.get_meta("Appointment").has_field(fieldname))
    except Exception:
        return False


def _meet_link(appointment) -> str:
    """Melhor-esforço: link do Google Meet do Event vinculado (pode não estar
    sincronizado no instante do booking; o lembrete A05-03 já o encontra)."""
    if not appointment.get("calendar_event"):
        return ""
    try:
        return frappe.db.get_value("Event", appointment.calendar_event, "google_meet_link") or ""
    except Exception:
        return ""


def _course_for(email: str) -> str:
    """COURSE = idioma de interesse do lead (do CRM), pra personalizar o A05/A06."""
    if not email:
        return ""
    try:
        if frappe.db.exists("DocType", "CRM Lead"):
            val = frappe.db.get_value("CRM Lead", {"email": email}, "custom_curso_interesse")
            if val:
                return val
    except Exception:
        pass
    return ""


def _params(appointment) -> dict:
    sched = get_datetime(appointment.scheduled_time) if appointment.get("scheduled_time") else None
    course = appointment.get("custom_course_interest") or _course_for(appointment.get("customer_email"))
    params = {
        "booking_url": BOOKING_URL,
        "calendar_url": BOOKING_URL,
        "reschedule_url": BOOKING_URL,
        "preference_url": BOOKING_URL,
        "meeting_url": _meet_link(appointment) or BOOKING_URL,
        "timezone": frappe.utils.get_time_zone(),
    }
    if sched:
        params["meeting_datetime"] = str(sched)
        params["date"] = format_date(sched, "dd/MM/yyyy")
        params["time"] = get_time(sched).strftime("%H:%M")
    if course:
        params["course"] = course
    return params


def _emit(appointment, event_name: str):
    email = (appointment.get("customer_email") or "").strip()
    if not email or "@" not in email or not brevo.is_enabled():
        return False
    contact_props = {}
    course = appointment.get("custom_course_interest") or _course_for(email)
    if course:
        contact_props["COURSE"] = course
    name = (appointment.get("customer_name") or "").strip()
    if name:
        contact_props["FIRSTNAME"] = name.split(" ", 1)[0]
    try:
        brevo.emit_contact_event(
            email,
            event_name,
            event_properties=_params(appointment),
            contact_properties=contact_props or None,
        )
        return True
    except Exception:
        frappe.log_error(frappe.get_traceback(), f"Vedium.appointment.{event_name}")
        return False


# ---------------------------------------------------------------------------
# doc_events
# ---------------------------------------------------------------------------
def on_appointment_after_insert(doc, method=None):
    """Novo agendamento → garante o Meet no Event e emite meeting_booked (A05)."""
    try:
        # Garante que o Event vinculado gere um link de Google Meet (o sync do
        # Google preenche google_meet_link quando add_video_conferencing=1).
        if doc.get("calendar_event"):
            ev = frappe.get_doc("Event", doc.calendar_event)
            if ev.meta.has_field("add_video_conferencing") and not ev.get("add_video_conferencing"):
                ev.add_video_conferencing = 1
                ev.save(ignore_permissions=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.appointment.meet_setup")

    if _has_field("custom_booked_event_on") and doc.get("custom_booked_event_on"):
        return
    if _emit(doc, "meeting_booked") and _has_field("custom_booked_event_on"):
        frappe.db.set_value("Appointment", doc.name, "custom_booked_event_on", now_datetime())


def on_appointment_outcome(doc, method=None):
    """Equipe marcou presença/falta → emite o evento correspondente (uma vez)."""
    if not _has_field("custom_attendance_outcome") or not _has_field("custom_outcome_event_on"):
        return
    if doc.get("custom_outcome_event_on"):
        return
    event_name = outcome_to_event(doc.get("custom_attendance_outcome"))
    if not event_name:
        return
    if _emit(doc, event_name):
        frappe.db.set_value("Appointment", doc.name, "custom_outcome_event_on", now_datetime())


# ---------------------------------------------------------------------------
# Scheduler (híbrido): assume "compareceu" para o que não foi marcado como falta
# ---------------------------------------------------------------------------
def finalize_past_appointments() -> dict:
    """Job horário: encontros passados (horário + tolerância) que ninguém marcou
    como falta são assumidos como "compareceu" → emite meeting_attended (A05-04).
    As faltas são marcadas pela equipe (on_appointment_outcome já tratou). Idempotente."""
    if not _has_field("custom_outcome_event_on") or not _has_field("custom_attendance_outcome"):
        return {"skipped": "field_missing", "finalized": 0}

    cutoff = add_to_date(now_datetime(), hours=-_grace_hours())
    rows = frappe.get_all(
        "Appointment",
        filters={
            "scheduled_time": ["<=", cutoff],
            "custom_outcome_event_on": ["is", "not set"],
            "status": ["!=", "Unverified"],
        },
        fields=["name"],
        limit=500,
    )
    finalized = 0
    for row in rows:
        doc = frappe.get_doc("Appointment", row.name)
        # A equipe marcou falta mas o on_update não emitiu? trata aqui também.
        event_name = outcome_to_event(doc.get("custom_attendance_outcome")) or "meeting_attended"
        if event_name == "meeting_attended" and not doc.get("custom_attendance_outcome"):
            doc.db_set("custom_attendance_outcome", OUTCOME_ATTENDED, update_modified=False)
        if _emit(doc, event_name):
            doc.db_set("custom_outcome_event_on", now_datetime(), update_modified=False)
            finalized += 1
    frappe.db.commit()
    return {"candidates": len(rows), "finalized": finalized}
