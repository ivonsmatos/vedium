"""Public funnel endpoints for marketing and sales handoff.

These endpoints intentionally create human-reviewable Helpdesk tickets instead
of mutating checkout, enrollments, payment sessions, or LMS progress directly.
"""

import json
import re

import frappe
from frappe import _
from frappe.utils import cint, now_datetime


ALLOWED_INTENTS = {
    "lead": "Lead",
    "diagnostic": "Aula diagnóstica",
    "community": "Comunidade",
    "referral": "Indicação",
    "b2b": "B2B",
    "review": "Depoimento verificado",
}


def _clean(value, limit=500):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def _payload():
    data = frappe.local.form_dict.copy()
    raw = getattr(frappe.request, "data", None)
    if raw:
        try:
            parsed = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
            if isinstance(parsed, dict):
                data.update(parsed)
        except Exception:
            pass
    return data


def _upsert_crm_lead_from_public_intent(intent, name, email, phone, company, team_size, message, course, goal):
    """Cria (ou comenta em) um CRM Lead a partir de QUALQUER intent do
    formulario publico (/empresas, /comunidade, aula diagnostica,
    indicacao, depoimento, lead generico) -- antes so intent 'b2b' tinha
    isso, o resto so virava ticket. Agora todo mundo que preenche
    um formulario publico fica visivel no CRM, alem do ticket humano.

    Campos extras de B2B (organization/no_of_employees) setados de forma
    defensiva -- se o schema do CRM Lead instalado nao tiver esses campos,
    a criacao do lead ainda funciona, e a informacao vai pro comentario de
    qualquer forma."""
    if not frappe.db.exists("DocType", "CRM Lead"):
        return

    intent_label = ALLOWED_INTENTS.get(intent, intent)
    note_lines = [f"Interesse via site -- {intent_label}"]
    if course:
        note_lines.append(f"Curso: {course}")
    if goal:
        note_lines.append(f"Objetivo: {goal}")
    if company:
        note_lines.append(f"Empresa: {company}")
    if team_size:
        note_lines.append(f"Tamanho do time: {team_size}")
    if message:
        note_lines.append(f"Mensagem: {message}")
    note = "\n".join(note_lines)

    from vedium_core.integrations import ensure_contact

    parts = (name or "").strip().split(" ", 1)
    ensure_contact(
        email,
        first_name=parts[0],
        last_name=parts[1] if len(parts) > 1 else None,
        mobile=phone,
    )

    existing = frappe.db.get_value("CRM Lead", {"email": email}, "name")
    if existing:
        frappe.get_doc("CRM Lead", existing).add_comment("Comment", note)
        return

    lead = frappe.new_doc("CRM Lead")
    lead.first_name = parts[0]
    if len(parts) > 1:
        lead.last_name = parts[1]
    lead.lead_name = (name or "").strip()
    lead.email = email
    if phone:
        lead.mobile_no = phone
    lead.source = f"Website {intent_label}"
    if company:
        try:
            lead.organization = company
        except Exception:
            pass
    if team_size:
        try:
            lead.no_of_employees = team_size
        except Exception:
            pass
    lead.insert(ignore_permissions=True)
    lead.add_comment("Comment", note)


