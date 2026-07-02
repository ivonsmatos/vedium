import frappe

from vedium_core.courses import get_published_courses


def get_context(context):
    """
    Context for courses listing page
    Fetches all published courses from LMS
    """
    # Get all published courses
    context.courses = get_published_courses()

    # Get course categories for filtering
    context.categories = get_course_categories()

    # Shopping cart count
    context.cart_count = get_cart_count()

    # Page metadata (SEO) — título genérico: a página lista TODOS os idiomas
    # (Inglês, Iorubá, PLE), não só Inglês (bug achado no QA 2026-07-02: o
    # título antigo mencionava só "Inglês... A1 a C1", enganando quem chegava
    # via busca/redes procurando iorubá ou português para estrangeiros).
    context.title = "Catálogo de Cursos de Idiomas Online ao Vivo | Vedium"
    context.description = (
        "Catálogo de cursos online ao vivo da Vedium: Inglês (A1 ao C1), Iorubá e "
        "Português para Estrangeiros (PLE). Professores qualificados e certificado."
    )


def get_cart_count():
    """Get shopping cart item count for current user"""
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
    """Get all course categories for filtering"""
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
