# -*- coding: utf-8 -*-
"""Notificacoes operacionais da Vedium.

Este modulo cobre lacunas que nao podem depender apenas do fluxo nativo do LMS:
candidaturas de professor e agendamentos de aula precisam chegar por e-mail e,
quando possivel, aparecer tambem no sino do Desk.
"""

import frappe


OPS_EMAIL = "contato@vediums.com"
OPS_ROLES = ("System Manager", "HR Manager")


def _clean(value):
    return str(value or "").strip()


def _html(value):
    return frappe.utils.escape_html(_clean(value))


def _field(doc, *fieldnames):
    for fieldname in fieldnames:
        value = None
        if hasattr(doc, "get"):
            value = doc.get(fieldname)
        if value in (None, ""):
            value = getattr(doc, fieldname, None)
        if value not in (None, ""):
            return value
    return None


def _form_url(doctype, name):
    slug = doctype.lower().replace(" ", "-")
    return frappe.utils.get_url(f"/app/{slug}/{name}")


def _user_email(user):
    user = _clean(user)
    if not user:
        return None
    email = None
    try:
        if frappe.db.exists("User", user):
            email = frappe.db.get_value("User", user, "email")
    except Exception:
        email = None
    email = _clean(email) or user
    return email if "@" in email else None


def _user_label(user):
    user = _clean(user)
    if not user:
        return "Nao informado"
    try:
        if frappe.db.exists("User", user):
            return frappe.db.get_value("User", user, "full_name") or user
    except Exception:
        pass
    return user


def _course_label(course):
    course = _clean(course)
    if not course:
        return "Nao informado"
    try:
        if frappe.db.exists("DocType", "LMS Course") and frappe.db.exists("LMS Course", course):
            return frappe.db.get_value("LMS Course", course, "title") or course
    except Exception:
        pass
    return course


def _system_users_with_roles(roles=OPS_ROLES):
    try:
        rows = frappe.get_all(
            "Has Role",
            filters={"role": ["in", list(roles)], "parenttype": "User"},
            fields=["parent"],
        )
    except Exception:
        return []

    names = sorted({row.parent for row in rows if row.parent not in ("Guest", "Administrator")})
    if not names:
        return []

    try:
        users = frappe.get_all(
            "User",
            filters={"name": ["in", names], "enabled": 1, "user_type": "System User"},
            fields=["name", "email"],
        )
    except Exception:
        return []
    return users


def _ops_recipients():
    recipients = {OPS_EMAIL}

    for user in _system_users_with_roles():
        email = _clean(user.email)
        if email and "@" in email:
            recipients.add(email)

    return sorted(recipients)


def _notify_desk_users(users, subject, message, reference_doctype=None, reference_name=None):
    if not users:
        return
    try:
        if not frappe.db.exists("DocType", "Notification Log"):
            return
    except Exception:
        return

    for user in users:
        user_name = _clean(getattr(user, "name", user))
        if not user_name or user_name == "Guest":
            continue
        try:
            log = frappe.new_doc("Notification Log")
            values = {
                "subject": subject,
                "email_content": message,
                "for_user": user_name,
                "type": "Alert",
                "document_type": reference_doctype,
                "document_name": reference_name,
                "from_user": "Administrator",
            }
            for fieldname, value in values.items():
                if value is not None and (fieldname == "doctype" or log.meta.has_field(fieldname)):
                    log.set(fieldname, value)
            log.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Vedium.notifications.notification_log")


def _send_email(recipients, subject, message, reference_doctype=None, reference_name=None, reply_to=None):
    recipients = sorted({r for r in recipients if r and "@" in r})
    if not recipients:
        return
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message,
        reference_doctype=reference_doctype,
        reference_name=reference_name,
        reply_to=reply_to,
        delayed=True,
    )


def _format_datetime(value):
    if not value:
        return None
    try:
        return frappe.utils.format_datetime(value, "dd/MM/yyyy HH:mm")
    except Exception:
        return _clean(value)


def _format_date(value):
    if not value:
        return None
    try:
        return frappe.utils.formatdate(value, "dd/MM/yyyy")
    except Exception:
        return _clean(value)


def _format_time(value):
    if not value:
        return None
    try:
        return frappe.utils.format_time(value, "HH:mm")
    except Exception:
        return _clean(value)


def _datetime_line(doc):
    start = _field(doc, "start_time", "starts_on", "from_time")
    end = _field(doc, "end_time", "ends_on", "to_time")
    date = _field(doc, "date", "evaluation_date", "scheduled_date")
    slot = _field(doc, "slot", "time_slot")

    if start:
        text = _format_datetime(start)
        if end:
            text = f"{text} ate {_format_time(end) or _clean(end)}"
        return text

    parts = []
    if date:
        parts.append(_format_date(date) or _clean(date))
    if slot:
        parts.append(_clean(slot))
    if end and not slot:
        parts.append(_format_time(end) or _clean(end))
    return " - ".join(parts) if parts else "Nao informado"


