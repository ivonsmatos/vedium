import frappe


no_cache = 1
APP_URL = "https://app.vediums.com"
PUBLIC_HOSTS = {"vediums.com", "www.vediums.com"}


def _redirect_public_host(path):
    host = (getattr(frappe.local, "request", None) and frappe.local.request.host) or ""
    host = host.split(":")[0].lower()
    if host in PUBLIC_HOSTS:
        frappe.local.flags.redirect_location = f"{APP_URL}{path}"
        raise frappe.Redirect


def get_context(context):
    context.no_cache = 1
    context.title = "Minha agenda — Vedium"
    context.description = "Cadastre sua disponibilidade e veja as aulas agendadas pelos alunos."
    _redirect_public_host("/minha-agenda")

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = (
            "https://app.vediums.com/login?redirect-to=/minha-agenda"
        )
        raise frappe.Redirect

    context.csrf_token = frappe.sessions.get_csrf_token()
    return context
