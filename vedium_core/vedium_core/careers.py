# Vedium Core — Carreiras / Trabalhe Conosco
# Doctype "Candidatura" (custom) + handler do formulario publico de /carreiras.
# Integra com o Contato (mesma identidade unificadora do CRM/Helpdesk).

import frappe

CANDIDATURA = "Candidatura"


def ensure_candidatura_doctype():
    """Cria o doctype custom 'Candidatura' (idempotente). Roda no contexto do servidor."""
    if frappe.db.exists("DocType", CANDIDATURA):
        return CANDIDATURA
    dt = frappe.new_doc("DocType")
    dt.name = CANDIDATURA
    dt.module = "Vedium Core"
    dt.custom = 1
    dt.autoname = "format:CAND-{#####}"
    dt.track_changes = 1
    dt.sort_field = "modified"
    dt.sort_order = "DESC"
    dt.title_field = "candidate_name"
    fields = [
        ("candidate_name", "Nome completo", "Data", {"reqd": 1, "in_list_view": 1}),
        ("email", "E-mail", "Data", {"options": "Email", "reqd": 1, "in_list_view": 1}),
        ("phone", "Telefone / WhatsApp", "Data", {}),
        ("position", "Vaga / Area de interesse", "Data", {"in_list_view": 1}),
        ("resume_url", "Link do curriculo (LinkedIn/Drive)", "Data", {}),
        ("message", "Mensagem / Apresentacao", "Text", {}),
        ("status", "Status", "Select",
         {"options": "Nova\nEm analise\nEntrevista\nAprovada\nReprovada", "default": "Nova", "in_list_view": 1}),
        ("source", "Origem", "Data", {"default": "Site /carreiras", "read_only": 1}),
    ]
    for fn, label, ft, extra in fields:
        row = {"fieldname": fn, "label": label, "fieldtype": ft}
        row.update(extra)
        dt.append("fields", row)
    for role in ["System Manager", "LMS Moderator", "HR Manager", "Sales Manager"]:
        if not frappe.db.exists("Role", role):
            continue  # pula papeis que nao existem (ex.: LMS Moderator/HR Manager podem nao estar instalados)
        dt.append("permissions", {
            "role": role, "read": 1, "write": 1, "create": 1, "delete": 1,
            "email": 1, "export": 1, "report": 1, "share": 1, "print": 1,
        })
    dt.insert(ignore_permissions=True)
    frappe.db.commit()
    return CANDIDATURA


@frappe.whitelist(allow_guest=True)
def submit_candidatura(candidate_name, email, position=None, phone=None, message=None, resume_url=None):
    """Recebe a candidatura do formulario publico /carreiras e cria o registro."""
    candidate_name = (candidate_name or "").strip()
    email = (email or "").strip()
    if not candidate_name or not email:
        frappe.throw("Nome e e-mail sao obrigatorios.")

    ensure_candidatura_doctype()

    doc = frappe.new_doc(CANDIDATURA)
    doc.candidate_name = candidate_name
    doc.email = email
    doc.phone = (phone or "").strip()
    doc.position = (position or "").strip()
    doc.resume_url = (resume_url or "").strip()
    doc.message = (message or "").strip()
    doc.status = "Nova"
    doc.source = "Site /carreiras"
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    # Integracao: garante um Contato (mesma identidade do CRM/Helpdesk)
    try:
        from vedium_core.integrations import ensure_contact
        ensure_contact(email, candidate_name)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium: erro ao criar contato da candidatura")

    return {"ok": True, "name": doc.name}
