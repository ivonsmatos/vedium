"""Verifica a fila de e-mails e configuração SMTP.

bench execute vedium_core.scripts.migrations.oneshot.check_email_queue.run
"""
import frappe


def run():
    # Últimos 5 e-mails na fila
    rows = frappe.db.sql(
        "SELECT name, status, error, creation FROM `tabEmail Queue` ORDER BY creation DESC LIMIT 5",
        as_dict=True,
    )
    print("=== Email Queue (últimos 5) ===")
    for r in rows:
        print(f"  {r.creation}  status={r.status}  error={r.error or '-'}  id={r.name}")

    # Configuração de e-mail de saída. Algumas versões do Frappe usam
    # "enabled", outras usam apenas "enable_outgoing"/"no_smtp".
    columns = {
        row[0]
        for row in frappe.db.sql("SHOW COLUMNS FROM `tabEmail Account`")
    }
    fields = ["name", "email_id"]
    if "enabled" in columns:
        fields.append("enabled")
    if "no_smtp" in columns:
        fields.append("no_smtp")
    where = "WHERE enable_outgoing=1" if "enable_outgoing" in columns else ""
    smtp = frappe.db.sql(
        f"SELECT {', '.join(fields)} FROM `tabEmail Account` {where} LIMIT 5",
        as_dict=True,
    )
    print("\n=== Email Accounts (outgoing) ===")
    for s in smtp:
        status = []
        if "enabled" in s:
            status.append(f"enabled={s.enabled}")
        if "no_smtp" in s:
            status.append(f"no_smtp={s.no_smtp}")
        suffix = "  " + "  ".join(status) if status else ""
        print(f"  {s.name}  email={s.email_id}{suffix}")

    if not smtp:
        print("  ⚠️  Nenhuma conta de e-mail de saída configurada!")
