"""Checkout endpoint with weekly class frequency for every paid course."""

from __future__ import annotations

import frappe
from frappe import _

from vedium_core.frequency_pricing_rules import normalize_classes_per_week


@frappe.whitelist()
def create_checkout_session(
    course_name,
    billing_period=None,
    classes_per_week=1,
    display_currency=None,
):
    """Create a Stripe subscription for 1 to 5 weekly classes.

    The browser only sends the selected frequency. Price, recurring discount and
    Stripe Price ID are recalculated and validated on the server.
    """
    if getattr(frappe.request, "method", "POST").upper() != "POST":
        frappe.throw(_("Método não permitido (exige POST)"), frappe.PermissionError)

    if frappe.session.user == "Guest":
        frappe.throw(_("Por favor, faça login para comprar este curso"))

    if not course_name or not frappe.db.exists("LMS Course", course_name):
        frappe.throw(_("Curso não encontrado."), frappe.DoesNotExistError)

    course = frappe.get_doc("LMS Course", course_name)
    if not course.paid_course:
        frappe.throw(_("Este curso é gratuito"))

    existing = frappe.db.exists(
        "LMS Enrollment",
        {"course": course_name, "member": frappe.session.user},
    )
    if existing:
        frappe.throw(_("Você já está inscrito neste curso"))

    try:
        frequency = normalize_classes_per_week(classes_per_week)
    except ValueError as exc:
        frappe.throw(_(str(exc)))

    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        frappe.throw(_("STRIPE_SECRET_KEY não configurada."))

    from vedium_core.stripe_billing import create_subscription_checkout

    checkout_url = create_subscription_checkout(
        course,
        frappe.session.user,
        billing_period=billing_period,
        display_currency=display_currency,
        classes_per_week=frequency,
    )
    return {"checkout_url": checkout_url}
