"""Liga o Appointment Booking NATIVO do Frappe (encontro pré-venda dos fluxos
A05/A06). É config, não página custom — a regra de ouro é usar o nativo (ver
doc 01). Idempotente e defensivo: só semeia defaults quando ainda está desligado,
nunca sobrescreve uma agenda que a coordenação já ajustou no Desk.

⚠️ Passo manual que fica com o dono: vincular o AGENTE (o usuário cuja conta
Google Calendar hospeda o encontro e gera o Meet) em Appointment Booking
Settings → agent_list. Sem isso o booking funciona, mas sem Meet automático.
"""

from __future__ import annotations

import frappe

# Agenda default: seg–sex, 09:00–18:00 (a coordenação ajusta no Desk depois).
_DEFAULT_SLOTS = [
    ("Monday", "09:00:00", "18:00:00"),
    ("Tuesday", "09:00:00", "18:00:00"),
    ("Wednesday", "09:00:00", "18:00:00"),
    ("Thursday", "09:00:00", "18:00:00"),
    ("Friday", "09:00:00", "18:00:00"),
]


def ensure_appointment_booking() -> dict:
    """Ativa o agendamento nativo com defaults sensatos. Só age se ainda estiver
    desligado (não pisa em ajustes manuais). Retorna o que mudou."""
    if not frappe.db.exists("DocType", "Appointment Booking Settings"):
        return {"skipped": "no_doctype"}

    settings = frappe.get_single("Appointment Booking Settings")
    if settings.get("enable_scheduling"):
        return {"skipped": "already_enabled"}

    settings.enable_scheduling = 1
    settings.appointment_duration = settings.get("appointment_duration") or 30
    settings.advance_booking_days = settings.get("advance_booking_days") or 30
    settings.number_of_agents = settings.get("number_of_agents") or 1
    if settings.meta.has_field("email_reminders"):
        settings.email_reminders = 1
    if settings.meta.has_field("success_redirect_url") and not settings.get("success_redirect_url"):
        settings.success_redirect_url = "/agendamento-confirmado"

    if settings.meta.has_field("availability_of_slots") and not settings.get("availability_of_slots"):
        for day, frm, to in _DEFAULT_SLOTS:
            settings.append("availability_of_slots", {"day_of_week": day, "from_time": frm, "to_time": to})

    settings.save(ignore_permissions=True)
    frappe.db.commit()
    return {"enabled": True, "slots": len(_DEFAULT_SLOTS)}
