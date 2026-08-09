"""Relatório mensal de evolução do aluno (P5 — Acompanhamento pedagógico).

A CAPTURA já é nativa: o child "Aluno da Aula Vedium" guarda, por aula, as
competências (participação, compreensão, produção oral/escrita, pronúncia) +
presença + dificuldade/evolução observadas. Aqui só SINTETIZAMOS isso num
resumo mensal por aluno e emitimos o evento Brevo `monthly_evolution` (fluxo
A08-05 "Síntese do mês") — grande alavanca de retenção (pais/corporativo/
particular). Enquanto o Brevo não é dono do ciclo de vida, o Frappe manda o
resumo por e-mail. Ver [[project_email_lifecycle_brevo]].
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, getdate, now_datetime

from vedium_core import brevo

SKILL_FIELDS = ("participacao", "compreensao", "producao_oral", "producao_escrita", "pronuncia")
SKILL_LABELS = {
    "participacao": "Participação",
    "compreensao": "Compreensão",
    "producao_oral": "Conversação",
    "producao_escrita": "Escrita",
    "pronuncia": "Pronúncia",
}
_SCORE = {"Baixa": 1, "Média": 2, "Alta": 3}
_SCORE_LABEL = {1: "Baixa", 2: "Média", 3: "Alta"}
_ATTENDED = ("Presente", "Atrasado", "Saida antecipada")

REPORT_URL = "https://app.vediums.com/aluno"
# Mínimo de aulas no período para valer um relatório.
MIN_CLASSES = 2


def student_evolution_summary(member, days: int = 30) -> dict | None:
    """Resumo de evolução do aluno no período (padrão 30 dias). None se não houver
    aulas finalizadas suficientes."""
    since = getdate(add_to_date(now_datetime(), days=-days))
    rows = frappe.db.sql(
        """
        SELECT c.status_presenca AS presenca, c.participacao, c.compreensao,
               c.producao_oral, c.producao_escrita, c.pronuncia,
               c.dificuldade_observada AS dificuldade, r.data_aula AS data_aula,
               r.curso AS curso
        FROM `tabAluno da Aula Vedium` c
        JOIN `tabRegistro de Aula Vedium` r ON r.name = c.parent
        WHERE c.aluno = %s AND COALESCE(r.status_registro, '') != 'Rascunho'
          AND r.data_aula >= %s
        ORDER BY r.data_aula DESC
        """,
        (member, since),
        as_dict=True,
    )
    if len(rows) < MIN_CLASSES:
        return None

    total = len(rows)
    attended = sum(1 for r in rows if r.presenca in _ATTENDED)
    skills: dict[str, float] = {}
    for field in SKILL_FIELDS:
        scores = [_SCORE[r[field]] for r in rows if r.get(field) in _SCORE]
        if scores:
            skills[field] = round(sum(scores) / len(scores), 1)

    # Competência mais forte e ponto de atenção (mais fraco), rótulos humanos.
    strongest = weakest = None
    if skills:
        strongest = SKILL_LABELS[max(skills, key=skills.get)]
        weakest = SKILL_LABELS[min(skills, key=skills.get)]
    dificuldade = next((r.dificuldade for r in rows if r.dificuldade), None)
    course = frappe.db.get_value("LMS Course", rows[0].curso, "title") or rows[0].curso

    return {
        "classes": total,
        "attendance_rate": int(round(attended * 100 / total)) if total else 0,
        "skills": {SKILL_LABELS[k]: _SCORE_LABEL.get(round(v), "-") for k, v in skills.items()},
        "current_competence": strongest,
        "next_focus": weakest or dificuldade,
        "course": course,
    }


def _evolution_email(first_name: str, s: dict) -> tuple[str, str]:
    hi = f", {frappe.utils.escape_html(first_name)}" if first_name else ""
    course = frappe.utils.escape_html(s.get("course") or "seu curso")
    skills_rows = "".join(
        f"<tr><td style='padding:4px 14px 4px 0;color:#5a6b7b'>{frappe.utils.escape_html(k)}</td>"
        f"<td style='padding:4px 0;font-weight:700'>{frappe.utils.escape_html(v)}</td></tr>"
        for k, v in (s.get("skills") or {}).items()
    )
    subject = f"Sua evolução em {course} — resumo do mês"
    html = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;color:#152233;max-width:560px">
      <h2 style="color:#2E6DA4;margin:0 0 12px">Seu mês em {course}{hi}</h2>
      <p><b>{s['classes']}</b> aulas · <b>{s['attendance_rate']}%</b> de presença.</p>
      {"<table style='border-collapse:collapse;margin:12px 0'>" + skills_rows + "</table>" if skills_rows else ""}
      {f"<p>Destaque: <b>{frappe.utils.escape_html(s['current_competence'])}</b>.</p>" if s.get('current_competence') else ""}
      {f"<p>Próximo foco: <b>{frappe.utils.escape_html(s['next_focus'])}</b>.</p>" if s.get('next_focus') else ""}
      <p style="margin:22px 0">
        <a href="{REPORT_URL}" style="background:#A12D1C;color:#fff;text-decoration:none;
           padding:12px 22px;border-radius:6px;display:inline-block;font-weight:bold">Ver minha jornada</a>
      </p>
      <p style="color:#5a6b7b;font-size:13px">Continue firme — cada aula conta.<br>— Equipe Vedium</p>
    </div>
    """
    return subject, html


def emit_monthly_evolution(limit: int = 500) -> dict:
    """Job mensal: para cada aluno ativo com aulas no mês, sintetiza a evolução e
    emite `monthly_evolution` pro Brevo (A08-05) + e-mail interino (gated)."""
    members = frappe.get_all(
        "LMS Enrollment",
        filters={"custom_vedium_status": ["in", ["Active", "Trial"]]},
        fields=["member"],
        limit_page_length=limit,
    )
    seen = set()
    brevo_owns = brevo.lifecycle_owned_by_brevo()
    sent = 0
    for row in members:
        member = row.member
        if member in seen or member in ("Administrator", "Guest"):
            continue
        seen.add(member)
        summary = student_evolution_summary(member)
        if not summary:
            continue
        email = frappe.db.get_value("User", member, "email") or member
        if not email or "@" not in str(email):
            continue
        first_name = frappe.db.get_value("User", member, "first_name") or ""

        brevo.emit_contact_event(
            email,
            "monthly_evolution",
            event_properties={
                "course": summary.get("course"),
                "course_level": summary.get("course"),
                "attendance_rate": f"{summary['attendance_rate']}%",
                "activities_summary": f"{summary['classes']} aulas no mês",
                "current_competence": summary.get("current_competence") or "",
                "next_milestone": summary.get("next_focus") or "",
                "monthly_report_url": REPORT_URL,
            },
            contact_properties={"COURSE": summary.get("course")},
        )
        if not brevo_owns:
            try:
                subject, html = _evolution_email(first_name, summary)
                frappe.sendmail(recipients=[email], subject=subject, message=html)
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Vedium.pedagogical_report.email")
        sent += 1

    return {"students": len(seen), "reports": sent, "brevo_owns": brevo_owns}
