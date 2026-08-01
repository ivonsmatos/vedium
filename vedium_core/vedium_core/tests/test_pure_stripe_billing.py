"""Contratos puros da integração recorrente Stripe/Frappe."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"
API = (CORE / "api.py").read_text(encoding="utf-8")
BILLING = (CORE / "stripe_billing.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_checkout_uses_recurring_stripe_price():
    assert 'mode="subscription"' in BILLING
    assert 'line_items=[{"price": price_id, "quantity": 1}]' in BILLING
    assert "return create_subscription_checkout" in API
    assert 'duration="once"' in BILLING


def test_course_links_both_contract_plans():
    assert "custom_stripe_semestral_plan" in CUSTOM_SETUP
    assert "custom_stripe_annual_plan" in CUSTOM_SETUP
    assert '"options": "Subscription Plan"' in CUSTOM_SETUP


def test_enrollment_stores_subscription_state():
    for fieldname in (
        "custom_stripe_customer_id",
        "custom_stripe_subscription_id",
        "custom_stripe_price_id",
        "custom_billing_period",
        "custom_minimum_term_ends_on",
        "custom_payment_failed_on",
    ):
        assert fieldname in CUSTOM_SETUP


def test_required_webhook_events_are_dispatched():
    for event in (
        "checkout.session.completed",
        "invoice.paid",
        "invoice.payment_failed",
        "customer.subscription.updated",
        "customer.subscription.deleted",
        "charge.refunded",
        "charge.dispute.created",
    ):
        assert event in BILLING


def test_ten_day_grace_period_is_scheduled():
    assert "GRACE_DAYS = 10" in BILLING
    assert "vedium_core.stripe_billing.suspend_overdue_enrollments" in HOOKS
