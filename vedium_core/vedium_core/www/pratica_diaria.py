import frappe


APP_URL = "https://app.vediums.com"
PUBLIC_HOSTS = {"vediums.com", "www.vediums.com"}


def _redirect_public_host(path):
    host = (getattr(frappe.local, "request", None) and frappe.local.request.host) or ""
    host = host.split(":")[0].lower()
    if host in PUBLIC_HOSTS:
        frappe.local.flags.redirect_location = f"{APP_URL}{path}"
        raise frappe.Redirect


def get_context(context):
    _redirect_public_host("/pratica-diaria")
    context.title = "Prática diária com voz — Vedium"
    context.description = "Pratique fala, shadowing e revisão diária com recursos seguros no navegador."
    context.no_cache = 1
    return context
