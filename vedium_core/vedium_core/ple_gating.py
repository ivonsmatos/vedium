# -*- coding: utf-8 -*-
"""
Vedium — Gate entre níveis do curso PLE (Português para Estrangeiros)

Regra de negócio (pedido explícito do usuário, 2026-07-07):
    Básico, Intermediário e Avançado são 3 cursos PAGOS separados.
    - Passar na prova final de um nível (>= 70%, até 3 tentativas) NUNCA dá
      acesso pago de graça ao próximo nível -- só remove a barreira
      PEDAGÓGICA.
    - Se o aluno JÁ COMPROU o próximo nível (ex.: comprou os 3 de uma vez),
      passar na prova do nível anterior libera o conteúdo imediatamente.
    - Se o aluno NÃO comprou o próximo nível ainda, ele fica apto/habilitado
      (tem o certificado do nível anterior), mas o conteúdo continua
      bloqueado até ele comprar -- a compra sempre passa pelo checkout
      normal (Stripe), este módulo nunca cria/ativa matrícula sozinho.

Mecânica:
    - LMS Course.custom_prerequisite_course (Link -> LMS Course) marca qual
      curso precisa ter certificado emitido antes deste liberar conteúdo.
      Setado só em Intermediário (-> Básico) e Avançado (-> Intermediário).
    - has_permission (hooks.py) barra leitura de LMS Course/Course Chapter/
      Course Lesson/LMS Quiz quando o pré-requisito existe e o aluno NÃO tem
      LMS Certificate emitido pro curso pré-requisito -- mesmo que ele já
      tenha uma LMS Enrollment paga pro curso atual (o pagamento continua
      valendo, só o conteúdo fica retido até o pré-requisito ser cumprido).
    - Dentro de cada curso PLE, Módulo 2 exige aprovação >= 70% na atividade
      do Módulo 1, Módulo 3 exige aprovação na atividade do Módulo 2, e
      Avaliação Final exige aprovação na atividade do Módulo 3.
"""

import frappe

PLE_COURSES = {
    "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado",
}


def _prerequisite_course(course_name):
    return frappe.db.get_value("LMS Course", course_name, "custom_prerequisite_course")


def has_passed_course(member, course_name):
    """True se o aluno tem um LMS Certificate emitido pra esse curso."""
    return bool(frappe.db.exists("LMS Certificate", {"member": member, "course": course_name}))


def _course_name_for(doctype, docname):
    if doctype == "LMS Course":
        return docname
    if doctype == "Course Chapter":
        return frappe.db.get_value("Course Chapter", docname, "course")
    if doctype == "Course Lesson":
        return frappe.db.get_value("Course Lesson", docname, "course")
    if doctype == "LMS Quiz":
        return frappe.db.get_value("LMS Quiz", docname, "course")
    return None


def _has_enrollment(member, course_name):
    if not member or member == "Guest":
        return False
    return bool(frappe.db.exists("LMS Enrollment", {"member": member, "course": course_name}))


def _is_course_staff(member, course_name):
    if not member or member == "Guest":
        return False

    roles = set(frappe.get_roles(member))
    if roles.intersection({"Course Creator", "Moderator", "Batch Evaluator", "System Manager"}):
        return True

    return bool(frappe.db.exists(
        "Course Instructor",
        {
            "parent": course_name,
            "instructor": member,
        },
    ))


def _chapter_for(doctype, docname):
    if doctype == "Course Chapter":
        return docname
    if doctype == "Course Lesson":
        return frappe.db.get_value("Course Lesson", docname, "chapter")
    if doctype == "LMS Quiz":
        lesson = frappe.db.get_value("LMS Quiz", docname, "lesson")
        if lesson:
            return frappe.db.get_value("Course Lesson", lesson, "chapter")
    return None


def _required_module_activity(course_name, doctype, docname):
    """Return the quiz title that must be passed before reading this doc."""
    if course_name not in PLE_COURSES:
        return None

    chapter_name = _chapter_for(doctype, docname)
    if not chapter_name:
        return None

    chapter_title = frappe.db.get_value("Course Chapter", chapter_name, "title") or ""

    if chapter_title.startswith("Módulo 2"):
        return _activity_title_for_module(course_name, 1)
    if chapter_title.startswith("Módulo 3"):
        return _activity_title_for_module(course_name, 2)
    if chapter_title == "Avaliação Final":
        return _activity_title_for_module(course_name, 3)

    return None


def _activity_title_for_module(course_name, module_number):
    chapters = frappe.get_all(
        "Course Chapter",
        filters={"course": course_name},
        fields=["title"],
        order_by="idx asc, creation asc, name asc",
    )
    for row in chapters:
        title = row.title or ""
        if title.startswith(f"Módulo {module_number}"):
            return f"Exercícios de Fixação — {title}"
    return None


def _has_passed_quiz(member, course_name, quiz_title):
    if not quiz_title:
        return False

    quiz = frappe.db.get_value(
        "LMS Quiz",
        {"course": course_name, "title": quiz_title},
        ["name", "passing_percentage"],
        as_dict=True,
    )
    if not quiz:
        return False

    passing = quiz.passing_percentage or 70
    return bool(frappe.db.exists(
        "LMS Quiz Submission",
        {
            "member": member,
            "quiz": quiz.name,
            "percentage": [">=", passing],
        },
    ))


def has_permission(doc, ptype, user):
    """Hook genérico (hooks.py → has_permission) pra LMS Course/Course
    Chapter/Course Lesson/LMS Quiz. Só atua em leitura; nunca bloqueia
    System Manager/Administrator (gestão do curso não pode travar).

    Também bloqueia alunos com custom_vedium_status=Suspended ou Cancelled
    para cursos pagos (assinatura recorrente Stripe).
    O acesso é restaurado automaticamente quando invoice.paid chega e o
    scheduler atualiza o status para Active.
    """
    if ptype != "read" or user in ("Administrator", None):
        return None
    if "System Manager" in frappe.get_roles(user):
        return None

    docname = doc.name if hasattr(doc, "name") else doc
    course_name = _course_name_for(doc.doctype, docname)
    if not course_name:
        return None

    if course_name in PLE_COURSES and _is_course_staff(user, course_name):
        return True if doc.doctype == "LMS Quiz" else None

    # ── Bloqueio por status de assinatura ──────────────────────────────────
    # Verificamos ANTES do gate de pré-requisito para evitar N consultas
    # em cursos não-PLE onde o pré-req não existe.
    _BLOCKED_STATUSES = ("Suspended", "Cancelled")
    enrollment_data = frappe.db.get_value(
        "LMS Enrollment",
        {"member": user, "course": course_name},
        ["name", "custom_vedium_status", "custom_stripe_subscription_id"],
        as_dict=True,
    )
    if (
        enrollment_data
        and enrollment_data.get("custom_stripe_subscription_id")  # assinatura recorrente
        and enrollment_data.get("custom_vedium_status") in _BLOCKED_STATUSES
    ):
        return False
    # ────────────────────────────────────────────────────────────────────────

    prereq = _prerequisite_course(course_name)
    if prereq and not has_passed_course(user, prereq):
        return False

    if doc.doctype == "LMS Quiz" and course_name in PLE_COURSES and _has_enrollment(user, course_name):
        return True

    required_quiz = _required_module_activity(course_name, doc.doctype, docname)
    if required_quiz and not _has_passed_quiz(user, course_name, required_quiz):
        return False

    return None
