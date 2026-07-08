# -*- coding: utf-8 -*-
"""Make PLE quizzes visible inside LMS lessons.

The PLE quizzes existed in LMS Quiz, but the lesson pages only render the
questions/options when Course Lesson.quiz_id is set and Course Lesson.content
is empty, allowing the frontend to render the body plus the quiz component.

This creates one visible "Exercicios de Fixacao" lesson at the end of each
module, embeds the module quiz there, and embeds the final exam quiz in the
existing "Avaliacao Final" lesson.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.fix_ple_quiz_lesson_content.run
"""

import frappe

COURSES = [
    {
        "course": "portugues-para-estrangeiros-basico",
        "final_quiz": "Prova Final — Português Básico (PLE)",
        "modules": [
            "Módulo 1 — Primeiros Contatos e Informações Pessoais",
            "Módulo 2 — O Dia a Dia e o Ambiente",
            "Módulo 3 — Interações e Cultura Brasileira",
        ],
    },
    {
        "course": "portugues-para-estrangeiros-intermediario",
        "final_quiz": "Prova Final — Português Intermediário (PLE)",
        "modules": [
            "Módulo 1 — Narrativa e Experiências Passadas",
            "Módulo 2 — Saúde, Trabalho e Vida Social",
            "Módulo 3 — Cultura, Opinião e Variação Linguística",
        ],
    },
    {
        "course": "portugues-para-estrangeiros-avancado",
        "final_quiz": "Prova Final — Português Avançado (PLE)",
        "modules": [
            "Módulo 1 — Opinião, Hipótese e Argumentação",
            "Módulo 2 — Cultura, Sociedade e Mídia",
            "Módulo 3 — Contextos Profissionais e Acadêmicos",
        ],
    },
]

FINAL_CHAPTER_TITLE = "Avaliação Final"
FINAL_LESSON_TITLE = "Prova Final — faça a avaliação do nível"


def run():
    schema = _get_lms_schema()

    for data in COURSES:
        course = data["course"]
        print(f"\n=== {course} ===")
        if not frappe.db.exists("LMS Course", course):
            print("  curso não existe, pulando.")
            continue

        _sync_chapter_order(course, data["modules"])

        for module_number, chapter_title in enumerate(data["modules"], start=1):
            _ensure_fixation_lesson(course, chapter_title, module_number)

        _ensure_final_exam_lesson(course, data["final_quiz"])
        _sync_navigation(course, schema)

    frappe.db.commit()
    print("\nConcluído. Quizzes PLE agora aparecem como lições com perguntas e opções.")


def _ensure_fixation_lesson(course, chapter_title, module_number):
    chapter_name = frappe.db.get_value("Course Chapter", {"course": course, "title": chapter_title})
    if not chapter_name:
        print(f"  AVISO: capítulo '{chapter_title}' não encontrado.")
        return

    quiz_title = f"Exercícios de Fixação — {chapter_title}"
    quiz_name = frappe.db.get_value("LMS Quiz", {"course": course, "title": quiz_title})
    if not quiz_name:
        print(f"  AVISO: quiz '{quiz_title}' não encontrado.")
        return

    lesson_title = f"Quiz — Exercícios de Fixação — Módulo {module_number}"
    old_lesson_title = f"Exercícios de Fixação — Módulo {module_number}"
    lesson_name = frappe.db.get_value(
        "Course Lesson", {"chapter": chapter_name, "title": lesson_title}, "name"
    ) or frappe.db.get_value(
        "Course Lesson", {"chapter": chapter_name, "title": old_lesson_title}, "name"
    )
    if not lesson_name:
        lesson = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": lesson_title,
            "chapter": chapter_name,
            "course": course,
            "content": "",
            "body": _quiz_body(
                "Responda às 10 perguntas de múltipla escolha deste módulo. "
                "Cada pergunta tem 4 alternativas e apenas 1 resposta correta.",
            ),
            "quiz_id": quiz_name,
        })
        lesson.insert(ignore_permissions=True)
        lesson_name = lesson.name
        print(f"  ✓ criada lição '{lesson_title}'")
    else:
        lesson = frappe.get_doc("Course Lesson", lesson_name)
        lesson.title = lesson_title
        lesson.content = ""
        lesson.body = _quiz_body(
            "Responda às 10 perguntas de múltipla escolha deste módulo. "
            "Cada pergunta tem 4 alternativas e apenas 1 resposta correta.",
        )
        lesson.quiz_id = quiz_name
        lesson.save(ignore_permissions=True)
        print(f"  ✓ atualizada lição '{lesson_title}'")

    _move_lesson_to_start(chapter_name, lesson_name)
    frappe.db.set_value("LMS Quiz", quiz_name, {"course": course, "lesson": lesson_name})


