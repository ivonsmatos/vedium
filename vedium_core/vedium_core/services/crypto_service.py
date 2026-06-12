import frappe
import requests


class CryptoService:
    """
    Integração Coinbase Commerce — INCOMPLETA.
    Só funciona com CRYPTO_API_KEY + CRYPTO_ENABLED no site_config.json
    (o gateway 'crypto' fica fora da factory sem essas flags).
    NUNCA retorna mock: sem API key é erro de configuração, não fallback.
    """

    def __init__(self):
        self.api_key = frappe.conf.get("CRYPTO_API_KEY")
        self.base_url = "https://api.commerce.coinbase.com"

    def create_charge(self, amount, currency="USD", student_email=None):
        """
        Creates a cryptocurrency charge/payment request.
        """
        if not self.api_key:
            frappe.throw(
                "CRYPTO_API_KEY não configurado — pagamento crypto indisponível"
            )

        headers = {
            "Content-Type": "application/json",
            "X-CC-Api-Key": self.api_key,
            "X-CC-Version": "2018-03-22",
        }

        payload = {
            "name": "Vedium Course Payment",
            "description": "Payment for Language Course",
            "pricing_type": "fixed_price",
            "local_price": {"amount": str(amount), "currency": currency},
            "metadata": {"customer_email": student_email},
        }

        try:
            response = requests.post(
                f"{self.base_url}/charges", json=payload, headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            frappe.log_error(
                f"Crypto Payment Error: {e}", "Vedium.payments.crypto"
            )
            return {"error": str(e)}

    def verify_payment(self, charge_id):
        """
        Verifies the status of a crypto charge against the Coinbase API.
        Retorna o status real informado pela API (NEW/PENDING/COMPLETED/...).
        Qualquer falha → "UNKNOWN" (nunca um sucesso presumido).
        """
        if not self.api_key:
            frappe.throw(
                "CRYPTO_API_KEY não configurado — verificação crypto indisponível"
            )

        headers = {
            "X-CC-Api-Key": self.api_key,
            "X-CC-Version": "2018-03-22",
        }
        try:
            response = requests.get(
                f"{self.base_url}/charges/{charge_id}", headers=headers,
                timeout=15,
            )
            response.raise_for_status()
            timeline = response.json()["data"].get("timeline", [])
            return timeline[-1]["status"] if timeline else "UNKNOWN"
        except Exception as e:
            frappe.log_error(
                f"Crypto verify error ({charge_id}): {e}",
                "Vedium.payments.crypto",
            )
            return "UNKNOWN"
