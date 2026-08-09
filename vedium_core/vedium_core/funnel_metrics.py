"""Métricas do funil comercial (P8 — Crescimento).

Camada de DADOS do funil, do lado Frappe, num só lugar. O **dashboard visual**
se monta no app **Insights** (instalado) consumindo isto + os eventos do GA4
server-side (visitantes/topo de funil, que vivem no GA4, não no Frappe).

Funil: visita → curso → lead → checkout → compra → aluno ativo → renovação.
Aqui cobrimos de "lead" pra baixo (o topo — visita/curso — é GA4).
"""

from __future__ import annotations

import frappe
from frappe.utils import add_to_date, cint, now_datetime

_ACTIVE = ("Active", "Trial")
_CHURNED = ("Cancelled", "Ended", "Expired")


_STAFF_ROLES = {"System Manager", "Administrator", "Vedium Ops", "Sales Manager"}


@frappe.whitelist()
def funnel_metrics(days: int = 30) -> dict:
    """Snapshot do funil comercial (lead→matrícula→receita→churn) + recortes por
    idioma e origem. `days` define a janela dos números de período.

    Restrito à gestão: expõe métricas de negócio (MRR, churn, leads) — não pode
    ficar acessível a qualquer usuário logado (aluno). Ver QA 2026-08-09."""
    if not set(frappe.get_roles()) & _STAFF_ROLES:
        frappe.throw("Acesso restrito à equipe.", frappe.PermissionError)
    since = add_to_date(now_datetime(), days=-cint(days))
    out: dict = {"period_days": cint(days)}

    # --- Leads (CRM) ---
    if frappe.db.exists("DocType", "CRM Lead"):
        out["leads_total"] = frappe.db.count("CRM Lead")
        out["leads_new"] = frappe.db.count("CRM Lead", {"creation": [">=", since]})
        out["leads_by_source"] = {
            r.source or "—": r.n
            for r in frappe.db.sql(
                """SELECT source, COUNT(name) AS n FROM `tabCRM Lead`
                   GROUP BY source ORDER BY n DESC""",
                as_dict=True,
            )
        }
        won = frappe.db.count("CRM Lead", {"status": "Converted"})
        out["lead_conversion_rate"] = (
            round(won * 100 / out["leads_total"], 1) if out["leads_total"] else 0
        )

    # --- Matrículas / receita ---
    out["enrollments_active"] = frappe.db.count(
        "LMS Enrollment", {"custom_vedium_status": ["in", _ACTIVE]}
    )
    out["enrollments_new"] = frappe.db.count(
        "LMS Enrollment", {"creation": [">=", since]}
    )
    mrr = (
        frappe.db.sql(
            """SELECT COALESCE(SUM(custom_contract_monthly_amount), 0)
               FROM `tabLMS Enrollment`
               WHERE custom_vedium_status IN ('Active','Trial')"""
        )[0][0]
        or 0
    )
    out["mrr"] = round(float(mrr), 2)
    out["ticket_medio"] = (
        round(out["mrr"] / out["enrollments_active"], 2) if out["enrollments_active"] else 0
    )

    # --- Churn (janela) ---
    churned = frappe.db.count(
        "LMS Enrollment",
        {"custom_vedium_status": ["in", _CHURNED], "modified": [">=", since]},
    )
    base = out["enrollments_active"] + churned
    out["churned_period"] = churned
    out["churn_rate"] = round(churned * 100 / base, 1) if base else 0

    # --- Conversão por idioma (categoria do curso) ---
    out["active_by_language"] = {
        (r.category or "—"): r.n
        for r in frappe.db.sql(
            """SELECT c.category AS category, COUNT(e.name) AS n
               FROM `tabLMS Enrollment` e
               JOIN `tabLMS Course` c ON c.name = e.course
               WHERE COALESCE(e.custom_vedium_status,'Active') IN ('Active','Trial')
               GROUP BY c.category ORDER BY n DESC""",
            as_dict=True,
        )
    }

    # --- Indicação (reusa P7) ---
    try:
        from vedium_core.referrals import referral_metrics

        out["referral"] = referral_metrics()
    except Exception:
        out["referral"] = {}

    return out
