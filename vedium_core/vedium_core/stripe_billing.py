"""Cobrança recorrente Stripe e sincronização de acesso ao LMS."""

from datetime import timedelta

import frappe
from frappe import _
from frappe.utils import add_months, now_datetime, today


GRACE_DAYS = 10
ACTIVE_STATUSES = {"active", "trialing"}
INACTIVE_STATUSES = {"canceled", "unpaid", "incomplete_expired", "paused"}


def normalize_period(value=None):
    value = (value or "semestral").strip().lower()
    return "annual" if value in {"annual", "yearly", "anual"} else "semestral"


def minimum_term_months(period):
    return 12 if normalize_period(period) == "annual" else 6


def get_subscription_price(course, period):
    period = normalize_period(period)
    field = "custom_stripe_annual_plan" if period == "annual" else "custom_stripe_semestral_plan"
    plan_name = getattr(course, field, None)
    if not plan_name:
        frappe.throw(_("O curso ainda não possui plano Stripe {0} vinculado.").format(period))
    plan = frappe.get_doc("Subscription Plan", plan_name)
    price_id = getattr(plan, "product_price_id", None)
    if not price_id:
        frappe.throw(_("O plano {0} não possui Product Price ID.").format(plan_name))
    return price_id


def create_subscription_checkout(course, user, coupon_code=None, billing_period=None):
    """Cria Checkout recorrente usando o price_id auditado no Frappe."""
    import stripe

    period = normalize_period(billing_period)
    price_id = get_subscription_price(course, period)
    email = frappe.db.get_value("User", user, "email") or user
    base_url = frappe.utils.get_url()
    metadata = {
        "course_name": str(course.name),
        "user": str(user),
        "site": str(frappe.local.site),
        "coupon_code": coupon_code or "",
        "billing_period": period,
        "minimum_term_months": str(minimum_term_months(period)),
        "price_id": price_id,
    }
    params = dict(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        customer_email=email,
        client_reference_id=f"{course.name}|{user}",
        success_url=f"{base_url}/lms/courses/{course.name}?payment=success&session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{base_url}/lms/courses/{course.name}?payment=cancelled",
        metadata=metadata,
        subscription_data={"metadata": metadata},
    )
    discount = _discount_percent(coupon_code, user)
    if discount:
        stripe_coupon = stripe.Coupon.create(
            percent_off=discount,
            duration="once",
            name=f"Vedium {coupon_code}",
            metadata={"vedium_coupon_code": coupon_code, "site": frappe.local.site},
        )
        params["discounts"] = [{"coupon": stripe_coupon.id}]
    session = stripe.checkout.Session.create(**params)
    return session.url


def _discount_percent(coupon_code, user):
    """Retorna o desconto já elegível; aplicado só na primeira mensalidade."""
    if not coupon_code:
        return 0
    coupon = frappe.db.get_value(
        "Coupon", coupon_code,
        ["discount_percent", "active", "max_uses", "used_count", "valid_from", "valid_to"],
        as_dict=True,
    )
    now = now_datetime()
    if coupon:
        valid = coupon.active and (not coupon.valid_from or coupon.valid_from <= now) and (not coupon.valid_to or coupon.valid_to >= now)
        available = not coupon.max_uses or (coupon.used_count or 0) < coupon.max_uses
        return float(coupon.discount_percent or 0) if valid and available else 0

    from vedium_core.referrals import validate_referral_code

    referral = validate_referral_code(coupon_code, referee=user)
    return float(referral.discount_percent or 0) if referral else 0


def handle_stripe_event(event):
    event_type = event.get("type")
    obj = event.get("data", {}).get("object", {})
    if event_type == "checkout.session.completed":
        _checkout_completed(obj)
    elif event_type == "invoice.paid":
        _invoice_paid(obj)
    elif event_type == "invoice.payment_failed":
        _invoice_failed(obj)
    elif event_type == "customer.subscription.updated":
        _subscription_updated(obj)
    elif event_type == "customer.subscription.deleted":
        _set_access(obj.get("id"), "Cancelled", "Assinatura cancelada na Stripe")
    elif event_type == "charge.refunded" and obj.get("refunded"):
        _charge_event(obj, "Suspended", "Pagamento integralmente reembolsado")
    elif event_type == "charge.dispute.created":
        _charge_event(obj, "Suspended", "Pagamento em contestação")


