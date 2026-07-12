# Vedium Installation Script

import frappe


def before_install():
    pass


def after_install():
    frappe.msgprint("Vedium Core Installed Successfully!")
    _ensure_custom_doctypes()
    _remove_ai_tutor_artifacts()


def after_migrate():
    # Garante DocTypes criados dinamicamente (fora de doctype/*.json).
    # Mantém a mutação de schema no caminho de migração, não no de request.
    _ensure_custom_doctypes()
    _remove_ai_tutor_artifacts()
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


def _remove_ai_tutor_artifacts():
    """Remove o antigo Tutor IA custom.

    O recurso foi descontinuado porque o widget travava a área do aluno.
    Mantemos esta limpeza no migrate para apagar resíduos de instalações
    anteriores sem depender de intervenção manual no Desk.
    """
    try:
        for custom_field in (
            "System Settings-custom_groq_api_key",
            "System Settings-custom_vedium_ai_tutor_model",
        ):
            if frappe.db.exists("Custom Field", custom_field):
                frappe.delete_doc(
                    "Custom Field",
                    custom_field,
                    force=True,
                    ignore_permissions=True,
                    delete_permanently=True,
                )

        for doctype in ("AI Tutor Session", "AI Tutor Message"):
            if frappe.db.exists("DocType", doctype):
                frappe.delete_doc(
                    "DocType",
                    doctype,
                    force=True,
                    ignore_permissions=True,
                    delete_permanently=True,
                )

        frappe.db.commit()
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.install.remove_ai_tutor_artifacts"
        )
