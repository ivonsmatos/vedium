# -*- coding: utf-8 -*-
"""Ensure enrolled LMS users can read and submit LMS quizzes.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.ensure_lms_student_role_for_enrollments.run
"""

import frappe


def run():
    members = frappe.get_all(
        "LMS Enrollment",
        filters={"member": ["not in", ["", "Guest"]]},
        pluck="member",
        distinct=True,
    )

    updated = 0
    for member in members:
        if not frappe.db.exists("User", member):
            continue

        user = frappe.get_doc("User", member)
        if any(row.role == "LMS Student" for row in user.roles):
            continue

        user.append("roles", {"role": "LMS Student"})
        user.save(ignore_permissions=True)
        updated += 1
        print(f"  ✓ LMS Student adicionado para {member}")

    frappe.db.commit()
    print(f"Concluído. Usuários atualizados: {updated}")