def _checkout_completed(session):
    if session.get("mode") != "subscription":
        return  # compatibilidade com sessões avulsas antigas
    if session.get("payment_status") not in {"paid", "no_payment_required"}:
        return
    metadata = session.get("metadata") or {}
    course_name, user = _validated_reference(session, metadata)
    subscription_id = session.get("subscription")
    if not subscription_id:
        frappe.throw(_("Checkout sem assinatura Stripe"))

    from vedium_core.api import create_enrollment_if_paid

    name = frappe.db.exists("LMS Enrollment", {"course": course_name, "member": user})
    if not name:
        create_enrollment_if_paid(
            course_name, user, "stripe", subscription_id,
            (session.get("amount_total") or 0) / 100,
            (session.get("currency") or "brl").upper(),
            metadata.get("coupon_code") or None,
        )
        name = frappe.db.exists("LMS Enrollment", {"course": course_name, "member": user})
    period = normalize_period(metadata.get("billing_period"))
    frappe.db.set_value("LMS Enrollment", name, {
        "custom_stripe_customer_id": session.get("customer"),
        "custom_stripe_subscription_id": subscription_id,
        "custom_stripe_price_id": metadata.get("price_id"),
        "custom_billing_period": period,
        "custom_minimum_term_ends_on": add_months(today(), minimum_term_months(period)),
        "custom_payment_failed_on": None,
        "custom_vedium_status": "Active",
        "custom_vedium_status_changed_on": now_datetime(),
        "custom_vedium_status_reason": "Assinatura Stripe ativa",
    })


def _validated_reference(session, metadata):
    try:
        course_name, user = (session.get("client_reference_id") or "").split("|", 1)
    except ValueError:
        frappe.throw(_("Referência Stripe inválida"), frappe.AuthenticationError)
    checks = (("site", frappe.local.site), ("course_name", course_name), ("user", user))
    if any(metadata.get(key) and metadata.get(key) != expected for key, expected in checks):
        frappe.throw(_("Metadados Stripe inválidos"), frappe.AuthenticationError)
    return course_name, user


def _find_enrollment(subscription_id):
    if not subscription_id:
        return None
    return frappe.db.get_value("LMS Enrollment", {"custom_stripe_subscription_id": subscription_id}, "name")


def _invoice_paid(invoice):
    name = _find_enrollment(invoice.get("subscription"))
    if name:
        frappe.db.set_value("LMS Enrollment", name, {
            "custom_payment_failed_on": None,
            "custom_vedium_status": "Active",
            "custom_vedium_status_changed_on": now_datetime(),
            "custom_vedium_status_reason": "Mensalidade confirmada pela Stripe",
            "payment_reference": invoice.get("payment_intent") or invoice.get("id"),
        })


def _invoice_failed(invoice):
    name = _find_enrollment(invoice.get("subscription"))
    if name and not frappe.db.get_value("LMS Enrollment", name, "custom_payment_failed_on"):
        frappe.db.set_value("LMS Enrollment", name, {
            "custom_payment_failed_on": now_datetime(),
            "custom_vedium_status_reason": "Falha de pagamento; tolerância de 10 dias iniciada",
        })


def _subscription_updated(subscription):
    status = subscription.get("status")
    if status in ACTIVE_STATUSES:
        _set_access(subscription.get("id"), "Active", "Assinatura ativa na Stripe", True)
    elif status in INACTIVE_STATUSES:
        target = "Cancelled" if status == "canceled" else "Suspended"
        _set_access(subscription.get("id"), target, f"Assinatura Stripe: {status}")


def _charge_event(charge, status, reason):
    if not charge.get("invoice"):
        return
    import stripe
    invoice = stripe.Invoice.retrieve(charge.get("invoice"))
    _set_access(invoice.get("subscription"), status, reason)


def _set_access(subscription_id, status, reason, clear_failure=False):
    name = _find_enrollment(subscription_id)
    if not name:
        return
    values = {
        "custom_vedium_status": status,
        "custom_vedium_status_changed_on": now_datetime(),
        "custom_vedium_status_reason": reason,
    }
    if clear_failure:
        values["custom_payment_failed_on"] = None
    frappe.db.set_value("LMS Enrollment", name, values)


def suspend_overdue_enrollments():
    cutoff = now_datetime() - timedelta(days=GRACE_DAYS)
    names = frappe.get_all("LMS Enrollment", filters={
        "custom_payment_failed_on": ["<=", cutoff],
        "custom_vedium_status": ["in", ["Active", "Trial"]],
    }, pluck="name")
    for name in names:
        frappe.db.set_value("LMS Enrollment", name, {
            "custom_vedium_status": "Suspended",
            "custom_vedium_status_changed_on": now_datetime(),
            "custom_vedium_status_reason": "Pagamento não regularizado após 10 dias",
        })
    return len(names)
