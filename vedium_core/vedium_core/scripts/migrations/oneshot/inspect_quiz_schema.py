"""Diagnostico temporario, SO LEITURA: imprime os campos reais dos doctypes
de quiz/certificado em producao, pra confirmar o schema antes de escrever o
seed de conteudo do curso PLE (provas/exercicios/gate entre niveis).

Nao muda nada no banco. Apagar depois de usar.

Rodar:
  bench --site app.vediums.com execute \
    vedium_core.scripts.migrations.oneshot.inspect_quiz_schema.run
"""
import frappe

DOCTYPES = [
    "LMS Quiz",
    "LMS Quiz Question",
    "LMS Question",
    "LMS Certificate",
    "LMS Enrollment",
    "Course Lesson",
]


def run():
    for dt in DOCTYPES:
        print(f"\n=== {dt} ===")
        if not frappe.db.exists("DocType", dt):
            print("  NAO EXISTE nesta instalacao.")
            continue
        meta = frappe.get_meta(dt)
        for f in meta.fields:
            extra = []
            if f.fieldtype == "Link":
                extra.append(f"-> {f.options}")
            if f.fieldtype == "Select" and f.options:
                extra.append(f"opcoes: {f.options}")
            if f.reqd:
                extra.append("obrigatorio")
            print(f"  {f.fieldname} ({f.fieldtype}) {' '.join(extra)}")

        count = frappe.db.count(dt)
        print(f"  -- total de registros: {count}")
        if count:
            sample = frappe.get_all(dt, limit=1, fields=["*"])
            print(f"  -- exemplo: {sample[0]}")
