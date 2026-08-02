"""Read-only purchase options for paid LMS courses."""

from __future__ import annotations

import frappe
from frappe import _

from vedium_core.checkout_pricing_rules import annual_savings, money, twelve_month_total


def _plan_payload(plan_name: str, billing_period: str) -> dict | None:
    if not plan_name or not frappe.db.exists("Subscription Plan", plan_name):
        return None

    plan = frappe.get_doc("Subscription Plan", plan_name)
    amount = money(getattr(plan, "cost", 0))
    currency = (getattr(plan, "currency", None) or "").upper()

    if amount <= 0 or currency not in {"BRL", "USD"}:
        return None

    if billing_period == "annual":
        return {
            "billing_period": "annual",
            "title": "Plano anual",
            "amount": float(amount),
            "currency": currency,
            "charge_count": 12,
            "billing_frequency": "monthly",
            "minimum_term_months": 12,
            "twelve_month_total": float(twelve_month_total(amount)),
            "terms": (
                "12 cobranças mensais. Permanência mínima de 12 meses."
            ),
        }

    return {
        "billing_period": "monthly",
        "title": "Plano mensal",
        "amount": float(amount),
        "currency": currency,
        "charge_count": None,
        "billing_frequency": "monthly",
        "minimum_term_months": 0,
        "twelve_month_total": None,
        "terms": "Cobrança mensal. Sem permanência mínima.",
    }


@frappe.whitelist(allow_guest=True)
def get_course_purchase_options(course_name):
    """Return safe, display-only monthly and annual options for a course."""
    if not course_name or not frappe.db.exists("LMS Course", course_name):
        frappe.throw(_("Curso não encontrado."), frappe.DoesNotExistError)

    course = frappe.get_doc("LMS Course", course_name)
    if not getattr(course, "paid_course", False):
        return {"is_paid": False, "plans": []}

    monthly = _plan_payload(
        getattr(course, "custom_stripe_monthly_plan", None),
        "monthly",
    )
    annual = _plan_payload(
        getattr(course, "custom_stripe_annual_plan", None),
        "annual",
    )

    plans = [plan for plan in (monthly, annual) if plan]
    if not plans:
        frappe.throw(_("Este curso ainda não possui planos disponíveis."))

    currencies = {plan["currency"] for plan in plans}
    if len(currencies) > 1:
        frappe.throw(_("Os planos mensal e anual estão em moedas diferentes."))

    if monthly and annual:
        saving = annual_savings(monthly["amount"], annual["amount"])
        annual["savings"] = float(saving)
        annual["savings_period_months"] = 12
    elif annual:
        annual["savings"] = 0.0
        annual["savings_period_months"] = 12

    return {
        "is_paid": True,
        "course_name": course.name,
        "course_title": getattr(course, "title", None) or course.name,
        "plans": plans,
    }
