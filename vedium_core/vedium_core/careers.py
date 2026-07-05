# Vedium Core — Carreiras / Trabalhe Conosco
# Doctype "Candidatura" (custom) + handler do formulario publico de /carreiras.
# Integra com o Contato (mesma identidade unificadora do CRM/Helpdesk).

import frappe

CANDIDATURA = "Candidatura"


CANDIDATURA_FIELDS = [
    ("candidate_name", "Nome completo", "Data", {"reqd": 1, "in_list_view": 1}),
    ("email", "E-mail", "Data", {"options": "Email", "reqd": 1, "in_list_view": 1}),
    ("phone", "Telefone / WhatsApp", "Data", {}),
    ("position", "Vaga / Area de interesse", "Data", {"in_list_view": 1}),
    ("resume_url", "Link do curriculo (LinkedIn/Drive)", "Data", {}),
    ("resume_attachment", "Curriculo (arquivo)", "Attach", {}),
    ("message", "Mensagem / Apresentacao", "Text", {}),
    ("status", "Status", "Select",
     {"options": "Nova\nEm analise\nEntrevista\nAprovada\nReprovada", "default": "Nova", "in_list_view": 1}),
    ("source", "Origem", "Data", {"default": "Site /carreiras", "read_only": 1}),
]


def ensure_candidatura_doctype():
    """Cria o doctype custom 'Candidatura' (idempotente). Se ja existir, so
    adiciona campos novos que ainda faltem (ex.: resume_attachment,
    introduzido depois) sem tocar no que ja esta la. Roda no servidor."""
    if frappe.db.exists("DocType", CANDIDATURA):
        dt = frappe.get_doc("DocType", CANDIDATURA)
        existing = {f.fieldname for f in dt.fields}
        changed = False
        for fn, label, ft, extra in CANDIDATURA_FIELDS:
            if fn in existing:
                continue
            row = {"fieldname": fn, "label": label, "fieldtype": ft}
            row.update(extra)
            dt.append("fields", row)
            changed = True
        if changed:
            dt.save(ignore_permissions=True)
            frappe.db.commit()
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
    for fn, label, ft, extra in CANDIDATURA_FIELDS:
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
def submit_candidatura(
    candidate_name, email, position=None, phone=None, message=None,
    resume_url=None, resume_attachment=None,
):
    """Recebe a candidatura do formulario publico /carreiras e cria o registro."""
    from vedium_core.api import rate_limit_by_ip

    rate_limit_by_ip("candidatura", limit=3, window_sec=3600)

    candidate_name = (candidate_name or "").strip()
    email = (email or "").strip()
    if not candidate_name or not email:
        frappe.throw("Nome e e-mail sao obrigatorios.")

    # Fallback idempotente — o caminho normal é o after_migrate já ter criado
    ensure_candidatura_doctype()

    doc = frappe.new_doc(CANDIDATURA)
    doc.candidate_name = candidate_name
    doc.email = email
    doc.phone = (phone or "").strip()
    doc.position = (position or "").strip()
    doc.resume_url = (resume_url or "").strip()
    doc.resume_attachment = (resume_attachment or "").strip()
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

    # Integracao: cria tambem o Job Applicant nativo do Frappe HR (hrms),
    # se o app estiver instalado. Nunca quebra o fluxo acima (Candidatura
    # ja foi salva) se o hrms nao estiver la ou o schema for diferente.
    try:
        _create_hrms_job_applicant(candidate_name, email, phone, position, message, resume_url, resume_attachment)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium: erro ao criar Job Applicant (hrms)")

    return {"ok": True, "name": doc.name}


def _create_hrms_job_applicant(candidate_name, email, phone, position, message, resume_url, resume_attachment):
    """Espelha a candidatura no doctype nativo 'Job Applicant' do Frappe HR,
    ligando a vaga (job_title) ao Job Opening correspondente se existir
    (ver oneshot setup_hrms_job_openings.py)."""
    if not frappe.db.exists("DocType", "Job Applicant"):
        return  # hrms nao instalado

    job_opening = None
    if position:
        job_opening = frappe.db.get_value("Job Opening", {"job_title": position}, "name")

    applicant = frappe.new_doc("Job Applicant")
    applicant.applicant_name = candidate_name
    applicant.email_id = email
    if phone:
        applicant.phone_number = phone
    if job_opening:
        applicant.job_title = job_opening
    if message:
        applicant.cover_letter = message
    if resume_url:
        applicant.resume_link = resume_url
    if resume_attachment:
        applicant.resume_attachment = resume_attachment
    applicant.insert(ignore_permissions=True)
