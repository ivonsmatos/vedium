"""Safely reactivate the Microsoft 365 support inbox after OAuth recovery.

The IMAP XOAUTH2 connection is tested before any state is changed. Outgoing
email remains disabled because transactional sending uses the dedicated
outgoing account/provider.
"""

from __future__ import annotations

import json

import frappe


ACCOUNT = "Suporte Vedium"


def run() -> dict[str, object]:
    account = frappe.get_doc("Email Account", ACCOUNT)

    # Fail closed: never re-enable a mailbox whose OAuth connection is invalid.
    account.flags.validate_imap_pop_connection = True
    server = account.get_incoming_server(in_receive=False)
    try:
        server.logout()
    except Exception:
        pass

    frappe.db.set_value(
        "Email Account",
        ACCOUNT,
        {
            "enable_incoming": 1,
            "enable_outgoing": 0,
            "no_failed": 0,
            "awaiting_password": 0,
        },
    )
    frappe.clear_cache(doctype="Email Account")
    frappe.db.commit()

    result = {
        "account": ACCOUNT,
        "email_id": account.email_id,
        "incoming_auth": "ok",
        "enable_incoming": 1,
        "enable_outgoing": 0,
        "no_failed": 0,
        "append_to": account.append_to,
    }
    print(json.dumps(result, indent=2))
    return result


def sync() -> dict[str, object]:
    """Run the same receive path used by the scheduler as a smoke test."""
    account = frappe.get_doc("Email Account", ACCOUNT)
    if not account.enable_incoming:
        frappe.throw(f"Incoming email is disabled for {ACCOUNT}")

    account.receive()
    frappe.db.commit()
    result = {
        "account": ACCOUNT,
        "receive": "ok",
        "enable_incoming": account.enable_incoming,
        "no_failed": account.get_failed_attempts_count(),
        "append_to": account.append_to,
    }
    print(json.dumps(result, indent=2))
    return result
