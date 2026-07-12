# -*- coding: utf-8 -*-
"""Diagnóstico read-only pra planejar canais/grupos do Raven.

Antes de criar canais por idioma "no chute", precisamos saber:
  1. Quais cursos/idiomas a Vedium realmente oferece (LMS Course).
  2. Quem são os professores reais de cada curso (Course Instructor -> User).
  3. Quem já tem role de coordenação/professor (Vedium Coordenacao
     Pedagogica / Vedium Professor) -- candidatos a entrar nos canais.
  4. Estado atual do workspace/canais Raven (o que já existe, pra não
     duplicar).

Não cria nem altera nada.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_raven_setup.run
"""

import frappe


def run():
    print("=== Cursos publicados (LMS Course) ===")
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "title"],
        order_by="title",
    )
    for c in courses:
        instructors = frappe.get_all(
            "Course Instructor", filters={"parent": c.name}, pluck="instructor"
        )
        print(f"  {c.name!r} | {c.title!r} | professores: {instructors}")

    print("\n=== Usuarios com role 'Vedium Professor' ===")
    profs = frappe.get_all(
        "Has Role", filters={"role": "Vedium Professor", "parenttype": "User"}, pluck="parent"
    )
    for u in profs:
        full_name = frappe.db.get_value("User", u, "full_name")
        print(f"  {u} | {full_name}")

    print("\n=== Usuarios com role 'Vedium Coordenacao Pedagogica' ===")
    coords = frappe.get_all(
        "Has Role",
        filters={"role": "Vedium Coordenacao Pedagogica", "parenttype": "User"},
        pluck="parent",
    )
    for u in coords:
        full_name = frappe.db.get_value("User", u, "full_name")
        print(f"  {u} | {full_name}")

    print("\n=== Usuarios com role 'Raven User' ===")
    raven_users = frappe.get_all(
        "Has Role", filters={"role": "Raven User", "parenttype": "User"}, pluck="parent"
    )
    for u in raven_users:
        full_name = frappe.db.get_value("User", u, "full_name")
        print(f"  {u} | {full_name}")

    print("\n=== Raven Workspace(s) ===")
    workspaces = frappe.get_all("Raven Workspace", fields=["name", "type", "logo"])
    for w in workspaces:
        print(f"  {w.name!r} | tipo={w.type} | logo={w.logo!r}")

    print("\n=== Raven Channel(s) existentes ===")
    channels = frappe.get_all(
        "Raven Channel",
        fields=["name", "channel_name", "type", "workspace", "linked_doctype", "linked_document", "is_archived"],
    )
    if not channels:
        print("  (nenhum)")
    for ch in channels:
        print(
            f"  {ch.name!r} | {ch.channel_name!r} | tipo={ch.type} | workspace={ch.workspace} "
            f"| link={ch.linked_doctype}:{ch.linked_document} | arquivado={ch.is_archived}"
        )

    print("\n=== Campos do Raven Workspace (pra saber o nome certo do campo de logo) ===")
    meta = frappe.get_meta("Raven Workspace")
    for f in meta.fields:
        if "logo" in f.fieldname.lower() or "icon" in f.fieldname.lower() or "image" in f.fieldname.lower():
            print(f"  fieldname={f.fieldname!r} | fieldtype={f.fieldtype!r} | label={f.label!r}")
