"""Read-only catalog audits for production checks."""

import re

import frappe


def _infer_expected_level(title, category=None):
    text = f"{title or ''} {category or ''}".lower()
    normalized = re.sub(r"\s+", " ", text)
    if "ingl" not in normalized and "english" not in normalized:
        return None
    if "upper" in normalized or "intermediário superior" in normalized:
        return "B2"
    if "pré-intermedi" in normalized or "pre-intermedi" in normalized:
        return "B1-"
    if "intermedi" in normalized:
        return "B1"
    return None


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
        expected = _infer_expected_level(course.title, course.category)
        if not expected:
            continue
        row = {
            "name": course.name,
            "title": course.title,
            "category": course.category,
            "expected_level": expected,
        }
        checked.append(row)
        haystack = f"{course.title or ''} {course.category or ''}".lower()
        if expected == "B2" and "b1" in haystack:
            issues.append({**row, "issue": "Upper Intermediario appears with B1"})
        if expected == "B1" and "upper" not in haystack and "b2" in haystack:
            issues.append({**row, "issue": "Intermediario appears with B2"})

    return {
        "ok": not issues,
        "checked_count": len(checked),
        "issues": issues,
        "checked": checked,
    }
