
import sys
sys.path.insert(0, '/home/frappe/frappe-bench/apps/frappe')
import frappe
frappe.init(site="app.vediums.com", sites_path="/home/frappe/frappe-bench/sites")
frappe.connect()

courses = frappe.get_all("LMS Course", fields=["name", "title"])
print(f"Total courses in database: {len(courses)}")
for course in courses:
    doc = frappe.get_doc("LMS Course", course.name)
    chapters = doc.get("chapters")
    print(f"Course: {course.title} - Chapters: {len(chapters) if chapters else 0}")
