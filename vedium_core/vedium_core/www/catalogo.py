import frappe


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


def get_published_courses():
    """Fetch all published courses with enriched data"""
    try:
        courses = frappe.get_all(
            "LMS Course",
            fields=[
                "name",
                "title",
                "short_introduction",
                "image",
                "paid_course",
                "course_price",
                "currency",
                "category",
                "published",
            ],
            filters={"published": 1},
            order_by="creation desc",
        )

        # Enrich each course with additional data
        for course in courses:
            # Fallback image
            if not course.image:
                course.image = "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg"

            # Get lesson count
            course.lesson_count = frappe.db.count(
                "Course Lesson", {"course": course.name}
            )

            # Get enrollment count
            course.enrollment_count = frappe.db.count(
                "LMS Enrollment", {"course": course.name}
            )

            # Course URL — página SEO server-rendered (não o SPA)
            course.url = f"/curso/{course.name}"

            # Format price
            if course.paid_course and course.course_price:
                course.formatted_price = _format_price(course.course_price, course.currency)
            else:
                course.formatted_price = "Gratuito"

            # CEFR level badge from title
            course.level_badge = _get_level_badge(course.title or "")

            # Category name
            if course.category:
                course.category_name = frappe.db.get_value(
                    "LMS Category", course.category, "category"
                )

        # Sort by level — CEFR first (A1→C1), PLE after, outros por último
        level_order = {"A1": 1, "A2": 2, "B1-": 3, "B1": 4, "B2": 5, "C1": 6,
                       "Básico": 10, "Intermediário": 11, "Avançado": 12}
        courses.sort(key=lambda c: level_order.get(c.get("level_badge", ""), 99))

        return courses

    except Exception as e:
        frappe.log_error(f"Error fetching courses: {str(e)}", "Vedium Courses Page")
        return []


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


def _format_price(price, currency):
    p = float(price)
    if (currency or "BRL") == "USD":
        return f"US$ {p:,.2f}"
    return f"R$ {p:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _get_level_badge(title):
    """Retorna o nível/código a partir do título do curso."""
    # PLE tem labels próprios (não CEFR)
    if "PLE" in title or "Estrangeiros" in title:
        for label in ("Básico", "Intermediário", "Avançado"):
            if label in title:
                return label
    # Cursos CEFR (Inglês, Iorubá)
    cefr = {
        "Beginner": "A1",
        "Elementary": "A2",
        "Pré-Intermediário": "B1-",
        "Upper Intermediário": "B2",
        "Intermediário": "B1",
        "Avançado": "C1",
    }
    for label, code in cefr.items():
        if label in title:
            return code
    return ""
