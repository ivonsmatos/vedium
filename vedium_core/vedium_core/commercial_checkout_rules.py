"""Commercial checkout restrictions for exceptional course offers."""

from __future__ import annotations


HEBRAICO_PARTICULAR_COURSE = "hebraico-particular"


def get_checkout_restriction(course_name: str):
    """Return an explicit commercial restriction for courses that are not generic 1-5x offers."""
    if course_name == HEBRAICO_PARTICULAR_COURSE:
        return {
            "billing_periods": ("monthly",),
            "classes_per_week": (1,),
        }
    return None


def validate_checkout_selection(course_name: str, billing_period: str, classes_per_week: int) -> None:
    """Raise ValueError when the selected checkout option is not commercially available."""
    restriction = get_checkout_restriction(course_name)
    if not restriction:
        return

    period = (billing_period or "monthly").strip().lower()
    try:
        frequency = int(classes_per_week)
    except (TypeError, ValueError) as exc:
        raise ValueError("Frequência de aulas inválida.") from exc

    if period not in restriction["billing_periods"]:
        raise ValueError("Hebraico Particular está disponível apenas no plano mensal.")
    if frequency not in restriction["classes_per_week"]:
        raise ValueError("Hebraico Particular está disponível apenas em 1 aula por semana.")
