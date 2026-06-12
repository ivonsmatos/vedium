# Vedium Core — Relatórios de gestão
# Digest semanal enviado por e-mail (scheduler: segunda-feira de manhã).
# Materializa a rotina de gestão: leads, matrículas, tickets e erros da
# semana num único e-mail, sem precisar abrir o /app.

import frappe

DIGEST_RECIPIENTS = ["contato@vediums.com"]


def _count_since(doctype, days=7, filters=None):
    """Conta documentos criados nos últimos N dias. 0 se o DocType não existe."""
    if not frappe.db.exists("DocType", doctype):
        return None
    f = dict(filters or {})
    f["creation"] = [">", frappe.utils.add_to_date(None, days=-days)]
    try:
        return frappe.db.count(doctype, f)
    except Exception:
        return None


def send_weekly_digest():
    """Envia o resumo semanal de operação para a equipe."""
    novos_leads = _count_since("CRM Lead")
    matriculas = _count_since("LMS Enrollment")
    tickets = _count_since("HD Ticket")
    tickets_abertos = None
    if frappe.db.exists("DocType", "HD Ticket"):
        try:
            tickets_abertos = frappe.db.count("HD Ticket", {"status": "Open"})
        except Exception:
            pass
    erros = _count_since("Error Log")
    candidaturas = _count_since("Candidatura")

    def fmt(valor):
        return "—" if valor is None else str(valor)

    linhas = [
        ("Novos leads (CRM)", fmt(novos_leads), "/crm"),
        ("Novas matrículas (LMS)", fmt(matriculas), "/app/lms-enrollment"),
        ("Tickets abertos na semana", fmt(tickets), "/helpdesk"),
        ("Tickets ainda em aberto (total)", fmt(tickets_abertos), "/helpdesk"),
        ("Candidaturas (carreiras)", fmt(candidaturas), "/app/candidatura"),
        ("Erros no sistema (Error Log)", fmt(erros), "/app/error-log"),
    ]

    corpo = "<h3>Resumo semanal — Vedium</h3><table border='0' cellpadding='6'>"
    for titulo, valor, link in linhas:
        corpo += (
            f"<tr><td>{titulo}</td><td><strong>{valor}</strong></td>"
            f"<td><a href='https://app.vediums.com{link}'>abrir</a></td></tr>"
        )
    corpo += "</table>"
    corpo += (
        "<p>Checklist de 15 minutos: leads novos respondidos? "
        "Tickets em aberto tratados? Algum erro recorrente no log?</p>"
        "<p>— enviado automaticamente toda segunda-feira "
        "(vedium_core.reports.send_weekly_digest)</p>"
    )

    try:
        frappe.sendmail(
            recipients=DIGEST_RECIPIENTS,
            subject="[Vedium] Resumo semanal de operação",
            message=corpo,
        )
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Vedium.reports.weekly_digest")
