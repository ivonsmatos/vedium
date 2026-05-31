# Vedium Core — Integrações entre LMS, CRM e Helpdesk
# Conecta o aluno (LMS) ao CRM (Lead/Contato) e ao Helpdesk (via Contato/e-mail),
# para que as ferramentas se comuniquem (perfil unificado do aluno).

import frappe


def ensure_contact(email, first_name=None, last_name=None, mobile=None):
    """Garante um Contact (frappe core) para o e-mail.

    O Contact é a entidade que UNIFICA: o Helpdesk liga os tickets ao Contact
    (pelo e-mail) e o CRM também usa o Contact. Assim, LMS + CRM + Helpdesk
    convergem para a mesma identidade do aluno.
    """
    if not email:
        return None
    existing = frappe.db.get_value("Contact", {"email_id": email}, "name")
    if existing:
        return existing
    contact = frappe.new_doc("Contact")
    contact.first_name = first_name or email.split("@")[0]
    if last_name:
        contact.last_name = last_name
    if mobile:
        contact.mobile_no = mobile
    contact.append("email_ids", {"email_id": email, "is_primary": 1})
    contact.insert(ignore_permissions=True)
    return contact.name


def sync_student_to_crm(member, course=None):
    """Cria/atualiza um CRM Lead (status Converted) + Contact para o aluno.

    Roda em background (enfileirado); protegido por try/except para NUNCA
    quebrar a matrícula do aluno.
    """
    try:
        if not member or member in ("Administrator", "Guest"):
            return
        user = frappe.get_doc("User", member)
        email = (user.email or member).strip()
        first_name = (user.first_name or (user.full_name or email).split(" ")[0] or email).strip()
        last_name = (user.last_name or "").strip()
        mobile = (user.mobile_no or user.phone or "").strip()

        # 1) Contato unificador (Helpdesk liga tickets a ele; CRM também usa)
        ensure_contact(email, first_name, last_name, mobile)

        # 2) CRM Lead (se o app CRM estiver instalado)
        if not frappe.db.exists("DocType", "CRM Lead"):
            return
        existing_lead = frappe.db.get_value("CRM Lead", {"email": email}, "name")
        if existing_lead:
            # Já existia como lead/prospect → marca como Convertido (matriculou)
            frappe.db.set_value("CRM Lead", existing_lead, "status", "Converted")
        else:
            lead = frappe.new_doc("CRM Lead")
            lead.first_name = first_name
            lead.last_name = last_name
            lead.lead_name = user.full_name or first_name
            lead.email = email
            if mobile:
                lead.mobile_no = mobile
            lead.status = "Converted"
            lead.source = "Website"
            lead.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium: erro ao sincronizar aluno com CRM")


def on_enrollment(doc, method=None):
    """Hook after_insert de 'LMS Enrollment' → sincroniza o aluno com o CRM.

    Enfileira em background (após o commit) para não bloquear nem quebrar a
    criação da matrícula.
    """
    try:
        frappe.enqueue(
            "vedium_core.integrations.sync_student_to_crm",
            queue="short",
            enqueue_after_commit=True,
            member=doc.member,
            course=getattr(doc, "course", None),
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium: erro ao enfileirar sync CRM")


@frappe.whitelist()
def get_student_360(email):
    """Visão unificada do aluno: dados + cursos (LMS) + chamados (Helpdesk) + lead (CRM).

    Restrito à equipe (não a alunos).
    """
    roles = set(frappe.get_roles())
    staff = {"System Manager", "LMS Moderator", "Sales Manager", "Sales User", "Agent", "Agent Manager"}
    if not staff.intersection(roles):
        frappe.throw("Acesso restrito à equipe.", frappe.PermissionError)
    if not email:
        return {}

    user = frappe.db.get_value(
        "User", {"email": email}, ["name", "full_name", "mobile_no", "phone"], as_dict=True
    )
    member = user.name if user else email

    enrollments = []
    for e in frappe.get_all("LMS Enrollment", filters={"member": member}, fields=["course", "creation"]):
        enrollments.append({
            "course": e.course,
            "title": frappe.db.get_value("LMS Course", e.course, "title") or e.course,
            "date": frappe.utils.format_datetime(e.creation, "dd/MM/yyyy"),
        })

    tickets = []
    if frappe.db.exists("DocType", "HD Ticket"):
        for t in frappe.get_all(
            "HD Ticket", filters={"raised_by": email},
            fields=["name", "subject", "status", "creation"], order_by="creation desc",
        ):
            tickets.append({
                "name": t.name, "subject": t.subject, "status": t.status,
                "date": frappe.utils.format_datetime(t.creation, "dd/MM/yyyy"),
            })

    lead = None
    if frappe.db.exists("DocType", "CRM Lead"):
        lead = frappe.db.get_value("CRM Lead", {"email": email}, ["name", "status"], as_dict=True)

    return {
        "user": user,
        "email": email,
        "enrollments": enrollments,
        "tickets": tickets,
        "lead": lead,
    }
