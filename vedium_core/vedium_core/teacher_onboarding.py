"""Onboarding de professor e de turma (P2 — Operação).

Dois momentos operacionais, ambos por notificação interna (NÃO são cobertos pelo
kit de e-mail do Brevo, que é para aluno/lead/B2B — ver
[[project_email_lifecycle_brevo]]; por isso aqui é `frappe.sendmail` mesmo):

1. **Turma nova** (`LMS Batch` after_insert): a turma nasce "completa" — ganha o
   canal no Raven e o(s) professor(es) recebem os detalhes + um checklist do que
   fazer para começar.
2. **Professor novo** (User ganhou a role "Vedium Professor"): recebe um e-mail
   de orientação uma única vez (detecção por transição de role, sem campo/flag).

Nunca lança: falha de notificação não pode derrubar a criação da turma nem o
salvar do usuário.
"""

from __future__ import annotations

import frappe
from frappe.utils import now_datetime

DESK_BATCH_URL = "https://app.vediums.com/app/lms-batch"
DESK_URL = "https://app.vediums.com/app"
PLATFORM_URL = "https://app.vediums.com/lms"
PROFESSOR_ROLE = "Vedium Professor"


def _user_has_role(user_doc, role: str) -> bool:
    return role in {row.role for row in (user_doc.get("roles") or [])}


def _instructor_emails(doc) -> list[str]:
    """E-mails dos instrutores da turma (child table `instructors`)."""
    emails: list[str] = []
    for row in (doc.get("instructors") or []):
        instructor = getattr(row, "instructor", None)
        if not instructor:
            continue
        email = frappe.db.get_value("User", instructor, "email") or instructor
        if email and "@" in str(email):
            emails.append(email)
    return list(dict.fromkeys(emails))


def _batch_courses_text(doc) -> str:
    titles = []
    for row in (doc.get("courses") or []):
        title = getattr(row, "title", None) or getattr(row, "course", None)
        if title:
            titles.append(str(title))
    return ", ".join(titles) or "—"


def _batch_schedule_text(doc) -> str:
    parts = []
    if doc.get("start_date"):
        span = frappe.utils.formatdate(doc.start_date)
        if doc.get("end_date"):
            span += f" a {frappe.utils.formatdate(doc.end_date)}"
        parts.append(span)
    if doc.get("start_time"):
        clock = str(doc.start_time)[:5]
        if doc.get("end_time"):
            clock += f"–{str(doc.end_time)[:5]}"
        parts.append(clock)
    if doc.get("timezone"):
        parts.append(str(doc.timezone))
    return " · ".join(parts) or "a definir com a coordenação"


