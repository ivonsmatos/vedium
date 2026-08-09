"""Testes "pure" do programa de indicação — espelham a lógica de
referrals.validate_referral_code / record_referral_conversion sem
nenhuma chamada a frappe/DB, seguindo a convenção de test_pure_payments.py.
"""

from pathlib import Path

_REFERRALS = (
    Path(__file__).resolve().parents[1] / "referrals.py"
).read_text(encoding="utf-8")


class TestReferralCrmSourceAndMetrics:
    def test_source_bug_fixed_uses_valid_link(self):
        """O bug latente era `lead.source = "Indicação"` (acentuado) — origem
        inexistente no CRM Lead Source (o válido é "Indicacao") → insert falhava.
        Agora resolve para uma origem VÁLIDA."""
        assert 'lead.source = "Indicação"' not in _REFERRALS
        assert 'resolve_lead_source("referral")' in _REFERRALS

    def test_referral_metrics_exists_for_measurement(self):
        assert "def referral_metrics(" in _REFERRALS
        assert "conversions" in _REFERRALS and "referred_mrr" in _REFERRALS


# ---------------------------------------------------------------------------
# Espelha referrals.validate_referral_code (anti-abuso: ninguém usa o
# próprio código; código inativo é rejeitado).
# ---------------------------------------------------------------------------
def validate_referral(referral: dict | None, referee: str | None = None):
    if not referral or not referral.get("active"):
        return None
    if referee and referral.get("referrer") == referee:
        return None
    return referral


class TestReferralCodeValidation:
    def test_no_referral_returns_none(self):
        assert validate_referral(None) is None

    def test_inactive_referral_rejected(self):
        referral = {"referrer": "amigo@vediums.com", "active": False}
        assert validate_referral(referral, referee="aluno@vediums.com") is None

    def test_active_referral_accepted(self):
        referral = {"referrer": "amigo@vediums.com", "active": True, "discount_percent": 10}
        result = validate_referral(referral, referee="aluno@vediums.com")
        assert result is not None
        assert result["discount_percent"] == 10

    def test_self_referral_rejected(self):
        referral = {"referrer": "aluno@vediums.com", "active": True, "discount_percent": 10}
        assert validate_referral(referral, referee="aluno@vediums.com") is None

    def test_self_referral_without_referee_check_is_accepted(self):
        # Sem referee informado (ex.: validação fora do contexto de checkout),
        # não há como checar auto-indicação — comportamento documentado.
        referral = {"referrer": "amigo@vediums.com", "active": True, "discount_percent": 10}
        assert validate_referral(referral, referee=None) is not None


# ---------------------------------------------------------------------------
# Espelha o desconto aplicado no checkout quando o coupon_code é, na
# verdade, um Referral (mesma fórmula de api.create_checkout/apply_coupon).
# ---------------------------------------------------------------------------
def apply_referral_discount(course_price: float, discount_percent: float) -> float:
    return round(float(course_price) * (1 - float(discount_percent) / 100), 2)


class TestReferralDiscountMath:
    def test_ten_percent_discount(self):
        assert apply_referral_discount(320.00, 10) == 288.00

    def test_zero_percent_is_noop(self):
        assert apply_referral_discount(320.00, 0) == 320.00


# ---------------------------------------------------------------------------
# Espelha a regra anti-abuso de record_referral_conversion: cada referee só
# gera recompensa uma vez, mesmo reusando o código em outra compra.
# ---------------------------------------------------------------------------
def should_grant_reward(referee: str, existing_conversions: set[str]) -> bool:
    return referee not in existing_conversions


class TestRewardAntiAbuse:
    def test_first_conversion_grants_reward(self):
        assert should_grant_reward("amigo@vediums.com", set()) is True

    def test_repeat_referee_does_not_grant_again(self):
        assert should_grant_reward("amigo@vediums.com", {"amigo@vediums.com"}) is False
