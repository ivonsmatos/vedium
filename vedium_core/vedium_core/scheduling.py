"""Agendamento de aulas — aluno matriculado escolhe o professor do curso
comprado e reserva um horário disponível na agenda dele (Lesson Slot).

Regra de negócio:
- Só pode reservar quem está matriculado (LMS Enrollment) no curso.
- Só pode reservar horário de um professor que é de fato instrutor
  (Course Instructor) daquele curso.
- Reserva é atômica (UPDATE condicional em status='Available') para dois
  alunos não conseguirem roubar o mesmo horário em uma corrida — mesmo
  padrão já usado em gamification.add_points e Coupon.used_count.
- O doctype "Lesson Slot" trava a REST API padrão do Frappe (ver
  permission_query_conditions/has_permission abaixo): toda escrita de
  aluno/professor passa por estas funções whitelisted, nunca por
  /api/resource/Lesson Slot direto.
"""

import json
import re

import frappe
from frappe import _


# =====================
# Helpers
# =====================


def _clean_name(value):
    value = (value or "").strip()
    if not value:
        frappe.throw(_("Parâmetro obrigatório ausente."))
    return value


def _clean_text(value, limit=500):
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def _require_login():
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Por favor, faça login para continuar."))
    return user


def _is_enrolled(user, course):
    return bool(frappe.db.exists("LMS Enrollment", {"course": course, "member": user}))


def _is_course_instructor(user, course):
    return bool(frappe.db.exists("Course Instructor", {"parent": course, "instructor": user}))


# =====================
# Permissões do doctype Lesson Slot
# (referenciadas em hooks.py: permission_query_conditions / has_permission)
# =====================


def lesson_slot_has_permission(doc, ptype=None, user=None):
    user = user or frappe.session.user
    if user == "Administrator":
        return True
    roles = set(frappe.get_roles(user))
    if roles & {"System Manager", "LMS Moderator"}:
        return True
    if doc.teacher == user:
        return True
    if doc.student and doc.student == user:
        return ptype in ("read", "select", "email", "print")
    if doc.status == "Available" and not doc.student:
        return ptype in ("read", "select")
    return False


def lesson_slot_query_conditions(user=None):
    user = user or frappe.session.user
    if user in ("Administrator", "Guest"):
        return "1=0" if user == "Guest" else ""
    roles = set(frappe.get_roles(user))
    if roles & {"System Manager", "LMS Moderator"}:
        return ""
    user_esc = frappe.db.escape(user)
    return (
        f"(`tabLesson Slot`.teacher = {user_esc} "
        f"OR `tabLesson Slot`.student = {user_esc} "
        f"OR (`tabLesson Slot`.status = 'Available' "
        f"AND (`tabLesson Slot`.student IS NULL OR `tabLesson Slot`.student = '')))"
    )


# =====================
# Notificações por e-mail
# =====================


