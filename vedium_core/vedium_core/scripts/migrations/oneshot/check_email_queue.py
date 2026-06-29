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

    # Configuração de e-mail de saída
    smtp = frappe.db.sql(
        "SELECT name, email_id, enabled FROM `tabEmail Account` WHERE enable_outgoing=1 LIMIT 5",
        as_dict=True,
    )
    print("\n=== Email Accounts (outgoing) ===")
    for s in smtp:
        print(f"  {s.name}  email={s.email_id}  enabled={s.enabled}")

    if not smtp:
        print("  ⚠️  Nenhuma conta de e-mail de saída configurada!")
