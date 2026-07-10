# -*- coding: utf-8 -*-
"""Faz o checkout do LMS cobrar na moeda do curso (R$/BRL), não em dólar.

Causa do bug (achado em 2026-07-10): o Frappe LMS tem a setting
`LMS Settings.show_usd_equivalent`. Quando LIGADA, a função
`check_multicurrency` (lms/lms/utils.py) converte todo preço não-USD para
USD pela taxa de câmbio antes de montar o checkout Stripe. Resultado: um
curso de R$ 497 aparecia como US$ 97 na hora de pagar.

A Vedium é 100% Brasil e todos os cursos têm preço em BRL — a cobrança deve
ser em real. Este script desliga a conversão automática para USD.

Idempotente. Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.fix_lms_charge_currency.run

Depois: docker restart vedium-frappe (para o LMS recarregar a setting).
"""

import frappe

FIELD = "show_usd_equivalent"


def run():
    if not frappe.db.exists("DocType", "LMS Settings"):
        print("  AVISO: doctype 'LMS Settings' não existe, nada a fazer.")
        return

    if not frappe.get_meta("LMS Settings").has_field(FIELD):
        print(f"  AVISO: campo '{FIELD}' não existe em LMS Settings nesta versão do LMS.")
        print("  Verifique manualmente a config de moeda/checkout do LMS.")
        return

    before = frappe.db.get_single_value("LMS Settings", FIELD)
    frappe.db.set_single_value("LMS Settings", FIELD, 0)
    frappe.db.commit()
    after = frappe.db.get_single_value("LMS Settings", FIELD)

    print(f"  LMS Settings.{FIELD}: {before!r} -> {after!r}")
    print("  ✓ Checkout do LMS volta a cobrar na moeda do curso (BRL).")
    print("  Rode 'docker restart vedium-frappe' para recarregar a setting.")
