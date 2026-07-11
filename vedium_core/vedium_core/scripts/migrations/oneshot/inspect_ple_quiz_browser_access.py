# -*- coding: utf-8 -*-
"""Read-only check that mimics the browser quiz fetch for an enrolled user.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_ple_quiz_browser_access.run
"""

import frappe
from frappe.client import get


def run():
    course = "portugues-para-estrangeiros-basico"
    lesson_indexes = [(1, 8), (2, 8), (3, 7)]

    members = []
    enrolled = frappe.db.get_value("LMS Enrollment", {"course": course}, "member")
    if enrolled:
        members.append(("enrolled", enrolled))

    instructors = frappe.get_all(
        "Course Instructor",
        filters={"parent": course},
        fields=["instructor"],
    )
    for instructor in instructors:
        if instructor.instructor:
            members.append(("instructor", instructor.instructor))

    if not members:
        print("Nenhuma matrícula encontrada para o curso básico.")
        return

    for label, member in members:
        frappe.set_user(member)

        print(f"\nrole_case={label} user={member}")

        for lesson_index in lesson_indexes:
            lesson = frappe.get_attr("lms.lms.utils.get_lesson")(
                course, lesson_index[0], lesson_index[1]
            )
            quiz_name = lesson.get("quiz_id")
            print(
                f"lesson_index={lesson_index[0]}.{lesson_index[1]} "
                f"lesson={lesson.get('name')} title={lesson.get('title')}"
            )
            print(f"quiz_id={quiz_name}")

            quiz = get("LMS Quiz", quiz_name)
            print(f"quiz_title={quiz.get('title')}")
            print(f"questions_returned={len(quiz.get('questions') or [])}")

    frappe.set_user("Administrator")
