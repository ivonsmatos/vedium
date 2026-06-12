"""
Testes "pure" para verificação de assinatura HMAC do MercadoPago.

Replica a lógica de api.handle_payment_webhook (gateway=mercadopago)
sem precisar de Frappe bench. Garante que mudanças no algoritmo de
assinatura não passam despercebidas.
"""

import hashlib
import hmac


def verify_mercadopago_signature(
    sig_header: str,
    request_id: str,
    data_id: str,
    secret: str,
) -> bool:
    """
    Replica o algoritmo de api.handle_payment_webhook para MercadoPago:

    1. Parse "ts=<ts>,v1=<hmac>" do header X-Signature.
    2. Manifest = "id:<data_id>;request-id:<request_id>;ts:<ts>"
    3. expected = HMAC-SHA256(secret, manifest)
    4. Comparação constant-time com v1.
    """
    try:
        parts = {k: v for k, v in (p.split("=", 1) for p in sig_header.split(","))}
        ts = parts.get("ts", "")
        v1 = parts.get("v1", "")
        manifest = f"id:{data_id};request-id:{request_id};ts:{ts}"
        expected = hmac.new(
            secret.encode(), manifest.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, v1)
    except Exception:
        return False


def _make_signature(ts: str, data_id: str, request_id: str, secret: str) -> str:
    manifest = f"id:{data_id};request-id:{request_id};ts:{ts}"
    v1 = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
    return f"ts={ts},v1={v1}"


class TestMercadoPagoSignature:
    SECRET = "test-secret-do-not-use-in-prod"

    def test_valid_signature_passes(self):
        sig = _make_signature("1700000000", "pay_123", "req_abc", self.SECRET)
        assert (
            verify_mercadopago_signature(sig, "req_abc", "pay_123", self.SECRET)
            is True
        )

    def test_wrong_secret_fails(self):
        sig = _make_signature("1700000000", "pay_123", "req_abc", self.SECRET)
        assert (
            verify_mercadopago_signature(sig, "req_abc", "pay_123", "outro-secret")
            is False
        )

    def test_tampered_data_id_fails(self):
        sig = _make_signature("1700000000", "pay_123", "req_abc", self.SECRET)
        # Atacante troca o ID do pagamento mantendo assinatura
        assert (
            verify_mercadopago_signature(sig, "req_abc", "pay_999", self.SECRET)
            is False
        )

    def test_tampered_request_id_fails(self):
        sig = _make_signature("1700000000", "pay_123", "req_abc", self.SECRET)
        assert (
            verify_mercadopago_signature(sig, "req_xxx", "pay_123", self.SECRET)
            is False
        )

    def test_malformed_header_fails(self):
        assert (
            verify_mercadopago_signature("garbage", "req_abc", "pay_123", self.SECRET)
            is False
        )

    def test_missing_v1_fails(self):
        assert (
            verify_mercadopago_signature(
                "ts=1700000000", "req_abc", "pay_123", self.SECRET
            )
            is False
        )

    def test_empty_string_fails(self):
        assert (
            verify_mercadopago_signature("", "req_abc", "pay_123", self.SECRET)
            is False
        )
