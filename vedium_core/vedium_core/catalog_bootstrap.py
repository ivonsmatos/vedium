"""Audit and activate the complete Vedium Stripe/Frappe catalog."""

from __future__ import annotations

from typing import Any

import frappe
from frappe.utils import cint

from vedium_core.catalog_definitions import get_catalog_configs
from vedium_core.catalog_sync import sync_course_catalog


def _selected_configs(course: str | None = None) -> list[dict]:
    configs = get_catalog_configs()
    if not course:
        return configs
    selected = [config for config in configs if config["course_name"] == course]
    if not selected:
        frappe.throw(f"Curso não definido no catálogo canônico: {course}")
    return selected


def run(execute_apply: bool = False, course: str | None = None) -> dict[str, Any]:
    """Run a read-only audit or an idempotent live catalog apply.

    This command never creates a customer, subscription, invoice, Checkout
    Session or charge. It creates/reuses Stripe Prices and activates verified
    Frappe mappings only.
    """
    apply_mode = bool(cint(execute_apply))
    selected = _selected_configs(course)
    reports: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for config in selected:
        try:
            report = sync_course_catalog(config, execute_apply=apply_mode)
            reports.append(report)
            print(
                f"[{report['mode'].upper()}] {report['commercial_name']}: "
                f"{len(report['prices'])} combinações verificadas"
            )
        except Exception as exc:
            failures.append({"course": config["course_name"], "error": str(exc)})
            print(f"[ERRO] {config['commercial_name']}: {exc}")

    result = {
        "mode": "apply" if apply_mode else "audit",
        "expected_courses": len(selected),
        "successful_courses": len(reports),
        "failed_courses": len(failures),
        "reports": reports,
        "failures": failures,
    }
    if failures:
        frappe.throw(
            "Falha na sincronização do catálogo: "
            + "; ".join(f"{row['course']}: {row['error']}" for row in failures)
        )
    return result


def status() -> dict[str, Any]:
    """Return a payment-readiness summary without contacting Stripe."""
    configs = get_catalog_configs()
    rows = frappe.get_all(
        "Vedium Course Price",
        filters={"stripe_environment": "live", "catalog_version": 1},
        fields=[
            "course",
            "commercial_name",
            "billing_period",
            "classes_per_week",
            "enabled",
            "stripe_validated",
        ],
        limit_page_length=500,
    )

    course_status: dict[str, dict[str, Any]] = {}
    for config in configs:
        course_rows = [
            row
            for row in rows
            if row.get("commercial_name") == config["commercial_name"]
            or row.get("course") == config["course_name"]
        ]
        monthly = {
            int(row["classes_per_week"])
            for row in course_rows
            if row["billing_period"] == "monthly"
            and int(row["enabled"] or 0) == 1
            and int(row["stripe_validated"] or 0) == 1
        }
        annual = {
            int(row["classes_per_week"])
            for row in course_rows
            if row["billing_period"] == "annual"
            and int(row["enabled"] or 0) == 1
            and int(row["stripe_validated"] or 0) == 1
        }
        ready = monthly == {1, 2, 3, 4, 5} and annual == {1, 2, 3, 4, 5}
        course_status[config["course_name"]] = {
            "commercial_name": config["commercial_name"],
            "resolved_course": course_rows[0]["course"] if course_rows else None,
            "ready": ready,
            "monthly": sorted(monthly),
            "annual": sorted(annual),
        }

    ready_courses = sum(1 for row in course_status.values() if row["ready"])
    return {
        "expected_courses": len(configs),
        "ready_courses": ready_courses,
        "ready": ready_courses == len(configs),
        "courses": course_status,
    }
