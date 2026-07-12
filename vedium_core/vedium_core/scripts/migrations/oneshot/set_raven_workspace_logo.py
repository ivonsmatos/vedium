# -*- coding: utf-8 -*-
"""Coloca o logo da Vedium no workspace 'Vedium' do Raven.

Reusa o mesmo icone quadrado 192x192 ja usado no PWA do LMS
(fix_lms_pwa_icon.py) -- mesma marca, sem precisar subir arquivo novo.
Raven Workspace.logo e "Attach Image" mas aceita apontar direto pra um
asset publico existente (mesmo padrao usado em Website Settings.banner_image).
Idempotente.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.set_raven_workspace_logo.run
"""

import frappe

VEDIUM_ICON = "/assets/vedium_core/images/icon-192x192.png"
WORKSPACE_NAME = "Vedium"


def run():
    if not frappe.db.exists("Raven Workspace", WORKSPACE_NAME):
        print(f"Raven Workspace {WORKSPACE_NAME!r} nao existe ainda.")
        return

    current = frappe.db.get_value("Raven Workspace", WORKSPACE_NAME, "logo")
    if current == VEDIUM_ICON:
        print(f"Ja correto: logo = {current}")
        return

    frappe.db.set_value("Raven Workspace", WORKSPACE_NAME, "logo", VEDIUM_ICON)
    frappe.db.commit()
    print(f"logo: {current!r} -> {VEDIUM_ICON!r}")
