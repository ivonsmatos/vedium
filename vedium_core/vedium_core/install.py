# Vedium Installation Script

import frappe


def before_install():
    pass


def after_install():
    frappe.msgprint("Vedium Core Installed Successfully!")
    _ensure_custom_doctypes()


def after_migrate():
    # Garante DocTypes criados dinamicamente (fora de doctype/*.json).
    # Mantém a mutação de schema no caminho de migração, não no de request.
    _ensure_custom_doctypes()


def _ensure_custom_doctypes():
    try:
        from vedium_core.careers import ensure_candidatura_doctype

        ensure_candidatura_doctype()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.ensure_custom_doctypes"
        )

    # User.vedium_points etc. — gamification depende destes campos
    try:
        from vedium_core.custom_setup import setup_custom_fields

        setup_custom_fields()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.setup_custom_fields"
        )