def _create_ticket(intent, subject, details):
    from vedium_core.helpdesk import create_ticket

    category = ALLOWED_INTENTS.get(intent, "Lead")
    description = "\n".join(
        f"{key}: {_clean(value, 1000)}"
        for key, value in details.items()
        if _clean(value, 1000)
    )
    ticket = create_ticket(
        subject=_clean(subject, 140) or category,
        description=description,
        category=category,
        raised_by=_clean(details.get("email"), 180) or None,
        requester_name=_clean(details.get("name"), 180) or None,
        phone=_clean(details.get("phone"), 40) or None,
    )
    try:
        frappe.sendmail(
            recipients=["contato@vediums.com"],
            subject=f"[Vedium] {category}: {ticket.subject}",
            message=description.replace("\n", "<br>"),
            delayed=False,
        )
    except Exception as exc:
        frappe.log_error(f"Public funnel email failed: {exc}", "Vedium Public Funnel")
    lead_email = _clean(details.get("email"), 180)
    if lead_email:
        try:
            frappe.sendmail(
                recipients=[lead_email],
                subject="Recebemos seu contato | Vedium",
                message=(
                    "<p>Olá! Recebemos seu interesse na Vedium.</p>"
                    "<p>Nossa equipe vai analisar seu objetivo e retornar com o próximo passo. "
                    "Se preferir atendimento imediato, fale pelo WhatsApp: "
                    '<a href="https://wa.me/5511911293075">+55 (11) 91129-3075</a>.</p>'
                    "<p>Equipe Vedium</p>"
                ),
                delayed=False,
            )
        except Exception as exc:
            frappe.log_error(
                f"Public funnel lead confirmation failed: {exc}",
                "Vedium Public Funnel",
            )
    return ticket


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@frappe.whitelist(allow_guest=True)
def submit_public_intent():
    from vedium_core.api import rate_limit_by_ip

    rate_limit_by_ip("public_intent", limit=8, window_sec=3600)

    data = _payload()
    intent = _clean(data.get("intent") or "lead", 40)
    if intent not in ALLOWED_INTENTS:
        frappe.throw(_("Tipo de intenção inválido."))

    email = _clean(data.get("email"), 180)
    phone = _clean(data.get("phone"), 40)
    name = _clean(data.get("name"), 180)
    course = _clean(data.get("course"), 180)
    plan = _clean(data.get("plan"), 80)
    goal = _clean(data.get("goal"), 180)
    company = _clean(data.get("company"), 180)
    team_size = _clean(data.get("team_size"), 40)
    referer = ""
    try:
        referer = frappe.request.headers.get("Referer", "")
    except Exception:
        referer = ""
    source = _clean(data.get("source") or referer, 300)
    message = _clean(data.get("message"), 1200)

    if not name or not email:
        frappe.throw(_("Nome e e-mail são obrigatórios."))
    if not EMAIL_RE.match(email):
        frappe.throw(_("E-mail inválido."))

    subject_parts = [ALLOWED_INTENTS[intent], name or email or phone or "site"]
    if course:
        subject_parts.append(course)
    if company:
        subject_parts.append(company)
    ticket = _create_ticket(
        intent,
        " | ".join(subject_parts),
        {
            "name": name,
            "email": email,
            "phone": phone,
            "course": course,
            "plan": plan,
            "goal": goal,
            "company": company,
            "team_size": team_size,
            "source": source,
            "message": message,
        },
    )

    try:
        _upsert_crm_lead_from_public_intent(
            intent, name, email, phone, company, team_size, message, course, goal
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium: erro ao criar CRM Lead do funil publico")

    return {"ok": True, "ticket": ticket.name}


@frappe.whitelist(allow_guest=True)
def request_diagnostic_class():
    data = _payload()
    data["intent"] = "diagnostic"
    frappe.local.form_dict.update(data)
    return submit_public_intent()


@frappe.whitelist(allow_guest=True)
def get_available_diagnostic_slots(limit=8):
    """Lista horários livres para a aula diagnóstica pública.

    ATENÇÃO (2026-07-01): o doctype Lesson Slot que esta função consulta é
    legado — o agendamento de aulas migrou para o fluxo NATIVO do Frappe LMS
    (Course Evaluator + Google Calendar/Meet), que não tem endpoint público
    equivalente para "aula diagnóstica" ainda. Lesson Slot está permanente e
    propositalmente vazio em produção (0 registros, ninguém mais escreve
    nele), então esta função sempre retorna `slots: []`. Isso é aceitável
    hoje: www/aula-diagnostica.html já cai no fallback "consultar pelo
    WhatsApp" quando a lista vem vazia.
    Mantido de propósito (não removido) porque o JS de aula-diagnostica.html
    ainda chama este endpoint. NÃO portar isso para Course Evaluator aqui —
    é uma decisão de produto maior (unificar a aula diagnóstica com o
    agendamento nativo), fora do escopo desta limpeza. Ver
    docs/plataforma/01-mapa-nativo-vs-custom.md.
    """
    limit = max(1, min(cint(limit) or 8, 20))
    slots = frappe.get_all(
        "Lesson Slot",
        filters={"status": "Available", "start_time": [">=", now_datetime()]},
        fields=["name", "start_time", "end_time"],
        order_by="start_time asc",
        limit_page_length=limit,
    )
    return {
        "ok": True,
        "slots": [
            {
                "slot": slot.name,
                "start_time": str(slot.start_time),
                "end_time": str(slot.end_time),
            }
            for slot in slots
        ],
    }


@frappe.whitelist(allow_guest=True)
def verify_certificate(code):
    code = _clean(code, 120)
    if not code:
        frappe.throw(_("Código obrigatório."))
    cert = frappe.db.get_value(
        "LMS Certificate",
        {"verification_code": code},
        ["name", "member", "course", "issue_date"],
        as_dict=True,
    )
    if not cert:
        return {"ok": False, "valid": False}
    title = frappe.db.get_value("LMS Course", cert.course, "title")
    member_name = frappe.db.get_value("User", cert.member, "full_name")
    return {
        "ok": True,
        "valid": True,
        "certificate": cert.name,
        "student": member_name or cert.member,
        "course": title or cert.course,
        "issue_date": cert.issue_date,
    }
