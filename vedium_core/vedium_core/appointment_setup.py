"""Liga o Appointment Booking NATIVO do Frappe (encontro pré-venda dos fluxos
A05/A06). É config, não página custom — a regra de ouro é usar o nativo (ver
doc 01). Idempotente e defensivo: só liga quando dá para satisfazer os campos
obrigatórios do nativo (agente + holiday list) e nunca sobrescreve uma agenda que
a coordenação já ajustou no Desk.

O AGENTE (usuário cuja conta Google Calendar hospeda o encontro e gera o Meet) é
uma decisão de negócio — vem da config `VEDIUM_APPOINTMENT_AGENT`. Sem ela, o
ensure PULA em vez de chutar (não queremos rotear encontros reais pra agenda
errada). A Holiday List é criada automaticamente se não houver.

⚠️ AppointmentBookingSettings.save() NÃO aceita ignore_permissions como kwarg
(o controller do ERPNext sobrescreve save()); usa-se flags.ignore_permissions.
"""

from __future__ import annotations

import frappe
from frappe.utils import add_years, getdate, nowdate

# Agenda default: seg–sex, 09:00–18:00 (a coordenação ajusta no Desk depois).
_DEFAULT_SLOTS = [
    ("Monday", "09:00:00", "18:00:00"),
    ("Tuesday", "09:00:00", "18:00:00"),
    ("Wednesday", "09:00:00", "18:00:00"),
    ("Thursday", "09:00:00", "18:00:00"),
    ("Friday", "09:00:00", "18:00:00"),
]


def _ensure_holiday_list() -> str:
    """Nome de uma Holiday List existente; cria uma básica (1 ano) se não houver.
    O nativo exige holiday_list, mesmo sem feriados cadastrados."""
    existing = frappe.db.get_value("Holiday List", {}, "name")
    if existing:
        return existing
    hl = frappe.get_doc(
        {
            "doctype": "Holiday List",
            "holiday_list_name": "Vedium - Agenda",
            "from_date": nowdate(),
            "to_date": add_years(getdate(nowdate()), 1),
        }
    )
    hl.flags.ignore_permissions = True
    hl.insert()
    return hl.name


def _resolve_agent() -> str | None:
    """Agente = usuário da config VEDIUM_APPOINTMENT_AGENT (não chuta um padrão:
    rotear encontro pra agenda errada é pior que não ligar). Aceita as duas
    grafias da chave, como o resto do app (ver brevo._config)."""
    for key in ("VEDIUM_APPOINTMENT_AGENT", "vedium_appointment_agent"):
        agent = frappe.conf.get(key)
        if agent and frappe.db.exists("User", agent):
            return agent
    return None


def ensure_appointment_booking() -> dict:
    """Ativa o agendamento nativo com defaults sensatos. Só age se ainda estiver
    desligado E houver um agente configurado (não pisa em ajuste manual, não
    chuta o dono da agenda). Retorna o que mudou/pulou."""
    if not frappe.db.exists("DocType", "Appointment Booking Settings"):
        return {"skipped": "no_doctype"}

    settings = frappe.get_single("Appointment Booking Settings")
    if settings.get("enable_scheduling"):
        return {"skipped": "already_enabled"}

    agent = _resolve_agent()
    if not agent:
        # Sem agente definido não dá pra ligar (campo obrigatório do nativo).
        # Configure com: bench set-config VEDIUM_APPOINTMENT_AGENT <email>.
        return {"skipped": "needs_agent"}

    settings.enable_scheduling = 1
    settings.appointment_duration = settings.get("appointment_duration") or 30
    settings.advance_booking_days = settings.get("advance_booking_days") or 30
    settings.number_of_agents = 1
    settings.holiday_list = _ensure_holiday_list()
    settings.set("agent_list", [])
    settings.append("agent_list", {"user": agent})
    if settings.meta.has_field("email_reminders"):
        settings.email_reminders = 1
    if settings.meta.has_field("success_redirect_url") and not settings.get("success_redirect_url"):
        settings.success_redirect_url = "/agendamento-confirmado"

    if settings.meta.has_field("availability_of_slots") and not settings.get("availability_of_slots"):
        for day, frm, to in _DEFAULT_SLOTS:
            settings.append("availability_of_slots", {"day_of_week": day, "from_time": frm, "to_time": to})

    # O controller do ERPNext sobrescreve save() sem aceitar ignore_permissions.
    settings.flags.ignore_permissions = True
    settings.save()
    frappe.db.commit()
    return {"enabled": True, "agent": agent, "slots": len(_DEFAULT_SLOTS)}