def _ensure_final_exam_lesson(course, quiz_title):
    quiz_name = frappe.db.get_value("LMS Quiz", {"course": course, "title": quiz_title})
    if not quiz_name:
        print(f"  AVISO: quiz final '{quiz_title}' não encontrado.")
        return

    chapter_name = frappe.db.get_value(
        "Course Chapter", {"course": course, "title": FINAL_CHAPTER_TITLE}
    )
    if not chapter_name:
        chapter = frappe.get_doc({
            "doctype": "Course Chapter",
            "title": FINAL_CHAPTER_TITLE,
            "course": course,
        })
        chapter.insert(ignore_permissions=True)
        chapter_name = chapter.name
        print(f"  ✓ criado capítulo '{FINAL_CHAPTER_TITLE}'")

    lesson_name = frappe.db.get_value(
        "Course Lesson", {"chapter": chapter_name, "title": FINAL_LESSON_TITLE}, "name"
    )
    if not lesson_name:
        lesson = frappe.get_doc({
            "doctype": "Course Lesson",
            "title": FINAL_LESSON_TITLE,
            "chapter": chapter_name,
            "course": course,
            "content": "",
            "body": _final_exam_body(),
            "quiz_id": quiz_name,
        })
        lesson.insert(ignore_permissions=True)
        lesson_name = lesson.name
        print(f"  ✓ criada lição '{FINAL_LESSON_TITLE}'")
    else:
        lesson = frappe.get_doc("Course Lesson", lesson_name)
        lesson.content = ""
        lesson.body = _final_exam_body()
        lesson.quiz_id = quiz_name
        lesson.save(ignore_permissions=True)
        print(f"  ✓ atualizada lição '{FINAL_LESSON_TITLE}'")

    frappe.db.set_value("Course Lesson", lesson_name, "idx", 1)
    frappe.db.set_value("LMS Quiz", quiz_name, {"course": course, "lesson": lesson_name})


def _quiz_body(text):
    return text


def _final_exam_body():
    return _quiz_body(
        "Prova final do nível: são 40 questões por tentativa, nota mínima de "
        "70% e até 3 tentativas. A ordem muda e parte das perguntas pode mudar "
        "a cada tentativa.",
    )


def _sync_chapter_order(course, module_titles):
    for idx, chapter_title in enumerate(module_titles, start=1):
        chapter_name = frappe.db.get_value(
            "Course Chapter", {"course": course, "title": chapter_title}
        )
        if chapter_name:
            frappe.db.set_value("Course Chapter", chapter_name, "idx", idx)

    final_chapter = frappe.db.get_value(
        "Course Chapter", {"course": course, "title": FINAL_CHAPTER_TITLE}
    )
    if final_chapter:
        frappe.db.set_value("Course Chapter", final_chapter, "idx", len(module_titles) + 1)


def _move_lesson_to_start(chapter_name, lesson_name):
    rows = frappe.get_all(
        "Course Lesson",
        filters={"chapter": chapter_name},
        fields=["name"],
        order_by="idx asc, creation asc, name asc",
    )
    ordered = [row.name for row in rows if row.name != lesson_name]
    ordered.insert(0, lesson_name)
    for idx, name in enumerate(ordered, start=1):
        frappe.db.set_value("Course Lesson", name, "idx", idx)


def _get_lms_schema():
    course_meta = frappe.get_meta("LMS Course")
    chapters_field = course_meta.get_field("chapters")
    if not chapters_field or chapters_field.fieldtype != "Table":
        frappe.throw("LMS Course.chapters table field was not found.")

    chapter_meta = frappe.get_meta("Course Chapter")
    lessons_field = chapter_meta.get_field("lessons")
    if not lessons_field or lessons_field.fieldtype != "Table":
        frappe.throw("Course Chapter.lessons table field was not found.")

    if not frappe.get_meta("LMS Course").get_field("lessons"):
        frappe.throw("LMS Course.lessons counter field was not found.")

    return {
        "chapter_reference_doctype": chapters_field.options,
        "lesson_reference_doctype": lessons_field.options,
    }


def _sync_navigation(course, schema):
    chapters = frappe.get_all(
        "Course Chapter",
        filters={"course": course},
        fields=["name"],
        order_by="idx asc, creation asc, name asc",
    )
    _sync_child_links(
        schema["chapter_reference_doctype"],
        "LMS Course",
        course,
        "chapters",
        "chapter",
        [chapter.name for chapter in chapters],
    )

    for chapter in chapters:
        lessons = frappe.get_all(
            "Course Lesson",
            filters={"chapter": chapter.name},
            fields=["name"],
            order_by="idx asc, creation asc, name asc",
        )
        _sync_child_links(
            schema["lesson_reference_doctype"],
            "Course Chapter",
            chapter.name,
            "lessons",
            "lesson",
            [lesson.name for lesson in lessons],
        )

    chapter_names = [chapter.name for chapter in chapters]
    lesson_count = (
        frappe.db.count(schema["lesson_reference_doctype"], {"parent": ("in", chapter_names)})
        if chapter_names
        else 0
    )
    frappe.db.set_value("LMS Course", course, "lessons", lesson_count)
    print(f"  ✓ navegação sincronizada ({lesson_count} lições)")


def _sync_child_links(child_doctype, parent_doctype, parent, parentfield, link_field, targets):
    current_rows = frappe.get_all(
        child_doctype,
        filters={"parent": parent},
        fields=["name", link_field],
        order_by="idx asc, creation asc, name asc",
    )
    current = [row.get(link_field) for row in current_rows]
    if current == targets:
        return

    for row in current_rows:
        frappe.delete_doc(child_doctype, row.name, ignore_permissions=True, force=True)

    for idx, target in enumerate(targets, start=1):
        frappe.get_doc({
            "doctype": child_doctype,
            "parent": parent,
            "parenttype": parent_doctype,
            "parentfield": parentfield,
            "idx": idx,
            link_field: target,
        }).insert(ignore_permissions=True)
