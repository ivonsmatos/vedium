"""Query the verified Stripe/Frappe course price catalog."""

from __future__ import annotations

import frappe
from frappe import _

from vedium_core.catalog_definitions import get_catalog_configs


EXPECTED_FREQUENCIES = {1, 2, 3, 4, 5}


def managed_course_names() -> set[str]:
    return {config["course_name"] for config in get_catalog_configs()}


def is_catalog_managed_course(course_name: str) -> bool:
    if not course_name:
        return False
    if course_name in managed_course_names():
        return True
    commercial_names = {config["commercial_name"] for config in get_catalog_configs()}
    title = frappe.db.get_value("LMS Course", course_name, "title")
    return bool(title and title in commercial_names)


def get_course_price(course_name, billing_period, classes_per_week, environment="live"):
    """Return exactly one active and Stripe-validated catalog record."""
    if not course_name:
        frappe.throw(_("Curso não informado."))
    if billing_period not in {"monthly", "annual"}:
        frappe.throw(_("Período de cobrança inválido."))
    frequency = int(classes_per_week or 0)
    if frequency not in EXPECTED_FREQUENCIES:
        frappe.throw(_("Aulas por semana deve estar entre 1 e 5."))

    if not is_catalog_complete(course_name, environment):
        frappe.throw(
            _("O catálogo de pagamento deste curso está indisponível ou incompleto. Tente novamente mais tarde.")
        )

    records = frappe.get_all(
        "Vedium Course Price",
        filters={
            "course": course_name,
            "billing_period": billing_period,
            "classes_per_week": frequency,
            "stripe_environment": environment,
            "enabled": 1,
            "stripe_validated": 1,
        },
        fields=["name", "catalog_version"],
        order_by="catalog_version desc",
        limit_page_length=2,
    )
    if not records:
        frappe.throw(_("Preço não encontrado no catálogo para as opções selecionadas."))
    if len(records) > 1 and records[0]["catalog_version"] == records[1]["catalog_version"]:
        frappe.throw(_("Múltiplos preços ativos encontrados. Contate o suporte administrativo."))
    return frappe.get_doc("Vedium Course Price", records[0]["name"])


def is_catalog_complete(course_name: str, environment: str = "live") -> bool:
    """Require distinct frequencies 1..5 for monthly and annual periods."""
    if not course_name:
        return False

    rows = frappe.get_all(
        "Vedium Course Price",
        filters={
            "course": course_name,
            "stripe_environment": environment,
            "enabled": 1,
            "stripe_validated": 1,
        },
        fields=["billing_period", "classes_per_week", "catalog_version"],
        order_by="catalog_version desc",
        limit_page_length=50,
    )
    if not rows:
        return False

    latest_version = max(int(row["catalog_version"] or 0) for row in rows)
    latest = [row for row in rows if int(row["catalog_version"] or 0) == latest_version]
    monthly = {
        int(row["classes_per_week"])
        for row in latest
        if row["billing_period"] == "monthly"
    }
    annual = {
        int(row["classes_per_week"])
        for row in latest
        if row["billing_period"] == "annual"
    }
    complete = monthly == EXPECTED_FREQUENCIES and annual == EXPECTED_FREQUENCIES and len(latest) == 10
    if not complete:
        frappe.log_error(
            message=(
                f"Catálogo incompleto para {course_name}. "
                f"Versão {latest_version}; monthly={sorted(monthly)}; annual={sorted(annual)}."
            ),
            title="Vedium Course Price Error",
        )
    return complete
