import frappe
from vedium_core.integrations import get_student_360

no_cache = 1


def get_context(context):
    context.no_cache = 1

    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/aluno_360"
        raise frappe.Redirect

    roles = set(frappe.get_roles())
    staff = {"System Manager", "LMS Moderator", "Sales Manager", "Sales User", "Agent", "Agent Manager"}
    context.is_staff = bool(staff.intersection(roles))

    email = (frappe.form_dict.get("email") or "").strip()
    context.email = email
    context.data = None

    if context.is_staff and email:
        try:
            context.data = get_student_360(email)
        except Exception:
            context.data = None

    context.students = []
    if context.is_staff:
        members = frappe.get_all("LMS Enrollment", fields=["member"], pluck="member")
        context.students = sorted(set(members))