def notify_teacher_application(doc, method=None):
    """Avisa a operacao quando alguem envia candidatura em /carreiras."""
    try:
        candidate_name = _field(doc, "candidate_name", "applicant_name") or "Novo candidato"
        email = _field(doc, "email", "email_id")
        phone = _field(doc, "phone", "phone_number", "mobile_no")
        nationality = _field(doc, "nationality")
        marital_status = _field(doc, "marital_status")
        full_address = _field(doc, "full_address")
        rate_expectation = _field(doc, "rate_expectation")
        initial_availability = _field(doc, "initial_availability")
        position = _field(doc, "position", "job_title")
        resume_url = _field(doc, "resume_url", "resume_link")
        resume_attachment = _field(doc, "resume_attachment")
        message_text = _field(doc, "message", "cover_letter")
        rate_display = _html(rate_expectation or "Nao informado")
        availability_display = _html(initial_availability or "Nao informada")
        resume_display = _html(resume_url or resume_attachment or "Nao informado")

        subject = f"[Vedium] Nova candidatura de professor: {_clean(candidate_name)}"
        form_url = _form_url(doc.doctype, doc.name)
        body = f"""
            <h3>Nova candidatura recebida</h3>
            <p>Uma pessoa acabou de se candidatar pela pagina de carreiras.</p>
            <table border="0" cellpadding="6">
                <tr><td><strong>Nome</strong></td><td>{_html(candidate_name)}</td></tr>
                <tr><td><strong>E-mail</strong></td><td>{_html(email)}</td></tr>
                <tr><td><strong>Telefone</strong></td><td>{_html(phone or "Nao informado")}</td></tr>
                <tr><td><strong>Nacionalidade</strong></td><td>{_html(nationality or "Nao informada")}</td></tr>
                <tr><td><strong>Estado civil</strong></td><td>{_html(marital_status or "Nao informado")}</td></tr>
                <tr><td><strong>Endereco completo</strong></td><td>{_html(full_address or "Nao informado")}</td></tr>
                <tr><td><strong>Vaga/area</strong></td><td>{_html(position or "Nao informado")}</td></tr>
                <tr><td><strong>Valor por aula/hora</strong></td><td>{rate_display}</td></tr>
                <tr><td><strong>Disponibilidade inicial</strong></td><td>{availability_display}</td></tr>
                <tr><td><strong>Curriculo/link</strong></td><td>{resume_display}</td></tr>
            </table>
            <p><strong>Mensagem</strong></p>
            <p>{_html(message_text or "").replace(chr(10), "<br>") or "Nao informada"}</p>
            <p><a href="{form_url}">Abrir candidatura no Desk</a></p>
        """

        users = _system_users_with_roles()
        _send_email(
            _ops_recipients(),
            subject,
            body,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
            reply_to=_clean(email) or None,
        )
        _notify_desk_users(users, subject, body, doc.doctype, doc.name)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.notifications.teacher_application")


def notify_lesson_slot_booked(doc, method=None):
    """Avisa o professor quando um Lesson Slot legado vira reserva."""
    try:
        if _clean(_field(doc, "status")) != "Booked" or not _field(doc, "student"):
            return
        if method != "after_insert":
            changed = False
            for fieldname in ("status", "student", "start_time", "end_time"):
                if hasattr(doc, "has_value_changed") and doc.has_value_changed(fieldname):
                    changed = True
                    break
            if not changed:
                return

        teacher = _field(doc, "teacher")
        teacher_email = _user_email(teacher)
        if not teacher_email:
            return

        student = _field(doc, "student")
        course = _field(doc, "course")
        meeting_link = _field(doc, "meeting_link")
        subject = f"[Vedium] Nova aula agendada: {_course_label(course)}"
        form_url = _form_url(doc.doctype, doc.name)
        body = f"""
            <h3>Nova aula agendada</h3>
            <p>Um aluno reservou um horario com voce na Vedium.</p>
            <table border="0" cellpadding="6">
                <tr><td><strong>Aluno</strong></td><td>{_html(_user_label(student))}</td></tr>
                <tr><td><strong>Curso</strong></td><td>{_html(_course_label(course))}</td></tr>
                <tr><td><strong>Horario</strong></td><td>{_html(_datetime_line(doc))}</td></tr>
                <tr><td><strong>Link da aula</strong></td><td>{_html(meeting_link or "Ainda nao informado")}</td></tr>
            </table>
            <p><a href="{form_url}">Abrir agendamento no Desk</a></p>
        """
        _send_email([teacher_email], subject, body, doc.doctype, doc.name)
        _notify_desk_users([teacher], subject, body, doc.doctype, doc.name)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.notifications.lesson_slot")


def notify_lms_certificate_request(doc, method=None):
    """Avisa professor e operacao quando o aluno agenda pelo LMS nativo."""
    try:
        course = _field(doc, "course", "lms_course")
        evaluator = _field(doc, "evaluator", "teacher", "instructor")
        if not evaluator and course:
            try:
                evaluator = frappe.db.get_value("LMS Course", course, "evaluator")
            except Exception:
                evaluator = None

        teacher_email = _user_email(evaluator)
        if not teacher_email:
            return

        student = _field(doc, "member", "student", "user", "owner")
        subject = f"[Vedium] Novo agendamento: {_course_label(course)}"
        form_url = _form_url(doc.doctype, doc.name)
        body = f"""
            <h3>Novo agendamento no LMS</h3>
            <p>Um aluno escolheu dia e horario para aula/avaliacao.</p>
            <table border="0" cellpadding="6">
                <tr><td><strong>Professor</strong></td><td>{_html(_user_label(evaluator))}</td></tr>
                <tr><td><strong>Aluno</strong></td><td>{_html(_user_label(student))}</td></tr>
                <tr><td><strong>Curso</strong></td><td>{_html(_course_label(course))}</td></tr>
                <tr><td><strong>Horario</strong></td><td>{_html(_datetime_line(doc))}</td></tr>
            </table>
            <p>O link do Google Meet pode ser gerado alguns minutos depois pelo job do LMS.</p>
            <p><a href="{form_url}">Abrir solicitacao no Desk</a></p>
        """

        recipients = {teacher_email, OPS_EMAIL}
        _send_email(recipients, subject, body, doc.doctype, doc.name)
        _notify_desk_users([evaluator], subject, body, doc.doctype, doc.name)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.notifications.lms_certificate_request")
