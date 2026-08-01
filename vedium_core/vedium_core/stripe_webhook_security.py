"""Small, testable Stripe webhook signature boundary."""


def construct_verified_event(stripe_module, payload, signature, webhook_secret):
    if not webhook_secret:
        raise ValueError("stripe_webhook_secret_missing")
    if not signature:
        raise ValueError("stripe_signature_missing")
    return stripe_module.Webhook.construct_event(payload, signature, webhook_secret)
