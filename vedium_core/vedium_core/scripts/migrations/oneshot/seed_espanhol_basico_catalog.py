import frappe
from vedium_core.catalog_sync import sync_course_catalog
from decimal import Decimal, ROUND_HALF_UP

def execute(execute_apply=False):
    # Regras do Básico
    # 1x Mensal = R$ 297,00
    # 1x Anual = R$ 247,50
    # Frequências 2x-5x ganham desconto de 10%.
    # "Para frequências 2 a 5, o valor-base não sofre desconto cumulativo extra. Aplicar o desconto de 10% sobre o preço final."
    
    # Mensais (já pre-calculados conforme requisitos anteriores da tarefa Básico):
    # 1x: 297,00 (0% off)
    # 2x: 534,60 (10% off de 594)
    # 3x: 801,90 (10% off de 891)
    # 4x: 1069,20 (10% off de 1188)
    # 5x: 1336,50 (10% off de 1485)
    
    # Anuais (já pre-calculados - para o Básico a regra era desconto sobre o base anual de 247,50):
    # 1x: 247,50
    # 2x: 445,50
    # 3x: 668,25
    # 4x: 891,00
    # 5x: 1113,75
    
    config = {
        "course_name": "espanhol-basico",
        "commercial_name": "Espanhol Nível Básico (A1-A2)",
        "product_id": "prod_UznRZM83HU7unf",
        "currency": "brl",
        "catalog_version": 1,
        "monthly_prices": [
            {"classes_per_week": 1, "unit_amount": 29700, "lookup_key": "espanhol-basico_monthly", "nickname": "Vedium — Espanhol Básico A1-A2 — Mensal — 1 aula/semana", "amount": 297.00, "subtotal": 297.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 53460, "lookup_key": "espanhol-basico_monthly_2x", "nickname": "Vedium — Espanhol Básico A1-A2 — Mensal — 2 aulas/semana", "amount": 534.60, "subtotal": 594.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 80190, "lookup_key": "espanhol-basico_monthly_3x", "nickname": "Vedium — Espanhol Básico A1-A2 — Mensal — 3 aulas/semana", "amount": 801.90, "subtotal": 891.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 106920, "lookup_key": "espanhol-basico_monthly_4x", "nickname": "Vedium — Espanhol Básico A1-A2 — Mensal — 4 aulas/semana", "amount": 1069.20, "subtotal": 1188.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 133650, "lookup_key": "espanhol-basico_monthly_5x", "nickname": "Vedium — Espanhol Básico A1-A2 — Mensal — 5 aulas/semana", "amount": 1336.50, "subtotal": 1485.00, "frequency_discount_percent": 10},
        ],
        "annual_prices": [
            {"classes_per_week": 1, "unit_amount": 24750, "lookup_key": "espanhol-basico_annual", "nickname": "Vedium — Espanhol Básico A1-A2 — Anual — 1 aula/semana", "amount": 247.50, "subtotal": 297.00, "frequency_discount_percent": 0},
            {"classes_per_week": 2, "unit_amount": 44550, "lookup_key": "espanhol-basico_annual_2x", "nickname": "Vedium — Espanhol Básico A1-A2 — Anual — 2 aulas/semana", "amount": 445.50, "subtotal": 594.00, "frequency_discount_percent": 10},
            {"classes_per_week": 3, "unit_amount": 66825, "lookup_key": "espanhol-basico_annual_3x", "nickname": "Vedium — Espanhol Básico A1-A2 — Anual — 3 aulas/semana", "amount": 668.25, "subtotal": 891.00, "frequency_discount_percent": 10},
            {"classes_per_week": 4, "unit_amount": 89100, "lookup_key": "espanhol-basico_annual_4x", "nickname": "Vedium — Espanhol Básico A1-A2 — Anual — 4 aulas/semana", "amount": 891.00, "subtotal": 1188.00, "frequency_discount_percent": 10},
            {"classes_per_week": 5, "unit_amount": 111375, "lookup_key": "espanhol-basico_annual_5x", "nickname": "Vedium — Espanhol Básico A1-A2 — Anual — 5 aulas/semana", "amount": 1113.75, "subtotal": 1485.00, "frequency_discount_percent": 10},
        ]
    }
    
    return sync_course_catalog(config, execute_apply)
