import frappe

from vedium_core.course_urls import get_course_url

# Cache de páginas públicas (catálogo, landings, página de curso). Um único
# contador de versão, incrementado via doc_events (hooks.py) sempre que
# LMS Course/Course Chapter/Course Lesson/LMS Enrollment/LMS Course Review
# mudam — invalida TODAS as chaves de uma vez (mais simples que rastrear
# cada combinação de filtro individualmente). TTL é só um teto de segurança
# caso algum evento escape da invalidação explícita.
CACHE_VERSION_KEY = "vedium:courses_cache_version"
CACHE_TTL = 300  # 5 minutos


def _courses_cache_version():
    version = frappe.cache().get_value(CACHE_VERSION_KEY)
    if version is None:
        version = 1
        frappe.cache().set_value(CACHE_VERSION_KEY, version)
    return version


def bump_courses_cache_version(doc=None, method=None):
    """Invalida o cache de cursos públicos. Assinatura compatível com
    doc_events do Frappe (doc, method), registrada em hooks.py."""
    try:
        frappe.cache().set_value(CACHE_VERSION_KEY, _courses_cache_version() + 1)
    except Exception:
        pass


def get_published_courses(category_prefix=None, category_exact=None):
    """Busca cursos publicados da LMS, com dados enriquecidos para exibição.

    Usado tanto pelo /catalogo (todos os cursos) quanto pelas páginas pilar
    de campanha (filtradas por idioma via categoria) — ver marketing_landing_content.py.
    """
    cache_key = (
        f"vedium:published_courses:v{_courses_cache_version()}:"
        f"{category_prefix or ''}:{category_exact or ''}"
    )
    cached = frappe.cache().get_value(cache_key)
    if cached is not None:
        return cached

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
            course.url = get_course_url(course.name)

            if course.paid_course and course.course_price:
                course.formatted_price = format_price(course.course_price, course.currency)
            else:
                course.formatted_price = "Gratuito"

            course.level_badge = get_level_badge(course.title or "")
            schema_text = (course.short_introduction or course.title or "").strip()
            course.schema_description = schema_text[:60].rstrip()

            if course.category:
                course.category_name = frappe.db.get_value(
                    "LMS Category", course.category, "category"
                )

        level_order = {"A1": 1, "A2": 2, "B1": 3, "B1+": 4, "B2": 5, "C1": 6,
                       "Básico": 10, "Intermediário": 11, "Avançado": 12}
        courses.sort(key=lambda c: level_order.get(c.get("level_badge", ""), 99))

        frappe.cache().set_value(cache_key, courses, expires_in_sec=CACHE_TTL)
        return courses

    except Exception as e:
        frappe.log_error(f"Error fetching courses: {str(e)}", "Vedium Courses Page")
        return []


# Contas de sistema usadas como preenchimento obrigatório do campo
# "instructors" quando nenhum professor real foi associado ainda (ver
# scripts/migrations/oneshot/create_ple_courses.py:_default_instructor).
# Nunca podem aparecer numa página pública: mostrar "Administrator" como
# professor destrói a confiança que o card deveria construir.
PLACEHOLDER_INSTRUCTOR_ACCOUNTS = {"Administrator", "admin@example.com", "contato@vediums.com"}


def get_public_instructors(course_name):
    """Instrutores reais (nome + foto, se houver) de um curso, prontos pra
    exibição pública -- filtra as contas placeholder acima."""
    cache_key = f"vedium:public_instructors:v{_courses_cache_version()}:{course_name}"
    cached = frappe.cache().get_value(cache_key)
    if cached is not None:
        return cached

    rows = frappe.get_all(
        "Course Instructor",
        filters={"parent": course_name},
        fields=["instructor"],
    )
    instructors = []
    for row in rows:
        if row.instructor in PLACEHOLDER_INSTRUCTOR_ACCOUNTS:
            continue
        data = frappe.db.get_value(
            "User", row.instructor, ["full_name", "user_image"], as_dict=True
        )
        if data and data.full_name:
            instructors.append(data)

    frappe.cache().set_value(cache_key, instructors, expires_in_sec=CACHE_TTL)
    return instructors


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
        if "A0" in title or "Alfabetiza" in title:
            return "A0"
        if "A2" in title or "B1" in title:
            return "A2/B1"
        if "Bíblico" in title or "Biblico" in title:
            return "Bíblico"
        if "Particular" in title:
            return "1:1"
        return "A1"
    # Cursos CEFR (Inglês) — título já traz o código explícito (ex: "Inglês
    # Online ao Vivo B1+ – Intermediário"); checar "B1+" antes de "B1" evita
    # que o "+" seja perdido por match de substring.
    cefr = {
        "B1+": "B1+",
        "A1": "A1",
        "A2": "A2",
        "B1": "B1",
        "B2": "B2",
        "C1": "C1",
    }
    for label, code in cefr.items():
        if label in title:
            return code
    return ""
