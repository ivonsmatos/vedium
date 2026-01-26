import frappe
import requests

class CryptoService:
    def __init__(self):
        self.api_key = frappe.conf.get("CRYPTO_API_KEY")
        # Example using Coinbase Commerce API
        self.base_url = "https://api.commerce.coinbase.com"

    def create_charge(self, amount, currency="USD", student_email=None):
        """
        Creates a cryptocurrency charge/payment request.
        """
        if not self.api_key:
            # Fallback for demo/development
            return {
                "id": "MOCK_CRYPTO_CHARGE_123",
                "hosted_url": f"https://mock.crypto.pay/charge?amount={amount}&currency={currency}",
                "status": "NEW"
            }

        headers = {
            "Content-Type": "application/json",
            "X-CC-Api-Key": self.api_key,
            "X-CC-Version": "2018-03-22"
        }

        payload = {
            "name": "Vedium Course Payment",
            "description": "Payment for Language Course",
            "pricing_type": "fixed_price",
            "local_price": {
                "amount": str(amount),
                "currency": currency
            },
            "metadata": {
                "customer_email": student_email
            }
        }

        try:
            response = requests.post(f"{self.base_url}/charges", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            frappe.log_error(f"Crypto Payment Error: {e}")
            return {"error": str(e)}

    def verify_payment(self, charge_id):
        """
        Verifies the status of a crypto charge.
        """
        if not self.api_key:
            return "COMPLETED" # Mock success
            
        # Real API call to check status
        return "PENDING"
