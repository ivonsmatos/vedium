"""Canonical Stripe/Frappe price definitions for every commercial Vedium course."""

from __future__ import annotations

from copy import deepcopy


def _standard_course(
    *,
    course_name: str,
    commercial_name: str,
    product_id: str,
    monthly_cents: list[int],
    annual_cents: list[int],
    currency: str = "brl",
    explicit_one_x_lookup: bool = False,
) -> dict:
    if len(monthly_cents) != 5 or len(annual_cents) != 5:
        raise ValueError(f"{course_name}: every period must define five prices")

    monthly_base = monthly_cents[0] / 100
    periods = {}
    for period, values in (("monthly", monthly_cents), ("annual", annual_cents)):
        price_rows = []
        for index, cents in enumerate(values, start=1):
            suffix = f"_{index}x" if explicit_one_x_lookup or index > 1 else ""
            price_rows.append(
                {
                    "classes_per_week": index,
                    "unit_amount": cents,
                    "amount": cents / 100,
                    "subtotal": monthly_base * index,
                    "frequency_discount_percent": 0 if index == 1 else 10,
                    "lookup_key": f"{course_name}_{period}{suffix}",
                    "nickname": (
                        f"Vedium — {commercial_name} — "
                        f"{'Mensal' if period == 'monthly' else 'Anual'} — "
                        f"{index} {'aula' if index == 1 else 'aulas'}/semana"
                    ),
                }
            )
        periods[period] = price_rows

    return {
        "course_name": course_name,
        "commercial_name": commercial_name,
        "product_id": product_id,
        "currency": currency.lower(),
        "catalog_version": 1,
        "monthly_prices": periods["monthly"],
        "annual_prices": periods["annual"],
    }


def _private_hebrew() -> dict:
    monthly = [56000, 100800, 151200, 201600, 252000]
    annual = [46667, 84000, 126000, 168000, 210000]
    config = _standard_course(
        course_name="hebraico-particular",
        commercial_name="Hebraico Particular",
        product_id="prod_UznRzhBCmMC5y8",
        monthly_cents=monthly,
        annual_cents=annual,
        explicit_one_x_lookup=True,
    )
    config.update(
        {
            "pricing_basis": "4_weeks",
            "unit_lesson_amount": 14000,
            "annual_discount_months": 2,
            "legacy_price_ids": [
                "price_1TznqDJu78f2k3L0sABKX4Tz",
                "price_1TznqFJu78f2k3L0kmipHrjV",
            ],
        }
    )
    for period in ("monthly_prices", "annual_prices"):
        for row in config[period]:
            row["classes_per_month"] = row["classes_per_week"] * 4
    return config