def notify_batch_professor(batch_name: str) -> dict:
    """Envia aos professores da turma os detalhes + checklist de início."""
    doc = frappe.get_doc("LMS Batch", batch_name)
    recipients = _instructor_emails(doc)
    if not recipients:
        return {"skipped": "sem instrutores", "batch": batch_name}

    title = frappe.utils.escape_html(doc.get("title") or batch_name)
    courses = frappe.utils.escape_html(_batch_courses_text(doc))
    schedule = frappe.utils.escape_html(_batch_schedule_text(doc))
    seats = doc.get("seat_count")
    is_individual = seats == 1
    kind = "aula particular (1:1)" if is_individual else "turma"

    message = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;color:#152233;max-width:600px">
      <h2 style="color:#2E6DA4;margin:0 0 12px">Nova {kind}: {title}</h2>
      <table style="border-collapse:collapse;margin:8px 0 18px">
        <tr><td style="padding:4px 10px 4px 0;color:#5a6b7b">Curso(s)</td>
            <td style="padding:4px 0"><strong>{courses}</strong></td></tr>
        <tr><td style="padding:4px 10px 4px 0;color:#5a6b7b">Quando</td>
            <td style="padding:4px 0">{schedule}</td></tr>
        <tr><td style="padding:4px 10px 4px 0;color:#5a6b7b">Modalidade</td>
            <td style="padding:4px 0">{frappe.utils.escape_html(str(doc.get('medium') or 'Online'))}</td></tr>
      </table>
      <h3 style="color:#152233;margin:0 0 6px">Próximos passos</h3>
      <ol style="margin:0 0 18px;padding-left:20px;line-height:1.7">
        <li>Confirme os dias e horários das aulas com a coordenação.</li>
        <li>As aulas ao vivo são geradas pela coordenação — o link do Google Meet
            aparece em cada aula automaticamente.</li>
        <li>Use o canal da turma no chat (Raven) para falar com {'o aluno' if is_individual else 'os alunos'}.</li>
        <li>Prepare a primeira aula com o objetivo do nível em mente.</li>
      </ol>
      <p style="margin:0 0 18px">
        <a href="{DESK_BATCH_URL}/{frappe.utils.escape_html(batch_name)}"
           style="background:#2E6DA4;color:#fff;text-decoration:none;padding:11px 20px;
                  border-radius:6px;display:inline-block;font-weight:bold">Abrir a turma no painel</a>
      </p>
      <p style="color:#5a6b7b;font-size:13px">Dúvidas? Fale com a coordenação em
        contato@vediums.com.<br>— Vedium</p>
    </div>
    """
    try:
        frappe.sendmail(
            recipients=recipients,
            subject=f"Nova {kind}: {doc.get('title') or batch_name} | Vedium",
            message=message,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.teacher_onboarding.batch_email")
        return {"error": True, "batch": batch_name}
    return {"notified": recipients, "batch": batch_name}


def on_batch_created(doc, method=None) -> None:
    """Hook after_insert de LMS Batch: canal Raven + notifica professores.
    Nunca lança (não pode derrubar a criação da turma)."""
    # 1) A turma nasce com seu canal no Raven (chat turma ↔ alunos/professor).
    try:
        from vedium_core import communication

        if communication.raven_available():
            communication.ensure_batch_channel(doc.name)
            frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.teacher_onboarding.batch_channel")

    # 2) Notifica o(s) professor(es) com os detalhes + checklist.
    try:
        notify_batch_professor(doc.name)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.teacher_onboarding.batch_notify")


def _send_professor_welcome(email: str, first_name: str) -> None:
    hi = f", {frappe.utils.escape_html(first_name)}" if first_name else ""
    message = f"""
    <div style="font-family:Arial,Helvetica,sans-serif;color:#152233;max-width:600px">
      <h2 style="color:#2E6DA4;margin:0 0 12px">Bem-vindo(a) à equipe Vedium{hi} 🎓</h2>
      <p>Que bom ter você com a gente. Aqui vai o essencial para começar:</p>
      <ul style="margin:0 0 18px;padding-left:20px;line-height:1.7">
        <li><strong>Painel:</strong> gerencie cursos, turmas e alunos em
            <a href="{DESK_URL}">{DESK_URL}</a>.</li>
        <li><strong>Chat (Raven):</strong> você já tem acesso — cada turma tem seu
            canal para falar com os alunos.</li>
        <li><strong>Aulas ao vivo:</strong> o link do Google Meet é gerado
            automaticamente em cada aula; a coordenação monta a agenda com você.</li>
        <li><strong>Suas turmas:</strong> aparecem no painel assim que forem criadas.</li>
      </ul>
      <p style="margin:0 0 18px">
        <a href="{DESK_URL}"
           style="background:#A12D1C;color:#fff;text-decoration:none;padding:11px 20px;
                  border-radius:6px;display:inline-block;font-weight:bold">Acessar o painel</a>
      </p>
      <p style="color:#5a6b7b;font-size:13px">Qualquer dúvida, fale com a
        coordenação em contato@vediums.com.<br>— Vedium</p>
    </div>
    """
    frappe.sendmail(
        recipients=[email],
        subject="Bem-vindo à equipe Vedium 🎓",
        message=message,
    )


def on_user_became_professor(doc, method=None) -> None:
    """Hook on_update de User: quando a role "Vedium Professor" é adicionada
    (transição ausente→presente), manda o e-mail de orientação uma única vez.
    Detecção por transição (get_doc_before_save) — não precisa de campo/flag."""
    if doc.name in ("Administrator", "Guest"):
        return
    if not _user_has_role(doc, PROFESSOR_ROLE):
        return

    before = doc.get_doc_before_save() if hasattr(doc, "get_doc_before_save") else None
    if before and _user_has_role(before, PROFESSOR_ROLE):
        return  # já era professor antes deste save — não reenvia

    email = doc.get("email") or doc.name
    if not email or "@" not in str(email):
        return
    try:
        _send_professor_welcome(email, doc.get("first_name") or "")
    except Exception:
        frappe.log_error(
            frappe.get_traceback(), "Vedium.teacher_onboarding.professor_welcome"
        )
