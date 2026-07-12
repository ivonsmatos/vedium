# -*- coding: utf-8 -*-
"""Adiciona ivonmatos@vediums.com como membro de TODOS os canais fixos de
equipe criados por setup_raven_staff_channels.py (hoje ele só estava no
canal "coordenacao").

Idempotente.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.add_admin_to_all_raven_channels.run
"""

import frappe

from vedium_core.communication import ensure_raven_user, ensure_workspace, ensure_workspace_member

USER = "ivonmatos@vediums.com"

CHANNEL_NAMES = (
    "professores-ingles",
    "professores-espanhol",
    "professores-portugues-ple",
    "professores-hebraico",
    "professores-ioruba",
    "coordenacao",
)


def run():
    workspace = ensure_workspace()
    raven_user = ensure_raven_user(USER)
    if not raven_user:
        print(f"Nao consegui garantir Raven User para {USER!r}")
        return

    ensure_workspace_member(workspace, raven_user)

    for channel_name in CHANNEL_NAMES:
        channel = frappe.db.get_value(
            "Raven Channel", {"channel_name": channel_name, "workspace": workspace}, "name"
        )
        if not channel:
            print(f"  [{channel_name}] canal nao existe, pulei")
            continue

        existing = frappe.db.exists(
            "Raven Channel Member", {"channel_id": channel, "user_id": raven_user}
        )
        if existing:
            print(f"  [{channel_name}] ja era membro")
            continue

        frappe.get_doc({
            "doctype": "Raven Channel Member",
            "channel_id": channel,
            "user_id": raven_user,
            "is_admin": 1,
            "last_visit": frappe.utils.now_datetime(),
            "allow_notifications": 1,
        }).insert(ignore_permissions=True)
        print(f"  [{channel_name}] membro adicionado")
