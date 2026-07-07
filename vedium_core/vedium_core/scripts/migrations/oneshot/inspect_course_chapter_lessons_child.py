# -*- coding: utf-8 -*-
"""Diagnostico temporario, SO LEITURA: confere o doctype filho usado pelo
campo Course Chapter.lessons (Table), pra entender como popular a lista
ordenada de licoes de cada capitulo do PLE.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_course_chapter_lessons_child.run
"""
import frappe


def run():
    meta = frappe.get_meta("Course Chapter")
    lessons_field = meta.get_field("lessons")
    child_doctype = lessons_field.options
    print(f"Course Chapter.lessons -> child doctype: {child_doctype!r}")

    child_meta = frappe.get_meta(child_doctype)
    print(f"\n=== {child_doctype} (campos) ===")
    for f in child_meta.fields:
        extra = []
        if f.fieldtype == "Link":
            extra.append(f"-> {f.options}")
        print(f"  {f.fieldname} ({f.fieldtype}) {' '.join(extra)}")

    # Um capitulo com licoes (de outro curso ja funcional) como referencia,
    # se existir algum com esse campo preenchido.
    sample = frappe.get_all("Course Chapter", filters={}, fields=["name"], limit=200)
    found = False
    for ch in sample:
        doc = frappe.get_doc("Course Chapter", ch.name)
        if doc.lessons:
            print(f"\nExemplo de capitulo COM child table preenchida: {ch.name}")
            for row in doc.lessons:
                print(f"  {row.as_dict()}")
            found = True
            break
    if not found:
        print("\nNenhum capitulo no sistema tem essa child table preenchida (nem os PLE, nem outros).")

    # Curso de demonstracao nativo do LMS (sabemos que funciona/navega) --
    # confere se ELE depende dessa child table ou nao.
    demo_course = "a-guide-to-frappe-learning"
    if frappe.db.exists("LMS Course", demo_course):
        print(f"\n=== Curso de demonstracao '{demo_course}' ===")
        demo_chapters = frappe.get_all(
            "Course Chapter", filters={"course": demo_course}, fields=["name", "title"]
        )
        for ch in demo_chapters:
            doc = frappe.get_doc("Course Chapter", ch.name)
            n_lessons_linked = frappe.db.count("Course Lesson", {"chapter": ch.name})
            print(f"  {ch.title}: child table tem {len(doc.lessons)} linha(s), "
                  f"Course Lesson vinculadas por campo chapter: {n_lessons_linked}")
            for row in doc.lessons:
                print(f"    row: {row.as_dict()}")
