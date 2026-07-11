"""Inspeciona aulas ao vivo de uma LMS Batch."""

import json

import frappe


def run(batch_name="ple-b-sico-turma-agosto-2026"):
    classes = frappe.get_all(
        "LMS Live Class",
        filters={"batch_name": batch_name},
        fields=[
            "name",
            "title",
            "date",
            "time",
            "duration",
            "timezone",
            "host",
            "conferencing_provider",
            "google_meet_account",
            "event",
            "join_url",
            "start_url",
        ],
        order_by="date asc, time asc",
    )
    print(
        json.dumps(
            {
                "batch": batch_name,
                "count": len(classes),
                "classes": classes,
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )
