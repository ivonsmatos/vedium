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
      Course Lesson quando o pré-requisito existe e o aluno NÃO tem
      LMS Certificate emitido pro curso pré-requisito -- mesmo que ele já
      tenha uma LMS Enrollment paga pro curso atual (o pagamento continua
      valendo, só o conteúdo fica retido até o pré-requisito ser cumprido).
"""

import frappe


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
    return None


def has_permission(doc, ptype, user):
    """Hook genérico (hooks.py -> has_permission) pra LMS Course/Course
    Chapter/Course Lesson. Só atua em leitura; nunca bloqueia
    System Manager/Administrator (gestão do curso não pode travar).
    """
    if ptype != "read" or user in ("Administrator", None):
        return None
    if "System Manager" in frappe.get_roles(user):
        return None

    docname = doc.name if hasattr(doc, "name") else doc
    course_name = _course_name_for(doc.doctype, docname)
    if not course_name:
        return None

    prereq = _prerequisite_course(course_name)
    if not prereq:
        return None

    if has_passed_course(user, prereq):
        return None

    return False
