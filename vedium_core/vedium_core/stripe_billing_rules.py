"""Pure business rules shared by Stripe billing and its unit tests."""

from __future__ import annotations

import re
from datetime import date, datetime


GRACE_DAYS = 10
ACTIVE_ENROLLMENT_STATUSES = {
    "active",
    "trial",
    "cancellation requested",
    "pending review",
}
SUPPORTED_CURRENCIES = {"BRL", "USD"}
MONTHLY_CHECKOUT_NOTICE = (
    "Plano mensal selecionado: o valor exibido será cobrado mensalmente. "
    "Sem permanência mínima. O cancelamento segue os Termos da Vedium."
)
ANNUAL_CHECKOUT_NOTICE = (
    "Plano anual selecionado: o valor exibido é mensal. "
    "Ao assinar, você autoriza 12 cobranças mensais recorrentes no método "
    "de pagamento escolhido, com permanência mínima de 12 meses."
)
_SITE_HOST_PATTERN = re.compile(
    r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$",
    re.IGNORECASE,
)


def normalize_period(value=None) -> str:
    value = (value or "monthly").strip().lower()
    if value in {"semestral", "semiannual", "semi-annual"}:
        import frappe

        frappe.throw(
            "O plano semestral foi descontinuado. "
            "Escolha o Plano Mensal ou o Plano Anual."
        )
    return "annual" if value in {"annual", "yearly", "anual"} else "monthly"


def minimum_term_months(period) -> int:
    return 12 if normalize_period(period) == "annual" else 0


def is_active_enrollment_status(status) -> bool:
    return (status or "Active").strip().lower() in ACTIVE_ENROLLMENT_STATUSES


def invoice_subscription_id(invoice) -> str | None:
    """Support both legacy and newer Stripe invoice payload shapes."""
    subscription_id = invoice.get("subscription")
    if subscription_id:
        return subscription_id
    parent = invoice.get("parent") or {}
    details = parent.get("subscription_details") or {}
    return details.get("subscription")


def cancellation_status(minimum_term_ends_on, on_date=None) -> str:
    """Keep early cancellations pending; cancel only after the minimum term."""
    if not minimum_term_ends_on:
        return "Cancelled"
    if isinstance(minimum_term_ends_on, datetime):
        minimum_term_ends_on = minimum_term_ends_on.date()
    if isinstance(minimum_term_ends_on, str):
        minimum_term_ends_on = date.fromisoformat(minimum_term_ends_on)
    on_date = on_date or date.today()
    if isinstance(on_date, datetime):
        on_date = on_date.date()
    return (
        "Cancellation Requested"
        if on_date < minimum_term_ends_on
        else "Cancelled"
    )


def refund_access_status(amount_refunded, amount) -> str:
    """A full refund suspends access; a partial refund requires manual review."""
    amount_refunded = int(amount_refunded or 0)
    amount = int(amount or 0)
    return (
        "Suspended"
        if amount > 0 and amount_refunded >= amount
        else "Pending Review"
    )


def canonical_checkout_base_url(base_url, metadata=None) -> str:
    """Prefer the Frappe site hostname over a reverse-proxy host header.

    Production requests can arrive through ``vediums.com`` even though the
    authenticated LMS site is ``app.vediums.com``. The site value is generated
    server-side and stored in Checkout metadata, so it is the authoritative
    return host when it is a valid DNS hostname.
    """
    site = str((metadata or {}).get("site") or "").strip().lower()
    if "." in site and _SITE_HOST_PATTERN.fullmatch(site):
        return f"https://{site}"
    return str(base_url or "").rstrip("/")


def build_checkout_params(
    price_id,
    email,
    reference,
    base_url,
    course_name,
    metadata,
):
    """Build the side-effect-free Stripe Checkout request."""
    checkout_base_url = canonical_checkout_base_url(base_url, metadata)
    period = normalize_period((metadata or {}).get("billing_period"))
    notice = (
        ANNUAL_CHECKOUT_NOTICE
        if period == "annual"
        else MONTHLY_CHECKOUT_NOTICE
    )

    return {
        "mode": "subscription",
        "line_items": [{"price": price_id, "quantity": 1}],
        "customer_email": email,
        "client_reference_id": reference,
        "success_url": (
            f"{checkout_base_url}/lms/courses/{course_name}"
            "?payment=success&session_id={CHECKOUT_SESSION_ID}"
        ),
        "cancel_url": (
            f"{checkout_base_url}/lms/courses/{course_name}"
            "?payment=cancelled"
        ),
        "metadata": metadata,
        "subscription_data": {"metadata": metadata},
        "custom_text": {
            "submit": {
                "message": notice,
            }
        },
    }
