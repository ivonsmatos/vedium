"""Eleva Almir ao papel de instrutor do LMS para gerenciar cursos.

bench execute vedium_core.scripts.migrations.oneshot.fix_almir_instructor_role.run
"""
import frappe

EMAIL = "almirseller@yahoo.com"


def run():
    # Mostra os papéis disponíveis relacionados a LMS/curso
    available = frappe.db.sql(
        "SELECT name FROM `tabRole` WHERE LOWER(name) LIKE '%course%' "
        "OR LOWER(name) LIKE '%instructor%' OR LOWER(name) LIKE '%lms%' "
        "OR LOWER(name) LIKE '%creator%'",
        as_dict=True,
    )
    print("Papéis LMS disponíveis:", [r.name for r in available])

    # Papéis a atribuir ao professor
    instructor_roles = [r.name for r in available]

    # Garante que é System User para ter acesso ao Desk (gerenciar cursos)
    frappe.db.set_value("User", EMAIL, "user_type", "System User")

    user = frappe.get_doc("User", EMAIL)
    existing = {r.role for r in user.roles}

    added = []
    for role in instructor_roles:
        if role not in existing:
            user.append("roles", {"role": role})
            added.append(role)

    # Papel mínimo para acesso ao Desk
    for role in ("Desk User",):
        if role not in existing and frappe.db.exists("Role", role):
            user.append("roles", {"role": role})
            added.append(role)

    user.save(ignore_permissions=True)
    frappe.db.commit()

    print(f"  ✓ {EMAIL} → System User")
    print(f"  ✓ Papéis adicionados: {added}")
    print(f"\nAlmir pode gerenciar cursos em:")
    print(f"  https://app.vediums.com/app/lms-course")
    print(f"  https://app.vediums.com/lms/courses")
