"""
Testes "pure" — rodam no GitHub Actions sem precisar de Frappe bench.

Cobrem a lógica de cálculo de preço com cupom (que é a parte mais
sensível do api.create_checkout) isolada de qualquer chamada a DB
ou gateway externo.

Convenção: arquivos test_pure_*.py rodam no CI (workflows/test.yml).
Arquivos test_*.py (sem o prefixo "pure") são para integração com bench.
"""

from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from vedium_core.payment_methods import get_stripe_payment_method_types  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers replicando a lógica de api.create_checkout (preço + cupom).
# Mantemos puros para evitar import de frappe nos testes do CI.
# ---------------------------------------------------------------------------
def apply_coupon(course_price: float, coupon: dict | None, now=None) -> tuple[float, bool, str | None]:
    """
    Aplica desconto de cupom seguindo a mesma lógica de api.create_checkout.

    Retorna (final_price, coupon_valid, coupon_msg).
    Coupon_msg é None se cupom OK ou inexistente; string descritiva no erro.
    """
    now = now or datetime.now()
    if not coupon:
        return round(float(course_price), 2), False, None

    if not coupon.get("active"):
        return round(float(course_price), 2), False, "Cupom inválido ou expirado"

    valid_from = coupon.get("valid_from")
    valid_to = coupon.get("valid_to")
    if valid_from and valid_from > now:
        return round(float(course_price), 2), False, "Cupom inválido ou expirado"
    if valid_to and valid_to < now:
        return round(float(course_price), 2), False, "Cupom inválido ou expirado"

    max_uses = coupon.get("max_uses")
    used_count = coupon.get("used_count") or 0
    if max_uses and used_count >= max_uses:
        return round(float(course_price), 2), False, "Cupom já atingiu o limite de uso"

    discount = float(coupon.get("discount_percent") or 0)
    if discount <= 0:
        return round(float(course_price), 2), False, None

    final = round(float(course_price) * (1 - discount / 100), 2)
    return final, True, None


# ---------------------------------------------------------------------------
# Casos
# ---------------------------------------------------------------------------
class TestCouponApplication:
    def test_no_coupon_returns_full_price(self):
        final, valid, msg = apply_coupon(320.00, None)
        assert final == 320.00
        assert valid is False
        assert msg is None

    def test_active_10_percent(self):
        coupon = {"active": True, "discount_percent": 10}
        final, valid, _ = apply_coupon(320.00, coupon)
        assert final == 288.00
        assert valid is True

    def test_active_50_percent_rounds_to_cents(self):
        coupon = {"active": True, "discount_percent": 50}
        # Caso simples sem rounding ambíguo (333.33*0.5 cai em half-to-even).
        final, valid, _ = apply_coupon(199.90, coupon)
        assert final == 99.95
        assert valid is True

    def test_inactive_coupon_rejected(self):
        coupon = {"active": False, "discount_percent": 10}
        final, valid, msg = apply_coupon(320.00, coupon)
        assert final == 320.00
        assert valid is False
        assert msg == "Cupom inválido ou expirado"

    def test_expired_coupon_rejected(self):
        coupon = {
            "active": True,
            "discount_percent": 10,
            "valid_to": datetime.now() - timedelta(days=1),
        }
        final, valid, msg = apply_coupon(320.00, coupon)
        assert final == 320.00
        assert valid is False
        assert msg == "Cupom inválido ou expirado"

    def test_not_yet_valid_coupon_rejected(self):
        coupon = {
            "active": True,
            "discount_percent": 10,
            "valid_from": datetime.now() + timedelta(days=1),
        }
        final, valid, _ = apply_coupon(320.00, coupon)
        assert final == 320.00
        assert valid is False

    def test_max_uses_reached(self):
        coupon = {
            "active": True,
            "discount_percent": 20,
            "max_uses": 10,
            "used_count": 10,
        }
        final, valid, msg = apply_coupon(320.00, coupon)
        assert final == 320.00
        assert valid is False
        assert msg == "Cupom já atingiu o limite de uso"

    def test_max_uses_not_reached(self):
        coupon = {
            "active": True,
            "discount_percent": 20,
            "max_uses": 10,
            "used_count": 9,
        }
        final, valid, _ = apply_coupon(320.00, coupon)
        assert final == 256.00
        assert valid is True

    def test_zero_discount_no_op(self):
        coupon = {"active": True, "discount_percent": 0}
        final, valid, _ = apply_coupon(320.00, coupon)
        assert final == 320.00
        assert valid is False

    def test_negative_discount_no_op(self):
        # Defensivo: cupom corrompido com discount negativo não inflaciona preço
        coupon = {"active": True, "discount_percent": -10}
        final, valid, _ = apply_coupon(320.00, coupon)
        assert final == 320.00
        assert valid is False


class TestStripePaymentMethods:
    def test_brl_accepts_card_and_boleto_without_pix(self):
        methods = get_stripe_payment_method_types("BRL")

        assert methods == ["card", "boleto"]
        assert "pix" not in methods

    def test_other_currencies_accept_only_card(self):
        assert get_stripe_payment_method_types("USD") == ["card"]


# ---------------------------------------------------------------------------
# Parsing do external_reference do MercadoPago (course|user[|coupon]).
# Replica a lógica do MercadoPagoGateway.handle_webhook — formato de 3
# segmentos carrega o cupom; o de 2 é o legado (preferences criadas antes
# do deploy do cupom rastreável, que ainda podem gerar webhooks).
# ---------------------------------------------------------------------------
def parse_external_reference(external_ref: str) -> tuple[str, str, str | None]:
    parts = external_ref.split("|")
    if len(parts) < 2:
        raise ValueError(external_ref)
    course_name, user = parts[0], parts[1]
    coupon_code = parts[2] if len(parts) > 2 and parts[2] else None
    return course_name, user, coupon_code


class TestExternalReferenceParsing:
    def test_legacy_two_segments(self):
        course, user, coupon = parse_external_reference(
            "ingles-beginner|aluno@vediums.com"
        )
        assert course == "ingles-beginner"
        assert user == "aluno@vediums.com"
        assert coupon is None

    def test_three_segments_with_coupon(self):
        course, user, coupon = parse_external_reference(
            "ingles-beginner|aluno@vediums.com|PROMO10"
        )
        assert course == "ingles-beginner"
        assert user == "aluno@vediums.com"
        assert coupon == "PROMO10"

    def test_three_segments_empty_coupon(self):
        # Checkout sem cupom gera "course|user|" — cupom deve ser None
        course, user, coupon = parse_external_reference(
            "ingles-beginner|aluno@vediums.com|"
        )
        assert course == "ingles-beginner"
        assert user == "aluno@vediums.com"
        assert coupon is None

    def test_single_segment_raises(self):
        import pytest

        with pytest.raises(ValueError):
            parse_external_reference("garbage-no-separator")
