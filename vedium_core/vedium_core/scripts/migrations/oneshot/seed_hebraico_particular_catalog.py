import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do Hebraico Particular
    # Valor unitário: R$ 140,00 por aula
    # Base: 4 semanas por mês
    
    # 1x Mensal = R$ 560,00 (0% off)
    # 2x Mensal = R$ 1.008,00 (10% off de 1120)
    # 3x Mensal = R$ 1.512,00 (10% off de 1680)
    # 4x Mensal = R$ 2.016,00 (10% off de 2240)
    # 5x Mensal = R$ 2.520,00 (10% off de 2800)
    
    # Anuais calculados rigorosamente sobre o mensal descontado (mensal * 10 / 12):
    # 1x Anual = 560.00 * 10 / 12 = 466.67
    # 2x Anual = 1008.00 * 10 / 12 = 840.00
    # 3x Anual = 1512.00 * 10 / 12 = 1260.00
    # 4x Anual = 2016.00 * 10 / 12 = 1680.00
    # 5x Anual = 2520.00 * 10 / 12 = 2100.00
    
    # Prices legados que devem ser preservados:
    # Mensal: price_1TznqDJu78f2k3L0sABKX4Tz (R$ 1.120,00)
    # Anual: price_1TznqFJu78f2k3L0kmipHrjV (R$ 933,33)
    
    config = {
        "course_name": "hebraico-particular",
        "commercial_name": "Hebraico Particular",
        "product_id": "prod_UznRzhBCmMC5y8",
        "currency": "brl",
        "catalog_version": 1,
        "pricing_basis": "4_weeks",
        "unit_lesson_amount": 14000,
        "annual_discount_months": 2,
        "legacy_price_ids": [
            "price_1TznqDJu78f2k3L0sABKX4Tz",
            "price_1TznqFJu78f2k3L0kmipHrjV"
        ],
        "monthly_prices": [
            {"classes_per_week": 1, "classes_per_month": 4, "unit_amount": 56000, "lookup_key": "hebraico-particular_monthly_1x", "nickname": "Vedium — Hebraico Particular — Mensal — 1 aula/semana", "amount": 560.00, "subtotal": 560.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "classes_per_month": 8, "unit_amount": 100800, "lookup_key": "hebraico-particular_monthly_2x", "nickname": "Vedium — Hebraico Particular — Mensal — 2 aulas/semana", "amount": 1008.00, "subtotal": 1120.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "classes_per_month": 12, "unit_amount": 151200, "lookup_key": "hebraico-particular_monthly_3x", "nickname": "Vedium — Hebraico Particular — Mensal — 3 aulas/semana", "amount": 1512.00, "subtotal": 1680.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "classes_per_month": 16, "unit_amount": 201600, "lookup_key": "hebraico-particular_monthly_4x", "nickname": "Vedium — Hebraico Particular — Mensal — 4 aulas/semana", "amount": 2016.00, "subtotal": 2240.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "classes_per_month": 20, "unit_amount": 252000, "lookup_key": "hebraico-particular_monthly_5x", "nickname": "Vedium — Hebraico Particular — Mensal — 5 aulas/semana", "amount": 2520.00, "subtotal": 2800.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "classes_per_month": 4, "unit_amount": 46667, "lookup_key": "hebraico-particular_annual_1x", "nickname": "Vedium — Hebraico Particular — Anual — 1 aula/semana", "amount": 466.67, "subtotal": 560.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "classes_per_month": 8, "unit_amount": 84000, "lookup_key": "hebraico-particular_annual_2x", "nickname": "Vedium — Hebraico Particular — Anual — 2 aulas/semana", "amount": 840.00, "subtotal": 1120.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "classes_per_month": 12, "unit_amount": 126000, "lookup_key": "hebraico-particular_annual_3x", "nickname": "Vedium — Hebraico Particular — Anual — 3 aulas/semana", "amount": 1260.00, "subtotal": 1680.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "classes_per_month": 16, "unit_amount": 168000, "lookup_key": "hebraico-particular_annual_4x", "nickname": "Vedium — Hebraico Particular — Anual — 4 aulas/semana", "amount": 1680.00, "subtotal": 2240.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "classes_per_month": 20, "unit_amount": 210000, "lookup_key": "hebraico-particular_annual_5x", "nickname": "Vedium — Hebraico Particular — Anual — 5 aulas/semana", "amount": 2100.00, "subtotal": 2800.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
