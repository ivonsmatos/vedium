"""Configura o Frappe Helpdesk para a operação inicial da Vedium.

Uso:
bench --site app.vediums.com execute \
  vedium_core.scripts.migrations.oneshot.setup_helpdesk_support.run
"""

import json

import frappe


AGENT_USER = "ivonmatos@vediums.com"
TEAM_NAME = "Vedium Support"


def _add_role(user, role):
    if not frappe.db.exists("Role", role):
        return False
    if frappe.db.exists("Has Role", {"parent": user, "role": role, "parenttype": "User"}):
        return False
    doc = frappe.get_doc("User", user)
    doc.append("roles", {"role": role})
    doc.save(ignore_permissions=True)
    return True


def _ensure_agent(user):
    if not frappe.db.exists("DocType", "HD Agent"):
        return None
    existing = frappe.db.exists("HD Agent", {"user": user})
    if existing:
        agent = frappe.get_doc("HD Agent", existing)
        if hasattr(agent, "is_active") and not agent.is_active:
            agent.is_active = 1
            agent.save(ignore_permissions=True)
        return agent.name

    full_name = frappe.db.get_value("User", user, "full_name") or user
    agent = frappe.new_doc("HD Agent")
    agent.user = user
    agent.agent_name = full_name
    if agent.meta.has_field("is_active"):
        agent.is_active = 1
    agent.insert(ignore_permissions=True)
    return agent.name


def _ensure_team(user):
    if not frappe.db.exists("DocType", "HD Team"):
        return None
    if frappe.db.exists("HD Team", TEAM_NAME):
        team = frappe.get_doc("HD Team", TEAM_NAME)
    else:
        team = frappe.new_doc("HD Team")
        team.team_name = TEAM_NAME
    members = {row.user for row in getattr(team, "users", []) if row.user}
    if user not in members:
        team.append("users", {"user": user})
    team.ignore_restrictions = 1
    team.save(ignore_permissions=True)
    return team.name


def _configure_settings():
    if not frappe.db.exists("DocType", "HD Settings"):
        return {}

    values = {}
    fields = {
        "default_priority": "Medium",
        "default_ticket_status": "Open",
        "ticket_reopen_status": "Open",
        "brand_name": "Vedium",
        "setup_complete": 1,
        "initial_helpdesk_name_setup_skipped": 1,
        "allow_anyone_to_create_tickets": 1,
        "skip_email_workflow": 0,
        "send_acknowledgement_email": 1,
    }
    for fieldname, value in fields.items():
        try:
            if frappe.get_meta("HD Settings").has_field(fieldname):
                frappe.db.set_single_value("HD Settings", fieldname, value)
                values[fieldname] = value
        except Exception:
            frappe.log_error(frappe.get_traceback(), f"Vedium.helpdesk.setting.{fieldname}")
    return values


def run():
    if not frappe.db.exists("User", AGENT_USER):
        frappe.throw(f"Usuário agente não encontrado: {AGENT_USER}")

    changed_roles = []
    for role in ("Agent", "Agent Manager"):
        if _add_role(AGENT_USER, role):
            changed_roles.append(role)

    agent = _ensure_agent(AGENT_USER)
    team = _ensure_team(AGENT_USER)
    settings = _configure_settings()
    frappe.db.commit()

    print(
        json.dumps(
            {
                "agent_user": AGENT_USER,
                "roles_added": changed_roles,
                "agent": agent,
                "team": team,
                "settings": settings,
                "hd_agent_count": frappe.db.count("HD Agent") if frappe.db.exists("DocType", "HD Agent") else None,
                "hd_team_count": frappe.db.count("HD Team") if frappe.db.exists("DocType", "HD Team") else None,
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )
