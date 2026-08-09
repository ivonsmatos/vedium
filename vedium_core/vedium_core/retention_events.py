"""Automação de retenção (P6).

Aquisição custa caro; depois da matrícula, retenção é a métrica-chave. Aqui
detectamos sinais de risco e disparamos ação — reusando o que já existe:

- **Aluno inativo no LMS há ~10 dias** (começou mas sumiu) → evento `student_inactive`
  (fluxo A09/win-back) + e-mail interino. Field-free: janela sobre `User.last_active`.
- **Progresso abaixo do esperado** → digest semanal pra coordenação (sinalização
  pedagógica interna, não e-mail ao aluno).
- **Aluno muito engajado → pedir avaliação/indicação:** JÁ coberto pelo evento
  `progress_milestone` (=100) que `gamification.py` emite → mapear pro A12 no Brevo
  (ver doc 16). Não duplicar aqui.

Distinto de `student_onboarding.detect_inactive_students` (aquele é quem NUNCA
começou; este é quem começou e esfriou). Ver [[project_email_lifecycle_brevo]].
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, cint, now_datetime

from vedium_core import brevo

# Dias sem entrar no LMS (começou e sumiu) antes de acionar o win-back.
INACTIVE_DAYS = 10
# "Abaixo do esperado": matriculado há N dias com menos de M% de progresso.
RISK_MIN_DAYS = 45
RISK_MAX_PROGRESS = 25
COORDINATION_EMAIL = "contato@vediums.com"
STUDENT_PORTAL_URL = brevo.STUDENT_PORTAL_URL


def _has_started(member) -> bool:
    return bool(frappe.db.exists("LMS Course Progress", {"member": member}))


def _inactive_email(first_name: str) -> tuple[str, str]:
    hi = f", {frappe.utils.escape_html(first_name)}" if first_name else ""
    subject = "Que tal retomar seus estudos?"
    html = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;color:#152233;max-width:520px">
      <h2 style="color:#2E6DA4;margin:0 0 12px">Sentimos sua falta{hi}</h2>
      <p>Faz alguns dias que você não acessa seu curso. Retomar agora, mesmo que
      por 15 minutos, mantém seu ritmo — a gente ajuda no que precisar.</p>
      <p style="margin:22px 0">
        <a href="{STUDENT_PORTAL_URL}" style="background:#A12D1C;color:#fff;
           text-decoration:none;padding:12px 22px;border-radius:6px;display:inline-block;
           font-weight:bold">Voltar a estudar</a>
      </p>
      <p style="color:#5a6b7b;font-size:13px">Precisa remarcar ou ajustar algo?
      Responda este e-mail.<br>— Equipe Vedium</p>
    </div>
    """
    return subject, html


def detect_dormant_students(limit: int = 300) -> dict:
    """Job diário: aluno que começou mas está há ~INACTIVE_DAYS sem entrar no LMS
    → evento `student_inactive` + e-mail interino. Field-free (janela sobre
    last_active): dispara uma vez ao cruzar o limite."""
    lower = add_to_date(now_datetime(), days=-(INACTIVE_DAYS + 1))
    upper = add_to_date(now_datetime(), days=-INACTIVE_DAYS)
    rows = frappe.db.sql(
        """
        SELECT DISTINCT e.member
        FROM `tabLMS Enrollment` e
        JOIN `tabUser` u ON u.name = e.member
        WHERE COALESCE(e.custom_vedium_status, 'Active') IN ('Active', 'Trial')
          AND u.last_active >= %(lower)s AND u.last_active < %(upper)s
          AND u.name NOT IN ('Administrator', 'Guest') AND u.enabled = 1
        LIMIT %(limit)s
        """,
        {"lower": lower, "upper": upper, "limit": cint(limit)},
        as_dict=True,
    )
    brevo_owns = brevo.lifecycle_owned_by_brevo()
    sent = 0
    for row in rows:
        member = row.member
        if not _has_started(member):
            continue  # nunca começou → é caso de ativação (student_onboarding)
        email = frappe.db.get_value("User", member, "email") or member
        if not email or "@" not in str(email):
            continue
        first_name = frappe.db.get_value("User", member, "first_name") or ""
        brevo.emit_contact_event(
            email,
            "student_inactive",
            event_properties={
                "days_idle": INACTIVE_DAYS,
                "student_portal_url": STUDENT_PORTAL_URL,
                "support_checkin_url": STUDENT_PORTAL_URL,
            },
        )
        if not brevo_owns:
            try:
                subject, html = _inactive_email(first_name)
                frappe.sendmail(recipients=[email], subject=subject, message=html)
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Vedium.retention.inactive_email")
        sent += 1
    return {"candidates": len(rows), "notified": sent, "brevo_owns": brevo_owns}


def weekly_at_risk_digest(limit: int = 200) -> dict:
    """Job semanal: alunos matriculados há ≥RISK_MIN_DAYS com progresso <
    RISK_MAX_PROGRESS% → digest pra coordenação (sinalização pedagógica interna).
    Re-envia semanalmente de propósito (é um relatório, não um alerta 1x)."""
    cutoff = add_to_date(now_datetime(), days=-RISK_MIN_DAYS)
    rows = frappe.get_all(
        "LMS Enrollment",
        filters={
            "custom_vedium_status": "Active",
            "creation": ["<", cutoff],
            "progress": ["<", RISK_MAX_PROGRESS],
        },
        fields=["member", "course", "progress", "creation"],
        order_by="progress asc",
        limit_page_length=cint(limit),
    )
    if not rows:
        return {"at_risk": 0}
    items = ""
    for r in rows:
        name = frappe.db.get_value("User", r.member, "full_name") or r.member
        course = frappe.db.get_value("LMS Course", r.course, "title") or r.course
        items += (
            f"<li><b>{frappe.utils.escape_html(name)}</b> — "
            f"{frappe.utils.escape_html(course)}: {int(r.progress or 0)}% "
            f"(matriculado {frappe.utils.pretty_date(r.creation)})</li>"
        )
    message = (
        f"<p>{len(rows)} aluno(s) com progresso abaixo do esperado "
        f"(matriculados há +{RISK_MIN_DAYS} dias, &lt;{RISK_MAX_PROGRESS}%):</p>"
        f"<ul>{items}</ul><p>Vale um contato pedagógico / ajuste de plano.</p>"
    )
    try:
        frappe.sendmail(
            recipients=[COORDINATION_EMAIL],
            subject=f"[Vedium] {len(rows)} aluno(s) em risco (progresso baixo)",
            message=message,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.retention.at_risk_digest")
        return {"error": True}
    return {"at_risk": len(rows)}
