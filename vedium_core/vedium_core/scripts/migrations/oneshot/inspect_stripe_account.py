# -*- coding: utf-8 -*-
"""Diagnóstico do Stripe (somente leitura de conta + teste de sessão).

Usa a chave que já está no site_config.json (STRIPE_SECRET_KEY) — não muda
nenhuma config, não cobra ninguém. Serve para descobrir por que o checkout
hospedado do vedium_core (start_course_checkout) estoura em todo curso:

  1. Mostra país e moeda padrão da conta Stripe (se a conta for US/USD e não
     tiver BRL habilitado, ela recusa qualquer sessão em real).
  2. Tenta criar uma Checkout Session em BRL (R$ 497,00) — se o Stripe
     recusar, imprime a mensagem exata de erro. Criar a sessão NÃO cobra
     nada (só vira cobrança quando alguém paga); a sessão expira sozinha.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_stripe_account.run
"""

import frappe


def run():
    key = frappe.conf.get("STRIPE_SECRET_KEY")
    print("STRIPE_SECRET_KEY presente:", bool(key), "| modo:",
          "live" if str(key).startswith("sk_live") else ("test" if str(key).startswith("sk_test") else "?"))

    try:
        import stripe
    except Exception as e:
        print("FALHA ao importar 'stripe':", type(e).__name__, "|", str(e)[:200])
        return

    stripe.api_key = key

    # 1) Conta
    try:
        a = stripe.Account.retrieve()
        print("Conta:", a.get("id"))
        print("País:", a.get("country"))
        print("Moeda padrão:", a.get("default_currency"))
        caps = a.get("capabilities") or {}
        print("Capabilities (amostra):", {k: caps[k] for k in list(caps)[:8]})
    except Exception as e:
        print("Account.retrieve FALHOU ->", type(e).__name__, "|", str(e)[:250])
        return

    # 2) Tenta uma Checkout Session em BRL (não cobra nada)
    for cur in ("brl", "usd"):
        try:
            s = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": cur,
                        "product_data": {"name": "Diagnóstico Vedium"},
                        "unit_amount": 49700,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="https://vediums.com/?diag=ok",
                cancel_url="https://vediums.com/?diag=cancel",
            )
            print(f"Sessão {cur.upper()}: OK -> {s.url[:55]}...")
        except Exception as e:
            print(f"Sessão {cur.upper()}: FALHOU -> {type(e).__name__} | {str(e)[:250]}")
