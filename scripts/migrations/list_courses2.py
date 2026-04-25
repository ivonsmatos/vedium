import frappe

rows = frappe.db.sql("SELECT name, title FROM `tabLMS Course`", as_dict=True)
for r in rows:
    print(r.name, "||", r.title)
