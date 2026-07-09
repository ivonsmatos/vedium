# -*- coding: utf-8 -*-
"""
Vedium — Cria os badges automáticos de gamificação usando o LMS Badge
NATIVO do Frappe LMS (zero código de runtime: o próprio LMS avalia a
condição a cada insert/update do doctype de referência e cria o
LMS Badge Assignment sozinho — ver lms/doctype/lms_badge/lms_badge.py,
process_badges).

Semântica confirmada no código-fonte oficial (2026-07-09):
    - condition: expressão Python avaliada com frappe.safe_eval sobre o
      doc como dict (ex.: "doc.percentage == 100"). Não dá pra consultar
      o banco na condição — badges de agregado (ex.: "10 lições") não são
      possíveis nativamente.
    - user_field: campo do doctype de referência que identifica o aluno.
    - grant_only_once: garante 1 badge por aluno.

Idempotente: não duplica badges que já existem (por título).

Rodar:
    bench --site app.vediums.com execute \
        vedium_core.scripts.migrations.oneshot.setup_lms_badges.run
"""
import frappe

ICON_BASE = "/assets/vedium_core/images/icones/SVG/SOLID"

BADGES = [
    {
        "title": "Primeira Lição",
        "description": "Você concluiu sua primeira lição na Vedium. Bem-vindo à jornada!",
        "image": f"{ICON_BASE}/Curriculum.svg",
        "reference_doctype": "LMS Course Progress",
        "event": "New",
        "condition": "True",
        "user_field": "member",
        "grant_only_once": 1,
        "enabled": 1,
    },
    {
        "title": "Nota Máxima",
        "description": "Você gabaritou um quiz: 100% de acerto.",
        "image": f"{ICON_BASE}/Quiz.svg",
        "reference_doctype": "LMS Quiz Submission",
        "event": "New",
        "condition": "doc.percentage == 100",
        "user_field": "member",
        "grant_only_once": 1,
        "enabled": 1,
    },
    {
        "title": "Nível Concluído",
        "description": "Você conquistou um certificado de conclusão de nível.",
        "image": f"{ICON_BASE}/E-Certificate.svg",
        "reference_doctype": "LMS Certificate",
        "event": "New",
        "condition": "True",
        "user_field": "member",
        "grant_only_once": 1,
        "enabled": 1,
    },
]


def run():
    created, skipped = [], []
    for badge in BADGES:
        if frappe.db.exists("LMS Badge", {"title": badge["title"]}):
            skipped.append(badge["title"])
            continue
        doc = frappe.get_doc({"doctype": "LMS Badge", **badge})
        doc.insert(ignore_permissions=True)
        created.append(badge["title"])

    frappe.db.commit()

    for title in created:
        print(f"  ✓ badge criado: {title}")
    for title in skipped:
        print(f"  — já existia: {title}")
    print(f"\nResumo: {len(created)} criados, {len(skipped)} já existiam.")
