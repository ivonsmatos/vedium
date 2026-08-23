import frappe
from vedium_core.course_urls import get_course_url
from vedium_core.image_optimization import responsive_course_image

# Mesma lógica de vedium_core.www.index (duplicada, não importada): não há
# __init__.py em www/, então import cruzado entre controllers www/*.py não é
# um padrão testado no Frappe (template_page.set_pymodule importa cada
# controller isoladamente). Mantém os dois arquivos em sincronia manualmente
# se a lógica de cursos mudar.
LANGUAGE_ORDER = ["Inglês", "Espanhol", "Hebraico", "Iorubá", "Português para Estrangeiros"]

LANGUAGE_FALLBACK_IMAGES = {
    "Inglês": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg",
    "Espanhol": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg",
    "Hebraico": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img3.jpg",
    "Iorubá": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img2.jpg",
    "Português para Estrangeiros": "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img3.jpg",
}

DEFAULT_FALLBACK = (
    "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg"
)


def get_context(context):
    _redirect_app_root_to_login()

    context.courses = get_courses()
    context.courses_by_language = get_courses_by_language(context.courses)
    context.featured_courses = context.courses[:4] if context.courses else []
    context.language_programs = LANGUAGE_ORDER
    context.cart_count = get_cart_count()

    # Preços do Inglês em USD — convertidos por câmbio do catálogo (INTERIM até
    # existir preço USD fixo). Fonte única: checkout_options (bate com o checkout).
    from vedium_core.checkout_options import get_frequency_plans_for_display

    context.english_plans = get_frequency_plans_for_display("ingl-s-beginner", "USD")

    context.title = "Vedium - Live Online Courses in Five Languages"
    context.description = (
        "Learn English, Spanish, Hebrew, Yoruba or Brazilian Portuguese with Vedium: "
        "live classes, qualified teachers, a completion certificate and real support. "
        "Start your fluency journey today."
    )
    context.lang = "en"
    context.canonical_url = "https://vediums.com/en"
    context.alt_lang_url = "https://vediums.com/"


def _redirect_app_root_to_login():
    """Keep app.vediums.com as product/login, while vediums.com remains marketing."""
    request = getattr(frappe.local, "request", None)
    host_candidates = [
        frappe.get_request_header("X-Forwarded-Host"),
        frappe.get_request_header("Host"),
        getattr(request, "host", ""),
        getattr(request, "host_url", ""),
    ]
    host = " ".join(str(item or "") for item in host_candidates).lower()
    path = getattr(frappe.local, "path", "") or getattr(request, "path", "") or "/"
    if "app.vediums.com" in host and path in ("", "/"):
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect


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


def get_courses_by_language(all_courses=None):
    """Retorna dict {idioma: [cursos]} para uso no template com agrupamento."""
    if all_courses is None:
        all_courses = get_courses()
    result = {lang: [] for lang in LANGUAGE_ORDER}

    for course in all_courses:
        lang = _detect_language(course.get("category", ""))
        if lang in result:
            result[lang].append(course)
        else:
            result[lang] = [course]

    return result


def _detect_language(category: str) -> str:
    if not category:
        return "Outros"
    for lang in LANGUAGE_ORDER:
        if category.startswith(lang):
            return lang
    return "Outros"


def _enrich(course) -> dict:
    course = dict(course)

    if not course.get("image"):
        lang = _detect_language(course.get("category", ""))
        course["image"] = LANGUAGE_FALLBACK_IMAGES.get(lang, DEFAULT_FALLBACK)
    course.update(responsive_course_image(course["image"]))

    if course.get("paid_course") and course.get("course_price"):
        price = float(course["course_price"])
        course["formatted_price"] = (
            f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
    else:
        course["formatted_price"] = "Free"

    course["level_badge"] = _level_badge(course.get("title", ""))
    course["url"] = get_course_url(course["name"])

    return course


def _level_badge(title: str) -> str:
    # Course titles now carry the explicit CEFR code (e.g. "Inglês Online
    # ao Vivo B1+ – Intermediário") — check "B1+" before "B1" so the "+"
    # is not lost to a substring match.
    BADGES = {
        "B1+": "B1+",
        "A1": "A1",
        "A2": "A2",
        "B1": "B1",
        "B2": "B2",
        "C1": "C1",
    }
    for label, code in BADGES.items():
        if label in title:
            return code
    return ""
