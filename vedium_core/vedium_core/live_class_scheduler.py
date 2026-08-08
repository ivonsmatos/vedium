"""Gerador de aulas ao vivo recorrentes (LMS Live Class).

Reduz o trabalho manual de criar aula por aula (P2 — Operação). Para TURMAS
(LMS Batch): dado o período (start/end date da turma), o horário e os dias da
semana, cria uma `LMS Live Class` por ocorrência. O LMS nativo gera o Google
Meet ao salvar (via `google_meet_account`). Idempotente: pula ocorrências que já
existem (mesma turma + data + hora). Também gera aulas 1:1 recorrentes por aluno.

Uso (turma):
  bench --site <site> execute vedium_core.live_class_scheduler.generate_batch_live_classes \
    --kwargs '{"batch_name": "ple-b-sico-turma-agosto-2026", "weekdays": ["segunda"]}'
"""

from __future__ import annotations

from datetime import timedelta

import frappe
from frappe.utils import add_to_date, getdate, get_datetime

_WEEKDAYS = {
    "monday": 0, "segunda": 0, "segunda-feira": 0, "seg": 0,
    "tuesday": 1, "terca": 1, "terça": 1, "terca-feira": 1, "ter": 1,
    "wednesday": 2, "quarta": 2, "quarta-feira": 2, "qua": 2,
    "thursday": 3, "quinta": 3, "quinta-feira": 3, "qui": 3,
    "friday": 4, "sexta": 4, "sexta-feira": 4, "sex": 4,
    "saturday": 5, "sabado": 5, "sábado": 5, "sab": 5,
    "sunday": 6, "domingo": 6, "dom": 6,
}


def _normalize_weekdays(weekdays):
    if not isinstance(weekdays, (list, tuple, set)):
        weekdays = [weekdays]
    out = set()
    for w in weekdays:
        if isinstance(w, int):
            out.add(w % 7)
            continue
        key = str(w).strip().lower()
        if key in _WEEKDAYS:
            out.add(_WEEKDAYS[key])
        elif key.isdigit():
            out.add(int(key) % 7)
    return out


