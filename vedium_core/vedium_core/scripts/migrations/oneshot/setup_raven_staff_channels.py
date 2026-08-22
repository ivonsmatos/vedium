# -*- coding: utf-8 -*-
"""Cria os canais fixos de equipe no Raven (Coordenação + 1 por idioma
realmente ofertado) e adiciona professores/coordenação como membros.

Baseado no catalogo real levantado por inspect_raven_setup.py (2026-07-12):
  - Ingles: kayode@vediums.com
  - Iorubá: busayo@vediums.com
  - Português p/ Estrangeiros (PLE): almir@vediums.com
  - Espanhol: sem professor real cadastrado ainda -- canal criado vazio
  - Hebraico: sem professor real cadastrado ainda -- canal criado vazio
  - Coordenação: ivonmatos@vediums.com + todos os professores acima

Diferente dos canais de curso/turma (vedium_core.communication), estes NÃO
são gerenciados por matrícula -- são grupos fixos de equipe, sem is_synced,
e não são removidos automaticamente por cancelamento.

Idempotente: rodar de novo não duplica canal nem membro.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.setup_raven_staff_channels.run
"""

import frappe

from vedium_core.communication import (
    ensure_raven_user,
    ensure_workspace,
    ensure_workspace_member,
    raven_available,
)

COORDINATION_USER = "ivonmatos@vediums.com"

LANGUAGE_CHANNELS = {
    "professores-ingles": {
        "description": "Grupo de professores de Inglês",
        "members": ["kayode@vediums.com"],
    },
    "professores-espanhol": {
        "description": "Grupo de professores de Espanhol",
        "members": [],
    },
    "professores-portugues-ple": {
        "description": "Grupo de professores de Português para Estrangeiros (PLE)",
        "members": ["almir@vediums.com"],
    },
    "professores-hebraico": {
        "description": "Grupo de professores de Hebraico",
        "members": [],
    },
    "professores-ioruba": {
        "description": "Grupo de professores de Iorubá",
        "members": ["busayo@vediums.com"],
    },
}

COORDENACAO_CHANNEL = "coordenacao"
COORDENACAO_MEMBERS = [
    COORDINATION_USER,
    "kayode@vediums.com",
    "busayo@vediums.com",
    "almir@vediums.com",
]


def run():
    if not raven_available():
        print("Raven nao instalado neste site.")
        return

    workspace = ensure_workspace()

    all_channels = dict(LANGUAGE_CHANNELS)
    all_channels[COORDENACAO_CHANNEL] = {
        "description": "Canal da coordenação pedagógica com todos os professores",
        "members": COORDENACAO_MEMBERS,
    }

    for channel_name, info in all_channels.items():
        channel = _ensure_staff_channel(workspace, channel_name, info["description"])
        for user in info["members"]:
            raven_user = ensure_raven_user(user)
            if not raven_user:
                print(f"  [{channel_name}] pulei {user!r} (sem User valido ou e Administrator)")
                continue
            ensure_workspace_member(workspace, raven_user)
            _ensure_plain_channel_member(channel, raven_user)
            print(f"  [{channel_name}] membro garantido: {user}")


def _ensure_staff_channel(workspace, channel_name, description):
    existing = frappe.db.get_value(
        "Raven Channel", {"channel_name": channel_name, "workspace": workspace}, "name"
    )
    if existing:
        return existing
    channel = frappe.get_doc({
        "doctype": "Raven Channel",
        "type": "Private",
        "channel_name": channel_name,
        "channel_description": description,
        "workspace": workspace,
    })
    channel.flags.do_not_add_member = True
    channel.insert(ignore_permissions=True)
    print(f"Canal criado: {channel_name}")
    return channel.name


def _ensure_plain_channel_member(channel, raven_user):
    existing = frappe.db.exists(
        "Raven Channel Member", {"channel_id": channel, "user_id": raven_user}
    )
    if existing:
        return existing
    member = frappe.get_doc({
        "doctype": "Raven Channel Member",
        "channel_id": channel,
        "user_id": raven_user,
        "is_admin": 0,
        "last_visit": frappe.utils.now_datetime(),
        "allow_notifications": 1,
    })
    member.insert(ignore_permissions=True)
    return member.name
