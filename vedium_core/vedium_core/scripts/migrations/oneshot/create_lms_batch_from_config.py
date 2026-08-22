"""Cria uma LMS Batch a partir de um JSON validado.

Fluxo recomendado:
1. Criar /tmp/vedium_lms_batch_config.json no servidor.
2. Rodar:
   bench --site app.vediums.com execute \
     vedium_core.scripts.migrations.oneshot.create_lms_batch_from_config.run

Exemplo minimo de config:
{
  "title": "PLE Básico - Turma Agosto/2026",
  "course": "portugues-para-estrangeiros-basico",
  "instructor": "almir@vediums.com",
  "start_date": "2026-08-03",
  "end_date": "2026-09-28",
  "start_time": "19:00:00",
  "end_time": "20:00:00",
  "seat_count": 8,
  "description": "Turma ao vivo de PLE Básico.",
  "batch_details": "<p>Encontros semanais ao vivo pelo Google Meet.</p>",
  "published": false
}
"""

import json
from pathlib import Path

import frappe


DEFAULT_CONFIG_PATH = "/tmp/vedium_lms_batch_config.json"
DEFAULT_TIMEZONE = "America/Sao_Paulo"


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


def _get_course(course):
    if not frappe.db.exists("LMS Course", course):
        frappe.throw(f"Curso não encontrado: {course}")
    return frappe.get_doc("LMS Course", course)


def _default_google_meet_account(instructor):
    if not frappe.db.exists("DocType", "LMS Google Meet Settings"):
        return None
    return frappe.db.get_value("LMS Google Meet Settings", {"member": instructor}, "name")


def _validate_instructor(instructor):
    if not frappe.db.exists("User", instructor):
        frappe.throw(f"Usuário/instrutor não encontrado: {instructor}")
    return instructor


def _ensure_not_duplicate(title):
    existing = frappe.db.exists("LMS Batch", {"title": title})
    if existing:
        frappe.throw(f"Já existe LMS Batch com esse título: {title} ({existing})")


def run(config_path=None):
    config = _load_config(config_path)

    title = _required(config, "title")
    _ensure_not_duplicate(title)

    course = _get_course(_required(config, "course"))
    instructor = _validate_instructor(_required(config, "instructor"))
    evaluator = config.get("evaluator") or course.evaluator
    if evaluator and not frappe.db.exists("Course Evaluator", evaluator):
        frappe.throw(f"Course Evaluator não encontrado: {evaluator}")

    published = 1 if config.get("published") else 0
    google_meet_account = config.get("google_meet_account") or _default_google_meet_account(instructor)
    conferencing_provider = config.get("conferencing_provider")
    if not conferencing_provider and google_meet_account:
        conferencing_provider = "Google Meet"

    batch = frappe.new_doc("LMS Batch")
    batch.update(
        {
            "published": 0,
            "title": title,
            "start_date": _required(config, "start_date"),
            "end_date": _required(config, "end_date"),
            "start_time": _required(config, "start_time"),
            "end_time": _required(config, "end_time"),
            "timezone": config.get("timezone") or DEFAULT_TIMEZONE,
            "seat_count": config.get("seat_count") or 0,
            "description": _required(config, "description"),
            "batch_details": _required(config, "batch_details"),
            "medium": config.get("medium") or "Online",
            "allow_self_enrollment": 1 if config.get("allow_self_enrollment") else 0,
            "paid_batch": 1 if config.get("paid_batch") else 0,
            "show_live_class": 1 if config.get("show_live_class", True) else 0,
            "allow_future": 1 if config.get("allow_future", True) else 0,
        }
    )
    if config.get("category"):
        batch.category = config["category"]
    if config.get("paid_batch"):
        batch.amount = _required(config, "amount")
        batch.currency = _required(config, "currency")
        if config.get("amount_usd"):
            batch.amount_usd = config["amount_usd"]

    batch.append("instructors", {"instructor": instructor})
    batch.append(
        "courses",
        {
            "course": course.name,
            "title": course.title,
            "evaluator": evaluator,
        },
    )

    for entry in config.get("timetable") or []:
        batch.append(
            "timetable",
            {
                "date": entry.get("date"),
                "start_time": entry.get("start_time") or config["start_time"],
                "end_time": entry.get("end_time") or config["end_time"],
                "reference_doctype": entry.get("reference_doctype"),
                "reference_docname": entry.get("reference_docname"),
                "milestone": 1 if entry.get("milestone") else 0,
            },
        )

    batch.insert(ignore_permissions=True)

    # O LMS valida Google Meet apenas quando o batch já não é novo.
    if conferencing_provider:
        batch.conferencing_provider = conferencing_provider
    if google_meet_account:
        batch.google_meet_account = google_meet_account
    if published:
        batch.published = 1
    batch.save(ignore_permissions=True)
    frappe.db.commit()

    print(
        json.dumps(
            {
                "created": True,
                "name": batch.name,
                "title": batch.title,
                "course": course.name,
                "instructor": instructor,
                "evaluator": evaluator,
                "published": batch.published,
                "allow_self_enrollment": batch.allow_self_enrollment,
                "conferencing_provider": batch.conferencing_provider,
                "google_meet_account": batch.google_meet_account,
                "url": frappe.utils.get_url(f"/lms/batches/{batch.name}"),
            },
            indent=2,
            ensure_ascii=False,
            default=str,
        )
    )
