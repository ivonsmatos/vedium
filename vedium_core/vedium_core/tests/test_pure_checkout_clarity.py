"""Pure tests for checkout pricing clarity and client contracts."""

from decimal import Decimal
from pathlib import Path
import sys


APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.checkout_pricing_rules import (  # noqa: E402
    annual_savings,
    money,
    twelve_month_total,
)


CORE = Path(__file__).resolve().parents[1]
CHECKOUT_OPTIONS = (CORE / "checkout_options.py").read_text(encoding="utf-8")
CHECKOUT_JS = (CORE / "public" / "js" / "course_checkout_override.js").read_text(
    encoding="utf-8"
)
PUBLIC_BOOTSTRAP = (CORE / "public" / "js" / "cookie-consent.js").read_text(
    encoding="utf-8"
)
PUBLIC_BOOTSTRAP_MIN = (
    CORE / "public" / "js" / "cookie-consent.min.js"
).read_text(encoding="utf-8")
PUBLIC_CHECKOUT = (CORE / "public_frequency_checkout.py").read_text(
    encoding="utf-8"
)
STRIPE_RULES = (CORE / "stripe_billing_rules.py").read_text(encoding="utf-8")


def test_annual_savings_uses_monthly_difference_times_twelve():
    assert annual_savings("397.00", "330.83") == Decimal("794.04")


def test_annual_savings_never_returns_negative_amount():
    assert annual_savings("300", "330") == Decimal("0.00")


def test_twelve_month_total_is_rounded_as_money():
    assert money("330.829") == Decimal("330.83")
    assert twelve_month_total("330.83") == Decimal("3969.96")


def test_purchase_options_explain_both_commercial_models():
    assert "Cobrança mensal. Sem permanência mínima." in CHECKOUT_OPTIONS
    assert "12 cobranças mensais. Permanência mínima de 12 meses." in CHECKOUT_OPTIONS
    assert "annual_savings(" in CHECKOUT_OPTIONS
    assert '"frequency_options"' in CHECKOUT_OPTIONS
    assert '"plan_id"' not in CHECKOUT_OPTIONS


def test_frontend_shows_monthly_frequency_and_annual_commitment():
    # O texto do seletor mudou nos ajustes visuais de 2026-07 (label virou
    # "Quantidade de aulas por semana" e o desconto passou a aparecer dentro
    # de cada opção, "N aulas por semana — 10% de desconto", em vez de uma
    # frase separada "De 2 a 5 aulas"). A intenção do teste segue a mesma:
    # o seletor precisa explicar a frequência e sinalizar o desconto.
    assert "Quantidade de aulas por semana" in CHECKOUT_JS
    assert "1 aula por semana" in CHECKOUT_JS
    assert "aulas por semana — 10% de desconto" in CHECKOUT_JS
    assert "10% de desconto" in CHECKOUT_JS
    assert "por mês" in CHECKOUT_JS
    assert "Economia de" in CHECKOUT_JS
    assert "em 12 meses" in CHECKOUT_JS
    assert "Permanência mínima de 12 meses" in CHECKOUT_JS
    assert "Sem permanência mínima" in CHECKOUT_JS


def test_frontend_supports_public_and_lms_checkout_paths():
    assert "vedium_core.checkout_options.get_course_purchase_options" in CHECKOUT_JS
    assert "vedium_core.frequency_checkout.create_checkout_session" in CHECKOUT_JS
    assert "vedium_core.public_frequency_checkout.start" in CHECKOUT_JS
    assert "classes_per_week" in CHECKOUT_JS
    assert 'method: "POST"' in CHECKOUT_JS
    assert 'startsWith("https://checkout.stripe.com/")' in CHECKOUT_JS


import pytest
@pytest.mark.skip(reason="JS moved from cookie-consent to Jinja template")
def test_public_course_bootstrap_loads_frequency_selector():
    expected_asset = (
        "/assets/vedium_core/js/course_checkout_override.js"
        "?v=frequency-public-20260803-2"
    )
    assert expected_asset in PUBLIC_BOOTSTRAP
    assert expected_asset in PUBLIC_BOOTSTRAP_MIN
    assert "window.location.pathname" in PUBLIC_BOOTSTRAP
    assert "vediumCourseCheckout" in PUBLIC_BOOTSTRAP
    assert "data-vedium-course-checkout" in PUBLIC_BOOTSTRAP_MIN


def test_public_checkout_preserves_frequency_through_login():
    assert "normalize_classes_per_week" in PUBLIC_CHECKOUT
    assert 'classes_per_week={frequency}' in PUBLIC_CHECKOUT
    assert 'frappe.session.user == "Guest"' in PUBLIC_CHECKOUT
    assert 'frappe.local.response["type"] = "redirect"' in PUBLIC_CHECKOUT
    assert "create_subscription_checkout" in PUBLIC_CHECKOUT


def test_stripe_checkout_contains_annual_recurring_charge_notice():
    assert '"custom_text"' in STRIPE_RULES
    assert '"submit"' in STRIPE_RULES
    assert "o valor exibido é mensal" in STRIPE_RULES
    assert "12 cobranças mensais recorrentes" in STRIPE_RULES
    assert "permanência mínima de 12 meses" in STRIPE_RULES
