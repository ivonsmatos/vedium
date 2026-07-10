import frappe


def get_published_courses(category_prefix=None, category_exact=None):
    """Busca cursos publicados da LMS, com dados enriquecidos para exibição.

    Usado tanto pelo /catalogo (todos os cursos) quanto pelas páginas pilar
    de campanha (filtradas por idioma via categoria) — ver marketing_landing_content.py.
    """
    try:
        filters = {"published": 1}
        if category_exact:
            filters["category"] = category_exact
        elif category_prefix:
            filters["category"] = ["like", f"{category_prefix}%"]

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
            filters=filters,
            order_by="creation desc",
        )

        for course in courses:
            if not course.image:
                course.image = "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg"

            course.lesson_count = frappe.db.count("Course Lesson", {"course": course.name})
            course.enrollment_count = frappe.db.count("LMS Enrollment", {"course": course.name})
            course.url = f"/curso/{course.name}"

            if course.paid_course and course.course_price:
                course.formatted_price = format_price(course.course_price, course.currency)
            else:
                course.formatted_price = "Gratuito"

            course.level_badge = get_level_badge(course.title or "")

            if course.category:
                course.category_name = frappe.db.get_value(
                    "LMS Category", course.category, "category"
                )

        level_order = {"A1": 1, "A2": 2, "B1-": 3, "B1": 4, "B2": 5, "C1": 6,
                       "Básico": 10, "Intermediário": 11, "Avançado": 12}
        courses.sort(key=lambda c: level_order.get(c.get("level_badge", ""), 99))

        return courses

    except Exception as e:
        frappe.log_error(f"Error fetching courses: {str(e)}", "Vedium Courses Page")
        return []


def format_price(price, currency):
    p = float(price)
    if (currency or "BRL") == "USD":
        return f"US$ {p:,.2f}"
    return f"R$ {p:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def get_level_badge(title):
    """Retorna o nível/rótulo a partir do título do curso.

    PLE e Iorubá usam rótulos próprios (Básico/Intermediário/Avançado) — não
    são cursos CEFR, ainda que o título de Inglês também contenha "Avançado"
    (nesse caso mapeado para C1 mais abaixo).
    """
    if "PLE" in title or "Estrangeiros" in title or "Iorubá" in title or "Espanhol" in title:
        for label in ("Básico", "Intermediário", "Avançado"):
            if label in title:
                return label
    if "Hebraico" in title:
        return "A1"
    # Cursos CEFR (Inglês)
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
