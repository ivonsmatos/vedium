"""Regras de meios de pagamento sem dependencias do Frappe."""


def get_stripe_payment_method_types(currency: str) -> list[str]:
    """Retorna somente os meios de pagamento aceitos pela Vedium no Stripe."""
    methods = ["card"]
    if currency.lower() == "brl":
        methods.append("boleto")
    return methods
