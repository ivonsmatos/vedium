"""Sincronização opcional de contatos do Frappe com o Brevo."""

import frappe
import requests

from vedium_core.brevo_payload import build_contact_payload


BREVO_CONTACTS_URL = "https://api.brevo.com/v3/contacts"
BREVO_TIMEOUT_SECONDS = 15


def sync_contact_to_brevo(
    email,
    *,
    first_name=None,
    last_name=None,
    course=None,
):
    """Cria ou atualiza um contato no Brevo sem interromper o fluxo chamador."""
    api_key = (frappe.conf.get("BREVO_API_KEY") or "").strip()
    if not api_key:
        return {"status": "skipped", "reason": "BREVO_API_KEY not configured"}

    try:
        payload = build_contact_payload(
            email,
            first_name=first_name,
            last_name=last_name,
            course=course,
            list_ids=frappe.conf.get("BREVO_LIST_IDS"),
        )
    except (TypeError, ValueError) as exc:
        frappe.log_error(
            f"Configuração/payload inválido do Brevo: {exc}",
            "Vedium: sync Brevo",
        )
        return {"status": "error", "reason": "invalid configuration"}

    try:
        response = requests.post(
            BREVO_CONTACTS_URL,
            json=payload,
            headers={
                "api-key": api_key,
                "accept": "application/json",
                "content-type": "application/json",
            },
            timeout=BREVO_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json() if response.content else {}
        return {"status": "synced", "contact_id": data.get("id")}
    except requests.RequestException as exc:
        status_code = getattr(getattr(exc, "response", None), "status_code", None)
        detail = f"HTTP {status_code}" if status_code else type(exc).__name__
        frappe.log_error(
            f"Falha ao sincronizar contato com o Brevo: {detail}",
            "Vedium: sync Brevo",
        )
        return {"status": "error", "reason": detail}
