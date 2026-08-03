"""Pure rules for weekly class frequency and recurring discounts."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

MIN_CLASSES_PER_WEEK = 1
MAX_CLASSES_PER_WEEK = 5
FREQUENCY_DISCOUNT_PERCENT = Decimal("10")
_MONEY_QUANTUM = Decimal("0.01")


def normalize_classes_per_week(value=None) -> int:
    """Return a validated weekly class quantity between 1 and 5."""
    if value in (None, ""):
        return MIN_CLASSES_PER_WEEK
    try:
        classes = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("A frequência deve ser um número inteiro entre 1 e 5.") from exc
    if classes < MIN_CLASSES_PER_WEEK or classes > MAX_CLASSES_PER_WEEK:
        raise ValueError("Escolha entre 1 e 5 aulas por semana.")
    return classes


def frequency_discount_percent(classes_per_week) -> Decimal:
    classes = normalize_classes_per_week(classes_per_week)
    return FREQUENCY_DISCOUNT_PERCENT if classes >= 2 else Decimal("0")


def money(value) -> Decimal:
    return Decimal(str(value or 0)).quantize(_MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def frequency_quote(unit_amount, classes_per_week) -> dict:
    """Calculate subtotal, recurring discount and final monthly amount."""
    classes = normalize_classes_per_week(classes_per_week)
    unit = money(unit_amount)
    subtotal = money(unit * classes)
    discount_percent = frequency_discount_percent(classes)
    discount_amount = money(subtotal * discount_percent / Decimal("100"))
    final_amount = money(subtotal - discount_amount)
    return {
        "classes_per_week": classes,
        "unit_amount": unit,
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "amount": final_amount,
    }
