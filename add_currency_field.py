import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def add_currency_field():
    frappe.init(site="app.vediums.com")
    frappe.connect()

    if not frappe.db.exists("Custom Field", "LMS Enrollment-custom_contract_currency"):
        create_custom_field(
            "LMS Enrollment",
            {
                "fieldname": "custom_contract_currency",
                "label": "Contract Currency",
                "fieldtype": "Data",
                "insert_after": "custom_contract_monthly_amount",
                "read_only": 1,
                "default": "BRL"
            },
        )
        frappe.db.commit()
        print("Campo custom_contract_currency criado com sucesso!")
    else:
        print("Campo custom_contract_currency já existe.")

    frappe.destroy()

if __name__ == "__main__":
    add_currency_field()
