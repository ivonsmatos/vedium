"""Read-only production audit for a Frappe Email Account.

Run inside the bench container:
    python /tmp/audit_email_account.py app.vediums.com suporte@vediums.com

Passwords, OAuth client secrets, and tokens are never printed.
"""

from __future__ import annotations

import json
import sys
import traceback
import base64

import frappe


SAFE_ACCOUNT_FIELDS = (
    "name",
    "email_id",
    "auth_method",
    "enable_incoming",
    "enable_outgoing",
    "service",
    "domain",
    "email_server",
    "email_port",
    "smtp_server",
    "smtp_port",
    "use_imap",
    "use_ssl",
    "use_tls",
    "append_to",
    "connected_app",
    "connected_user",
    "backend_app_flow",
    "awaiting_password",
    "no_failed",
    "last_synced_at",
    "modified",
)


def safe_error(exc: BaseException) -> dict[str, str]:
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": "".join(traceback.format_exception(exc))[-4000:],
    }


def main(site: str, email_id: str) -> None:
    frappe.init(site=site, sites_path="/home/frappe/frappe-bench/sites")
    frappe.connect()
    result: dict[str, object] = {"site": site, "email_id": email_id}

    try:
        name = frappe.db.get_value("Email Account", {"email_id": email_id}, "name")
        if not name:
            result["error"] = "Email Account not found"
            print(json.dumps(result, indent=2, default=str))
            return

        doc = frappe.get_doc("Email Account", name)
        result["account"] = {
            field: doc.get(field)
            for field in SAFE_ACCOUNT_FIELDS
            if doc.meta.has_field(field)
        }

        if doc.get("connected_app"):
            app = frappe.get_doc("Connected App", doc.connected_app)
            result["connected_app"] = {
                "name": app.name,
                "provider_name": app.get("provider_name"),
                "token_uri": app.get("token_uri"),
                "authorization_uri": app.get("authorization_uri"),
                "redirect_uri": app.get("redirect_uri"),
                "modified": app.modified,
                "has_client_id": bool(app.get("client_id")),
                "has_client_secret": bool(app.get_password("client_secret", raise_exception=False)),
                "scopes": [row.scope for row in app.get("scopes", [])],
            }

            try:
                token = doc.get_oauth_token()
                result["oauth_token"] = {
                    "available": bool(token),
                    "keys": sorted(token.keys()) if isinstance(token, dict) else [],
                    "expires_in": token.get("expires_in") if isinstance(token, dict) else None,
                }
                if token and hasattr(token, "get_password"):
                    access_token = token.get_password("access_token", raise_exception=False)
                    if access_token and access_token.count(".") >= 2:
                        payload = access_token.split(".", 2)[1]
                        payload += "=" * (-len(payload) % 4)
                        claims = json.loads(base64.urlsafe_b64decode(payload))
                        result["oauth_token"]["claims"] = {
                            key: claims.get(key)
                            for key in ("aud", "appid", "azp", "tid", "roles", "scp", "exp", "iat")
                            if claims.get(key) is not None
                        }
            except Exception as exc:
                result["oauth_token_error"] = safe_error(exc)

        try:
            doc.flags.validate_imap_pop_connection = True
            incoming = doc.get_incoming_server(in_receive=False)
            result["incoming_auth"] = "ok"
            try:
                incoming.logout()
            except Exception:
                pass
        except Exception as exc:
            result["incoming_auth"] = "failed"
            result["incoming_error"] = safe_error(exc)

        logs = frappe.get_all(
            "Error Log",
            fields=["name", "creation", "method", "error"],
            order_by="creation desc",
            limit_page_length=100,
        )
        needles = (email_id.lower(), "login failed", "oauth", "email account")
        result["recent_relevant_errors"] = [
            {
                "name": row.name,
                "creation": row.creation,
                "method": row.method,
                "classification": (
                    "login_failed"
                    if "login failed" in (row.error or "").lower()
                    else "oauth_error"
                    if "oauth" in (row.error or "").lower()
                    else "email_account_error"
                ),
            }
            for row in logs
            if any(needle in f"{row.method}\n{row.error}".lower() for needle in needles)
        ][:10]

        versions = frappe.get_all(
            "Version",
            filters={
                "ref_doctype": ("in", ["Email Account", "Connected App"]),
                "docname": ("in", [doc.name, doc.get("connected_app")]),
            },
            fields=["creation", "owner", "ref_doctype", "docname", "data"],
            order_by="creation desc",
            limit_page_length=20,
        )
        result["versions"] = []
        for version in versions:
            try:
                data = json.loads(version.data or "{}")
                changed_fields = sorted(
                    {change[0] for change in data.get("changed", []) if change}
                    | {row[1] for row in data.get("row_changed", []) if len(row) > 1}
                )
            except (TypeError, ValueError):
                changed_fields = []
            result["versions"].append(
                {
                    "creation": version.creation,
                    "owner": version.owner,
                    "ref_doctype": version.ref_doctype,
                    "docname": version.docname,
                    "changed_fields": changed_fields,
                }
            )

        print(json.dumps(result, indent=2, default=str))
    finally:
        frappe.destroy()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
