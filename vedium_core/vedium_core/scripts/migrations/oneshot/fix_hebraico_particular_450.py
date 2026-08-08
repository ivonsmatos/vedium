"""Align Hebraico Particular to the approved R$450/month, 1x/week offer."""

from __future__ import annotations

import frappe


COURSE_NAME = "hebraico-particular"
PLAN_NAME = "Vedium — Hebraico Particular — Mensal"
ITEM_ID = "CURSO-HEBRAICO-PARTICULAR"
STRIPE_PRODUCT_ID = "prod_UznRzhBCmMC5y8"
STRIPE_PRICE_ID = "price_1U28ADJu78f2k3L08xHL5KCa"
STRIPE_LOOKUP_KEY = "hebraico-particular_monthly"
MONTHLY_AMOUNT = 450.00


def _stripe_gateway_reference(currency: str):
    gateways = frappe.get_all("Payment Gateway", fields=["name", "gateway_controller"])
    stripe_gateways = [
        row.name
        for row in gateways
        if "stripe" in (row.gateway_controller or "").lower()
    ]
    if not stripe_gateways:
        frappe.throw("Nenhum gateway Stripe encontrado.")

    meta = frappe.get_meta("Subscription Plan")
    field = meta.get_field("payment_gateway")
    target_doctype = field.options if field else None

    if target_doctype == "Payment Gateway":
        return stripe_gateways[0]

    if target_doctype == "Payment Gateway Account":
        accounts = frappe.get_all(
            "Payment Gateway Account",
            filters={"payment_gateway": ["in", stripe_gateways]},
            fields=["name", "currency"],
        )
        valid = [
            account
            for account in accounts
            if not account.currency or account.currency.upper() == currency.upper()
        ]
        if not valid:
            frappe.throw(f"Conta Stripe para a moeda {currency} não encontrada.")
        return valid[0].name

    return stripe_gateways[0]


def _validate_live_stripe_price():
    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        frappe.throw("STRIPE_SECRET_KEY não configurada.")
    if not stripe.api_key.startswith("sk_live_"):
        frappe.throw("A migração exige a chave Stripe de produção.")

    price = stripe.Price.retrieve(STRIPE_PRICE_ID)
    recurring = price.get("recurring") or {}

    checks = {
        "active": bool(price.get("active")),
        "product": price.get("product") == STRIPE_PRODUCT_ID,
        "currency": (price.get("currency") or "").lower() == "brl",
        "unit_amount": int(price.get("unit_amount") or 0) == 45000,
        "type": price.get("type") == "recurring",
        "interval": recurring.get("interval") == "month",
        "interval_count": int(recurring.get("interval_count") or 0) == 1,
        "lookup_key": price.get("lookup_key") == STRIPE_LOOKUP_KEY,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        frappe.throw(
            "Price Stripe do Hebraico Particular não corresponde à oferta aprovada: "
            + ", ".join(failed)
        )


def _ensure_item():
    if frappe.db.exists("Item", ITEM_ID):
        return

    item = frappe.new_doc("Item")
    item.item_code = ITEM_ID
    item.item_name = "Hebraico Particular"
    item.item_group = "Cursos e Serviços"
    item.stock_uom = "Nos"
    item.is_stock_item = 0
    item.insert(ignore_permissions=True)


def _ensure_monthly_plan():
    _ensure_item()
    gateway = _stripe_gateway_reference("BRL")

    if frappe.db.exists("Subscription Plan", PLAN_NAME):
        plan = frappe.get_doc("Subscription Plan", PLAN_NAME)
    else:
        plan = frappe.new_doc("Subscription Plan")
        plan.plan_name = PLAN_NAME

    plan.product_price_id = STRIPE_PRICE_ID
    plan.cost = MONTHLY_AMOUNT
    plan.currency = "BRL"
    plan.billing_interval = "Month"
    plan.billing_interval_count = 1
    plan.item = ITEM_ID
    plan.price_determination = "Fixed Rate"
    plan.payment_gateway = gateway
    plan.save(ignore_permissions=True)


def _disable_generic_frequency_catalog():
    """Force this course to use its explicit Subscription Plan, not the generic 1-5x catalog."""
    if not frappe.db.exists("DocType", "Vedium Course Price"):
        return

    rows = frappe.get_all(
        "Vedium Course Price",
        filters={"course": COURSE_NAME},
        pluck="name",
    )
    for name in rows:
        frappe.db.set_value("Vedium Course Price", name, "enabled", 0, update_modified=False)


def _align_course():
    if not frappe.db.exists("LMS Course", COURSE_NAME):
        frappe.throw(f"LMS Course {COURSE_NAME} não encontrado.")

    updates = {
        "custom_stripe_monthly_plan": PLAN_NAME,
        "custom_stripe_annual_plan": None,
        "paid_course": 1,
    }

    meta = frappe.get_meta("LMS Course")
    if meta.has_field("currency"):
        updates["currency"] = "BRL"
    if meta.has_field("price"):
        updates["price"] = MONTHLY_AMOUNT

    frappe.db.set_value("LMS Course", COURSE_NAME, updates, update_modified=False)


def execute():
    _validate_live_stripe_price()
    _ensure_monthly_plan()
    _disable_generic_frequency_catalog()
    _align_course()
    frappe.db.commit()

    print(
        "✅ Hebraico Particular alinhado: R$450/mês, 1x/semana, "
        f"Stripe Price {STRIPE_PRICE_ID}."
    )
