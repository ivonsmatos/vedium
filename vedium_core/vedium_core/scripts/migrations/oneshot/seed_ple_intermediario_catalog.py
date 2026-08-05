import frappe
from vedium_core.catalog_sync import sync_course_catalog

def execute(execute_apply=False):
    # Regras do PLE Intermediário (USD)
    # 1x Mensal = US$ 120,00
    # 1x Anual = US$ 100,00
    
    config = {
        "course_name": "portugues-para-estrangeiros-intermediario",
        "commercial_name": "Português para Estrangeiros Nível Intermediário (PLE)",
        "product_id": "prod_UznRHPXfGqcX5P",
        "currency": "usd",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 12000, "lookup_key": "portugues-para-estrangeiros-intermediario_monthly", "nickname": "Vedium — PLE Intermediário — Mensal — 1 aula/semana", "amount": 120.00, "subtotal": 120.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 21600, "lookup_key": "portugues-para-estrangeiros-intermediario_monthly_2x", "nickname": "Vedium — PLE Intermediário — Mensal — 2 aulas/semana", "amount": 216.00, "subtotal": 240.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 32400, "lookup_key": "portugues-para-estrangeiros-intermediario_monthly_3x", "nickname": "Vedium — PLE Intermediário — Mensal — 3 aulas/semana", "amount": 324.00, "subtotal": 360.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 43200, "lookup_key": "portugues-para-estrangeiros-intermediario_monthly_4x", "nickname": "Vedium — PLE Intermediário — Mensal — 4 aulas/semana", "amount": 432.00, "subtotal": 480.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 54000, "lookup_key": "portugues-para-estrangeiros-intermediario_monthly_5x", "nickname": "Vedium — PLE Intermediário — Mensal — 5 aulas/semana", "amount": 540.00, "subtotal": 600.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 10000, "lookup_key": "portugues-para-estrangeiros-intermediario_annual", "nickname": "Vedium — PLE Intermediário — Anual — 1 aula/semana", "amount": 100.00, "subtotal": 120.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 18000, "lookup_key": "portugues-para-estrangeiros-intermediario_annual_2x", "nickname": "Vedium — PLE Intermediário — Anual — 2 aulas/semana", "amount": 180.00, "subtotal": 240.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 27000, "lookup_key": "portugues-para-estrangeiros-intermediario_annual_3x", "nickname": "Vedium — PLE Intermediário — Anual — 3 aulas/semana", "amount": 270.00, "subtotal": 360.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 36000, "lookup_key": "portugues-para-estrangeiros-intermediario_annual_4x", "nickname": "Vedium — PLE Intermediário — Anual — 4 aulas/semana", "amount": 360.00, "subtotal": 480.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 45000, "lookup_key": "portugues-para-estrangeiros-intermediario_annual_5x", "nickname": "Vedium — PLE Intermediário — Anual — 5 aulas/semana", "amount": 450.00, "subtotal": 600.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
