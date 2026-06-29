"""Public funnel endpoints for marketing and sales handoff.

These endpoints intentionally create human-reviewable Support Tickets instead
of mutating checkout, enrollments, payment sessions, or LMS progress directly.
"""

import json
import re

import frappe
from frappe import _
from frappe.utils import cint, now_datetime


ALLOWED_INTENTS = {
    "lead": "Lead",
    "diagnostic": "Aula diagnóstica",
    "community": "Comunidade",
    "referral": "Indicação",
    "b2b": "B2B",
    "review": "Depoimento verificado",
}


def _clean(value, limit=500):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def _payload():
    data = frappe.local.form_dict.copy()
    raw = getattr(frappe.request, "data", None)
    if raw:
        try:
            parsed = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
            if isinstance(parsed, dict):
                data.update(parsed)
        except Exception:
            pass
    return data


def _create_ticket(intent, subject, details):
    category = ALLOWED_INTENTS.get(intent, "Lead")
    description = "\n".join(
        f"{key}: {_clean(value, 1000)}"
        for key, value in details.items()
        if _clean(value, 1000)
    )
    ticket_data = {
        "doctype": "Support Ticket",
        "subject": _clean(subject, 140) or category,
        "description": description,
        "category": category,
        "status": "Open",
    }
    if frappe.session.user and frappe.session.user != "Guest":
        ticket_data["opened_by"] = frappe.session.user
    ticket = frappe.get_doc(ticket_data)
    ticket.insert(ignore_permissions=True)
    try:
        frappe.sendmail(
            recipients=["contato@vediums.com"],
            subject=f"[Vedium] {category}: {ticket.subject}",
            message=description.replace("\n", "<br>"),
            delayed=False,
        )
    except Exception as exc:
        frappe.log_error(f"Public funnel email failed: {exc}", "Vedium Public Funnel")
    lead_email = _clean(details.get("email"), 180)
    if lead_email:
        try:
            frappe.sendmail(
                recipients=[lead_email],
                subject="Recebemos seu contato | Vedium",
                message=(
                    "<p>Olá! Recebemos seu interesse na Vedium.</p>"
                    "<p>Nossa equipe vai analisar seu objetivo e retornar com o próximo passo. "
                    "Se preferir atendimento imediato, fale pelo WhatsApp: "
                    '<a href="https://wa.me/5511911293075">+55 (11) 91129-3075</a>.</p>'
                    "<p>Equipe Vedium</p>"
                ),
                delayed=False,
            )
        except Exception as exc:
            frappe.log_error(
                f"Public funnel lead confirmation failed: {exc}",
                "Vedium Public Funnel",
            )
    return ticket


@frappe.whitelist(allow_guest=True)
def submit_public_intent():
    data = _payload()
    intent = _clean(data.get("intent") or "lead", 40)
    if intent not in ALLOWED_INTENTS:
        frappe.throw(_("Tipo de intenção inválido."))

    email = _clean(data.get("email"), 180)
    phone = _clean(data.get("phone"), 40)
    name = _clean(data.get("name"), 180)
    course = _clean(data.get("course"), 180)
    plan = _clean(data.get("plan"), 80)
    goal = _clean(data.get("goal"), 180)
    referer = ""
    try:
        referer = frappe.request.headers.get("Referer", "")
    except Exception:
        referer = ""
    source = _clean(data.get("source") or referer, 300)
    message = _clean(data.get("message"), 1200)

    subject_parts = [ALLOWED_INTENTS[intent], name or email or phone or "site"]
    if course:
        subject_parts.append(course)
    ticket = _create_ticket(
        intent,
        " | ".join(subject_parts),
        {
            "name": name,
            "email": email,
            "phone": phone,
            "course": course,
            "plan": plan,
            "goal": goal,
            "source": source,
            "message": message,
        },
    )
    return {"ok": True, "ticket": ticket.name}


@frappe.whitelist(allow_guest=True)
def request_diagnostic_class():
    data = _payload()
    data["intent"] = "diagnostic"
    frappe.local.form_dict.update(data)
    return submit_public_intent()


@frappe.whitelist(allow_guest=True)
def get_available_diagnostic_slots(limit=8):
    limit = max(1, min(cint(limit) or 8, 20))
    slots = frappe.get_all(
        "Lesson Slot",
        filters={"status": "Available", "start_time": [">=", now_datetime()]},
        fields=["name", "start_time", "end_time"],
        order_by="start_time asc",
        limit_page_length=limit,
    )
    return {
        "ok": True,
        "slots": [
            {
                "slot": slot.name,
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
            }
            for slot in slots
        ],
    }


@frappe.whitelist(allow_guest=True)
def verify_certificate(code):
    code = _clean(code, 120)
    if not code:
        frappe.throw(_("Código obrigatório."))
    cert = frappe.db.get_value(
        "LMS Certificate",
        {"verification_code": code},
        ["name", "member", "course", "issue_date"],
        as_dict=True,
    )
    if not cert:
        return {"ok": False, "valid": False}
    title = frappe.db.get_value("LMS Course", cert.course, "title")
    member_name = frappe.db.get_value("User", cert.member, "full_name")
    return {
        "ok": True,
        "valid": True,
        "certificate": cert.name,
        "student": member_name or cert.member,
        "course": title or cert.course,
        "issue_date": cert.issue_date,
    }
