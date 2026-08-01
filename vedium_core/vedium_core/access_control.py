"""Vedium access gates layered over the upstream LMS enrollment checks."""

from __future__ import annotations

import frappe
from frappe import _

from vedium_core.stripe_billing_rules import is_active_enrollment_status


STAFF_ROLES = {
    "Administrator",
    "System Manager",
    "Moderator",
    "Course Creator",
    "Batch Evaluator",
    "Vedium Professor",
}


def _user(user=None):
    return user or frappe.session.user


def _is_global_staff(user) -> bool:
    if user == "Administrator":
        return True
    return bool(STAFF_ROLES.intersection(set(frappe.get_roles(user))))


def is_course_staff(user, course) -> bool:
    if not user or user == "Guest":
        return False
    if _is_global_staff(user):
        return True
    return bool(
        frappe.db.exists(
            "Course Instructor",
            {"parent": course, "parenttype": "LMS Course", "instructor": user},
        )
    )


def enrollment_status(user, course):
    if not user or user == "Guest" or not course:
        return None
    row = frappe.db.get_value(
        "LMS Enrollment",
        {"member": user, "course": course},
        ["name", "custom_vedium_status"],
        as_dict=True,
    )
    if not row:
        return None
    return row.custom_vedium_status or "Active"


def has_active_enrollment(user, course) -> bool:
    status = enrollment_status(user, course)
    return status is not None and is_active_enrollment_status(status)


def has_inactive_enrollment(user, course) -> bool:
    status = enrollment_status(user, course)
    return status is not None and not is_active_enrollment_status(status)


def require_active_course_access(course, user=None):
    user = _user(user)
    if is_course_staff(user, course):
        return
    if not has_active_enrollment(user, course):
        frappe.throw(_("Sua matrícula não está ativa para este curso."), frappe.PermissionError)


def _batch_courses(batch):
    return frappe.get_all("Batch Course", {"parent": batch}, pluck="course")


def _batch_has_inactive_access(user, batch) -> bool:
    rows = frappe.get_all(
        "LMS Enrollment",
        filters={"member": user, "enrollment_from_batch": batch},
        fields=["custom_vedium_status"],
    )
    if not rows:
        courses = _batch_courses(batch)
        if courses:
            rows = frappe.get_all(
                "LMS Enrollment",
                filters={"member": user, "course": ["in", courses]},
                fields=["custom_vedium_status"],
            )
    return bool(rows) and not any(
        is_active_enrollment_status(row.custom_vedium_status) for row in rows
    )


def is_batch_staff(user, batch) -> bool:
    if not user or user == "Guest":
        return False
    if _is_global_staff(user):
        return True
    return bool(
        frappe.db.exists(
            "Course Instructor",
            {"parent": batch, "parenttype": "LMS Batch", "instructor": user},
        )
    )


def has_batch_permission(doc, ptype="read", user=None):
    """Preserve native LMS permissions, adding the Vedium status gate first."""
    user = _user(user)
    if not is_batch_staff(user, doc.name) and _batch_has_inactive_access(user, doc.name):
        return False
    from lms.lms.doctype.lms_batch.lms_batch import has_permission as native

    return native(doc, ptype, user)


def has_live_class_permission(doc, ptype="read", user=None):
    user = _user(user)
    batch = doc.batch_name
    if not is_batch_staff(user, batch) and _batch_has_inactive_access(user, batch):
        return False
    from lms.lms.doctype.lms_live_class.lms_live_class import has_permission as native

    return native(doc, ptype, user)


def save_progress(lesson: str, course: str, scorm_details=None):
    require_active_course_access(course)
    from lms.lms.doctype.course_lesson.course_lesson import save_progress as native

    return native(lesson, course, scorm_details)


def _require_topic_access(doctype, docname):
    if doctype == "Course Lesson":
        course = frappe.db.get_value("Course Lesson", docname, "course")
        require_active_course_access(course)
    elif doctype == "LMS Batch" and _batch_has_inactive_access(_user(), docname):
        frappe.throw(_("Sua matrícula não está ativa para esta turma."), frappe.PermissionError)


def get_discussion_topics(doctype: str, docname: str, single_thread=False):
    _require_topic_access(doctype, docname)
    from lms.lms.utils import get_discussion_topics as native

    return native(doctype, docname, single_thread)


def get_discussion_replies(topic: str):
    details = frappe.db.get_value(
        "Discussion Topic", topic, ["reference_doctype", "reference_docname"], as_dict=True
    )
    if details:
        _require_topic_access(details.reference_doctype, details.reference_docname)
    from lms.lms.utils import get_discussion_replies as native

    return native(topic)


def validate_discussion_reply(doc, method=None):
    details = frappe.db.get_value(
        "Discussion Topic",
        doc.topic,
        ["reference_doctype", "reference_docname"],
        as_dict=True,
    )
    if details:
        _require_topic_access(details.reference_doctype, details.reference_docname)
