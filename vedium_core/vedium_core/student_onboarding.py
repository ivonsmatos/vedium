"""Onboarding e ativação do aluno (P2 — Operação).

Arquitetura-alvo: o **Brevo** é o dono dos e-mails de ciclo de vida (fluxo A08
do kit em Cliente/Vedium/emailmkt), disparados por EVENTOS que o Frappe emite.
O Frappe é a fonte de verdade e o detector dos momentos — inclusive um que só
ele consegue enxergar: **o aluno matriculou mas ainda não começou o curso.**

Enquanto o setup do Brevo não está 100% no ar (``BREVO_LIFECYCLE_LIVE`` off),
o Frappe também é o REMETENTE interino: manda o empurrão de ativação por
``frappe.sendmail``. Ao ligar a chave, o Frappe para de enviar e só emite o
evento — o Brevo assume o corpo/entrega. Ver
``vedium_core.brevo.lifecycle_owned_by_brevo``.

Nada aqui duplica função nativa do LMS: é detecção + notificação, não uma
página/fluxo de curso paralelo.
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, now_datetime

from vedium_core import brevo

# Dias após a matrícula sem nenhum progresso para considerar o aluno "parado".
ACTIVATION_DELAY_DAYS = 3
# Teto de segurança por execução do job (evita rajada se houver acúmulo).
ACTIVATION_BATCH_LIMIT = 200

STUDENT_PORTAL_URL = brevo.STUDENT_PORTAL_URL


def _has_field(fieldname: str) -> bool:
    try:
        return bool(frappe.get_meta("LMS Enrollment").has_field(fieldname))
    except Exception:
        return False


def _find_inactive_enrollments(limit: int):
    """Matrículas Active, com >= ACTIVATION_DELAY_DAYS de idade, ainda não
    empurradas e SEM nenhum registro de progresso (aluno não começou)."""
    cutoff = add_to_date(now_datetime(), days=-ACTIVATION_DELAY_DAYS)
    return frappe.db.sql(
        """
        SELECT e.name, e.member, e.course
        FROM `tabLMS Enrollment` e
        WHERE COALESCE(e.custom_vedium_status, 'Active') = 'Active'
          AND e.custom_activation_nudged_on IS NULL
          AND e.creation <= %(cutoff)s
          AND e.member NOT IN ('Administrator', 'Guest')
          AND NOT EXISTS (
              SELECT 1 FROM `tabLMS Course Progress` p
              WHERE p.member = e.member AND p.course = e.course
          )
        ORDER BY e.creation ASC
        LIMIT %(limit)s
        """,
        {"cutoff": cutoff, "limit": int(limit)},
        as_dict=True,
    )


def _activation_email(first_name: str, course_title: str) -> tuple[str, str]:
    hi = f", {frappe.utils.escape_html(first_name)}" if first_name else ""
    course_title = frappe.utils.escape_html(course_title)
    subject = f"Vamos começar seu curso de {course_title}?"
    html = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;color:#152233;max-width:560px">
      <h2 style="color:#2E6DA4;margin:0 0 12px">Sua primeira aula te espera{hi}</h2>
      <p>Você já está matriculado(a) em <strong>{course_title}</strong>, mas ainda
      não deu o primeiro passo. Começar é a parte mais importante — e a mais
      rápida.</p>
      <p style="margin:24px 0">
        <a href="{STUDENT_PORTAL_URL}"
           style="background:#A12D1C;color:#fff;text-decoration:none;
                  padding:12px 22px;border-radius:6px;display:inline-block;
                  font-weight:bold">Abrir meu curso agora</a>
      </p>
      <p>Prefere aulas ao vivo? A coordenação define seu horário com o professor —
      responda este e-mail que combinamos.</p>
      <p style="color:#5a6b7b;font-size:13px;margin-top:28px">
        Qualquer dúvida, é só responder aqui ou escrever para
        contato@vediums.com.<br>— Equipe Vedium</p>
    </div>
    """
    return subject, html


def _emit_not_activated_event(email: str, course_title: str, enrollment_name: str) -> None:
    """Emite o evento Brevo que dispara o fluxo de ativação (A08/A09).
    Best-effort: Brevo desligado ou falho nunca quebra o job."""
    if not brevo.is_enabled():
        return
    try:
        brevo.track_event(
            "student_not_activated",
            email,
            event_properties={
                "enrollment_id": enrollment_name,
                "course": course_title,
                "course_level": course_title,
                "student_portal_url": STUDENT_PORTAL_URL,
                "onboarding_url": STUDENT_PORTAL_URL,
            },
            contact_properties={"COURSE": course_title},
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.onboarding.brevo_event")


def detect_inactive_students(limit: int = ACTIVATION_BATCH_LIMIT) -> dict:
    """Job diário: encontra quem matriculou e não começou, emite o evento de
    ativação pro Brevo e (enquanto o Brevo não for dono) manda o empurrão por
    e-mail. Idempotente via ``custom_activation_nudged_on``."""
    if not _has_field("custom_activation_nudged_on"):
        # Campo ainda não migrado (deploy anterior ao after_migrate) — no-op.
        return {"skipped": "field_missing", "nudged": 0}
    if not frappe.db.exists("DocType", "LMS Course Progress"):
        return {"skipped": "lms_missing", "nudged": 0}

    rows = _find_inactive_enrollments(limit)
    brevo_owns = brevo.lifecycle_owned_by_brevo()
    nudged = 0
    for row in rows:
        email = frappe.db.get_value("User", row.member, "email") or row.member
        if not email or email in ("Administrator", "Guest"):
            frappe.db.set_value("LMS Enrollment", row.name, "custom_activation_nudged_on", now_datetime())
            continue
        first_name = frappe.db.get_value("User", row.member, "first_name") or ""
        course_title = frappe.db.get_value("LMS Course", row.course, "title") or row.course

        _emit_not_activated_event(email, course_title, row.name)

        if not brevo_owns:
            try:
                subject, html = _activation_email(first_name, course_title)
                frappe.sendmail(recipients=[email], subject=subject, message=html)
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Vedium.onboarding.activation_email")

        frappe.db.set_value(
            "LMS Enrollment", row.name, "custom_activation_nudged_on", now_datetime()
        )
        nudged += 1

    frappe.db.commit()
    return {"checked": len(rows), "nudged": nudged, "brevo_owns": brevo_owns}
