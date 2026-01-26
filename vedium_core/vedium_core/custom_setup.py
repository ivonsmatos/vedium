import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def setup_custom_fields():
	fields = {
		"User": [
			{
				"fieldname": "vedium_points",
				"label": "Vedium Points",
				"fieldtype": "Int",
				"insert_after": "first_name",
				"default": "0",
				"read_only": 1
			},
			{
				"fieldname": "preferred_language",
				"label": "Preferred Language",
				"fieldtype": "Link",
				"options": "Language",
				"insert_after": "vedium_points"
			}
		]
	}
	for doctype, field_list in fields.items():
		for field in field_list:
			create_custom_field(doctype, field)
	
	frappe.db.commit()

if __name__ == "__main__":
	setup_custom_fields()
