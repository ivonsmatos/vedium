"""Regression tests for production Stripe Checkout return URLs and notices."""

from pathlib import Path
import sys


APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.stripe_billing_rules import (  # noqa: E402
    ANNUAL_CHECKOUT_NOTICE,
    MONTHLY_CHECKOUT_NOTICE,
    build_checkout_params,
    canonical_checkout_base_url,
)


def test_checkout_prefers_frappe_site_over_reverse_proxy_host():
    metadata = {
        "site": "app.vediums.com",
        "billing_period": "annual",
    }
    params = build_checkout_params(
        "price_live",
        "student@example.com",
        "course-a|student@example.com",
        "https://vediums.com",
        "course-a",
        metadata,
    )

    assert params["success_url"] == (
        "https://app.vediums.com/lms/courses/course-a"
        "?payment=success&session_id={CHECKOUT_SESSION_ID}"
    )
    assert params["cancel_url"] == (
        "https://app.vediums.com/lms/courses/course-a?payment=cancelled"
    )


def test_checkout_rejects_invalid_site_host_and_uses_safe_fallback():
    assert canonical_checkout_base_url(
        "https://safe.example.test/",
        {"site": "https://evil.example/path"},
    ) == "https://safe.example.test"


def test_annual_checkout_explains_twelve_monthly_charges():
    params = build_checkout_params(
        "price_annual",
        "student@example.com",
        "course-a|student@example.com",
        "https://app.vediums.com",
        "course-a",
        {"site": "app.vediums.com", "billing_period": "annual"},
    )

    assert params["custom_text"]["submit"]["message"] == ANNUAL_CHECKOUT_NOTICE
    assert "12 cobranças mensais" in ANNUAL_CHECKOUT_NOTICE
    assert "permanência mínima de 12 meses" in ANNUAL_CHECKOUT_NOTICE


def test_monthly_checkout_explains_no_minimum_term():
    params = build_checkout_params(
        "price_monthly",
        "student@example.com",
        "course-a|student@example.com",
        "https://app.vediums.com",
        "course-a",
        {"site": "app.vediums.com", "billing_period": "monthly"},
    )

    assert params["custom_text"]["submit"]["message"] == MONTHLY_CHECKOUT_NOTICE
    assert "Sem permanência mínima" in MONTHLY_CHECKOUT_NOTICE
