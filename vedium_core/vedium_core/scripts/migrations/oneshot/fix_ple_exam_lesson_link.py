# -*- coding: utf-8 -*-
"""
Vedium — Corrige a prova final do PLE: prende cada LMS Quiz de prova a uma
lição real (mesmo padrão do quiz nativo de demonstração do LMS, que também
usa uma lição dedicada "Quiz Time" pra hospedar o quiz).

Bug encontrado em produção (2026-07-07): seed_ple_*_activities.run criou
os 3 quizzes de "Prova Final" com lesson=None -- o card do curso mostrava
"0 lição" e a prova não aparecia em lugar nenhum pro aluno, porque o
front-end do LMS só exibe um quiz dentro do fluxo de uma lição.

Cria, por curso (idempotente):
    - 1 capítulo "Avaliação Final" (se não existir)
    - 1 lição dentro dele, hospedando a prova
    - religa o LMS Quiz da prova final a essa lição

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.fix_ple_exam_lesson_link.run
"""
import json

import frappe

COURSES = [
    ("portugues-para-estrangeiros-basico", "Prova Final — Português Básico (PLE)"),
    ("portugues-para-estrangeiros-intermediario", "Prova Final — Português Intermediário (PLE)"),
    ("portugues-para-estrangeiros-avancado", "Prova Final — Português Avançado (PLE)"),
]

FINAL_CHAPTER_TITLE = "Avaliação Final"
FINAL_LESSON_TITLE = "Prova Final — faça a avaliação do nível"


def _lesson_content(text):
    return json.dumps({
        "blocks": [{"type": "paragraph", "data": {"text": text}}],
        "version": "2.27.0",
        "time": 1000000000,
    })


def run():
    for course, quiz_title in COURSES:
        print(f"\n=== {course} ===")
        if not frappe.db.exists("LMS Course", course):
            print("  curso não existe, pulando.")
            continue

        quiz_name = frappe.db.get_value("LMS Quiz", {"title": quiz_title})
        if not quiz_name:
            print(f"  AVISO: quiz '{quiz_title}' não encontrado -- rode o seed de atividades primeiro.")
            continue

        quiz = frappe.get_doc("LMS Quiz", quiz_name)
        if quiz.lesson:
            print(f"  quiz já está vinculado à lição '{quiz.lesson}', nada a fazer.")
            continue

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
            print(f"  ✓ capítulo '{FINAL_CHAPTER_TITLE}' criado.")
        else:
            print(f"  — capítulo '{FINAL_CHAPTER_TITLE}' já existia.")

        lesson_name = frappe.db.get_value(
            "Course Lesson", {"chapter": chapter_name, "title": FINAL_LESSON_TITLE}
        )
        if not lesson_name:
            lesson = frappe.get_doc({
                "doctype": "Course Lesson",
                "title": FINAL_LESSON_TITLE,
                "chapter": chapter_name,
                "course": course,
                "content": _lesson_content(
                    "Chegou a hora da avaliação final deste nível! Você tem até 3 "
                    "tentativas, precisa acertar 70% das 40 questões sorteadas, e a "
                    "ordem e parte das questões mudam a cada tentativa. Boa prova!"
                ),
            })
            lesson.insert(ignore_permissions=True)
            lesson_name = lesson.name
            print(f"  ✓ lição '{FINAL_LESSON_TITLE}' criada ({lesson_name}).")
        else:
            print(f"  — lição '{FINAL_LESSON_TITLE}' já existia ({lesson_name}).")

        quiz.lesson = lesson_name
        quiz.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"  ✓ quiz '{quiz_title}' religado à lição {lesson_name}.")

    print("\n✓ Concluído. As 3 provas finais agora aparecem no fluxo normal do curso.")
