import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do PLE Básico (USD)
    # 1x Mensal = US$ 90,00
    # 1x Anual = US$ 75,00
    
    config = {
        "course_name": "portugues-para-estrangeiros-basico",
        "commercial_name": "Português para Estrangeiros Nível Básico (PLE)",
        "product_id": "prod_UznRbeMspEN6Xw",
        "currency": "usd",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 9000, "lookup_key": "portugues-para-estrangeiros-basico_monthly", "nickname": "Vedium — PLE Básico — Mensal — 1 aula/semana", "amount": 90.00, "subtotal": 90.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 16200, "lookup_key": "portugues-para-estrangeiros-basico_monthly_2x", "nickname": "Vedium — PLE Básico — Mensal — 2 aulas/semana", "amount": 162.00, "subtotal": 180.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 24300, "lookup_key": "portugues-para-estrangeiros-basico_monthly_3x", "nickname": "Vedium — PLE Básico — Mensal — 3 aulas/semana", "amount": 243.00, "subtotal": 270.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 32400, "lookup_key": "portugues-para-estrangeiros-basico_monthly_4x", "nickname": "Vedium — PLE Básico — Mensal — 4 aulas/semana", "amount": 324.00, "subtotal": 360.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 40500, "lookup_key": "portugues-para-estrangeiros-basico_monthly_5x", "nickname": "Vedium — PLE Básico — Mensal — 5 aulas/semana", "amount": 405.00, "subtotal": 450.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 7500, "lookup_key": "portugues-para-estrangeiros-basico_annual", "nickname": "Vedium — PLE Básico — Anual — 1 aula/semana", "amount": 75.00, "subtotal": 90.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 13500, "lookup_key": "portugues-para-estrangeiros-basico_annual_2x", "nickname": "Vedium — PLE Básico — Anual — 2 aulas/semana", "amount": 135.00, "subtotal": 180.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 20250, "lookup_key": "portugues-para-estrangeiros-basico_annual_3x", "nickname": "Vedium — PLE Básico — Anual — 3 aulas/semana", "amount": 202.50, "subtotal": 270.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 27000, "lookup_key": "portugues-para-estrangeiros-basico_annual_4x", "nickname": "Vedium — PLE Básico — Anual — 4 aulas/semana", "amount": 270.00, "subtotal": 360.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 33750, "lookup_key": "portugues-para-estrangeiros-basico_annual_5x", "nickname": "Vedium — PLE Básico — Anual — 5 aulas/semana", "amount": 337.50, "subtotal": 450.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
