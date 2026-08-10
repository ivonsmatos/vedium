"""Métricas do funil comercial (P8 — Crescimento).

Camada de DADOS do funil, do lado Frappe, num só lugar. O **dashboard visual**
se monta no app **Insights** (instalado) consumindo isto + os eventos do GA4
server-side (visitantes/topo de funil, que vivem no GA4, não no Frappe).

Funil: visita → curso → lead → checkout → compra → aluno ativo → renovação.
Aqui cobrimos de "lead" pra baixo (o topo — visita/curso — é GA4).
"""

from __future__ import annotations

import json

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


# ---------------------------------------------------------------------------
# Dashboard nativo do funil (Number Cards + Dashboard) — o painel VISUAL para as
# métricas que mapeiam pra agregados de doctype (Count/Sum). As métricas
# computadas (churn %, ticket médio, conversão por idioma) ficam em
# funnel_metrics() para o Insights consumir. Idempotente por label; nunca fatal.
# ---------------------------------------------------------------------------

_ACTIVE_FILTER = json.dumps([["custom_vedium_status", "in", ["Active", "Trial"]]])

_FUNNEL_CARDS = [
    {
        "label": "Vedium · Alunos ativos",
        "document_type": "LMS Enrollment",
        "function": "Count",
        "filters_json": _ACTIVE_FILTER,
    },
    {
        "label": "Vedium · MRR (R$/mês)",
        "document_type": "LMS Enrollment",
        "function": "Sum",
        "aggregate_function_based_on": "custom_contract_monthly_amount",
        "filters_json": _ACTIVE_FILTER,
    },
    {
        "label": "Vedium · Leads (total)",
        "document_type": "CRM Lead",
        "function": "Count",
        "filters_json": "[]",
    },
    {
        "label": "Vedium · Matrículas (total)",
        "document_type": "LMS Enrollment",
        "function": "Count",
        "filters_json": "[]",
    },
]


def ensure_funnel_dashboard() -> dict:
    """Cria (idempotente) os Number Cards do funil + um Dashboard 'Vedium Funil'.
    Nunca fatal. Só cria cards cujo document_type existe."""
    if not frappe.db.exists("DocType", "Number Card"):
        return {"skipped": "no_number_card"}

    created = []
    card_labels = []
    for cfg in _FUNNEL_CARDS:
        if not frappe.db.exists("DocType", cfg["document_type"]):
            continue
        existing = frappe.db.get_value("Number Card", {"label": cfg["label"]}, "name")
        if existing:
            card_labels.append(existing)
            continue
        try:
            doc = frappe.get_doc(
                {"doctype": "Number Card", "type": "Document Type", "is_public": 1, **cfg}
            )
            doc.insert(ignore_permissions=True)
            card_labels.append(doc.name)
            created.append(doc.name)
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Vedium.funnel.number_card")

    # O Dashboard exige ao menos um chart (campo `charts` obrigatório). Criamos um
    # Group By por status da matrícula.
    chart_name = None
    if frappe.db.exists("DocType", "Dashboard Chart") and frappe.db.exists(
        "DocType", "LMS Enrollment"
    ):
        chart_name = frappe.db.get_value(
            "Dashboard Chart", {"chart_name": "Vedium - Alunos por status"}, "name"
        )
        if not chart_name:
            try:
                chart = frappe.get_doc(
                    {
                        "doctype": "Dashboard Chart",
                        "chart_name": "Vedium - Alunos por status",
                        "chart_type": "Group By",
                        "document_type": "LMS Enrollment",
                        "group_by_type": "Count",
                        "group_by_based_on": "custom_vedium_status",
                        "filters_json": "[]",
                        "type": "Donut",
                        "is_public": 1,
                    }
                )
                chart.insert(ignore_permissions=True)
                chart_name = chart.name
                created.append(chart_name)
            except Exception:
                frappe.log_error(frappe.get_traceback(), "Vedium.funnel.chart")

    if (
        frappe.db.exists("DocType", "Dashboard")
        and card_labels
        and chart_name
        and not frappe.db.exists("Dashboard", "Vedium Funil")
    ):
        try:
            dash = frappe.get_doc({"doctype": "Dashboard", "dashboard_name": "Vedium Funil"})
            dash.append("charts", {"chart": chart_name, "width": "Full"})
            for name in card_labels:
                dash.append("cards", {"card": name, "width": "Half"})
            dash.insert(ignore_permissions=True)
            created.append("Dashboard:Vedium Funil")
        except Exception:
            frappe.log_error(frappe.get_traceback(), "Vedium.funnel.dashboard")

    frappe.db.commit()
    return {"created": created, "cards": card_labels}
