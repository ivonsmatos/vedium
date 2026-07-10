"""Inspeciona schema e configuração do Frappe Helpdesk em produção."""

import json

import frappe


def _meta_fields(doctype):
    if not frappe.db.exists("DocType", doctype):
        return []
    meta = frappe.get_meta(doctype)
    return [
        {
            "fieldname": field.fieldname,
            "label": field.label,
            "fieldtype": field.fieldtype,
            "options": field.options,
            "reqd": field.reqd,
            "default": field.default,
        }
        for field in meta.fields
        if field.fieldtype not in ("Section Break", "Column Break", "Tab Break")
    ]


def run():
    doctypes = [
        "HD Ticket",
        "HD Team",
        "HD Agent",
        "HD Service Level Agreement",
        "HD Ticket Priority",
        "HD Ticket Status",
        "HD Settings",
    ]
    result = {
        "installed": {doctype: frappe.db.exists("DocType", doctype) for doctype in doctypes},
        "counts": {},
        "fields": {},
        "users": frappe.get_all(
            "User",
            filters={"enabled": 1, "user_type": "System User"},
            fields=["name", "full_name", "email"],
            order_by="name asc",
        ),
        "roles": frappe.get_all(
            "Has Role",
            filters={"role": ["in", ["Agent", "Agent Manager", "System Manager"]], "parenttype": "User"},
            fields=["parent", "role"],
            order_by="parent asc, role asc",
        ),
    }
    for doctype in doctypes:
        if result["installed"][doctype]:
            try:
                result["counts"][doctype] = frappe.db.count(doctype)
            except Exception as exc:
                result["counts"][doctype] = f"unavailable: {exc}"
            result["fields"][doctype] = _meta_fields(doctype)

    for doctype in ("HD Team", "HD Ticket Priority", "HD Ticket Status", "HD Agent"):
        if result["installed"].get(doctype):
            fields = ["name"]
            meta_fields = {field["fieldname"] for field in result["fields"][doctype]}
            for candidate in ("team_name", "user", "agent_name", "priority", "status", "enabled"):
                if candidate in meta_fields:
                    fields.append(candidate)
            result[doctype] = frappe.get_all(doctype, fields=fields, limit_page_length=50)

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
