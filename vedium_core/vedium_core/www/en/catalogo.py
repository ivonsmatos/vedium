import frappe

from vedium_core.courses import get_published_courses


def get_context(context):
    """Context for the English course catalog page (/en/catalogo)."""
    context.courses = get_published_courses()
    context.categories = get_course_categories()
    context.cart_count = get_cart_count()

    context.title = "Course Catalog — Live Online Language Courses | Vedium"
    context.description = (
        "Vedium's live online course catalog: English (A1 to C1), Yoruba and "
        "Portuguese for Foreigners (PLE). Qualified teachers and a certificate."
    )
    context.lang = "en"
    context.canonical_url = "https://vediums.com/en/catalogo"
    context.alt_lang_url = "https://vediums.com/catalogo"


def get_cart_count():
    if frappe.session.user == "Guest":
        return 0

    if frappe.db.exists("DocType", "Quotation"):
        quotation = frappe.get_all(
            "Quotation",
            filters={"party_name": frappe.session.user, "docstatus": 0},
            fields=["name"],
            limit=1,
        )
        if quotation:
            return frappe.db.count("Quotation Item", {"parent": quotation[0].name})
    return 0


def get_course_categories():
    try:
        categories = frappe.get_all(
            "LMS Category",
            fields=["name", "category"],
            order_by="category",
        )
        return categories
    except Exception as e:
        frappe.log_error(f"Error fetching categories: {str(e)}", "Vedium Courses Page")
        return []