def _notify(event, details):
    """Envia e-mails de agendamento. Nunca lança exceção — falha aqui não
    pode derrubar a reserva/cancelamento que já foi confirmado no banco."""
    try:
        when = frappe.utils.format_datetime(details["start_time"], "dd/MM/yyyy HH:mm")
        course_title = details.get("course_title") or ""
        link_html = (
            f'<p><a href="{details["meeting_link"]}">Entrar na aula</a></p>'
            if details.get("meeting_link")
            else ""
        )

        if event == "booked":
            frappe.sendmail(
                recipients=[details["student_email"]],
                subject=f"Aula agendada — {course_title} | Vedium",
                message=f"""
                    <h3>Aula confirmada{', ' + frappe.utils.escape_html(details['student_first_name']) if details.get('student_first_name') else ''}!</h3>
                    <p>Sua aula de <strong>{frappe.utils.escape_html(course_title)}</strong> com
                    <strong>{frappe.utils.escape_html(details['teacher_name'])}</strong> foi agendada para
                    <strong>{when}</strong>.</p>
                    {link_html}
                    <p>Gerencie seus horários em
                    <a href="https://app.vediums.com/agendar-aula">app.vediums.com/agendar-aula</a>.</p>
                    <p>— Equipe Vedium</p>
                """,
                delayed=False,
            )
            frappe.sendmail(
                recipients=[details["teacher_email"]],
                subject=f"Nova aula agendada — {course_title} | Vedium",
                message=f"""
                    <h3>Novo agendamento</h3>
                    <p><strong>{frappe.utils.escape_html(details['student_name'])}</strong> agendou uma aula de
                    <strong>{frappe.utils.escape_html(course_title)}</strong> para <strong>{when}</strong>.</p>
                    {link_html}
                    <p>Gerencie sua agenda em
                    <a href="https://app.vediums.com/minha-agenda">app.vediums.com/minha-agenda</a>.</p>
                    <p>— Equipe Vedium</p>
                """,
                delayed=False,
            )
        elif event == "cancelled_by_student":
            frappe.sendmail(
                recipients=[details["teacher_email"]],
                subject=f"Aula cancelada pelo aluno — {course_title} | Vedium",
                message=f"""
                    <p>A aula de <strong>{frappe.utils.escape_html(course_title)}</strong> marcada para
                    <strong>{when}</strong> com <strong>{frappe.utils.escape_html(details['student_name'])}</strong>
                    foi cancelada pelo aluno. O horário voltou a ficar disponível na sua agenda.</p>
                """,
                delayed=False,
            )
        elif event == "cancelled_by_teacher":
            frappe.sendmail(
                recipients=[details["student_email"]],
                subject=f"Aula cancelada pelo professor — {course_title} | Vedium",
                message=f"""
                    <p>Sua aula de <strong>{frappe.utils.escape_html(course_title)}</strong> marcada para
                    <strong>{when}</strong> foi cancelada pelo professor <strong>{frappe.utils.escape_html(details['teacher_name'])}</strong>.</p>
                    <p>Acesse <a href="https://app.vediums.com/agendar-aula">app.vediums.com/agendar-aula</a>
                    para escolher outro horário.</p>
                """,
                delayed=False,
            )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.scheduling.notify")


# =====================
# Aluno
# =====================


@frappe.whitelist()
def get_my_courses():
    """Cursos em que o aluno logado está matriculado, com o(s) professor(es) de cada um."""
    user = _require_login()
    enrollments = frappe.get_all(
        "LMS Enrollment", filters={"member": user}, fields=["course"], order_by="creation desc"
    )
    courses = []
    seen = set()
    for e in enrollments:
        if not e.course or e.course in seen:
            continue
        seen.add(e.course)
        title = frappe.db.get_value("LMS Course", e.course, "title") or e.course
        instructor_rows = frappe.get_all(
            "Course Instructor", filters={"parent": e.course}, fields=["instructor"]
        )
        teachers = []
        for row in instructor_rows:
            info = frappe.db.get_value(
                "User", row.instructor, ["full_name", "user_image"], as_dict=True
            )
            if info:
                teachers.append(
                    {"user": row.instructor, "full_name": info.full_name, "user_image": info.user_image}
                )
        courses.append({"course": e.course, "title": title, "teachers": teachers})
    return courses


@frappe.whitelist()
def get_teacher_availability(course, teacher):
    """Horários disponíveis (futuros) de um professor, para um curso em que o aluno está matriculado."""
    user = _require_login()
    course = _clean_name(course)
    teacher = _clean_name(teacher)

    if not _is_enrolled(user, course):
        frappe.throw(_("Você precisa estar matriculado neste curso para ver a agenda."), frappe.PermissionError)
    if not _is_course_instructor(teacher, course):
        frappe.throw(_("Este professor não leciona este curso."))

    rows = frappe.get_all(
        "Lesson Slot",
        filters={
            "teacher": teacher,
            "status": "Available",
            "start_time": [">=", frappe.utils.now_datetime()],
        },
        fields=["name", "start_time", "end_time", "course"],
        order_by="start_time asc",
        limit_page_length=60,
        ignore_permissions=True,
    )
    # Slots sem curso vinculado (agenda genérica do professor) também servem.
    rows = [r for r in rows if not r.course or r.course == course]
    return [
        {
            "slot": r.name,
            "start_time": frappe.utils.format_datetime(r.start_time, "dd/MM/yyyy HH:mm"),
            "start_time_raw": str(r.start_time),
            "end_time": frappe.utils.format_datetime(r.end_time, "HH:mm"),
        }
        for r in rows
    ]