def _batch_duration_minutes(batch, default=60):
    if batch.start_time and batch.end_time:
        try:
            start = get_datetime(f"2000-01-01 {batch.start_time}")
            end = get_datetime(f"2000-01-01 {batch.end_time}")
            minutes = int((end - start).total_seconds() // 60)
            if minutes > 0:
                return minutes
        except Exception:
            pass
    return default


def generate_batch_live_classes(batch_name, weekdays, host=None, duration=None, dry_run=False):
    """Cria as LMS Live Class recorrentes de uma turma no período da turma.

    weekdays: dias da semana (nomes PT/EN ou 0=segunda..6=domingo). host: e-mail
    do professor (obrigatório se não vier). Idempotente. dry_run=True só simula.
    """
    if not frappe.db.exists("LMS Batch", batch_name):
        frappe.throw(f"Turma não encontrada: {batch_name}")
    batch = frappe.get_doc("LMS Batch", batch_name)
    days = _normalize_weekdays(weekdays)
    if not days:
        frappe.throw("Informe ao menos um dia da semana válido (ex.: 'segunda').")
    if not batch.start_date or not batch.end_date:
        frappe.throw("A turma precisa ter data de início e fim (start_date/end_date).")
    if not host:
        frappe.throw("Informe o host (e-mail do professor) da turma.")

    start, end = getdate(batch.start_date), getdate(batch.end_date)
    time = batch.start_time
    duration = int(duration) if duration else _batch_duration_minutes(batch)

    existing_count = frappe.db.count("LMS Live Class", {"batch_name": batch_name})
    created, skipped = [], []
    day = start
    while day <= end:
        if day.weekday() in days:
            if frappe.db.exists(
                "LMS Live Class", {"batch_name": batch_name, "date": day, "time": time}
            ):
                skipped.append(str(day))
            elif dry_run:
                created.append(str(day))
            else:
                seq = existing_count + len(created) + 1
                doc = frappe.get_doc({
                    "doctype": "LMS Live Class",
                    "title": f"Aula ao vivo {seq} - {batch.title}",
                    "host": host,
                    "google_meet_account": batch.google_meet_account,
                    "batch_name": batch_name,
                    "date": day,
                    "time": time,
                    "duration": duration,
                    "timezone": batch.timezone,
                })
                doc.insert(ignore_permissions=True)
                created.append(str(day))
        day += timedelta(days=1)

    if not dry_run:
        frappe.db.commit()
    return {
        "batch": batch_name,
        "host": host,
        "google_meet_account": batch.google_meet_account,
        "duration": duration,
        "created": created,
        "skipped_existing": skipped,
    }


def _find_individual_batch(member, course):
    """Turma-de-um (seat_count=1) do aluno para o curso, se já existe."""
    rows = frappe.db.sql(
        """
        SELECT be.batch
        FROM `tabLMS Batch Enrollment` be
        JOIN `tabLMS Batch` b ON b.name = be.batch
        JOIN `tabBatch Course` bc ON bc.parent = b.name
        WHERE be.member = %s AND bc.course = %s AND b.seat_count = 1
        LIMIT 1
        """,
        (member, course),
    )
    return rows[0][0] if rows else None


def setup_individual_classes(
    member,
    course,
    weekdays,
    start_time,
    end_time,
    host,
    start_date,
    end_date,
    timezone="America/Sao_Paulo",
    google_meet_account="Vedium Meet",
    duration=None,
):
    """1:1: cria (ou reusa) uma turma-de-um pro aluno+curso, matricula o aluno e
    gera as aulas recorrentes. A coordenação define os slots (weekdays + horário).

    bench --site <site> execute vedium_core.live_class_scheduler.setup_individual_classes \
      --kwargs "{'member':'aluno@x.com','course':'ingl-s-beginner','weekdays':['terca','quinta'],'start_time':'19:00:00','end_time':'20:00:00','host':'kayode@vediums.com','start_date':'2026-08-11','end_date':'2026-11-11'}"
    """
    if not frappe.db.exists("User", member):
        frappe.throw(f"Aluno não encontrado: {member}")
    if not frappe.db.exists("LMS Course", course):
        frappe.throw(f"Curso não encontrado: {course}")
    if not host:
        frappe.throw("Informe o host (e-mail do professor).")

    student_name = frappe.db.get_value("User", member, "full_name") or member
    course_title = frappe.db.get_value("LMS Course", course, "title") or course

    batch_name = _find_individual_batch(member, course)
    if not batch_name:
        batch = frappe.get_doc({
            "doctype": "LMS Batch",
            "title": f"1:1 {student_name} — {course_title}"[:140],
            "description": f"Aulas particulares 1:1 de {course_title}.",
            "batch_details": f"<p>Aulas particulares 1:1 de <b>{course_title}</b> para {student_name}.</p>",
            "start_date": start_date,
            "end_date": end_date,
            "start_time": start_time,
            "end_time": end_time,
            "timezone": timezone,
            "medium": "Online",
            "seat_count": 1,
            "google_meet_account": google_meet_account,
            "published": 1,
            "allow_self_enrollment": 0,
        })
        batch.append("instructors", {"instructor": host})
        batch.append("courses", {"course": course, "title": course_title})
        batch.insert(ignore_permissions=True)
        batch_name = batch.name
    else:
        # Reusa a turma existente; atualiza o período/horário caso mude.
        frappe.db.set_value(
            "LMS Batch",
            batch_name,
            {
                "start_date": start_date,
                "end_date": end_date,
                "start_time": start_time,
                "end_time": end_time,
            },
        )

    if not frappe.db.exists("LMS Batch Enrollment", {"member": member, "batch": batch_name}):
        frappe.get_doc({
            "doctype": "LMS Batch Enrollment",
            "member": member,
            "batch": batch_name,
        }).insert(ignore_permissions=True)

    frappe.db.commit()
    result = generate_batch_live_classes(batch_name, weekdays, host=host, duration=duration)
    result["member"] = member
    result["course"] = course
    return result
