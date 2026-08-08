"""Commercial checkout restrictions for exceptional course offers.

Ponto de extensão (dormente): nenhum curso tem restrição comercial hoje. O
Hebraico Particular voltou ao modelo genérico (mensal + anual, 1–5x/semana,
preço automático do catálogo/plano) em 2026-08-08 — decisão do usuário: "todos
os valores automáticos, como os outros". Para reintroduzir uma exceção no futuro,
retorne aqui um dict {"billing_periods": (...), "classes_per_week": (...)}.
"""

from __future__ import annotations


def get_checkout_restriction(course_name: str):
    """Restrição comercial explícita por curso. None = sem restrição (o padrão:
    o curso segue a matriz genérica 1–5x + mensal/anual)."""
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
