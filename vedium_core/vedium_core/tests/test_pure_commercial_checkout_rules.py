"""Pure tests for exceptional commercial checkout restrictions."""

from pathlib import Path
import sys

import pytest

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.commercial_checkout_rules import (  # noqa: E402
    HEBRAICO_PARTICULAR_COURSE,
    get_checkout_restriction,
    validate_checkout_selection,
)


def test_hebraico_particular_is_monthly_1x_only():
    restriction = get_checkout_restriction(HEBRAICO_PARTICULAR_COURSE)
    assert restriction == {
        "billing_periods": ("monthly",),
        "classes_per_week": (1,),
    }
    validate_checkout_selection(HEBRAICO_PARTICULAR_COURSE, "monthly", 1)


@pytest.mark.parametrize(
    ("billing_period", "classes_per_week"),
    [
        ("annual", 1),
        ("monthly", 2),
        ("annual", 2),
    ],
)
def test_hebraico_particular_rejects_unapproved_options(billing_period, classes_per_week):
    with pytest.raises(ValueError):
        validate_checkout_selection(
            HEBRAICO_PARTICULAR_COURSE,
            billing_period,
            classes_per_week,
        )


def test_other_courses_keep_generic_checkout_behavior():
    assert get_checkout_restriction("ingles-a1") is None
    validate_checkout_selection("ingles-a1", "annual", 5)
