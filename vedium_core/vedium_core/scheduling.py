"""Agendamento de aula 1-a-1 (aluno <-> professor) usando o fluxo NATIVO do
Frappe LMS (`Course Evaluator` + `Evaluator Schedule` + `LMS Certificate
Request`), sem passar pelo gate `LMS Course.paid_certificate`.

Por quê: o componente nativo do LMS que mostra o botão de agendamento
("Get Certified") só aparece quando o curso tem `paid_certificate=1`, ou
seja, quando o certificado é vendido como produto separado com cobrança
própria dentro do LMS. Isso não é o modelo da Vedium — o certificado já
está incluído no preço da aula, cobrado uma única vez via Stripe no
checkout. Ligar `paid_certificate` arriscaria mandar o aluno pra uma tela
de cobrança nativa do LMS e cobrá-lo de novo.

Este módulo cria o registro nativo (`LMS Certificate Request`) diretamente,
reaproveitando toda a validação nativa (conflito de horário, disponibilidade
do professor, limite de uma avaliação futura por curso etc. — ver
`lms.lms.doctype.lms_certificate_request.lms_certificate_request.py`), sem
nenhum campo de preço envolvido. Ver docs/plataforma/01-mapa-nativo-vs-custom.md.
"""

import frappe
from frappe import _


def _require_login():
    if frappe.session.user == "Guest":
        frappe.throw(_("Faça login para agendar sua aula."))


def _require_enrollment(course):
    if not frappe.db.exists(
        "LMS Enrollment", {"course": course, "member": frappe.session.user}
    ):
        frappe.throw(_("Você precisa estar matriculado neste curso para agendar uma aula."))


def _require_schedulable_course(course):
    course_doc = frappe.db.get_value(
        "LMS Course", course, ["evaluator", "enable_certification"], as_dict=True
    )
    if not course_doc or not course_doc.evaluator or not course_doc.enable_certification:
        frappe.throw(_("O agendamento de aulas ainda não está disponível para este curso."))
    return course_doc


@frappe.whitelist()
def get_my_evaluation_slots(course):
    """Repassa lms.get_schedule (nativo) só depois de confirmar matrícula —
    a função nativa não valida matrícula, só exige login."""
    _require_login()
    _require_enrollment(course)
    _require_schedulable_course(course)

    from lms.lms.doctype.course_evaluator.course_evaluator import get_schedule

    return get_schedule(course)


@frappe.whitelist()
def book_evaluation_slot(course, date, start_time, end_time):
    """Cria o agendamento nativo (LMS Certificate Request). Toda validação de
    conflito/disponibilidade roda no `validate()` nativo do doctype — não
    duplicamos essa lógica aqui, só garantimos matrícula antes de criar."""
    _require_login()
    _require_enrollment(course)
    _require_schedulable_course(course)

    request = frappe.get_doc(
        {
            "doctype": "LMS Certificate Request",
            "course": course,
            "member": frappe.session.user,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
        }
    )
    request.insert()

    return {
        "ok": True,
        "name": request.name,
        "date": str(request.date),
        "start_time": str(request.start_time),
        "end_time": str(request.end_time),
    }
