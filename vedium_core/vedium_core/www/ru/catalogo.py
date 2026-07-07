import frappe

from vedium_core.courses import get_published_courses


def get_context(context):
    """Context for the Russian course catalog page (/ru/catalogo)."""
    context.courses = get_published_courses()
    context.categories = get_course_categories()
    context.cart_count = get_cart_count()

    context.title = "Каталог курсов — Живые онлайн-курсы языков | Vedium"
    context.description = (
        "Каталог живых курсов Vedium: английский (A1–C1), йоруба и "
        "португальский для иностранцев (PLE). Квалифицированные преподаватели и сертификат."
    )
    context.lang = "ru"
    context.canonical_url = "https://vediums.com/ru/catalogo"
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
