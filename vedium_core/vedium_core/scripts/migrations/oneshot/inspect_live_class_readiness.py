# -*- coding: utf-8 -*-
"""Diagnóstico read-only: o que já está pronto pra aula ao vivo em grupo
(LMS Batch + LMS Live Class), pra decidir o que falta CONFIGURAR (não
codar) antes de tentar montar um formato "Community"-like.

Checa:
  1. LMS Batch existentes (nome, curso, datas, alunos matriculados).
  2. LMS Live Class já criadas (se existirem) e o provider usado.
  3. Zoom Settings -- configurado ou não.
  4. Google Settings (Meet/Calendar) -- configurado ou não.
  5. LMS Settings relevantes (enable_certification, batch, discussions).

Não altera nada.

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.inspect_live_class_readiness.run
"""

import frappe


def run():
    print("=== LMS Batch existentes ===")
    batches = frappe.get_all(
        "LMS Batch",
        fields=["name", "title", "start_date", "end_date", "published"],
        order_by="start_date desc",
    )
    if not batches:
        print("  (nenhuma)")
    for b in batches:
        try:
            student_count = frappe.db.count("Batch Student", {"parent": b.name})
        except Exception:
            student_count = frappe.db.count("LMS Enrollment", {"enrollment_from_batch": b.name})
        print(
            f"  {b.name!r} | {b.title!r} | {b.start_date} -> {b.end_date} "
            f"| published={b.published} | alunos={student_count}"
        )

    print("\n=== LMS Live Class existentes ===")
    if frappe.db.exists("DocType", "LMS Live Class"):
        meta = frappe.get_meta("LMS Live Class")
        candidate_fields = ["name", "title", "batch_name", "date", "time", "provider"]
        fields = [f for f in candidate_fields if f == "name" or meta.get_field(f)]
        classes = frappe.get_all(
            "LMS Live Class", fields=fields, order_by="creation desc", limit_page_length=20
        )
        if not classes:
            print("  (nenhuma)")
        for c in classes:
            print(f"  {c}")
    else:
        print("  DocType 'LMS Live Class' nao existe neste site")

    print("\n=== Zoom Settings ===")
    if frappe.db.exists("DocType", "Zoom Settings"):
        enabled = frappe.db.get_single_value("Zoom Settings", "enable")
        has_key = bool(frappe.db.get_single_value("Zoom Settings", "api_key"))
        print(f"  enable={enabled} | api_key presente={has_key}")
    else:
        print("  DocType 'Zoom Settings' nao existe")

    print("\n=== Google Settings ===")
    if frappe.db.exists("DocType", "Google Settings"):
        g_enabled = frappe.db.get_single_value("Google Settings", "enable")
        g_client = bool(frappe.db.get_single_value("Google Settings", "client_id"))
        print(f"  enable={g_enabled} | client_id presente={g_client}")
    else:
        print("  DocType 'Google Settings' nao existe")

    print("\n=== LMS Settings (campos relevantes) ===")
    lms_meta = frappe.get_meta("LMS Settings")
    for fieldname in ("enable_discussions", "batch", "enable_certification"):
        if lms_meta.get_field(fieldname):
            print(f"  {fieldname} = {frappe.db.get_single_value('LMS Settings', fieldname)}")

    print("\n=== Course Evaluator / Evaluator Schedule (agendamento 1-a-1 nativo) ===")
    for doctype in ("Course Evaluator", "Evaluator Schedule"):
        exists = frappe.db.exists("DocType", doctype)
        count = frappe.db.count(doctype) if exists else 0
        print(f"  {doctype}: existe={bool(exists)} | registros={count}")
