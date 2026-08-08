"""Read-only purchase options for paid LMS courses."""

from __future__ import annotations

import frappe
from frappe import _

from vedium_core.checkout_pricing_rules import annual_savings, money, twelve_month_total
from vedium_core.commercial_checkout_rules import get_checkout_restriction
from vedium_core.frequency_pricing_rules import (
    MAX_CLASSES_PER_WEEK,
    MIN_CLASSES_PER_WEEK,
    frequency_quote,
)
from vedium_core.catalog_pricing import is_catalog_complete, get_course_price


def _catalog_plan_payload(course_name: str, billing_period: str):
    options = []
    currency = "BRL"
    for classes in range(MIN_CLASSES_PER_WEEK, MAX_CLASSES_PER_WEEK + 1):
        price_doc = get_course_price(course_name, billing_period, classes, environment="live")
        currency = price_doc.currency
        options.append(
            {
                "classes_per_week": classes,
                "amount": float(price_doc.amount),
                "subtotal": float(price_doc.subtotal),
                "discount_percent": float(price_doc.frequency_discount_percent or 0),
                "stripe_catalog": True,
            }
        )

    base_price = get_course_price(course_name, billing_period, 1, environment="live")

    payload = {
        "billing_period": billing_period,
        "amount": float(base_price.amount),
        "currency": currency,
        "billing_frequency": "monthly",
        "frequency_options": options,
    }

    if billing_period == "annual":
        payload.update(
            {
                "title": "Plano anual",
                "charge_count": 12,
                "minimum_term_months": 12,
                "twelve_month_total": float(twelve_month_total(base_price.amount)),
                "terms": "12 cobranças mensais. Permanência mínima de 12 meses.",
            }
        )
        return payload

    payload.update(
        {
            "title": "Plano mensal",
            "charge_count": None,
            "minimum_term_months": 0,
            "twelve_month_total": None,
            "terms": "Cobrança mensal. Sem permanência mínima.",
        }
    )
    return payload


def _frequency_payloads(unit_amount) -> list[dict]:
    options = []
    for classes in range(MIN_CLASSES_PER_WEEK, MAX_CLASSES_PER_WEEK + 1):
        quote = frequency_quote(unit_amount, classes)
        options.append(
            {
                "classes_per_week": classes,
                "unit_amount": float(quote["unit_amount"]),
                "subtotal": float(quote["subtotal"]),
                "discount_percent": float(quote["discount_percent"]),
                "discount_amount": float(quote["discount_amount"]),
                "amount": float(quote["amount"]),
            }
        )
    return options


def _plan_payload(plan_name, billing_period: str):
    if not plan_name or not frappe.db.exists("Subscription Plan", plan_name):
        return None

    plan = frappe.get_doc("Subscription Plan", plan_name)
    amount = money(getattr(plan, "cost", 0))
    currency = (getattr(plan, "currency", None) or "").upper()

    if amount <= 0 or currency not in {"BRL", "USD"}:
        return None

    payload = {
        "billing_period": billing_period,
        "amount": float(amount),
        "currency": currency,
        "billing_frequency": "monthly",
        "frequency_options": _frequency_payloads(amount),
    }

    if billing_period == "annual":
        payload.update(
            {
                "title": "Plano anual",
                "charge_count": 12,
                "minimum_term_months": 12,
                "twelve_month_total": float(twelve_month_total(amount)),
                "terms": "12 cobranças mensais. Permanência mínima de 12 meses.",
            }
        )
        return payload

    payload.update(
        {
            "title": "Plano mensal",
            "charge_count": None,
            "minimum_term_months": 0,
            "twelve_month_total": None,
            "terms": "Cobrança mensal. Sem permanência mínima.",
        }
    )
    return payload


def _add_annual_savings(monthly: dict, annual: dict) -> None:
    monthly_by_frequency = {
        item["classes_per_week"]: item for item in monthly["frequency_options"]
    }
    for annual_option in annual["frequency_options"]:
        monthly_option = monthly_by_frequency[annual_option["classes_per_week"]]
        saving = annual_savings(monthly_option["amount"], annual_option["amount"])
        annual_option["savings"] = float(saving)
        annual_option["savings_period_months"] = 12
    annual["savings"] = annual["frequency_options"][0]["savings"]
    annual["savings_period_months"] = 12


from vedium_core.course_urls import get_internal_course_name


@frappe.whitelist(allow_guest=True)
def get_course_purchase_options(course_name):
    """Return the commercially allowed purchase options for a paid course."""
    real_course_name = get_internal_course_name(course_name)
    if not real_course_name or not frappe.db.exists("LMS Course", real_course_name):
        frappe.throw(_("Curso não encontrado."), frappe.DoesNotExistError)
    course_name = real_course_name

    course = frappe.get_doc("LMS Course", course_name)
    if not getattr(course, "paid_course", False):
        return {"is_paid": False, "plans": []}

    catalog_status = is_catalog_complete(course.name, environment="live")
    if catalog_status == "incomplete":
        frappe.throw(_("Este curso possui um catálogo de preços incompleto."))

    if catalog_status is True:
        monthly = _catalog_plan_payload(course.name, "monthly")
        annual = _catalog_plan_payload(course.name, "annual")
    else:
        monthly = _plan_payload(
            getattr(course, "custom_stripe_monthly_plan", None),
            "monthly",
        )
        annual = _plan_payload(
            getattr(course, "custom_stripe_annual_plan", None),
            "annual",
        )

    restriction = get_checkout_restriction(course.name)
    if restriction:
        allowed_periods = set(restriction["billing_periods"])
        allowed_frequencies = set(restriction["classes_per_week"])
        if "monthly" not in allowed_periods:
            monthly = None
        if "annual" not in allowed_periods:
            annual = None
        for plan in (monthly, annual):
            if plan:
                plan["frequency_options"] = [
                    option
                    for option in plan["frequency_options"]
                    if option["classes_per_week"] in allowed_frequencies
                ]
                if not plan["frequency_options"]:
                    frappe.throw(_("Este curso não possui frequência comercial disponível."))
                base_option = plan["frequency_options"][0]
                plan["amount"] = float(base_option["amount"])
                plan["subtotal"] = float(base_option["subtotal"])

    plans = [plan for plan in (monthly, annual) if plan]
    if not plans:
        frappe.throw(_("Este curso ainda não possui planos disponíveis."))

    currencies = {plan["currency"] for plan in plans}
    if len(currencies) > 1:
        frappe.throw(_("Os planos mensal e anual estão em moedas diferentes."))

    if monthly and annual:
        _add_annual_savings(monthly, annual)
    elif annual:
        annual["savings"] = 0.0
        annual["savings_period_months"] = 12
        for option in annual["frequency_options"]:
            option["savings"] = 0.0
            option["savings_period_months"] = 12

    if restriction:
        frequency_payload = {
            "minimum": min(restriction["classes_per_week"]),
            "maximum": max(restriction["classes_per_week"]),
            "discount_from": None,
            "discount_percent": 0,
        }
    else:
        frequency_payload = {
            "minimum": MIN_CLASSES_PER_WEEK,
            "maximum": MAX_CLASSES_PER_WEEK,
            "discount_from": 2,
            "discount_percent": 10,
        }

    return {
        "is_paid": True,
        "course_name": course.name,
        "course_title": getattr(course, "title", None) or course.name,
        "frequency": frequency_payload,
        "plans": plans,
    }
