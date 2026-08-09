"""Pipeline comercial (P3 — Automação comercial).

Modelo escolhido: **Lead → Deal (nativo do Frappe CRM)**. Este módulo cuida do
lado LEAD do funil e da entrada dos formulários no estágio/origem corretos.

Bug corrigido (2026-08-08): os formulários do site gravavam `source =
"Website <intent>"`, mas `CRM Lead.source` é um Link para `CRM Lead Source` —
esses registros não existiam, o insert do lead falhava (LinkValidationError) e o
try/except do funil engolia o erro. Resultado: **nenhum lead de formulário
chegava ao CRM.** Aqui garantimos as origens válidas + o estágio de entrada.

Estágios do lado Lead (nativos, já existem): New, Contacted, Nurture, Qualified,
Converted, Unqualified, Junk. Mapa do funil da Vedium:
- Novo lead → `New`  · Contato → `Contacted`  · Qualificado → `Qualified`
- Perdido → `Unqualified` (ou `Junk`)
Os estágios pós-qualificação (aula experimental → proposta → checkout iniciado →
matrícula) vivem no **CRM Deal** (próximas unidades da P3).
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, cint, now_datetime, today

# Destino das tarefas/alertas comerciais internos. Configurável por site
# (set-config VEDIUM_COMMERCIAL_EMAIL "vendas@..."); default = caixa da
# coordenação, já usada no funil público.
DEFAULT_COMMERCIAL_EMAIL = "contato@vediums.com"
# Papéis considerados "comercial/coordenação" para receber a tarefa (ToDo)
# quando o lead não tem dono definido.
_COMMERCIAL_ROLES = (
    "Sales Manager",
    "Sales User",
    "Vedium Coordenacao Pedagogica",
    "System Manager",
)
# Horas em "New" sem contato antes de alertar a coordenação.
STALE_LEAD_HOURS = 24

# Origem (CRM Lead Source) por intent do formulário público.
LEAD_SOURCE_BY_INTENT = {
    "lead": "Site Vediums",
    "diagnostic": "Site Vediums",
    "community": "Site Vediums",
    "b2b": "Site Vediums",
    "review": "Site Vediums",
    "referral": "Indicacao",
}
# Fallback garantido (o Frappe CRM sempre traz "Website" nativo).
FALLBACK_LEAD_SOURCE = "Website"
# Todo formulário entra como lead novo, ainda não contatado.
DEFAULT_LEAD_STATUS = "New"

# Origens que garantimos existir (idempotente) para os mapeamentos acima.
_ENSURE_SOURCES = ("Site Vediums", "Indicacao")


def ensure_crm_pipeline() -> dict:
    """Garante que as origens (CRM Lead Source) usadas pelos formulários existam.
    Idempotente; roda no after_migrate. Estágios (CRM Lead Status) são os nativos."""
    if not frappe.db.exists("DocType", "CRM Lead Source"):
        return {"skipped": "no_crm"}
    created = []
    for name in _ENSURE_SOURCES:
        if not frappe.db.exists("CRM Lead Source", name):
            # autoname = field:source_name → o próprio nome é o valor do campo.
            frappe.get_doc({"doctype": "CRM Lead Source", "source_name": name}).insert(
                ignore_permissions=True
            )
            created.append(name)
    if created:
        frappe.db.commit()
    return {"created_sources": created}


def resolve_lead_source(intent: str) -> str | None:
    """Origem VÁLIDA (existente) para o intent. Nunca retorna um link quebrado:
    cai no mapeado → 'Website' nativo → qualquer origem existente."""
    if not frappe.db.exists("DocType", "CRM Lead Source"):
        return None
    for candidate in (LEAD_SOURCE_BY_INTENT.get(intent), FALLBACK_LEAD_SOURCE):
        if candidate and frappe.db.exists("CRM Lead Source", candidate):
            return candidate
    return frappe.db.get_value("CRM Lead Source", {}, "name")


def resolve_lead_status(intent: str | None = None) -> str | None:
    """Estágio de entrada do lead. Todo formulário → 'New' (Novo lead)."""
    if not frappe.db.exists("DocType", "CRM Lead Status"):
        return None
    if frappe.db.exists("CRM Lead Status", DEFAULT_LEAD_STATUS):
        return DEFAULT_LEAD_STATUS
    return frappe.db.get_value("CRM Lead Status", {}, "name")


# ---------------------------------------------------------------------------
# Tarefas e alertas comerciais internos (P3) — NÃO é e-mail ao lead (isso é o
# Brevo A01); é o trabalho do time dentro do CRM.
# ---------------------------------------------------------------------------

def _commercial_email() -> str:
    val = frappe.conf.get("VEDIUM_COMMERCIAL_EMAIL") or frappe.conf.get(
        "vedium_commercial_email"
    )
    return (str(val).strip() if val else "") or DEFAULT_COMMERCIAL_EMAIL


def _commercial_user() -> str | None:
    """Usuário para receber a tarefa (ToDo) quando o lead não tem dono:
    o usuário do e-mail comercial, senão o 1º usuário habilitado com papel
    comercial/coordenação."""
    email = _commercial_email()
    if frappe.db.exists("User", email) and frappe.db.get_value("User", email, "enabled"):
        return email
    for role in _COMMERCIAL_ROLES:
        for u in frappe.get_all(
            "Has Role",
            filters={"role": role, "parenttype": "User"},
            pluck="parent",
            limit_page_length=10,
        ):
            if u not in ("Administrator", "Guest") and frappe.db.get_value(
                "User", u, "enabled"
            ):
                return u
    return None


def on_lead_created(doc, method=None) -> None:
    """CRM Lead after_insert: cria a TAREFA comercial (ToDo) de primeiro contato.
    O e-mail imediato ao lead é do Brevo (A01, via evento lead_created). Nunca
    lança — não pode derrubar a criação do lead."""
    try:
        if getattr(doc, "converted", 0):
            return
        assignee = getattr(doc, "lead_owner", None) or _commercial_user()
        if not assignee:
            return
        course = getattr(doc, "custom_curso_interesse", None)
        label = getattr(doc, "lead_name", None) or getattr(doc, "email", None) or doc.name
        desc = f"Primeiro contato — {label}"
        if course:
            desc += f" (interesse: {course})"
        frappe.get_doc(
            {
                "doctype": "ToDo",
                "description": desc,
                "reference_type": "CRM Lead",
                "reference_name": doc.name,
                "allocated_to": assignee,
                "date": today(),
                "priority": "Medium",
            }
        ).insert(ignore_permissions=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.crm_pipeline.on_lead_created")


def alert_stale_leads(limit: int = 200) -> dict:
    """Job diário: leads em 'New' há mais de STALE_LEAD_HOURS sem contato →
    alerta a coordenação comercial (uma vez). Idempotente via
    custom_stale_alerted_on."""
    if not frappe.db.exists("DocType", "CRM Lead"):
        return {"skipped": "no_crm"}
    if not frappe.get_meta("CRM Lead").has_field("custom_stale_alerted_on"):
        return {"skipped": "field_missing"}

    cutoff = add_to_date(now_datetime(), hours=-STALE_LEAD_HOURS)
    rows = frappe.get_all(
        "CRM Lead",
        filters={
            "status": "New",
            "creation": ["<", cutoff],
            "custom_stale_alerted_on": ["is", "not set"],
        },
        fields=["name", "lead_name", "email", "custom_curso_interesse", "creation"],
        order_by="creation asc",
        limit_page_length=cint(limit),
    )
    if not rows:
        return {"alerted": 0}

    base = frappe.utils.get_url()
    items = "".join(
        f"<li><b>{frappe.utils.escape_html(r.lead_name or r.email or r.name)}</b> "
        f"({frappe.utils.escape_html(r.custom_curso_interesse or 'sem curso')}) — "
        f"há {frappe.utils.pretty_date(r.creation)} · "
        f'<a href="{base}/app/crm-lead/{r.name}">abrir</a></li>'
        for r in rows
    )
    message = (
        f"<p>{len(rows)} lead(s) em <b>Novo</b> sem contato há mais de "
        f"{STALE_LEAD_HOURS}h:</p><ul>{items}</ul>"
        "<p>Faça o primeiro contato ou mova o estágio no CRM.</p>"
    )
    try:
        frappe.sendmail(
            recipients=[_commercial_email()],
            subject=f"[Vedium] {len(rows)} lead(s) sem contato há +{STALE_LEAD_HOURS}h",
            message=message,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.crm_pipeline.alert_stale_leads")
        return {"error": True}

    for r in rows:
        frappe.db.set_value("CRM Lead", r.name, "custom_stale_alerted_on", now_datetime())
    frappe.db.commit()
    return {"alerted": len(rows)}
