"""Pure tests for the (dormant) commercial checkout restriction framework.

Nenhum curso tem restrição comercial hoje — o Hebraico Particular voltou ao
modelo genérico (mensal + anual, 1–5x) em 2026-08-08. Estes testes garantem que
o ponto de extensão está inerte (não barra nada) até uma exceção ser reintroduzida.
"""

from pathlib import Path
import sys

import pytest

APP_ROOT = Path(__file__).resolve().parents[2]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from vedium_core.commercial_checkout_rules import (  # noqa: E402
    get_checkout_restriction,
    validate_checkout_selection,
)


@pytest.mark.parametrize("course_name", ["hebraico-particular", "ingles-a1", "espanhol-basico"])
def test_no_course_is_restricted(course_name):
    assert get_checkout_restriction(course_name) is None


@pytest.mark.parametrize(
    ("billing_period", "classes_per_week"),
    [
        ("monthly", 1),
        ("annual", 1),
        ("monthly", 5),
        ("annual", 5),
    ],
)
def test_any_selection_is_allowed(billing_period, classes_per_week):
    # Não levanta: sem restrição, qualquer combinação mensal/anual × 1–5x passa.
    validate_checkout_selection("hebraico-particular", billing_period, classes_per_week)
    validate_checkout_selection("ingles-a1", billing_period, classes_per_week)
