"""Pure contracts plus executable business-rule tests for Stripe billing."""

from datetime import date
from pathlib import Path
import sys

import pytest

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.stripe_billing_rules import (  # noqa: E402
    build_checkout_params,
    cancellation_status,
    invoice_subscription_id,
    is_active_enrollment_status,
    minimum_term_months,
    normalize_period,
    refund_access_status,
)
from vedium_core.stripe_webhook_security import construct_verified_event  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "vedium_core" / "vedium_core"
API = (CORE / "api.py").read_text(encoding="utf-8")
BILLING = (CORE / "stripe_billing.py").read_text(encoding="utf-8")
ACCESS = (CORE / "access_control.py").read_text(encoding="utf-8")
COMMUNICATION = (CORE / "communication.py").read_text(encoding="utf-8")
CUSTOM_SETUP = (CORE / "custom_setup.py").read_text(encoding="utf-8")
HOOKS = (CORE / "hooks.py").read_text(encoding="utf-8")


def test_creation_of_subscription_checkout_uses_exact_price():
    metadata = {"course_name": "course-a", "price_id": "price_exact"}
    params = build_checkout_params(
        "price_exact",
        "student@example.test",
        "course-a|student@example.test",
        "https://app.example.test",
        "course-a",
        metadata,
    )
    assert params["mode"] == "subscription"
    assert params["line_items"] == [{"price": "price_exact", "quantity": 1}]
    assert params["subscription_data"]["metadata"] == metadata
    assert "return create_subscription_checkout" in API
    assert 'duration="once"' in BILLING


def test_course_links_both_contract_plans_and_validates_missing_price():
    # plano semestral foi descontinuado (migrate_remove_semestral_add_monthly.py)
    assert "custom_stripe_semestral_plan" not in CUSTOM_SETUP
    assert "custom_stripe_annual_plan" in CUSTOM_SETUP
    assert '"options": "Subscription Plan"' in CUSTOM_SETUP
    assert 'price_id.startswith("price_")' in BILLING


def test_enrollment_after_payment_stores_subscription_state():
    for fieldname in (
        "custom_stripe_customer_id",
        "custom_stripe_subscription_id",
        "custom_stripe_price_id",
        "custom_billing_period",
        "custom_minimum_term_ends_on",
        "custom_payment_failed_on",
        "custom_stripe_last_invoice_id",
    ):
        assert fieldname in CUSTOM_SETUP
        assert fieldname in BILLING
    assert "create_enrollment_if_paid" in BILLING


@pytest.mark.parametrize(
    "event",
    (
        "checkout.session.completed",
        "invoice.paid",
        "invoice.payment_failed",
        "customer.subscription.updated",
        "customer.subscription.deleted",
        "charge.refunded",
        "charge.dispute.created",
    ),
)
def test_required_webhook_events_are_dispatched(event):
    assert event in BILLING


def test_invoice_paid_failed_and_recovery_paths_are_present():
    assert "def _invoice_paid" in BILLING
    assert "def _invoice_failed" in BILLING
    assert '"custom_payment_failed_on": None' in BILLING
    assert '"custom_vedium_status": "Cancellation Requested" if requested else "Active"' in BILLING


def test_invoice_subscription_supports_legacy_and_new_stripe_shapes():
    assert invoice_subscription_id({"subscription": "sub_legacy"}) == "sub_legacy"
    assert (
        invoice_subscription_id(
            {"parent": {"subscription_details": {"subscription": "sub_new"}}}
        )
        == "sub_new"
    )


def test_ten_day_grace_and_real_lms_block_are_wired():
    assert "GRACE_DAYS = 10" in (CORE / "stripe_billing_rules.py").read_text(
        encoding="utf-8"
    )
    assert "vedium_core.stripe_billing.suspend_overdue_enrollments" in HOOKS
    assert "has_inactive_enrollment" in (CORE / "ple_gating.py").read_text(
        encoding="utf-8"
    )
    assert "has_batch_permission" in HOOKS
    assert "has_live_class_permission" in HOOKS
    assert "require_active_course_access(course)" in ACCESS


def test_access_reactivation_and_inactive_statuses():
    assert is_active_enrollment_status("Active")
    assert is_active_enrollment_status("Trial")
    assert is_active_enrollment_status("Cancellation Requested")
    assert not is_active_enrollment_status("Suspended")
    assert not is_active_enrollment_status("Cancelled")
    assert '"Cancellation Requested"' in COMMUNICATION
    assert '"Pending Review"' in COMMUNICATION


def test_minimum_term_and_early_cancellation():
    assert normalize_period("anual") == "annual"
    assert minimum_term_months("annual") == 12
    # plano semestral foi descontinuado — normalize_period deve lançar exceção
    with pytest.raises((AssertionError, Exception)):
        minimum_term_months("semestral")
    assert cancellation_status(date(2027, 2, 1), date(2026, 8, 1)) == "Cancellation Requested"
    assert cancellation_status(date(2026, 7, 1), date(2026, 8, 1)) == "Cancelled"
    assert "request_subscription_cancellation" in BILLING
    assert "pending_review" in BILLING


def test_refund_and_dispute_rules():
    assert refund_access_status(10_000, 10_000) == "Suspended"
    assert refund_access_status(2_000, 10_000) == "Pending Review"
    assert '"Pagamento em contestação"' in BILLING


def test_duplicate_event_is_durable_and_short_circuits():
    assert '"Integration Request"' in BILLING
    assert 'row.status == "Completed"' in BILLING
    assert 'return {"duplicate": True}' in BILLING
    assert "frappe.db.commit()" in BILLING
    assert '"data"' not in BILLING.split("def _claim_event", 1)[1].split(
        "def _mark_event", 1
    )[0]


def test_invalid_webhook_signature_is_rejected():
    class Webhook:
        @staticmethod
        def construct_event(payload, signature, secret):
            raise RuntimeError("invalid signature")

    class Stripe:
        pass

    Stripe.Webhook = Webhook
    with pytest.raises(RuntimeError, match="invalid signature"):
        construct_verified_event(Stripe, "{}", "bad", "whsec_test")
    with pytest.raises(ValueError, match="stripe_signature_missing"):
        construct_verified_event(Stripe, "{}", "", "whsec_test")


def test_price_currency_and_plan_validation_are_mandatory():
    assert "SUPPORTED_CURRENCIES" in BILLING
    assert "billing_interval_count" in BILLING
    assert "stripe.Price.retrieve" in BILLING
    assert "A moeda exibida, o curso e o plano Stripe precisam ser iguais" in BILLING


def test_status_changes_use_document_save_to_trigger_lms_hooks():
    block = BILLING.split("def _save_enrollment", 1)[1].split(
        "def suspend_overdue_enrollments", 1
    )[0]
    assert "enrollment.save(ignore_permissions=True)" in block
    assert "frappe.db.set_value" not in block
