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
    _clear_module_cache()


def _ensure_custom_doctypes():
    try:
        from vedium_core.careers import ensure_candidatura_doctype

        ensure_candidatura_doctype()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.ensure_custom_doctypes"
        )

    try:
        from vedium_core.push_notifications import ensure_push_subscription_doctype

        ensure_push_subscription_doctype()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.ensure_push_subscription_doctype"
        )

    # User.vedium_points etc. — gamification depende destes campos
    try:
        from vedium_core.custom_setup import setup_custom_fields

        setup_custom_fields()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.setup_custom_fields"
        )

    try:
        from vedium_core.ai_tutor import ensure_ai_tutor_doctypes

        ensure_ai_tutor_doctypes()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.ensure_ai_tutor_doctypes"
        )

    try:
        from vedium_core.pedagogical_setup import ensure_pedagogical_setup

        ensure_pedagogical_setup()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.ensure_pedagogical_setup"
        )


def _clear_module_cache():
    try:
        from frappe.utils.modules import get_modules_from_app

        get_modules_from_app.clear_cache()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.clear_module_cache"
        )
