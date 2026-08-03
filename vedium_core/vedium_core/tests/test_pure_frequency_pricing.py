from decimal import Decimal

import pytest

from vedium_core.frequency_pricing_rules import (
    frequency_discount_percent,
    frequency_quote,
    normalize_classes_per_week,
)


def test_frequency_accepts_one_to_five_classes():
    assert [normalize_classes_per_week(value) for value in range(1, 6)] == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("value", [0, 6, -1, "abc", 1.5])
def test_frequency_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        normalize_classes_per_week(value)


def test_one_class_has_no_discount():
    quote = frequency_quote("297.00", 1)
    assert quote == {
        "classes_per_week": 1,
        "unit_amount": Decimal("297.00"),
        "subtotal": Decimal("297.00"),
        "discount_percent": Decimal("0"),
        "discount_amount": Decimal("0.00"),
        "amount": Decimal("297.00"),
    }


@pytest.mark.parametrize(
    ("classes", "subtotal", "discount", "final_amount"),
    [
        (2, "594.00", "59.40", "534.60"),
        (3, "891.00", "89.10", "801.90"),
        (4, "1188.00", "118.80", "1069.20"),
        (5, "1485.00", "148.50", "1336.50"),
    ],
)
def test_frequency_applies_recurring_ten_percent_discount(
    classes, subtotal, discount, final_amount
):
    quote = frequency_quote("297.00", classes)
    assert quote["subtotal"] == Decimal(subtotal)
    assert quote["discount_percent"] == Decimal("10")
    assert quote["discount_amount"] == Decimal(discount)
    assert quote["amount"] == Decimal(final_amount)
    assert frequency_discount_percent(classes) == Decimal("10")
