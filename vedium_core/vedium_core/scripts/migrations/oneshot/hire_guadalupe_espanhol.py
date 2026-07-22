# -*- coding: utf-8 -*-
"""Contrata Guadalupe Samayoa de Trindade como professora de Espanhol.

Ações:
  1. Cria/atualiza o User (convite por e-mail) com a role "Vedium
     Professor" -- isso já dispara sozinho a entrada automática no Raven
     (hook em User.on_update, communication.sync_new_professor).
  2. Se existir uma Candidatura com o mesmo e-mail, marca como Aprovada e
     position="Espanhol" (mesmo efeito do botão "Aprovar como Professor").
  3. Troca o instrutor placeholder ("Administrator") pela professora real
     nos 3 cursos de Espanhol já publicados (espanhol-basico/
     -intermediario/-avancado), pra ela aparecer na lista de professores
     igual aos demais (Kayode/Busayo/Almirseller nos seus cursos).

NÃO guarda CPF/RNM/endereço -- são dados sensíveis de contrato/RH sem
campo apropriado no User; se quiser um registro formal de RH (ex.
Employee do Frappe HR) com esses dados, é uma tarefa separada e deliberada
(LGPD).

Idempotente.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.hire_guadalupe_espanhol.run
"""

import frappe

EMAIL = "lupitasamayoa3@gmail.com"
FULL_NAME = "Guadalupe Samayoa de Trindade"
PHONE = "+55 11 94446-5427"
ROLE = "Vedium Professor"
FUNCAO = "Espanhol"
COURSES = ("espanhol-basico", "espanhol-intermediario", "espanhol-avancado")


def run():
    _ensure_user()
    _approve_matching_candidatura()
    _assign_as_course_instructor()
    frappe.db.commit()


def _ensure_user():
    user = frappe.db.exists("User", EMAIL)
    if not user:
        user_doc = frappe.get_doc({
            "doctype": "User",
            "email": EMAIL,
            "first_name": "Guadalupe",
            "full_name": FULL_NAME,
            "phone": PHONE,
            "send_welcome_email": 1,
            "user_type": "System User",
        })
        user_doc.append("roles", {"role": ROLE})
        user_doc.insert(ignore_permissions=True)
        print(f"User criado: {user_doc.name} (convite enviado por e-mail)")
        return

    user_doc = frappe.get_doc("User", user)
    changed = False
    if ROLE not in {r.role for r in user_doc.roles}:
        user_doc.append("roles", {"role": ROLE})
        changed = True
    if not user_doc.phone:
        user_doc.phone = PHONE
        changed = True
    if changed:
        user_doc.save(ignore_permissions=True)
    print(f"User já existia: {user} (role garantida)")


def _approve_matching_candidatura():
    if not frappe.db.exists("DocType", "Candidatura"):
        return
    candidatura = frappe.db.get_value("Candidatura", {"email": EMAIL}, "name")
    if not candidatura:
        print("Nenhuma Candidatura encontrada com esse e-mail (contratação direta).")
        return
    doc = frappe.get_doc("Candidatura", candidatura)
    doc.status = "Aprovada"
    doc.position = FUNCAO
    doc.save(ignore_permissions=True)
    print(f"Candidatura {candidatura} marcada como Aprovada ({FUNCAO})")


def _assign_as_course_instructor():
    for course_name in COURSES:
        if not frappe.db.exists("LMS Course", course_name):
            print(f"  [{course_name}] curso não existe, pulei")
            continue

        course = frappe.get_doc("LMS Course", course_name)
        before = [row.instructor for row in course.instructors]

        course.instructors = [row for row in course.instructors if row.instructor != "Administrator"]
        if EMAIL not in {row.instructor for row in course.instructors}:
            course.append("instructors", {"instructor": EMAIL})

        after = [row.instructor for row in course.instructors]
        if before != after:
            course.save(ignore_permissions=True)
            print(f"  [{course_name}] instrutores: {before} -> {after}")
        else:
            print(f"  [{course_name}] já estava correto")
