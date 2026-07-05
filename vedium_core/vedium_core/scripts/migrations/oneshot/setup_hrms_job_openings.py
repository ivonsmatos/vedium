"""Cria as vagas nativas do Frappe HR (hrms) que espelham a lista de
posicoes hoje hardcoded em www/carreiras.py, pra podermos ligar as
candidaturas do site a um Job Opening real (o campo Job Applicant.job_title
e um Link pra Job Opening, que por sua vez exige um Designation e uma
Company existentes).

Idempotente: nao duplica Designation nem Job Opening se ja existirem.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.setup_hrms_job_openings.run
"""
import frappe

COMPANY = "Vedium"

# Mesma lista de "positions" de www/carreiras.py, menos a opcao livre
# "Outra (especificar na mensagem)" -- essa nao vira Job Opening.
POSITIONS = [
    "Professor(a) de Ingles",
    "Professor(a) de Ioruba",
    "Professor(a) de Portugues para Estrangeiros",
    "Atendimento / Suporte ao Aluno",
    "Marketing / Conteudo",
    "Vendas / Comercial",
]


def _ensure_designation(name):
    if frappe.db.exists("Designation", name):
        return name
    doc = frappe.get_doc({"doctype": "Designation", "designation_name": name})
    doc.insert(ignore_permissions=True)
    return doc.name


def _ensure_job_opening(position):
    existing = frappe.db.get_value("Job Opening", {"job_title": position}, "name")
    if existing:
        return existing
    designation = _ensure_designation(position)
    doc = frappe.get_doc({
        "doctype": "Job Opening",
        "job_title": position,
        "designation": designation,
        "company": COMPANY,
        "status": "Open",
        "publish": 1,
    })
    doc.insert(ignore_permissions=True)
    return doc.name


def run():
    if not frappe.db.exists("Company", COMPANY):
        print(f"AVISO: Company '{COMPANY}' nao existe -- nada foi criado.")
        return

    created = []
    skipped = []
    for position in POSITIONS:
        existing = frappe.db.get_value("Job Opening", {"job_title": position}, "name")
        if existing:
            skipped.append(position)
            continue
        _ensure_job_opening(position)
        created.append(position)

    frappe.db.commit()

    print("=== Job Opening criadas ===")
    for p in created:
        print("  +", p)
    print("=== Ja existiam ===")
    for p in skipped:
        print("  -", p)
    print(f"\nResumo: {len(created)} criadas, {len(skipped)} ja existiam.")
