# -*- coding: utf-8 -*-
"""Integração da Vedium com o Frappe Helpdesk nativo."""

import frappe


DEFAULT_TEAM = "Vedium Support"
DEFAULT_PRIORITY = "Medium"
DEFAULT_STATUS = "Open"


def _clean(value, limit=1000):
    text = str(value or "").strip()
    return text[:limit]


def _html(value):
    return frappe.utils.escape_html(str(value or ""))


def _user_email(user=None):
    user = user or frappe.session.user
    if not user or user == "Guest":
        return None
    if "@" in user:
        return user
    try:
        return frappe.db.get_value("User", user, "email")
    except Exception:
        return None


def _ensure_contact_for_email(email, name=None, phone=None):
    if not email:
        return None
    try:
        from vedium_core.integrations import ensure_contact

        parts = (name or email).strip().split(" ", 1)
        return ensure_contact(
            email,
            first_name=parts[0],
            last_name=parts[1] if len(parts) > 1 else None,
            mobile=phone,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.helpdesk.ensure_contact")
        return None


def _fallback_support_ticket(subject, description, category=None, opened_by=None):
    ticket = frappe.get_doc(
        {
            "doctype": "Support Ticket",
            "subject": _clean(subject, 140),
            "description": description,
            "category": category or "Geral",
            "status": "Open",
        }
    )
    if opened_by and opened_by != "Guest":
        ticket.opened_by = opened_by
    ticket.insert(ignore_permissions=True)
    return ticket


def create_ticket(
    subject,
    description,
    category=None,
    raised_by=None,
    requester_name=None,
    phone=None,
    priority=None,
    team=None,
):
    """Cria chamado no Helpdesk nativo, com fallback para Support Ticket legado."""
    if not frappe.db.exists("DocType", "HD Ticket"):
        return _fallback_support_ticket(subject, description, category, frappe.session.user)

    raised_by = _clean(raised_by or _user_email() or "contato@vediums.com", 180)
    contact = _ensure_contact_for_email(raised_by, requester_name, phone)
    category = category or "Geral"
    description_html = (
        f"<p><strong>Categoria:</strong> {_html(category)}</p>"
        f"<p>{_html(description).replace(chr(10), '<br>')}</p>"
    )

    ticket = frappe.new_doc("HD Ticket")
    ticket.subject = _clean(subject, 140) or category
    ticket.raised_by = raised_by
    ticket.description = description_html
    ticket.summary = _clean(description, 500)
    ticket.status = DEFAULT_STATUS
    ticket.priority = priority or DEFAULT_PRIORITY
    if contact:
        ticket.contact = contact
    selected_team = team or DEFAULT_TEAM
    if frappe.db.exists("HD Team", selected_team):
        ticket.agent_group = selected_team
    ticket.via_customer_portal = 1
    ticket.insert(ignore_permissions=True)
    return ticket


def list_tickets_for_user(user=None):
    """Lista chamados do usuário atual, normalizado para o portal Vedium."""
    email = _user_email(user)
    if not email:
        return []

    if frappe.db.exists("DocType", "HD Ticket"):
        rows = frappe.get_all(
            "HD Ticket",
            filters={"raised_by": email},
            fields=["name", "subject", "status", "priority", "creation", "agent_group"],
            order_by="creation desc",
        )
        for row in rows:
            row["category"] = row.get("agent_group") or "Suporte"
        return rows

    if frappe.db.exists("DocType", "Support Ticket"):
        return frappe.get_all(
            "Support Ticket",
            filters={"opened_by": user or frappe.session.user},
            fields=["name", "subject", "status", "creation", "category"],
            order_by="creation desc",
        )
    return []
