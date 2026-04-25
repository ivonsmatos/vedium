import frappe

# Listar TODOS os cursos com detalhes
print("=== TODOS OS CURSOS NO BANCO ===")
all_courses = frappe.db.sql(
    "SELECT name, title, published, category, creation FROM `tabLMS Course` ORDER BY creation",
    as_dict=True,
)
print(f"Total: {len(all_courses)}\n")
for c in all_courses:
    print(f"  name={c.name}")
    print(f"  title={c.title}")
    print(f"  published={c.published} | category={c.category}")
    print()
