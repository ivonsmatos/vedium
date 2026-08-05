import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do Hebraico Bíblico Leitura Guiada
    # 1x Mensal = R$ 497,00 (price_1TznqFJu78f2k3L0aXVy57PK)
    # 1x Anual = R$ 414,16 (price_1TznqGJu78f2k3L0reAJhApT)
    # Frequências 2x-5x:
    # Parcela anual = valor_mensal_final × 10 ÷ 12
    # Arredondar para dois centavos com ROUND_HALF_UP
    
    # Mensais (10% off para 2-5):
    # 1x: 497,00 (0% off)
    # 2x: 894,60 (10% off de 994)
    # 3x: 1341,90 (10% off de 1491)
    # 4x: 1789,20 (10% off de 1988)
    # 5x: 2236,50 (10% off de 2485)
    
    # Anuais calculados rigorosamente sobre o mensal descontado:
    # 1x: 414,16 (histórico preservado)
    # 2x: 894.60 * 10 / 12 = 745,50
    # 3x: 1341.90 * 10 / 12 = 1118,25
    # 4x: 1789.20 * 10 / 12 = 1491,00
    # 5x: 2236.50 * 10 / 12 = 1863,75
    
    config = {
        "course_name": "hebraico-biblico-leitura-guiada",
        "commercial_name": "Hebraico Bíblico Leitura Guiada",
        "product_id": "prod_UznRo9Ul5fjr7s",
        "currency": "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 49700, "lookup_key": "hebraico-biblico-leitura-guiada_monthly", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Mensal — 1 aula/semana", "amount": 497.00, "subtotal": 497.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 89460, "lookup_key": "hebraico-biblico-leitura-guiada_monthly_2x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Mensal — 2 aulas/semana", "amount": 894.60, "subtotal": 994.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 134190, "lookup_key": "hebraico-biblico-leitura-guiada_monthly_3x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Mensal — 3 aulas/semana", "amount": 1341.90, "subtotal": 1491.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 178920, "lookup_key": "hebraico-biblico-leitura-guiada_monthly_4x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Mensal — 4 aulas/semana", "amount": 1789.20, "subtotal": 1988.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 223650, "lookup_key": "hebraico-biblico-leitura-guiada_monthly_5x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Mensal — 5 aulas/semana", "amount": 2236.50, "subtotal": 2485.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 41416, "lookup_key": "hebraico-biblico-leitura-guiada_annual", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Anual — 1 aula/semana", "amount": 414.16, "subtotal": 497.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 74550, "lookup_key": "hebraico-biblico-leitura-guiada_annual_2x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Anual — 2 aulas/semana", "amount": 745.50, "subtotal": 994.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 111825, "lookup_key": "hebraico-biblico-leitura-guiada_annual_3x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Anual — 3 aulas/semana", "amount": 1118.25, "subtotal": 1491.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 149100, "lookup_key": "hebraico-biblico-leitura-guiada_annual_4x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Anual — 4 aulas/semana", "amount": 1491.00, "subtotal": 1988.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 186375, "lookup_key": "hebraico-biblico-leitura-guiada_annual_5x", "nickname": "Vedium — Hebraico Bíblico Leitura Guiada — Anual — 5 aulas/semana", "amount": 1863.75, "subtotal": 2485.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
