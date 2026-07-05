"""EMERGENCIA 2026-07-05: o registro 'Module Def' de Vedium Core sumiu do
banco (provavelmente durante as tentativas de instalar o hrms), derrubando
o site inteiro (qualquer pagina que toque um doctype do vedium_core da
500/403 -- Vedium Blog Post, Candidatura, etc). Este script recria o
Module Def e forca o reload dos doctypes do vedium_core, com commit
explicito logo apos cada passo (para nao depender de uma conexao SSH
que pode cair no meio do comando).

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.fix_vedium_core_module.run
"""
import frappe

DOCTYPES_TO_RELOAD = [
    "Vedium Blog Post",
    "Vedium Blog FAQ",
    "Candidatura",
]


def run():
    if not frappe.db.exists("Module Def", "Vedium Core"):
        doc = frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Vedium Core",
            "app_name": "vedium_core",
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Module Def 'Vedium Core' criado.")
    else:
        print("Module Def 'Vedium Core' ja existe.")

    frappe.clear_cache()
    frappe.db.commit()
    print("Cache limpo.")

    for dt in DOCTYPES_TO_RELOAD:
        try:
            frappe.reload_doctype(dt, force=True)
            frappe.db.commit()
            print(f"Reload OK: {dt}")
        except Exception as e:
            print(f"FALHOU reload de {dt}: {e}")

    print("\nFEITO. Reinicie os containers (docker restart vedium-frappe "
          "vedium-worker-default vedium-worker-short vedium-worker-long "
          "vedium-scheduler) e teste /sobre de novo.")
