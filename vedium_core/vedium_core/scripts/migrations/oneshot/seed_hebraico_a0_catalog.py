import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do Hebraico A0 Alfabetização
    # 1x Mensal = R$ 197,00 (price_1TznqHJu78f2k3L0R5FQxHDg)
    # 1x Anual = R$ 164,16 (price_1TznqIJu78f2k3L0IM5UQbt9)
    # Frequências 2x-5x:
    # Parcela anual = valor_mensal_final × 10 ÷ 12
    # Arredondar para dois centavos com ROUND_HALF_UP
    
    # Mensais (10% off para 2-5):
    # 1x: 197,00 (0% off)
    # 2x: 354,60 (10% off de 394)
    # 3x: 531,90 (10% off de 591)
    # 4x: 709,20 (10% off de 788)
    # 5x: 886,50 (10% off de 985)
    
    # Anuais calculados rigorosamente sobre o mensal descontado:
    # 1x: 164,16 (histórico preservado)
    # 2x: 354.60 * 10 / 12 = 295,50
    # 3x: 531.90 * 10 / 12 = 443,25
    # 4x: 709.20 * 10 / 12 = 591,00
    # 5x: 886.50 * 10 / 12 = 738,75
    
    config = {
        "course_name": "hebraico-a0-alfabetizacao",
        "commercial_name": "Hebraico A0 Alfabetização",
        "product_id": "prod_UznRs3ValZEHMB",
        "currency": "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 19700, "lookup_key": "hebraico-a0-alfabetizacao_monthly", "nickname": "Vedium — Hebraico A0 — Mensal — 1 aula/semana", "amount": 197.00, "subtotal": 197.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 35460, "lookup_key": "hebraico-a0-alfabetizacao_monthly_2x", "nickname": "Vedium — Hebraico A0 — Mensal — 2 aulas/semana", "amount": 354.60, "subtotal": 394.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 53190, "lookup_key": "hebraico-a0-alfabetizacao_monthly_3x", "nickname": "Vedium — Hebraico A0 — Mensal — 3 aulas/semana", "amount": 531.90, "subtotal": 591.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 70920, "lookup_key": "hebraico-a0-alfabetizacao_monthly_4x", "nickname": "Vedium — Hebraico A0 — Mensal — 4 aulas/semana", "amount": 709.20, "subtotal": 788.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 88650, "lookup_key": "hebraico-a0-alfabetizacao_monthly_5x", "nickname": "Vedium — Hebraico A0 — Mensal — 5 aulas/semana", "amount": 886.50, "subtotal": 985.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 16416, "lookup_key": "hebraico-a0-alfabetizacao_annual", "nickname": "Vedium — Hebraico A0 — Anual — 1 aula/semana", "amount": 164.16, "subtotal": 197.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 29550, "lookup_key": "hebraico-a0-alfabetizacao_annual_2x", "nickname": "Vedium — Hebraico A0 — Anual — 2 aulas/semana", "amount": 295.50, "subtotal": 394.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 44325, "lookup_key": "hebraico-a0-alfabetizacao_annual_3x", "nickname": "Vedium — Hebraico A0 — Anual — 3 aulas/semana", "amount": 443.25, "subtotal": 591.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 59100, "lookup_key": "hebraico-a0-alfabetizacao_annual_4x", "nickname": "Vedium — Hebraico A0 — Anual — 4 aulas/semana", "amount": 591.00, "subtotal": 788.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 73875, "lookup_key": "hebraico-a0-alfabetizacao_annual_5x", "nickname": "Vedium — Hebraico A0 — Anual — 5 aulas/semana", "amount": 738.75, "subtotal": 985.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
