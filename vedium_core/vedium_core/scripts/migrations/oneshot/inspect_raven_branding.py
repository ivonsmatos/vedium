# -*- coding: utf-8 -*-
"""Diagnostico read-only: onde fica o logo da tela /raven/login (wordmark
"raven" preto), separado do logo por-workspace ja corrigido em
set_raven_workspace_logo.py.

Checa:
  1. Se existe DocType "Raven Settings" (singleton de branding do app) e
     seus campos de logo/marca.
  2. Website Settings.app_logo / app_name (usado por telas de login nativas
     do Frappe em geral).

Nao altera nada.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_raven_branding.run
"""

import frappe


def run():
    print("=== DocType 'Raven Settings' existe? ===")
    exists = frappe.db.exists("DocType", "Raven Settings")
    print(exists)
    if exists:
        meta = frappe.get_meta("Raven Settings")
        for f in meta.fields:
            if any(k in f.fieldname.lower() for k in ("logo", "icon", "image", "brand", "name", "favicon")):
                print(f"  fieldname={f.fieldname!r} | fieldtype={f.fieldtype!r} | label={f.label!r}")
        doc = frappe.get_single("Raven Settings")
        print("  valores atuais:", {
            f.fieldname: doc.get(f.fieldname)
            for f in meta.fields
            if any(k in f.fieldname.lower() for k in ("logo", "icon", "image", "brand", "name", "favicon"))
        })

    print("\n=== Website Settings (campos de marca) ===")
    ws_meta = frappe.get_meta("Website Settings")
    for f in ws_meta.fields:
        if any(k in f.fieldname.lower() for k in ("logo", "favicon", "app_name", "brand")):
            val = frappe.db.get_single_value("Website Settings", f.fieldname)
            print(f"  {f.fieldname} ({f.fieldtype}) = {val!r}")

    print("\n=== Outros doctypes com 'raven' + 'setting'/'branding' no nome ===")
    for name in frappe.get_all("DocType", filters=[["name", "like", "%Raven%"]], pluck="name"):
        if "setting" in name.lower() or "brand" in name.lower() or "config" in name.lower():
            print(" ", name)
