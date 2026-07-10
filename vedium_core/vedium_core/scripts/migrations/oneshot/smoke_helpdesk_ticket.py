"""Smoke test do fluxo Vedium -> HD Ticket."""

import json

import frappe


def run():
    from vedium_core.helpdesk import create_ticket

    ticket = create_ticket(
        subject="[SMOKE] Helpdesk Vedium",
        description="Chamado temporário criado para validar o fluxo nativo HD Ticket.",
        category="Teste",
        raised_by="ivonmatos@vediums.com",
        requester_name="Vedium Smoke Test",
    )
    data = frappe.db.get_value(
        "HD Ticket",
        ticket.name,
        ["name", "subject", "raised_by", "status", "priority", "agent_group"],
        as_dict=True,
    )
    frappe.delete_doc("HD Ticket", ticket.name, force=True, ignore_permissions=True)
    frappe.db.commit()
    print(json.dumps({"created_and_deleted": True, "ticket": data}, indent=2, ensure_ascii=False, default=str))
