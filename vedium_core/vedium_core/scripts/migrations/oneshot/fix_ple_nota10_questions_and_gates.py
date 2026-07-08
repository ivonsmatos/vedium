# -*- coding: utf-8 -*-
"""Replace PLE quiz banks with Nota 10 based questions and enforce settings.

All module activities and final exams are grounded in Nota 10 — Português do
Brasil, level A1/A2, using the course/unit mapping already present in the PLE
seeds:

    - Básico: units 0-8
    - Intermediário: units 9-14
    - Avançado: review/deepening of units 9-14, because the provided book is
      A1/A2 and does not contain external advanced grammar topics.

Run:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.fix_ple_nota10_questions_and_gates.run
"""

import frappe

from vedium_core.scripts.migrations.oneshot import (
    seed_ple_avancado_activities as avancado,
    seed_ple_basico_activities as basico,
    seed_ple_intermediario_activities as intermediario,
)


COURSES = [
    {
        "module": basico,
        "course": basico.COURSE,
        "final_quiz": "Prova Final — Português Básico (PLE)",
    },
    {
        "module": intermediario,
        "course": intermediario.COURSE,
        "final_quiz": "Prova Final — Português Intermediário (PLE)",
    },
    {
        "module": avancado,
        "course": avancado.COURSE,
        "final_quiz": "Prova Final — Português Avançado (PLE)",
    },
]


def run():
    for data in COURSES:
        course = data["course"]
        module = data["module"]
        print(f"\n=== {course} ===")
        if not frappe.db.exists("LMS Course", course):
            print("  curso não existe, pulando.")
            continue

        _replace_quiz_questions(
            course=course,
            title=data["final_quiz"],
            questions=module.EXAM_QUESTIONS,
            max_attempts=3,
            passing_percentage=70,
            shuffle_questions=True,
            limit_questions_to=40,
            total_marks=40,
        )

        for chapter_title, questions in module.MODULE_FIXATION.items():
            _replace_quiz_questions(
                course=course,
                title=f"Exercícios de Fixação — {chapter_title}",
                questions=questions,
                max_attempts=0,
                passing_percentage=70,
                shuffle_questions=True,
                limit_questions_to=0,
                total_marks=len(questions),
            )

    frappe.db.commit()
    print("\nConcluído. Bancos PLE atualizados com questões baseadas no Nota 10.")


def _replace_quiz_questions(course, title, questions, *, max_attempts, passing_percentage,
                            shuffle_questions, limit_questions_to, total_marks):
    quiz_name = frappe.db.get_value("LMS Quiz", {"course": course, "title": title})
    if not quiz_name:
        print(f"  AVISO: quiz '{title}' não encontrado.")
        return

    _validate_questions(title, questions)

    quiz = frappe.get_doc("LMS Quiz", quiz_name)
    quiz.max_attempts = max_attempts
    quiz.passing_percentage = passing_percentage
    quiz.shuffle_questions = 1 if shuffle_questions else 0
    quiz.limit_questions_to = limit_questions_to
    quiz.total_marks = total_marks

    quiz.set("questions", [])
    for question_text, options, correct_idx in questions:
        question_name = _upsert_question(question_text, options, correct_idx)
        quiz.append("questions", {"question": question_name, "marks": 1})

    quiz.save(ignore_permissions=True)
    print(f"  ✓ {title}: {len(questions)} questões, múltipla escolha 4 opções.")


def _validate_questions(title, questions):
    if len(questions) < 10:
        frappe.throw(f"Quiz '{title}' precisa ter pelo menos 10 questões.")

    for question_text, options, correct_idx in questions:
        if len(options) != 4:
            frappe.throw(f"Pergunta precisa ter exatamente 4 opções: {question_text}")
        if correct_idx not in range(4):
            frappe.throw(f"Resposta correta inválida em: {question_text}")


def _upsert_question(question_text, options, correct_idx):
    existing = frappe.db.get_value("LMS Question", {"question": question_text})
    if existing:
        doc = frappe.get_doc("LMS Question", existing)
    else:
        doc = frappe.get_doc({
            "doctype": "LMS Question",
            "question": question_text,
        })

    doc.type = "Choices"
    doc.multiple = 0
    for i, option_text in enumerate(options, start=1):
        doc.set(f"option_{i}", option_text)
        doc.set(f"is_correct_{i}", 1 if i - 1 == correct_idx else 0)

    if doc.is_new():
        doc.insert(ignore_permissions=True)
    else:
        doc.save(ignore_permissions=True)
    return doc.name
