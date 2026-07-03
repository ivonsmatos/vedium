import frappe

from vedium_core.courses import get_published_courses


def get_context(context):
    """Context for the Spanish course catalog page (/es/catalogo)."""
    context.courses = get_published_courses()
    context.categories = get_course_categories()
    context.cart_count = get_cart_count()

    context.title = "Catálogo de Cursos — Cursos de Idiomas Online en Vivo | Vedium"
    context.description = (
        "Catálogo de cursos en vivo de Vedium: inglés (A1 a C1), yoruba y "
        "portugués para extranjeros (PLE). Profesores calificados y certificado."
    )
    context.lang = "es"
    context.canonical_url = "https://vediums.com/es/catalogo"
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
