"""Pure pricing rules for the Vedium course checkout."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


MONEY_QUANTUM = Decimal("0.01")


def money(value) -> Decimal:
    """Convert a numeric value to a two-decimal Decimal safely."""
    try:
        amount = Decimal(str(value or 0))
    except (InvalidOperation, TypeError, ValueError):
        amount = Decimal("0")
    return amount.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def annual_savings(monthly_amount, annual_monthly_amount) -> Decimal:
    """Return the saving across 12 monthly charges of the annual plan."""
    monthly = money(monthly_amount)
    annual_monthly = money(annual_monthly_amount)
    saving = (monthly - annual_monthly) * Decimal("12")
    return max(saving, Decimal("0")).quantize(
        MONEY_QUANTUM,
        rounding=ROUND_HALF_UP,
    )


def twelve_month_total(monthly_amount) -> Decimal:
    """Return the total of 12 recurring monthly charges."""
    return (money(monthly_amount) * Decimal("12")).quantize(
        MONEY_QUANTUM,
        rounding=ROUND_HALF_UP,
    )