@frappe.whitelist()
def book_lesson(course, slot):
    """Reserva atômica de um horário. Falha com mensagem clara se outro aluno chegou primeiro."""
    user = _require_login()
    course = _clean_name(course)
    slot = _clean_name(slot)

    if not _is_enrolled(user, course):
        frappe.throw(_("Você precisa estar matriculado neste curso para agendar uma aula."), frappe.PermissionError)

    slot_doc = frappe.db.get_value(
        "Lesson Slot",
        slot,
        ["name", "teacher", "course", "status", "student", "start_time", "end_time", "meeting_link"],
        as_dict=True,
    )
    if not slot_doc:
        frappe.throw(_("Horário não encontrado."))
    if slot_doc.course and slot_doc.course != course:
        frappe.throw(_("Este horário pertence a outro curso."))
    if not _is_course_instructor(slot_doc.teacher, course):
        frappe.throw(_("Este horário não pertence a um professor deste curso."))

    # UPDATE condicional: só um aluno consegue "ganhar" a corrida pelo mesmo horário.
    frappe.db.sql(
        """UPDATE `tabLesson Slot`
           SET status='Booked', student=%(student)s, course=%(course)s
           WHERE name=%(slot)s AND status='Available'""",
        {"student": user, "course": course, "slot": slot},
    )
    frappe.db.commit()

    confirmed = frappe.db.get_value("Lesson Slot", slot, ["status", "student"], as_dict=True)
    if not confirmed or confirmed.status != "Booked" or confirmed.student != user:
        frappe.throw(_("Este horário acabou de ser reservado por outra pessoa. Escolha outro horário."))

    student_info = frappe.db.get_value("User", user, ["full_name", "first_name", "email"], as_dict=True) or {}
    teacher_info = frappe.db.get_value("User", slot_doc.teacher, ["full_name", "email"], as_dict=True) or {}
    _notify(
        "booked",
        {
            "start_time": slot_doc.start_time,
            "course_title": frappe.db.get_value("LMS Course", course, "title") or course,
            "meeting_link": slot_doc.meeting_link,
            "student_name": student_info.get("full_name") or user,
            "student_first_name": student_info.get("first_name") or "",
            "student_email": student_info.get("email") or user,
            "teacher_name": teacher_info.get("full_name") or slot_doc.teacher,
            "teacher_email": teacher_info.get("email") or slot_doc.teacher,
        },
    )
    return {"ok": True}


@frappe.whitelist()
def cancel_lesson(slot):
    """Cancela uma aula agendada. Aluno libera o horário (volta a Available);
    professor cancela definitivamente (Cancelled) e o aluno é avisado."""
    user = _require_login()
    slot = _clean_name(slot)

    slot_doc = frappe.db.get_value(
        "Lesson Slot",
        slot,
        ["name", "teacher", "student", "course", "status", "start_time", "meeting_link"],
        as_dict=True,
    )
    if not slot_doc:
        frappe.throw(_("Horário não encontrado."))
    if slot_doc.status != "Booked":
        frappe.throw(_("Este horário não está agendado."))
    if user not in (slot_doc.teacher, slot_doc.student):
        frappe.throw(_("Você não tem permissão para cancelar esta aula."), frappe.PermissionError)

    student_info = frappe.db.get_value("User", slot_doc.student, ["full_name", "email"], as_dict=True) or {}
    teacher_info = frappe.db.get_value("User", slot_doc.teacher, ["full_name", "email"], as_dict=True) or {}
    course_title = frappe.db.get_value("LMS Course", slot_doc.course, "title") if slot_doc.course else ""

    if slot_doc.student == user:
        event = "cancelled_by_student"
        frappe.db.set_value("Lesson Slot", slot, {"status": "Available", "student": ""})
    else:
        event = "cancelled_by_teacher"
        frappe.db.set_value("Lesson Slot", slot, "status", "Cancelled")
    frappe.db.commit()

    _notify(
        event,
        {
            "start_time": slot_doc.start_time,
            "course_title": course_title or "",
            "meeting_link": slot_doc.meeting_link,
            "student_name": student_info.get("full_name") or slot_doc.student,
            "student_email": student_info.get("email") or slot_doc.student,
            "teacher_name": teacher_info.get("full_name") or slot_doc.teacher,
            "teacher_email": teacher_info.get("email") or slot_doc.teacher,
        },
    )
    return {"ok": True}


