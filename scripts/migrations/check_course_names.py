import frappe

# Reexecutar apenas os chapters e lessons para os cursos já criados
# Os cursos estão com names: ingl-s-beginner, ingl-s-elementary, etc.

COURSE_MAP = [
    ("ingl-s-beginner", "Inglês - Beginner"),
    ("ingl-s-elementary", "Inglês - Elementary"),
    ("ingl-s-pr-intermedi-rio", "Inglês - Pré-Intermediário"),
    ("ingl-s-intermedi-rio", "Inglês - Intermediário"),
    ("ingl-s-upper-intermedi-rio", "Inglês - Upper Intermediário"),
    ("ingl-s-avan-ado", "Inglês - Avançado"),
]

# Verifica que todos existem
for name, title in COURSE_MAP:
    exists = frappe.db.exists("LMS Course", name)
    print(f"  {'✓' if exists else '✗'} {name} | {title}")
