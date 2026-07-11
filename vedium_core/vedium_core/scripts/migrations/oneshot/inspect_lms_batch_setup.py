"""Inspeciona o estado necessario para criar a primeira LMS Batch.

Uso:
bench --site app.vediums.com execute \
  vedium_core.scripts.migrations.oneshot.inspect_lms_batch_setup.run
"""

import json

import frappe


def _meta_fields(doctype):
    meta = frappe.get_meta(doctype)
    return [
        {
            "fieldname": field.fieldname,
            "label": field.label,
            "fieldtype": field.fieldtype,
            "options": field.options,
            "reqd": field.reqd,
            "default": field.default,
        }
        for field in meta.fields
        if field.fieldtype not in ("Section Break", "Column Break", "Tab Break")
    ]


def run():
    result = {
        "batch_count": frappe.db.count("LMS Batch"),
        "courses": frappe.get_all(
            "LMS Course",
            filters={"published": 1},
            fields=["name", "title", "evaluator", "paid_course", "paid_certificate"],
            order_by="title asc",
        ),
        "evaluators": frappe.get_all(
            "Course Evaluator",
            fields=["name", "evaluator"],
            order_by="name asc",
        ),
        "google_meet_settings": frappe.get_all(
            "LMS Google Meet Settings",
            fields=["name", "member", "google_calendar"],
            order_by="name asc",
        )
        if frappe.db.exists("DocType", "LMS Google Meet Settings")
        else [],
        "course_instructor_fields": _meta_fields("Course Instructor"),
        "batch_fields": _meta_fields("LMS Batch"),
        "child_tables": {},
    }

    for field in result["batch_fields"]:
        if field["fieldtype"] == "Table" and field["options"]:
            result["child_tables"][field["options"]] = _meta_fields(field["options"])

    if result["batch_count"]:
        result["existing_batches"] = frappe.get_all(
            "LMS Batch",
            fields=[
                "name",
                "title",
                "start_date",
                "end_date",
                "start_time",
                "end_time",
                "seat_count",
                "published",
                "allow_self_enrollment",
                "conferencing_provider",
                "google_meet_account",
            ],
            order_by="creation desc",
            limit_page_length=20,
        )
        for batch in result["existing_batches"]:
            batch["courses"] = frappe.get_all(
                "Batch Course",
                filters={"parent": batch.name},
                fields=["course", "title", "evaluator"],
            )

    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