@frappe.whitelist()
def get_my_upcoming_lessons():
    """Aulas (futuras e recentes) do aluno logado — usado em /agendar-aula e /meu-progresso."""
    user = _require_login()
    rows = frappe.get_all(
        "Lesson Slot",
        filters={"student": user, "status": ["in", ["Booked", "Completed"]]},
        fields=["name", "teacher", "course", "start_time", "end_time", "status", "meeting_link"],
        order_by="start_time desc",
        limit_page_length=30,
        ignore_permissions=True,
    )
    for r in rows:
        r["teacher_name"] = frappe.db.get_value("User", r.teacher, "full_name") or r.teacher
        r["course_title"] = (frappe.db.get_value("LMS Course", r.course, "title") if r.course else "") or ""
        r["start_display"] = frappe.utils.format_datetime(r.start_time, "dd/MM/yyyy HH:mm")
    return rows


# =====================
# Professor
# =====================


@frappe.whitelist()
def get_my_teaching_courses():
    """Cursos em que o usuário logado é instrutor."""
    user = _require_login()
    rows = frappe.get_all("Course Instructor", filters={"instructor": user}, fields=["parent"])
    courses = []
    for r in rows:
        title = frappe.db.get_value("LMS Course", r.parent, "title") or r.parent
        courses.append({"course": r.parent, "title": title})
    return courses


@frappe.whitelist()
def create_availability(course, slots):
    """Professor cadastra um ou mais horários disponíveis para um curso que leciona.

    slots: lista de {"start_time": "...", "end_time": "...", "meeting_link": "..."}
    (aceita JSON serializado como string, como vem de fetch()).
    """
    user = _require_login()
    course = _clean_name(course)
    if not _is_course_instructor(user, course):
        frappe.throw(_("Você não é professor deste curso."), frappe.PermissionError)

    if isinstance(slots, str):
        try:
            slots = json.loads(slots)
        except (TypeError, ValueError):
            frappe.throw(_("Lista de horários inválida."))
    if not isinstance(slots, list) or not slots:
        frappe.throw(_("Informe ao menos um horário."))

    now = frappe.utils.now_datetime()
    created = []
    for item in slots[:50]:
        if not isinstance(item, dict):
            continue
        start = frappe.utils.get_datetime(item.get("start_time"))
        end = frappe.utils.get_datetime(item.get("end_time"))
        if not start or not end or end <= start or start < now:
            continue
        doc = frappe.get_doc(
            {
                "doctype": "Lesson Slot",
                "teacher": user,
                "course": course,
                "start_time": start,
                "end_time": end,
                "status": "Available",
                "meeting_link": _clean_text(item.get("meeting_link"), 500),
            }
        )
        doc.insert(ignore_permissions=True)
        created.append(doc.name)
    frappe.db.commit()
    if not created:
        frappe.throw(_("Nenhum horário válido foi enviado (verifique datas futuras e fim após o início)."))
    return {"ok": True, "created": created}


@frappe.whitelist()
def cancel_availability(slot):
    """Professor remove um horário que ainda não foi reservado por ninguém."""
    user = _require_login()
    slot = _clean_name(slot)
    slot_doc = frappe.db.get_value("Lesson Slot", slot, ["teacher", "status"], as_dict=True)
    if not slot_doc:
        frappe.throw(_("Horário não encontrado."))
    if slot_doc.teacher != user:
        frappe.throw(_("Você não tem permissão para remover este horário."), frappe.PermissionError)
    if slot_doc.status != "Available":
        frappe.throw(_("Só é possível remover horários ainda não reservados. Para cancelar uma aula já agendada, use cancelar aula."))
    frappe.delete_doc("Lesson Slot", slot, ignore_permissions=True)
    frappe.db.commit()
    return {"ok": True}


@frappe.whitelist()
def get_my_agenda():
    """Agenda completa do professor logado (últimos 7 dias + futuro)."""
    user = _require_login()
    rows = frappe.get_all(
        "Lesson Slot",
        filters={
            "teacher": user,
            "start_time": [">=", frappe.utils.add_days(frappe.utils.now_datetime(), -7)],
        },
        fields=["name", "student", "course", "start_time", "end_time", "status", "meeting_link"],
        order_by="start_time asc",
        limit_page_length=150,
        ignore_permissions=True,
    )
    for r in rows:
        r["student_name"] = (frappe.db.get_value("User", r.student, "full_name") if r.student else "") or ""
        r["course_title"] = (frappe.db.get_value("LMS Course", r.course, "title") if r.course else "") or ""
        r["start_display"] = frappe.utils.format_datetime(r.start_time, "dd/MM/yyyy HH:mm")
        r["end_display"] = frappe.utils.format_datetime(r.end_time, "HH:mm")
    return rows