_CATALOG = [
    _standard_course(
        course_name="ingl-s-beginner",
        commercial_name="Inglês Online ao Vivo A1 – Iniciante",
        product_id="prod_UznRGM7yCjT6lg",
        monthly_cents=[24000, 43200, 64800, 86400, 108000],
        annual_cents=[20000, 36000, 54000, 72000, 90000],
    ),
    _standard_course(
        course_name="ingl-s-elementary",
        commercial_name="Inglês Online ao Vivo A2 – Elementar",
        product_id="prod_UznRycssZj7MaH",
        monthly_cents=[24000, 43200, 64800, 86400, 108000],
        annual_cents=[20000, 36000, 54000, 72000, 90000],
    ),
    _standard_course(
        course_name="ingl-s-pr-intermedi-rio",
        commercial_name="Inglês Online ao Vivo B1 – Pré-Intermediário",
        product_id="prod_UznRRZqfPDfCie",
        monthly_cents=[24000, 43200, 64800, 86400, 108000],
        annual_cents=[20000, 36000, 54000, 72000, 90000],
    ),
    _standard_course(
        course_name="ingl-s-intermedi-rio",
        commercial_name="Inglês Online ao Vivo B1+ – Intermediário",
        product_id="prod_UznRu2aqzaiSRp",
        monthly_cents=[24000, 43200, 64800, 86400, 108000],
        annual_cents=[20000, 36000, 54000, 72000, 90000],
    ),
    _standard_course(
        course_name="ingl-s-upper-intermedi-rio",
        commercial_name="Inglês Online ao Vivo B2 – Intermediário Avançado",
        product_id="prod_UznR3LZ6Wesyyc",
        monthly_cents=[24000, 43200, 64800, 86400, 108000],
        annual_cents=[20000, 36000, 54000, 72000, 90000],
    ),
    _standard_course(
        course_name="ingl-s-avan-ado",
        commercial_name="Inglês Online ao Vivo C1 – Avançado",
        product_id="prod_UznRM5sYVlZSuH",
        monthly_cents=[24000, 43200, 64800, 86400, 108000],
        annual_cents=[20000, 36000, 54000, 72000, 90000],
    ),
    _standard_course(
        course_name="iorub-b-sico",
        commercial_name="Iorubá Básico",
        product_id="prod_UznRrPZ7yuf9yL",
        monthly_cents=[32000, 57600, 86400, 115200, 144000],
        annual_cents=[26666, 47999, 71998, 95998, 119997],
    ),
    _standard_course(
        course_name="iorub-intermedi-rio",
        commercial_name="Iorubá Intermediário",
        product_id="prod_UznR5eXanIPt8H",
        monthly_cents=[32000, 57600, 86400, 115200, 144000],
        annual_cents=[26666, 47999, 71998, 95998, 119997],
    ),
    _standard_course(
        course_name="iorub-avan-ado",
        commercial_name="Iorubá Avançado",
        product_id="prod_UznRl193oyLvrF",
        monthly_cents=[32000, 57600, 86400, 115200, 144000],
        annual_cents=[26666, 47999, 71998, 95998, 119997],
    ),
    _standard_course(
        course_name="espanhol-basico",
        commercial_name="Espanhol Nível Básico (A1-A2)",
        product_id="prod_UznRZM83HU7unf",
        monthly_cents=[29700, 53460, 80190, 106920, 133650],
        annual_cents=[24750, 44550, 66825, 89100, 111375],
    ),
    _standard_course(
        course_name="espanhol-intermediario",
        commercial_name="Espanhol Nível Intermediário (B1-B2.1)",
        product_id="prod_UznR0Jq6tk3II4",
        monthly_cents=[39700, 71460, 107190, 142920, 178650],
        annual_cents=[33083, 59550, 89325, 119100, 148875],
    ),
    _standard_course(
        course_name="espanhol-avancado",
        commercial_name="Espanhol Nível Avançado (B2.2-C1)",
        product_id="prod_UznR52w5UCsZsw",
        monthly_cents=[49700, 89460, 134190, 178920, 223650],
        annual_cents=[41416, 74550, 111825, 149100, 186375],
    ),
    _standard_course(
        course_name="portugues-para-estrangeiros-basico",
        commercial_name="Português para Estrangeiros Nível Básico (PLE)",
        product_id="prod_UznRbeMspEN6Xw",
        currency="usd",
        monthly_cents=[9000, 16200, 24300, 32400, 40500],
        annual_cents=[7500, 13500, 20250, 27000, 33750],
    ),
    _standard_course(
        course_name="portugues-para-estrangeiros-intermediario",
        commercial_name="Português para Estrangeiros Nível Intermediário (PLE)",
        product_id="prod_UznRHPXfGqcX5P",
        currency="usd",
        monthly_cents=[12000, 21600, 32400, 43200, 54000],
        annual_cents=[10000, 18000, 27000, 36000, 45000],
    ),
    _standard_course(
        course_name="portugues-para-estrangeiros-avancado",
        commercial_name="Português para Estrangeiros Nível Avançado (PLE)",
        product_id="prod_UznRvtr8FIWJQY",
        currency="usd",
        monthly_cents=[12000, 21600, 32400, 43200, 54000],
        annual_cents=[10000, 18000, 27000, 36000, 45000],
    ),
    _standard_course(
        course_name="hebraico-a0-alfabetizacao",
        commercial_name="Hebraico A0 Alfabetização",
        product_id="prod_UznRs3ValZEHMB",
        monthly_cents=[19700, 35460, 53190, 70920, 88650],
        annual_cents=[16416, 29550, 44325, 59100, 73875],
    ),
    _standard_course(
        course_name="hebraico-moderno-a1",
        commercial_name="Hebraico Moderno Nível A1",
        product_id="prod_UznRkTmGluQK9B",
        monthly_cents=[39700, 71460, 107190, 142920, 178650],
        annual_cents=[33083, 59550, 89325, 119100, 148875],
    ),
    _standard_course(
        course_name="hebraico-moderno-a2-b1",
        commercial_name="Hebraico Moderno Nível A2/B1",
        product_id="prod_UznRiiitUJrbpj",
        monthly_cents=[44700, 80460, 120690, 160920, 201150],
        annual_cents=[37250, 67050, 100575, 134100, 167625],
    ),
    _standard_course(
        course_name="hebraico-biblico-leitura-guiada",
        commercial_name="Hebraico Bíblico Leitura Guiada",
        product_id="prod_UznRo9Ul5fjr7s",
        monthly_cents=[49700, 89460, 134190, 178920, 223650],
        annual_cents=[41416, 74550, 111825, 149100, 186375],
    ),
    _private_hebrew(),
]


def get_catalog_configs() -> list[dict]:
    """Return a defensive copy so the synchronizer may attach runtime IDs."""
    return deepcopy(_CATALOG)


def get_catalog_config(course_name: str) -> dict:
    for config in _CATALOG:
        if config["course_name"] == course_name:
            return deepcopy(config)
    raise KeyError(course_name)
