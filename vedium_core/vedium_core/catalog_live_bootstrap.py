"""Canonical live Stripe catalog bootstrap for Vedium.

This module adapts the intermediate catalog_registry definitions to the real
LMS Course names used in production and to the lookup-key convention already
present in Stripe. It is intentionally idempotent: catalog_sync reuses matching
Prices and only creates missing combinations.

Hebraico Particular remains blocked until the commercial rule is resolved.
"""

from __future__ import annotations

from typing import Any

import frappe

from vedium_core.catalog_registry import CATALOG, generate_config_for_course
from vedium_core.catalog_sync import sync_course_catalog


EXPECTED_FREQUENCIES = {1, 2, 3, 4, 5}

# Registry IDs that were created from titles/slugs during an intermediate
# migration. The values below are the real LMS Course names in production.
COURSE_ALIASES = {
    "espanhol-b-sico-a1-a2": "espanhol-basico",
    "espanhol-intermedi-rio-b1-b2-1": "espanhol-intermediario",
    "espanhol-avan-ado-b2-2-c1": "espanhol-avancado",
    "portugu-s-para-estrangeiros-b-sico-a1-a2": "portugues-para-estrangeiros-basico",
    "portugu-s-para-estrangeiros-intermedi-rio-b1-b2-1": "portugues-para-estrangeiros-intermediario",
    "portugu-s-para-estrangeiros-avan-ado-b2-2-c1": "portugues-para-estrangeiros-avancado",
    "hebraico-a0-alfabetiza-o": "hebraico-a0-alfabetizacao",
}

BLOCKED_COURSES = {"hebraico-particular"}


def _canonical_config(registry_id: str) -> dict[str, Any]:
    config = generate_config_for_course(registry_id)
    actual_course = COURSE_ALIASES.get(registry_id, registry_id)
    config["course_name"] = actual_course

    # The canonical convention already used by live Stripe Prices is based on
    # the LMS Course name, not on catalog_registry.commercial_id.
    for period in ("monthly", "annual"):
        rows = config[f"{period}_prices"]
        for row in rows:
            frequency = int(row["classes_per_week"])
            suffix = "" if frequency == 1 else f"_{frequency}x"
            row["lookup_key"] = f"{actual_course}_{period}{suffix}"

    return config


def get_active_configs() -> list[dict[str, Any]]:
    configs: list[dict[str, Any]] = []
    for registry_id, definition in CATALOG.items():
        actual_course = COURSE_ALIASES.get(registry_id, registry_id)
        if actual_course in BLOCKED_COURSES or definition.get("blocked_status"):
            continue
        configs.append(_canonical_config(registry_id))
    return configs


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def run(execute_apply: bool = False) -> dict[str, Any]:
    """Audit or apply every sellable course catalog.

    Audit is read-only. Apply can create/reuse Stripe Prices and writes the
    verified Vedium Course Price mappings in Frappe. It never creates a
    customer, subscription, Checkout Session, invoice or charge.
    """
    apply_mode = _as_bool(execute_apply)
    successes: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for config in get_active_configs():
        course_name = config["course_name"]
        try:
            if not frappe.db.exists("LMS Course", course_name):
                frappe.throw(f"LMS Course não encontrado: {course_name}")
            result = sync_course_catalog(config, execute_apply=apply_mode)
            successes.append(
                {
                    "course": course_name,
                    "commercial_name": config["commercial_name"],
                    "result": result,
                }
            )
        except Exception as exc:
            failures.append({"course": course_name, "error": str(exc)})
            print(f"[ERRO] {course_name}: {exc}")

    summary = {
        "mode": "apply" if apply_mode else "audit",
        "expected_courses": len(get_active_configs()),
        "successful_courses": len(successes),
        "failed_courses": len(failures),
        "blocked_courses": sorted(BLOCKED_COURSES),
        "successes": successes,
        "failures": failures,
    }
    if failures:
        frappe.throw(
            "Falha na sincronização do catálogo: "
            + "; ".join(f"{row['course']}: {row['error']}" for row in failures)
        )
    return summary


def status() -> dict[str, Any]:
    """Verify that every sellable course has 5 monthly + 5 annual mappings."""
    course_status: dict[str, dict[str, Any]] = {}

    for config in get_active_configs():
        course_name = config["course_name"]
        rows = frappe.get_all(
            "Vedium Course Price",
            filters={
                "course": course_name,
                "stripe_environment": "live",
                "catalog_version": 1,
            },
            fields=[
                "billing_period",
                "classes_per_week",
                "enabled",
                "stripe_validated",
                "stripe_price_id",
            ],
            limit_page_length=50,
        )

        def frequencies(period: str) -> set[int]:
            return {
                int(row["classes_per_week"])
                for row in rows
                if row.get("billing_period") == period
                and int(row.get("enabled") or 0) == 1
                and int(row.get("stripe_validated") or 0) == 1
                and str(row.get("stripe_price_id") or "").startswith("price_")
            }

        monthly = frequencies("monthly")
        annual = frequencies("annual")
        ready = monthly == EXPECTED_FREQUENCIES and annual == EXPECTED_FREQUENCIES
        course_status[course_name] = {
            "ready": ready,
            "monthly": sorted(monthly),
            "annual": sorted(annual),
        }

    ready_courses = sum(1 for row in course_status.values() if row["ready"])
    expected_courses = len(course_status)
    return {
        "ready": ready_courses == expected_courses,
        "expected_courses": expected_courses,
        "ready_courses": ready_courses,
        "blocked_courses": sorted(BLOCKED_COURSES),
        "courses": course_status,
    }
