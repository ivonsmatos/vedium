# -*- coding: utf-8 -*-
"""Diagnostico temporario, SO LEITURA: confere o estado real dos 3 cursos
PLE (capitulos, licoes, quizzes e a que licao cada quiz esta vinculado)
depois do seed de atividades. Apagar depois de usar.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_ple_course_state.run
"""
import frappe

COURSES = [
    "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado",
]


def run():
    for course in COURSES:
        print(f"\n=== {course} ===")
        if not frappe.db.exists("LMS Course", course):
            print("  NAO EXISTE")
            continue
        published = frappe.db.get_value("LMS Course", course, "published")
        print(f"  published: {published}")

        chapters = frappe.get_all(
            "Course Chapter", filters={"course": course}, fields=["name", "title", "idx"],
            order_by="idx",
        )
        print(f"  capitulos: {len(chapters)}")
        total_lessons = 0
        for ch in chapters:
            lessons = frappe.get_all(
                "Course Lesson", filters={"chapter": ch.name}, fields=["name", "title", "idx"],
                order_by="idx",
            )
            total_lessons += len(lessons)
            print(f"    {ch.title} ({len(lessons)} licoes)")
            for lesson in lessons:
                print(f"      - {lesson.title}")
        print(f"  total de licoes: {total_lessons}")

        quizzes = frappe.get_all(
            "LMS Quiz", filters={"course": course},
            fields=["name", "title", "lesson", "passing_percentage", "max_attempts",
                    "limit_questions_to", "shuffle_questions"],
        )
        print(f"  quizzes: {len(quizzes)}")
        for q in quizzes:
            n_questions = frappe.db.count("LMS Quiz Question", {"parent": q.name})
            print(f"    - {q.title} | lesson={q.lesson!r} | "
                  f"passing={q.passing_percentage} max_attempts={q.max_attempts} "
                  f"limit_to={q.limit_questions_to} shuffle={q.shuffle_questions} "
                  f"| questoes_no_banco={n_questions}")
