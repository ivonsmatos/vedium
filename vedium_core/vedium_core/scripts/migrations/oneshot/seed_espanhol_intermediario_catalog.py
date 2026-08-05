import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do Intermediário
    # 1x Mensal = R$ 397,00
    # 1x Anual = R$ 330,83 (Historicamente definido assim)
    # Frequências 2x-5x:
    # Parcela anual = valor_mensal_final × 10 ÷ 12
    # Arredondar para dois centavos com ROUND_HALF_UP
    
    # Mensais (10% off para 2-5):
    # 1x: 397,00 (0% off)
    # 2x: 714,60 (10% off de 794)
    # 3x: 1071,90 (10% off de 1191)
    # 4x: 1429,20 (10% off de 1588)
    # 5x: 1786,50 (10% off de 1985)
    
    # Anuais calculados rigorosamente:
    # 1x: 330,83
    # 2x: 714.60 * 10 / 12 = 595,50
    # 3x: 1071.90 * 10 / 12 = 893,25
    # 4x: 1429.20 * 10 / 12 = 1191,00
    # 5x: 1786.50 * 10 / 12 = 1488,75
    
    config = {
        "course_name": "espanhol-intermediario",
        "commercial_name": "Espanhol Nível Intermediário (B1-B2.1)",
        "product_id": "prod_UznR0Jq6tk3II4",
        "currency": "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 39700, "lookup_key": "espanhol-intermediario_monthly", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Mensal — 1 aula/semana", "amount": 397.00, "subtotal": 397.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 71460, "lookup_key": "espanhol-intermediario_monthly_2x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Mensal — 2 aulas/semana", "amount": 714.60, "subtotal": 794.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 107190, "lookup_key": "espanhol-intermediario_monthly_3x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Mensal — 3 aulas/semana", "amount": 1071.90, "subtotal": 1191.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 142920, "lookup_key": "espanhol-intermediario_monthly_4x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Mensal — 4 aulas/semana", "amount": 1429.20, "subtotal": 1588.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 178650, "lookup_key": "espanhol-intermediario_monthly_5x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Mensal — 5 aulas/semana", "amount": 1786.50, "subtotal": 1985.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 33083, "lookup_key": "espanhol-intermediario_annual", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Anual — 1 aula/semana", "amount": 330.83, "subtotal": 397.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 59550, "lookup_key": "espanhol-intermediario_annual_2x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Anual — 2 aulas/semana", "amount": 595.50, "subtotal": 794.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 89325, "lookup_key": "espanhol-intermediario_annual_3x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Anual — 3 aulas/semana", "amount": 893.25, "subtotal": 1191.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 119100, "lookup_key": "espanhol-intermediario_annual_4x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Anual — 4 aulas/semana", "amount": 1191.00, "subtotal": 1588.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 148875, "lookup_key": "espanhol-intermediario_annual_5x", "nickname": "Vedium — Espanhol Intermediário B1-B2.1 — Anual — 5 aulas/semana", "amount": 1488.75, "subtotal": 1985.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
