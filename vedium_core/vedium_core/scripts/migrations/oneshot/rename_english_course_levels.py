"""Align the six English LMS titles with the approved CEFR progression.

This changes only ``LMS Course.title``. Document identifiers, public slugs,
enrollments, checkout links and prices remain untouched.
"""

import frappe
from frappe.website.utils import clear_website_cache

from vedium_core.courses import bump_courses_cache_version


TITLE_CHANGES = {
    "ingl-s-beginner": (
        "Inglês Online ao Vivo A1 – Iniciante",
        "Inglês Online ao Vivo A1 – Iniciante",
    ),
    "ingl-s-elementary": (
        "Inglês Online ao Vivo A2 – Básico",
        "Inglês Online ao Vivo A2 – Elementar",
    ),
    "ingl-s-pr-intermedi-rio": (
        "Inglês Online ao Vivo B1 – Pré-Intermediário",
        "Inglês Online ao Vivo A2+ – Pré-Intermediário",
    ),
    "ingl-s-intermedi-rio": (
        "Inglês Online ao Vivo B1+ – Intermediário",
        "Inglês Online ao Vivo B1 – Intermediário",
    ),
    "ingl-s-upper-intermedi-rio": (
        "Inglês Online ao Vivo B2 – Intermediário Avançado",
        "Inglês Online ao Vivo B2 – Intermediário Superior",
    ),
    "ingl-s-avan-ado": (
        "Inglês Online ao Vivo C1 – Avançado",
        "Inglês Online ao Vivo C1 – Avançado",
    ),
}


def execute():
    updated = []
    unchanged = []
    unexpected = []

    for course_name, (expected_title, target_title) in TITLE_CHANGES.items():
        current_title = frappe.db.get_value("LMS Course", course_name, "title")
        if current_title == target_title:
            unchanged.append(course_name)
            continue
        if current_title != expected_title:
            unexpected.append({"course": course_name, "title": current_title})
            continue
        frappe.db.set_value(
            "LMS Course",
            course_name,
            "title",
            target_title,
            update_modified=True,
        )
        updated.append(course_name)

    if unexpected:
        frappe.throw(
            "Títulos inesperados; nenhuma confirmação automática: "
            f"{unexpected}"
        )

    bump_courses_cache_version()
    frappe.clear_cache()
    clear_website_cache()
    return {"updated": updated, "unchanged": unchanged}
