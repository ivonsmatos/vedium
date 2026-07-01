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
    context.title = "Agendar aula — Vedium"
    context.description = "Escolha o professor do seu curso e agende sua aula no horário disponível."
    _redirect_public_host("/agendar-aula")

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = (
            "https://app.vediums.com/login?redirect-to=/agendar-aula"
        )
        raise frappe.Redirect

    context.csrf_token = frappe.sessions.get_csrf_token()
    return context
