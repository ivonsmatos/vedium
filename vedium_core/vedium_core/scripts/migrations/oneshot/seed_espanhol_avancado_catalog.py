import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do Avançado
    # 1x Mensal = R$ 497,00
    # 1x Anual = R$ 414,16 (histórico, imutável)
    # Frequências 2x-5x:
    # Parcela anual = valor_mensal_final × 10 ÷ 12
    # Arredondar para dois centavos com ROUND_HALF_UP
    
    # Mensais (10% off para 2-5):
    # 1x: 497,00 (0% off)
    # 2x: 894,60 (10% off de 994)
    # 3x: 1341,90 (10% off de 1491)
    # 4x: 1789,20 (10% off de 1988)
    # 5x: 2236,50 (10% off de 2485)
    
    # Anuais calculados rigorosamente:
    # 1x: 414,16
    # 2x: 894.60 * 10 / 12 = 745,50
    # 3x: 1341.90 * 10 / 12 = 1118,25
    # 4x: 1789.20 * 10 / 12 = 1491,00
    # 5x: 2236.50 * 10 / 12 = 1863,75
    
    config = {
        "course_name": "espanhol-avancado",
        "commercial_name": "Espanhol Nível Avançado (B2.2-C1)",
        "product_id": "prod_UznR52w5UCsZsw",
        "currency": "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 49700, "lookup_key": "espanhol-avancado_monthly", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Mensal — 1 aula/semana", "amount": 497.00, "subtotal": 497.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 89460, "lookup_key": "espanhol-avancado_monthly_2x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Mensal — 2 aulas/semana", "amount": 894.60, "subtotal": 994.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 134190, "lookup_key": "espanhol-avancado_monthly_3x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Mensal — 3 aulas/semana", "amount": 1341.90, "subtotal": 1491.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 178920, "lookup_key": "espanhol-avancado_monthly_4x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Mensal — 4 aulas/semana", "amount": 1789.20, "subtotal": 1988.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 223650, "lookup_key": "espanhol-avancado_monthly_5x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Mensal — 5 aulas/semana", "amount": 2236.50, "subtotal": 2485.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 41416, "lookup_key": "espanhol-avancado_annual", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Anual — 1 aula/semana", "amount": 414.16, "subtotal": 497.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 74550, "lookup_key": "espanhol-avancado_annual_2x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Anual — 2 aulas/semana", "amount": 745.50, "subtotal": 994.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 111825, "lookup_key": "espanhol-avancado_annual_3x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Anual — 3 aulas/semana", "amount": 1118.25, "subtotal": 1491.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 149100, "lookup_key": "espanhol-avancado_annual_4x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Anual — 4 aulas/semana", "amount": 1491.00, "subtotal": 1988.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 186375, "lookup_key": "espanhol-avancado_annual_5x", "nickname": "Vedium — Espanhol Avançado B2.2-C1 — Anual — 5 aulas/semana", "amount": 1863.75, "subtotal": 2485.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
