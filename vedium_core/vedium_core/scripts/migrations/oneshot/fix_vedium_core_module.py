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
import os

import frappe

# Caminhos diretos dos .json -- evita depender da resolucao de "module"
# (que estava falhando: campo module vazio/quebrado nos registros de
# DocType existentes).
JSON_PATHS = [
    "vedium_core/vedium_core/vedium_core/doctype/vedium_blog_post/vedium_blog_post.json",
    "vedium_core/vedium_core/vedium_core/doctype/vedium_blog_faq/vedium_blog_faq.json",
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

    # Corrige o campo module de qualquer DocType do vedium_core que
    # esteja vazio/errado (causa raiz do "Module  not found").
    apps_root = os.path.abspath(os.path.join(frappe.get_app_path("frappe"), "..", ".."))

    for rel_path in JSON_PATHS:
        full_path = os.path.join(apps_root, rel_path)
        if not os.path.exists(full_path):
            print(f"NAO ACHOU o arquivo: {full_path}")
            continue
        try:
            from frappe.modules.import_file import import_file_by_path
            import_file_by_path(full_path, force=True, ignore_version=True)
            frappe.db.commit()
            print(f"Import OK (via caminho direto): {rel_path}")
        except Exception as e:
            print(f"FALHOU import de {rel_path}: {e}")

    # Garante que o campo module de cada doctype ficou certo apos o import.
    for dt in ["Vedium Blog Post", "Vedium Blog FAQ"]:
        mod = frappe.db.get_value("DocType", dt, "module")
        print(f"{dt}: module = {mod!r}")

    # Candidatura e um doctype custom (sem arquivo .json) -- so garante
    # que o campo module dele esta correto, sem tentar reload de arquivo.
    if frappe.db.exists("DocType", "Candidatura"):
        frappe.db.set_value("DocType", "Candidatura", "module", "Vedium Core")
        frappe.db.commit()
        print("Candidatura: module corrigido para 'Vedium Core' (sem reload de arquivo, e custom doctype).")

    frappe.clear_cache()
    frappe.db.commit()
    print("Cache limpo.")

    print("\nFEITO. Reinicie os containers (docker restart vedium-frappe "
          "vedium-worker-default vedium-worker-short vedium-worker-long "
          "vedium-scheduler) e teste /sobre de novo.")
