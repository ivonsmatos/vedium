import frappe

from vedium_core.courses import get_published_courses


def get_context(context):
    """Context for the French course catalog page (/fr/catalogo)."""
    context.courses = get_published_courses()
    context.categories = get_course_categories()
    context.cart_count = get_cart_count()

    context.title = "Catalogue de Cours — Cours de Langues en Ligne en Direct | Vedium"
    context.description = (
        "Catalogue de cours en direct Vedium : anglais (A1 à C1), yoruba et "
        "portugais pour étrangers (PLE). Professeurs qualifiés et certificat."
    )
    context.lang = "fr"
    context.canonical_url = "https://vediums.com/fr/catalogo"
    context.alt_lang_url = "https://vediums.com/cursos-de-idiomas-online"


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
