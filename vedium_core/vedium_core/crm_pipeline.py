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
