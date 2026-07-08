# -*- coding: utf-8 -*-
"""Fix PLE course navigation by syncing LMS child reference rows.

Production bug found on 2026-07-07: the PLE setup created Course Lesson
documents with Course Lesson.chapter set, but did not populate the native
child tables used by LMS navigation:

    - LMS Course.chapters -> Chapter Reference
    - Course Chapter.lessons -> Lesson Reference

The native LMS uses those child rows for curriculum navigation and lesson
counts.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.fix_ple_chapter_lesson_references.run
"""

import frappe

PLE_COURSES = [
    "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado",
]


def run():
    schema = _get_lms_schema()

    for course in PLE_COURSES:
        print(f"\n=== {course} ===")
        if not frappe.db.exists("LMS Course", course):
            print("  course does not exist, skipping.")
            continue

        chapters = _chapters_for_course(course)
        chapter_names = [chapter.name for chapter in chapters]
        chapters_changed = _sync_child_links(
            child_doctype=schema["chapter_reference_doctype"],
            parent_doctype="LMS Course",
            parent=course,
            parentfield="chapters",
            link_field="chapter",
            target_names=chapter_names,
        )
        chapters_status = "updated" if chapters_changed else "already ok"
        print(f"  {chapters_status}: LMS Course.chapters ({len(chapter_names)} chapter refs)")

        if not chapters:
            print("  no chapters found.")

        for chapter in chapters:
            lesson_names = _lesson_names_for_chapter(chapter.name)
            changed = _sync_child_links(
                child_doctype=schema["lesson_reference_doctype"],
                parent_doctype="Course Chapter",
                parent=chapter.name,
                parentfield="lessons",
                link_field="lesson",
                target_names=lesson_names,
            )
            status = "updated" if changed else "already ok"
            print(f"  {status}: {chapter.title} ({len(lesson_names)} lesson refs)")

        _sync_course_lesson_count(
            course,
            schema["chapter_reference_doctype"],
            schema["lesson_reference_doctype"],
        )

    frappe.db.commit()
    print("\nDone. PLE chapter and lesson references are synced.")


def _get_lms_schema():
    course_meta = frappe.get_meta("LMS Course")
    chapters_field = course_meta.get_field("chapters")
    if not chapters_field or chapters_field.fieldtype != "Table":
        frappe.throw("LMS Course.chapters table field was not found.")

    chapter_reference_doctype = chapters_field.options
    chapter_reference_meta = frappe.get_meta(chapter_reference_doctype)
    if not chapter_reference_meta.get_field("chapter"):
        frappe.throw(f"{chapter_reference_doctype}.chapter field was not found.")

    chapter_meta = frappe.get_meta("Course Chapter")
    lessons_field = chapter_meta.get_field("lessons")
    if not lessons_field or lessons_field.fieldtype != "Table":
        frappe.throw("Course Chapter.lessons table field was not found.")

    lesson_reference_doctype = lessons_field.options
    lesson_reference_meta = frappe.get_meta(lesson_reference_doctype)
    if not lesson_reference_meta.get_field("lesson"):
        frappe.throw(f"{lesson_reference_doctype}.lesson field was not found.")

    if not frappe.get_meta("LMS Course").get_field("lessons"):
        frappe.throw("LMS Course.lessons counter field was not found.")

    return {
        "chapter_reference_doctype": chapter_reference_doctype,
        "lesson_reference_doctype": lesson_reference_doctype,
    }


def _chapters_for_course(course):
    return frappe.get_all(
        "Course Chapter",
        filters={"course": course},
        fields=["name", "title", "idx"],
        order_by="idx asc, creation asc, name asc",
    )


def _lesson_names_for_chapter(chapter_name):
    lessons = frappe.get_all(
        "Course Lesson",
        filters={"chapter": chapter_name},
        fields=["name"],
        order_by="idx asc, creation asc, name asc",
    )
    return [lesson.name for lesson in lessons]


def _sync_child_links(child_doctype, parent_doctype, parent, parentfield, link_field, target_names):
    current_rows = frappe.get_all(
        child_doctype,
        filters={"parent": parent},
        fields=["name", link_field],
        order_by="idx asc, creation asc, name asc",
    )
    current = [row.get(link_field) for row in current_rows]

    if current == target_names:
        return False

    for row in current_rows:
        frappe.delete_doc(child_doctype, row.name, ignore_permissions=True, force=True)

    for idx, target_name in enumerate(target_names, start=1):
        frappe.get_doc({
            "doctype": child_doctype,
            "parent": parent,
            "parenttype": parent_doctype,
            "parentfield": parentfield,
            "idx": idx,
            link_field: target_name,
        }).insert(ignore_permissions=True)
    return True


def _sync_course_lesson_count(course, chapter_reference_doctype, lesson_reference_doctype):
    lesson_count = _native_lesson_count(course, chapter_reference_doctype, lesson_reference_doctype)
    current = frappe.db.get_value("LMS Course", course, "lessons")
    try:
        current_count = int(current or 0)
    except (TypeError, ValueError):
        current_count = None

    if current_count == lesson_count:
        print(f"  LMS Course.lessons already ok: {lesson_count}")
        return

    frappe.db.set_value("LMS Course", course, "lessons", lesson_count)
    print(f"  LMS Course.lessons updated: {current!r} -> {lesson_count}")


def _native_lesson_count(course, chapter_reference_doctype, lesson_reference_doctype):
    chapter_references = frappe.get_all(chapter_reference_doctype, {"parent": course}, pluck="chapter")
    if not chapter_references:
        return 0
    return frappe.db.count(lesson_reference_doctype, {"parent": ("in", chapter_references)})
