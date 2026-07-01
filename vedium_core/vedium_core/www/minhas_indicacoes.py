import frappe


no_cache = 1
PUBLIC_HOSTS = {"vediums.com", "www.vediums.com"}


def _redirect_public_host(path):
    host = (getattr(frappe.local, "request", None) and frappe.local.request.host) or ""
    host = host.split(":")[0].lower()
    if host in PUBLIC_HOSTS:
        frappe.local.flags.redirect_location = f"https://app.vediums.com{path}"
        raise frappe.Redirect


def get_context(context):
    context.no_cache = 1
    context.title = "Minhas indicações — Vedium"
    context.description = "Acompanhe seu código de indicação, amigos matriculados e recompensas."
    _redirect_public_host("/minhas-indicacoes")

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = (
            "https://app.vediums.com/login?redirect-to=/minhas-indicacoes"
        )
        raise frappe.Redirect

    from vedium_core.referrals import get_my_referral, get_my_referral_conversions

    context.referral = get_my_referral()
    context.conversions = get_my_referral_conversions()
    return context
