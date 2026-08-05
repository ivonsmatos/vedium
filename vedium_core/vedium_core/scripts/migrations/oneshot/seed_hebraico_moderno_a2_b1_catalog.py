import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do Hebraico Moderno A2/B1
    # 1x Mensal = R$ 447,00 (price_1TznqGJu78f2k3L09541XjDJ)
    # 1x Anual = R$ 372,50 (price_1TznqHJu78f2k3L07JGZWWsW)
    # Frequências 2x-5x:
    # Parcela anual = valor_mensal_final × 10 ÷ 12
    # Arredondar para dois centavos com ROUND_HALF_UP
    
    # Mensais (10% off para 2-5):
    # 1x: 447,00 (0% off)
    # 2x: 804,60 (10% off de 894)
    # 3x: 1206,90 (10% off de 1341)
    # 4x: 1609,20 (10% off de 1788)
    # 5x: 2011,50 (10% off de 2235)
    
    # Anuais calculados rigorosamente sobre o mensal descontado:
    # 1x: 372,50 (histórico preservado)
    # 2x: 804.60 * 10 / 12 = 670,50
    # 3x: 1206.90 * 10 / 12 = 1005,75
    # 4x: 1609.20 * 10 / 12 = 1341,00
    # 5x: 2011.50 * 10 / 12 = 1676,25
    
    config = {
        "course_name": "hebraico-moderno-a2-b1",
        "commercial_name": "Hebraico Moderno Nível A2/B1",
        "product_id": "prod_UznRiiitUJrbpj",
        "currency": "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 44700, "lookup_key": "hebraico-moderno-a2-b1_monthly", "nickname": "Vedium — Hebraico Moderno A2/B1 — Mensal — 1 aula/semana", "amount": 447.00, "subtotal": 447.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 80460, "lookup_key": "hebraico-moderno-a2-b1_monthly_2x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Mensal — 2 aulas/semana", "amount": 804.60, "subtotal": 894.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 120690, "lookup_key": "hebraico-moderno-a2-b1_monthly_3x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Mensal — 3 aulas/semana", "amount": 1206.90, "subtotal": 1341.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 160920, "lookup_key": "hebraico-moderno-a2-b1_monthly_4x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Mensal — 4 aulas/semana", "amount": 1609.20, "subtotal": 1788.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 201150, "lookup_key": "hebraico-moderno-a2-b1_monthly_5x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Mensal — 5 aulas/semana", "amount": 2011.50, "subtotal": 2235.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 37250, "lookup_key": "hebraico-moderno-a2-b1_annual", "nickname": "Vedium — Hebraico Moderno A2/B1 — Anual — 1 aula/semana", "amount": 372.50, "subtotal": 447.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 67050, "lookup_key": "hebraico-moderno-a2-b1_annual_2x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Anual — 2 aulas/semana", "amount": 670.50, "subtotal": 894.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 100575, "lookup_key": "hebraico-moderno-a2-b1_annual_3x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Anual — 3 aulas/semana", "amount": 1005.75, "subtotal": 1341.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 134100, "lookup_key": "hebraico-moderno-a2-b1_annual_4x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Anual — 4 aulas/semana", "amount": 1341.00, "subtotal": 1788.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 167625, "lookup_key": "hebraico-moderno-a2-b1_annual_5x", "nickname": "Vedium — Hebraico Moderno A2/B1 — Anual — 5 aulas/semana", "amount": 1676.25, "subtotal": 2235.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
