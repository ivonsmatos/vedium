import frappe

from vedium_core.courses import get_published_courses


def get_context(context):
    """Context for the German course catalog page (/de/catalogo)."""
    context.courses = get_published_courses()
    context.categories = get_course_categories()
    context.cart_count = get_cart_count()

    context.title = "Kursverzeichnis — Live Online Sprachkurse | Vedium"
    context.description = (
        "Vedium Live-Kursverzeichnis: Englisch (A1 bis C1), Yoruba und "
        "Portugiesisch für Ausländer (PLE). Qualifizierte Lehrkräfte und Zertifikat."
    )
    context.lang = "de"
    context.canonical_url = "https://vediums.com/de/catalogo"
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
