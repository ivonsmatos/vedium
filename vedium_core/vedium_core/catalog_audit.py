"""Read-only catalog audits for production checks."""

import frappe


CEFR_CODES = ("A1", "A2", "B1+", "B2", "C1", "B1")


def _found_levels(text):
    """Detecta códigos CEFR literais no título/categoria do curso.

    Desde a renomeação de 2026-07 ("Inglês - Beginner" -> "Inglês Online ao
    Vivo A1 - Iniciante"), o título já traz o código CEFR explícito. "B1" é
    substring de "B1+", então removemos o falso-positivo quando "B1+" já foi
    encontrado.
    """
    found = [code for code in CEFR_CODES if code in text]
    if "B1+" in found and "B1" in found:
        found.remove("B1")
    return found


def _infer_expected_level(title, category=None):
    text = f"{title or ''} {category or ''}"
    if "ingl" not in text.lower() and "english" not in text.lower():
        return None
    found = _found_levels(text)
    return found[0] if len(found) == 1 else None


def audit_course_levels():
    """Return a read-only audit of public English course level labels.

    This function is intended for `bench execute` in production. It does not
    write to the database, migrate, enqueue jobs, or touch checkout/payment.
    """
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "title", "category"],
    )
    checked = []
    issues = []
    for course in courses:
        text = f"{course.title or ''} {course.category or ''}"
        if "ingl" not in text.lower() and "english" not in text.lower():
            continue
        found = _found_levels(text)
        row = {
            "name": course.name,
            "title": course.title,
            "category": course.category,
            "found_levels": found,
        }
        checked.append(row)
        if len(found) != 1:
            issues.append({**row, "issue": f"Ambiguous or missing CEFR level: {found}"})

    return {
        "ok": not issues,
        "checked_count": len(checked),
        "issues": issues,
        "checked": checked,
    }
