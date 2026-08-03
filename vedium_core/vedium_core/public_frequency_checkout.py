"""Browser redirect endpoint for public course pages with weekly frequency."""

from __future__ import annotations

from urllib.parse import quote

import frappe
from frappe import _

from vedium_core.frequency_pricing_rules import normalize_classes_per_week
from vedium_core.stripe_billing_rules import normalize_period


@frappe.whitelist(allow_guest=True)
def start(
    course_name,
    billing_period=None,
    classes_per_week=1,
    display_currency=None,
):
    """Redirect a public-page visitor to login or to Stripe Checkout.

    The selected frequency is validated again on the server. Prices and the
    recurring 10% discount are never accepted from browser-calculated values.
    """
    if not course_name or not frappe.db.exists("LMS Course", course_name):
        frappe.throw(_("Curso não encontrado."), frappe.DoesNotExistError)

    period = normalize_period(billing_period)
    try:
        frequency = normalize_classes_per_week(classes_per_week)
    except ValueError as exc:
        frappe.throw(_(str(exc)))

    if frappe.session.user == "Guest":
        next_url = (
            "/api/method/vedium_core.public_frequency_checkout.start"
            f"?course_name={quote(str(course_name))}"
            f"&billing_period={quote(str(period))}"
            f"&classes_per_week={frequency}"
        )
        if display_currency:
            next_url += f"&display_currency={quote(str(display_currency))}"

        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = (
            f"/login?redirect-to={quote(next_url, safe='')}"
        )
        return

    course = frappe.get_doc("LMS Course", course_name)
    already_enrolled = frappe.db.exists(
        "LMS Enrollment",
        {"course": course_name, "member": frappe.session.user},
    )
    if already_enrolled or not course.paid_course:
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = (
            f"/lms/courses/{quote(str(course_name))}"
        )
        return

    import stripe

    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        frappe.throw(_("STRIPE_SECRET_KEY não configurada."))

    from vedium_core.stripe_billing import create_subscription_checkout

    checkout_url = create_subscription_checkout(
        course,
        frappe.session.user,
        billing_period=period,
        display_currency=display_currency,
        classes_per_week=frequency,
    )
    if not checkout_url:
        frappe.throw(_("Não foi possível criar o checkout do Stripe."))

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = checkout_url
