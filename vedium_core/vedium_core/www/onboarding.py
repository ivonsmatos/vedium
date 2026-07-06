import frappe


def get_context(context):
    user = frappe.session.user
    if user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect=/onboarding"
        raise frappe.Redirect
    context.no_cache = 1
    context.title = "Bem-vindo à Vedium!"
