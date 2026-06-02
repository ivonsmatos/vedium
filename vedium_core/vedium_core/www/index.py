import frappe

# Ordem de exibição dos idiomas no site
LANGUAGE_ORDER = ["Inglês", "Iorubá", "Português para Estrangeiros"]

# Fallback images por idioma (Unsplash free)
LANGUAGE_FALLBACK_IMAGES = {
    "Inglês": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg",
    "Iorubá": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img2.jpg",
    "Português para Estrangeiros": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img3.jpg",
}

DEFAULT_FALLBACK = (
    "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg"
)


def get_context(context):
    # Todos os cursos publicados, agrupados por idioma
    context.courses = get_courses()
    context.courses_by_language = get_courses_by_language()
    context.featured_courses = context.courses[:4] if context.courses else []

    # Idiomas disponíveis para filtro no template
    context.language_programs = LANGUAGE_ORDER

    # Shopping Cart Count
    context.cart_count = get_cart_count()


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


def get_courses():
    """Todos os cursos publicados, enriquecidos, ordenados por idioma e nível."""
    try:
        courses = frappe.get_all(
            "LMS Course",
            fields=[
                "name",
                "title",
                "short_introduction",
                "image",
                "category",
                "paid_course",
                "course_price",
                "currency",
            ],
            filters={"published": 1},
            limit=50,
        )
        return [_enrich(c) for c in courses]
    except Exception as e:
        frappe.log_error(f"Error fetching courses: {e}", "Vedium LMS")
        return []


def get_courses_by_language():
    """Retorna dict {idioma: [cursos]} para uso no template com agrupamento."""
    all_courses = get_courses()
    result = {lang: [] for lang in LANGUAGE_ORDER}

    for course in all_courses:
        # Detecta idioma pela categoria (ex: "Inglês - Beginner" → "Inglês")
        lang = _detect_language(course.get("category", ""))
        if lang in result:
            result[lang].append(course)
        else:
            # Idioma ainda não mapeado — cria entrada dinâmica
            result[lang] = [course]

    return result


def _detect_language(category: str) -> str:
    """Infere o idioma-pai a partir do nome da categoria do curso."""
    if not category:
        return "Outros"
    for lang in LANGUAGE_ORDER:
        if category.startswith(lang):
            return lang
    return "Outros"


def _enrich(course) -> dict:
    """Adiciona campos renderizáveis ao objeto de curso."""
    course = dict(course)

    # Imagem de fallback
    if not course.get("image"):
        lang = _detect_language(course.get("category", ""))
        course["image"] = LANGUAGE_FALLBACK_IMAGES.get(lang, DEFAULT_FALLBACK)

    # Nome do instrutor (instructors é child table, busca só o primeiro)
    instructors = frappe.get_all(
        "Course Instructor",
        filters={"parent": course["name"]},
        fields=["instructor"],
        limit=1,
    )
    if instructors:
        _idata = frappe.db.get_value("User", instructors[0]["instructor"], ["full_name", "user_image"], as_dict=True)
        course["instructor_name"] = (_idata.full_name if _idata else None) or "Vedium Instructor"
        course["instructor_image"] = _idata.user_image if _idata else None
    else:
        course["instructor_name"] = "Vedium Instructor"
        course["instructor_image"] = None

    # Preço formatado
    if course.get("paid_course") and course.get("course_price"):
        price = float(course["course_price"])
        course["formatted_price"] = (
            f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
    else:
        course["formatted_price"] = "Gratuito"

    # Nível CEFR a partir do título (ex: "Inglês - Beginner" → "A1")
    course["level_badge"] = _level_badge(course.get("title", ""))

    return course


def _level_badge(title: str) -> str:
    BADGES = {
        "Beginner": "A1",
        "Elementary": "A2",
        "Pré-Intermediário": "B1-",
        "Intermediário": "B1",
        "Upper Intermediário": "B2",
        "Avançado": "C1",
    }
    for label, code in BADGES.items():
        if label in title:
            return code
    return ""
