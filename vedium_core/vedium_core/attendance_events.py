"""Automação de ausência (P2 — Operação; alimenta o fluxo A09 do kit Brevo).

A CAPTURA de presença já existe nativa (doctype "Registro de Aula Vedium" +
child "Aluno da Aula Vedium" com `status_presenca`, além dos relatórios
"Vedium - Frequencia por aluno/turma"). Este módulo NÃO recria isso — ele só
DETECTA um padrão que merece ação: faltas consecutivas. Ao cruzar o limite, emite
o evento Brevo `student_absent` (dispara o A09 "contato de cuidado") e, enquanto
o Brevo não é dono do ciclo de vida, manda um check-in por e-mail.

Idempotente via `LMS Enrollment.custom_absence_alerted_on`: alerta uma vez por
sequência (no exato momento em que atinge o limite), não todo dia.
Ver [[project_email_lifecycle_brevo]].
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, getdate, now_datetime

from vedium_core import brevo

# Status de presença que contam como falta "de risco" (o resto — Presente,
# Atrasado, Saida antecipada, Falta justificada — quebra a sequência).
ABSENCE_STATUSES = {"Ausente", "Falta nao justificada"}
ABSENCE_THRESHOLD = 3
# Janela de varredura (dias) para limitar o custo do job.
LOOKBACK_DAYS = 90

SUPPORT_URL = "https://app.vediums.com/lms"


def _has_field(fieldname: str) -> bool:
    try:
        return bool(frappe.get_meta("LMS Enrollment").has_field(fieldname))
    except Exception:
        return False


def _attendance_rows(since):
    """Linhas de presença de registros FINALIZADOS (não rascunho), por aluno+curso,
    mais recentes primeiro."""
    return frappe.db.sql(
        """
        SELECT r.curso AS course, c.aluno AS member, r.data_aula AS data_aula,
               c.status_presenca AS status
        FROM `tabAluno da Aula Vedium` c
        JOIN `tabRegistro de Aula Vedium` r ON r.name = c.parent
        WHERE COALESCE(r.status_registro, '') != 'Rascunho'
          AND r.data_aula >= %(since)s
          AND r.data_aula IS NOT NULL
          AND c.aluno NOT IN ('Administrator', 'Guest')
          AND c.aluno IS NOT NULL AND r.curso IS NOT NULL
        ORDER BY c.aluno, r.curso, r.data_aula DESC
        """,
        {"since": since},
        as_dict=True,
    )


def _leading_absence_streak(rows) -> tuple[int, object]:
    """Conta faltas consecutivas a partir da aula mais recente (rows já vêm em
    ordem decrescente de data). Retorna (streak, data_da_aula_mais_recente)."""
    streak = 0
    newest = rows[0].data_aula if rows else None
    for row in rows:
        if row.status in ABSENCE_STATUSES:
            streak += 1
        else:
            break
    return streak, newest


def _absence_email(first_name: str, course_title: str) -> tuple[str, str]:
    hi = f", {frappe.utils.escape_html(first_name)}" if first_name else ""
    course_title = frappe.utils.escape_html(course_title)
    subject = f"Sentimos sua falta nas aulas de {course_title}"
    html = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;color:#152233;max-width:560px">
      <h2 style="color:#2E6DA4;margin:0 0 12px">Tudo bem por aí{hi}?</h2>
      <p>Notamos que você faltou às últimas aulas de
      <strong>{course_title}</strong>. Antes de qualquer coisa: queremos entender
      o que mudou e ajudar você a retomar sem tentar recuperar tudo de uma vez.</p>
      <p style="margin:24px 0">
        <a href="{SUPPORT_URL}"
           style="background:#2E6DA4;color:#fff;text-decoration:none;padding:12px 22px;
                  border-radius:6px;display:inline-block;font-weight:bold">Falar com a coordenação</a>
      </p>
      <p style="color:#5a6b7b;font-size:13px;margin-top:24px">Responda este e-mail
        ou escreva para contato@vediums.com — a gente combina um ponto de
        reentrada com seu professor.<br>— Equipe Vedium</p>
    </div>
    """
    return subject, html


def _emit_absent_event(email, course_title, enrollment_name, absences):
    if not brevo.is_enabled():
        return
    try:
        brevo.emit_contact_event(
            email,
            "student_absent",
            event_properties={
                "enrollment_id": enrollment_name,
                "course": course_title,
                "course_level": course_title,
                "absences": absences,
                "support_checkin_url": SUPPORT_URL,
                "student_portal_url": brevo.STUDENT_PORTAL_URL,
            },
            contact_properties={"COURSE": course_title},
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.attendance.brevo_event")


def detect_absent_students() -> dict:
    """Job diário: alunos que atingiram ABSENCE_THRESHOLD faltas consecutivas
    disparam o fluxo A09 (evento + e-mail interino). Idempotente por sequência."""
    if not _has_field("custom_absence_alerted_on"):
        return {"skipped": "field_missing", "alerted": 0}
    if not frappe.db.exists("DocType", "Registro de Aula Vedium"):
        return {"skipped": "no_attendance_doctype", "alerted": 0}

    since = getdate(add_to_date(now_datetime(), days=-LOOKBACK_DAYS))
    rows = _attendance_rows(since)
    brevo_owns = brevo.lifecycle_owned_by_brevo()

    # Agrupa por (aluno, curso) mantendo a ordem decrescente de data.
    groups: dict[tuple, list] = {}
    for row in rows:
        groups.setdefault((row.member, row.course), []).append(row)

    alerted = 0
    for (member, course), grp in groups.items():
        streak, newest = _leading_absence_streak(grp)
        # Dispara UMA vez, no exato momento em que atinge o limite.
        if streak != ABSENCE_THRESHOLD or not newest:
            continue
        enr = frappe.db.get_value(
            "LMS Enrollment",
            {"member": member, "course": course},
            ["name", "custom_absence_alerted_on", "custom_vedium_status"],
            as_dict=True,
        )
        if not enr:
            continue
        if enr.custom_vedium_status in {"Cancelled", "Ended", "Expired"}:
            continue
        # Já alertado para esta (ou mais nova) aula? não repete.
        if enr.custom_absence_alerted_on and getdate(enr.custom_absence_alerted_on) >= getdate(newest):
            continue

        email = frappe.db.get_value("User", member, "email") or member
        if not email or "@" not in str(email):
            continue
        first_name = frappe.db.get_value("User", member, "first_name") or ""
        course_title = frappe.db.get_value("LMS Course", course, "title") or course

        _emit_absent_event(email, course_title, enr.name, streak)
        if not brevo_owns:
            try:
                subject, html = _absence_email(first_name, course_title)
                frappe.sendmail(recipients=[email], subject=subject, message=html)
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Vedium.attendance.absence_email")

        frappe.db.set_value(
            "LMS Enrollment", enr.name, "custom_absence_alerted_on", getdate(newest)
        )
        alerted += 1

    frappe.db.commit()
    return {"groups": len(groups), "alerted": alerted, "brevo_owns": brevo_owns}
