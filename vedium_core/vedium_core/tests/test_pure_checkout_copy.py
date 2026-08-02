"""Pure tests for Stripe Checkout commercial copy."""

from pathlib import Path
import sys

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.stripe_billing_rules import (  # noqa: E402
    ANNUAL_CHECKOUT_NOTICE,
    build_checkout_params,
)


def _params(period):
    return build_checkout_params(
        "price_test",
        "student@example.test",
        "course-a|student@example.test",
        "https://app.example.test",
        "course-a",
        {"billing_period": period},
    )


def test_annual_checkout_explains_monthly_recurring_charge():
    params = _params("annual")
    message = params["custom_text"]["submit"]["message"]
    assert message == ANNUAL_CHECKOUT_NOTICE
    assert "valor exibido é mensal" in message
    assert "12 cobranças mensais recorrentes" in message
    assert "permanência mínima de 12 meses" in message


def test_monthly_checkout_does_not_show_annual_notice():
    assert "custom_text" not in _params("monthly")
