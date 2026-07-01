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
