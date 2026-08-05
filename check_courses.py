import sys
sys.path.insert(0,'/home/frappe/frappe-bench/apps/frappe')
import frappe
frappe.init(site='vedium.local', sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()

courses = frappe.get_all("LMS Course", fields=["name", "title"])
for c in courses:
    if "Iorub" in c.title or "Avan" in c.title:
        print(c)
