"""Cria aulas ao vivo (LMS Live Class) para uma LMS Batch.

Uso:
1. Criar /tmp/vedium_lms_live_classes_config.json no servidor.
2. Rodar:
   bench --site app.vediums.com execute \
     vedium_core.scripts.migrations.oneshot.create_lms_live_classes_from_config.run
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

import frappe


DEFAULT_CONFIG_PATH = "/tmp/vedium_lms_live_classes_config.json"


def _load_config(path):
    config_path = Path(path or DEFAULT_CONFIG_PATH)
    if not config_path.exists():
        frappe.throw(f"Arquivo de config não encontrado: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))


def _required(config, key):
    value = config.get(key)
    if value in (None, ""):
        frappe.throw(f"Campo obrigatório ausente na config: {key}")
    return value


def _parse_date(value):
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def _weekly_dates(start_date, end_date, weekday):
    current = _parse_date(start_date)
    end = _parse_date(end_date)
    while current.weekday() != weekday:
        current += timedelta(days=1)
    while current <= end:
        yield current
        current += timedelta(days=7)


def _duplicate_exists(batch_name, class_date, class_time, title):
    return frappe.db.exists(
        "LMS Live Class",
        {
            "batch_name": batch_name,
            "date": class_date,
            "time": class_time,
            "title": title,
        },
    )


def run(config_path=None):
    config = _load_config(config_path)

    batch_name = _required(config, "batch_name")
    if not frappe.db.exists("LMS Batch", batch_name):
        frappe.throw(f"LMS Batch não encontrada: {batch_name}")

    batch = frappe.get_doc("LMS Batch", batch_name)
    google_meet_account = config.get("google_meet_account") or batch.google_meet_account
    if not google_meet_account:
        frappe.throw("Google Meet account não informado e não definido na turma.")

    host = config.get("host")
    if not host:
        instructors = frappe.get_all(
            "Course Instructor",
            filters={"parenttype": "LMS Batch", "parent": batch_name},
            pluck="instructor",
        )
        host = instructors[0] if instructors else frappe.session.user

    start_date = config.get("start_date") or batch.start_date
    end_date = config.get("end_date") or batch.end_date
    class_time = config.get("time") or str(batch.start_time)
    duration = int(config.get("duration") or 60)
    timezone = config.get("timezone") or batch.timezone or "America/Sao_Paulo"
    weekday = int(config.get("weekday", 0))  # segunda-feira
    title_prefix = config.get("title_prefix") or "Aula ao vivo"
    description = config.get("description") or batch.description

    created = []
    skipped = []
    for index, class_date in enumerate(_weekly_dates(start_date, end_date, weekday), start=1):
        title = f"{title_prefix} {index} - {batch.title}"
        date_text = class_date.isoformat()
        if _duplicate_exists(batch_name, date_text, class_time, title):
            skipped.append({"date": date_text, "title": title, "reason": "duplicate"})
            continue

        live_class = frappe.get_doc(
            {
                "doctype": "LMS Live Class",
                "title": title,
                "host": host,
                "conferencing_provider": "Google Meet",
                "google_meet_account": google_meet_account,
                "batch_name": batch_name,
                "date": date_text,
                "time": class_time,
                "duration": duration,
                "timezone": timezone,
                "description": description,
            }
        )
        live_class.insert(ignore_permissions=True)
        created.append(
            {
                "name": live_class.name,
                "title": live_class.title,
                "date": date_text,
                "time": class_time,
                "duration": duration,
                "join_url": live_class.join_url,
                "event": live_class.event,
            }
        )

    if created:
        batch.show_live_class = 1
        batch.save(ignore_permissions=True)

    frappe.db.commit()
    print(
        json.dumps(
            {
                "batch": batch_name,
                "created_count": len(created),
                "skipped_count": len(skipped),
                "created": created,
                "skipped": skipped,
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )
