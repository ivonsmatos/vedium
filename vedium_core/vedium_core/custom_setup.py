import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

# Campos customizados do Vedium em DocTypes oficiais.
# gamification.add_points depende de User.vedium_points — por isso esta
# função roda no after_migrate (install.py), idempotente.

CUSTOM_FIELDS = {
    "User": [
        {
            "fieldname": "vedium_points",
            "label": "Vedium Points",
            "fieldtype": "Int",
            "insert_after": "first_name",
            "default": "0",
            "read_only": 1,
        },
        {
            "fieldname": "preferred_language",
            "label": "Preferred Language",
            "fieldtype": "Link",
            "options": "Language",
            "insert_after": "vedium_points",
        },
        # Onboarding wizard (/onboarding) — ver vedium_core/onboarding.py
        {
            "fieldname": "custom_preferred_language",
            "label": "Idioma de Interesse (Onboarding)",
            "fieldtype": "Data",
            "insert_after": "preferred_language",
        },
        {
            "fieldname": "custom_learning_goal",
            "label": "Objetivo de Aprendizado",
            "fieldtype": "Data",
            "insert_after": "custom_preferred_language",
        },
        {
            "fieldname": "custom_study_frequency",
            "label": "Frequência de Estudo",
            "fieldtype": "Data",
            "insert_after": "custom_learning_goal",
        },
        {
            "fieldname": "custom_onboarding_done",
            "label": "Onboarding Concluído",
            "fieldtype": "Check",
            "insert_after": "custom_study_frequency",
        },
    ],
    # Chaves VAPID pra Web Push — ver vedium_core/push_notifications.py
    "System Settings": [
        {
            "fieldname": "custom_vedium_vapid_public_key",
            "label": "Vedium VAPID Public Key",
            "fieldtype": "Data",
        },
        {
            "fieldname": "custom_vedium_vapid_private_key",
            "label": "Vedium VAPID Private Key",
            "fieldtype": "Password",
            "insert_after": "custom_vedium_vapid_public_key",
        },
        {
            "fieldname": "custom_vedium_vapid_email",
            "label": "Vedium VAPID Contact E-mail",
            "fieldtype": "Data",
            "insert_after": "custom_vedium_vapid_private_key",
        },
        # Fallback de configuração do Tutor IA (ver vedium_core/ai_tutor.py)
        # -- preferir site_config.json (frappe.conf.groq_api_key); este
        # campo existe pra quem preferir configurar pela UI.
        {
            "fieldname": "custom_groq_api_key",
            "label": "Vedium AI Tutor — Groq API Key",
            "fieldtype": "Password",
            "insert_after": "custom_vedium_vapid_email",
        },
    ],
    # Extensões Vedium ao certificado NATIVO do LMS (LMS Certificate).
    # Antes existia um doctype custom homônimo que sequestrava o nativo; foi
    # removido. Estas duas colunas dão suporte à verificação pública em
    # /certificado (api.issue_certificate / verify_certificate).
    "LMS Certificate": [
        {
            "fieldname": "verification_code",
            "label": "Verification Code",
            "fieldtype": "Data",
            "insert_after": "member",
            "unique": 1,
            "read_only": 1,
        },
        {
            "fieldname": "enrollment",
            "label": "Enrollment",
            "fieldtype": "Link",
            "options": "LMS Enrollment",
            "insert_after": "verification_code",
        },
    ],
    # Gate entre níveis do curso PLE (Básico -> Intermediário -> Avançado):
    # se setado, o aluno só enxerga o conteúdo deste curso depois de ter um
    # LMS Certificate emitido pro curso pré-requisito. Ver vedium_core/ple_gating.py.
    "LMS Course": [
        {
            "fieldname": "custom_prerequisite_course",
            "label": "Curso pré-requisito (gate de nível)",
            "fieldtype": "Link",
            "options": "LMS Course",
            "insert_after": "category",
        },
    ],
}


def setup_custom_fields():
    for doctype, field_list in CUSTOM_FIELDS.items():
        for field in field_list:
            if frappe.db.exists(
                "Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}
            ):
                continue
            create_custom_field(doctype, field)

    frappe.db.commit()


if __name__ == "__main__":
    setup_custom_fields()
