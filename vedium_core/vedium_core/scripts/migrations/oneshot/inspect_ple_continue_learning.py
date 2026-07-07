# -*- coding: utf-8 -*-
"""Diagnostico temporario, SO LEITURA: por que o card do curso mostra
"0 lição" e o botao "Continue Learning" nao navega pra lugar nenhum.

Confere:
    - campos do LMS Course relacionados a contagem/publicacao
    - campos do Course Chapter (algum flag de publicado/oculto?)
    - a matricula real do usuario no curso (current_lesson, progress)

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_ple_continue_learning.run
"""
import frappe

COURSE = "portugues-para-estrangeiros-basico"


def run():
    print("=== LMS Course (campos completos) ===")
    meta = frappe.get_meta("LMS Course")
    for f in meta.fields:
        print(f"  {f.fieldname} ({f.fieldtype})")
    course_doc = frappe.db.get_value("LMS Course", COURSE, "*", as_dict=True)
    print("\n  valores reais:")
    for k, v in course_doc.items():
        print(f"    {k}: {v!r}")

    print("\n=== Course Chapter (campos completos) ===")
    meta_ch = frappe.get_meta("Course Chapter")
    for f in meta_ch.fields:
        print(f"  {f.fieldname} ({f.fieldtype})")
    chapters = frappe.get_all(
        "Course Chapter", filters={"course": COURSE}, fields=["*"], order_by="idx"
    )
    print(f"\n  {len(chapters)} capitulos, exemplo do primeiro:")
    if chapters:
        for k, v in chapters[0].items():
            print(f"    {k}: {v!r}")

    print("\n=== Matriculas no curso ===")
    enrollments = frappe.get_all(
        "LMS Enrollment", filters={"course": COURSE}, fields=["*"]
    )
    for e in enrollments:
        print(f"  member={e.member} progress={e.progress} current_lesson={e.current_lesson!r} "
              f"purchased_certificate={e.purchased_certificate} certificate={e.certificate!r}")
