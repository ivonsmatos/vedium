"""Cadastra Almir Soares da Silva como professor e associa aos cursos PLE.

Idempotente -- seguro rodar de novo mesmo se o usuário já existir (ex.: pra
aplicar a foto adicionada em 2026-08-23, que precisa de uma nova execução se
o script já tinha rodado sem ela).

bench execute vedium_core.scripts.migrations.oneshot.add_professor_almir.run
"""

import frappe

EMAIL = "almir@vediums.com"
FIRST_NAME = "Almir"
LAST_NAME = "Soares da Silva"
FULL_NAME = "Almir Soares da Silva"
# Foto real, autorizada pelo dono em 2026-08-23 (PLE cluster SEO mission,
# item 1.3) -- publicada em vedium_core/public/vedium_assets/images/instructors/.
USER_IMAGE = "/assets/vedium_core/vedium_assets/images/instructors/almir-soares-da-silva.jpg"

PLE_SLUGS = [
    "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado",
]


def run():
    _ensure_user()
    _update_course_instructors()
    frappe.db.commit()
    print(f"\n✅ Professor {FULL_NAME} ({EMAIL}) cadastrado e associado aos cursos PLE.")


def _ensure_user():
    if frappe.db.exists("User", EMAIL):
        print(f"  — Usuário {EMAIL} já existe.")
        # Garante que está habilitado, com foto e papel de instrutor
        frappe.db.set_value("User", EMAIL, "enabled", 1)
        frappe.db.set_value("User", EMAIL, "user_image", USER_IMAGE)
        _ensure_roles(EMAIL)
        return

    user = frappe.get_doc({
        "doctype": "User",
        "email": EMAIL,
        "first_name": FIRST_NAME,
        "last_name": LAST_NAME,
        "full_name": FULL_NAME,
        "user_image": USER_IMAGE,
        "send_welcome_email": 0,
        "enabled": 1,
        "user_type": "Website User",
    })
    user.insert(ignore_permissions=True)
    _ensure_roles(EMAIL)
    print(f"  ✓ Usuário {FULL_NAME} criado ({EMAIL}).")


def _ensure_roles(email):
    user = frappe.get_doc("User", email)
    existing_roles = {r.role for r in user.roles}
    for role in ("LMS Student",):
        if role not in existing_roles and frappe.db.exists("Role", role):
            user.append("roles", {"role": role})
    user.save(ignore_permissions=True)


def _update_course_instructors():
    for slug in PLE_SLUGS:
        if not frappe.db.exists("LMS Course", slug):
            print(f"  ⚠ Curso '{slug}' não encontrado.")
            continue

        course = frappe.get_doc("LMS Course", slug)

        # Remove qualquer instructor placeholder (Administrator)
        course.instructors = [
            row for row in course.instructors
            if row.instructor not in ("Administrator", "admin@example.com")
        ]

        # Adiciona Almir se ainda não estiver
        already = any(r.instructor == EMAIL for r in course.instructors)
        if not already:
            course.append("instructors", {"instructor": EMAIL})

        course.save(ignore_permissions=True)
        print(f"  ✓ {slug}: instrutor → {FULL_NAME}")
