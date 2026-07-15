from urllib.parse import quote

import frappe
from frappe import _

from vedium_core.course_translations import COURSE_TRANSLATIONS
from vedium_core.course_urls import get_course_url, get_internal_course_name
from vedium_core.courses import CACHE_TTL, _courses_cache_version


def get_context(context):
    """
    Context for course details page
    Fetches specific course details and related data
    """
    # Resolve course slug from /curso/<slug> ou /en/curso/<slug> (form_dict)
    # ou path fallback
    requested_slug = frappe.form_dict.get("course")
    if not requested_slug:
        parts = [p for p in (frappe.local.path or "").split("/") if p and p not in ("en", "curso", "course-details")]
        requested_slug = parts[-1] if parts else None

    if not requested_slug:
        # Acesso sem curso (ex.: /curso) -> redireciona ao catálogo
        frappe.local.flags.redirect_location = "/cursos-de-idiomas-online"
        raise frappe.Redirect

    course_name = get_internal_course_name(requested_slug)

    # Versão traduzida: só existe pra cursos com tradução (Iorubá e PLE —
    # público que não fala PT). Sem tradução no idioma pedido, manda pra
    # versão em português em vez de criar uma página fina/duplicada.
    # OBS: frappe.local.path NUNCA tem barra inicial — PathResolver.__init__
    # faz path.strip("/ ") antes de setar frappe.local.path (ver
    # frappe/website/path_resolver.py). Checar com "/en/curso/" (barra na
    # frente) nunca bate — bug real que só apareceu em produção, pego via
    # verificação pós-deploy (curl mostrou title/canonical em PT mesmo em
    # /en/curso/<slug>). lstrip("/") deixa a checagem à prova disso.
    path = (frappe.local.path or "").lstrip("/")
    req_lang = None
    for candidate in ("en", "es", "fr", "de", "ru"):
        if path.startswith(f"{candidate}/curso/"):
            req_lang = candidate
            break

    translations_for_course = COURSE_TRANSLATIONS.get(course_name, {})
    has_translation = bool(translations_for_course)
    if req_lang and req_lang not in translations_for_course:
        frappe.local.flags.redirect_location = get_course_url(course_name)
        raise frappe.Redirect
    translation = translations_for_course.get(req_lang) if req_lang else None

    # Get course details (preço, vagas, avaliações etc. sempre ao vivo do banco)
    context.course = get_course_details(course_name)
    if translation:
        context.course.title = translation["title"]
        context.course.short_introduction = translation["short_introduction"]
        context.course.description = translation["description"]

    context.lang = req_lang or "pt-BR"

    # Check if user is enrolled
    context.is_enrolled = check_enrollment(course_name)

    # Get related courses
    context.related_courses = get_related_courses(context.course.category, course_name)

    # Shopping cart count
    context.cart_count = get_cart_count()

    # Page metadata (SEO) — título com nome do curso, descrição e canonical
    _title_suffix = {
        "en": "Live Online Language Course",
        "es": "Curso de Idiomas Online en Vivo",
        "fr": "Cours de Langue en Ligne en Direct",
        "de": "Live-Online-Sprachkurs",
        "ru": "Живой онлайн-курс языка",
    }
    _fallback_desc = {
        "en": "{title}: live classes, real teachers and a certificate. Enroll at Vedium.",
        "es": "{title}: clases en vivo, profesores reales y certificado. Inscríbete en Vedium.",
        "fr": "{title} : cours en direct, vrais professeurs et certificat. Inscrivez-vous chez Vedium.",
        "de": "{title}: Live-Unterricht, echte Lehrkräfte und Zertifikat. Jetzt bei Vedium anmelden.",
        "ru": "{title}: живые занятия, настоящие преподаватели и сертификат. Регистрируйтесь в Vedium.",
    }
    if translation:
        context.title = f"{context.course.title} — {_title_suffix[req_lang]} | Vedium"
    else:
        context.title = f"{context.course.title} — Curso de Idiomas Online ao Vivo | Vedium"
    desc = (context.course.get("short_introduction") or "").strip()
    if translation:
        context.description = (desc[:155] if desc else
                               _fallback_desc[req_lang].format(title=context.course.title))
    else:
        meta_description = (context.course.get("meta_description") or "").strip()
        context.description = (
            meta_description
            or (desc[:155] if desc else f"{context.course.title}: aulas ao vivo, professores e certificado. Matricule-se na Vedium.")
        )
    context.meta_keywords = (context.course.get("meta_keywords") or "").strip() if not translation else ""
    context.canonical_url = (
        f"https://vediums.com{get_course_url(course_name, req_lang)}" if translation
        else f"https://vediums.com{get_course_url(course_name)}"
    )
    # hreflang recíproco — um link por idioma que realmente tem tradução
    # pra esse curso, mais o canônico em pt-BR.
    if has_translation:
        context.alt_langs = {"pt-br": f"https://vediums.com{get_course_url(course_name)}"}
        for lang_code in translations_for_course:
            context.alt_langs[lang_code] = f"https://vediums.com{get_course_url(course_name, lang_code)}"
    else:
        context.alt_langs = None
    context.og_image = (context.course.image if context.course.image and context.course.image.startswith("http")
                        else f"https://vediums.com{context.course.image}") if context.course.image else "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png"
    context.lms_url = (
        f"https://app.vediums.com/lms/courses/{course_name}"
        "?source=public_course&intent=enrollment"
    )
    # Botão "Matricular": vai direto pro Stripe Checkout hospedado
    # (vedium_core.api.start_course_checkout → checkout.stripe.com, em BRL),
    # em vez do formulário embutido do LMS nativo.
    checkout_base_url = (
        "https://app.vediums.com/api/method/vedium_core.api.start_course_checkout"
        f"?course_name={quote(str(course_name))}"
    )
    context.monthly_checkout_url = f"{checkout_base_url}&billing_period=monthly"
    context.annual_checkout_url = f"{checkout_base_url}&billing_period=annual"
    context.checkout_url = context.monthly_checkout_url
    context.annual_price = None
    if context.course.paid_course and context.course.course_price:
        context.annual_price = _format_price(
            float(context.course.course_price or 0) * 10,
            context.course.currency,
        )

    # GTM Event - view_course
    context.gtm_event = {
        'event': 'view_course',
        'course_name': context.course.title,
        'course_category': context.course.category_name if hasattr(context.course, 'category_name') else 'Geral',
        'course_price': float(context.course.course_price or 0),
        'currency': context.course.currency or 'BRL'
    }

def get_cart_count():
    """Get shopping cart item count for current user"""
    if frappe.session.user == "Guest":
        return 0
    
    if frappe.db.exists("DocType", "Quotation"):
        quotation = frappe.get_all("Quotation", 
            filters={"party_name": frappe.session.user, "docstatus": 0}, 
            fields=["name"],
            limit=1)
        if quotation:
            return frappe.db.count("Quotation Item", {"parent": quotation[0].name})
    return 0

def get_course_details(course_name):
    """Fetch complete course details"""
    cache_key = f"vedium:course_details:v{_courses_cache_version()}:{course_name}"
    cached = frappe.cache().get_value(cache_key)
    if cached is not None:
        return frappe._dict(cached)

    try:
        # Get course document
        course = frappe.get_doc("LMS Course", course_name)

        if not course.published:
            frappe.throw("Course not available", frappe.PermissionError)

        # Fallback image
        image = course.image or "/assets/vedium_core/vedium_assets/images/resources/course-details-img1.jpg"

        # Get instructors with details
        instructors_list = []
        instructors = frappe.get_all("Course Instructor",
            filters={"parent": course.name},
            fields=["instructor"]
        )

        for instructor in instructors:
            instructor_data = frappe.db.get_value("User",
                instructor.instructor,
                ["full_name", "user_image"],
                as_dict=True
            )
            if instructor_data:
                instructors_list.append(instructor_data)

        # Get chapters and lessons
        chapters_list = []
        try:
            chapters_list = frappe.get_all("Course Chapter",
                filters={"course": course.name},
                fields=["name", "title"],
                order_by="idx"
            )
            for chapter in chapters_list:
                try:
                    chapter.lessons = frappe.get_all("Course Lesson",
                        filters={"chapter": chapter.name},
                        fields=["name", "title", "idx"],
                        order_by="idx"
                    )
                    chapter.lessons = _dedupe_lessons(chapter.lessons)
                except Exception:
                    chapter.lessons = []
            chapters_list = _dedupe_chapters(chapters_list)
        except Exception:
            chapters_list = []

        # Get total lesson count and duration
        total_lessons = frappe.db.count("Course Lesson", {"course": course.name})

        # Get enrollment count
        enrollment_count = frappe.db.count("LMS Enrollment", {"course": course.name})

        if course.paid_course and course.course_price:
            formatted_price = _format_price(course.course_price, course.currency)
        else:
            formatted_price = "Gratuito"

        # Category name
        category_name = None
        if course.category:
            category_name = frappe.db.get_value("LMS Category", course.category, "category")

        # Get reviews/ratings if available
        reviews = get_course_reviews(course_name)
        average_rating = calculate_average_rating(reviews)

        result = course.as_dict()
        result.update({
            "image": image,
            "instructors_list": instructors_list,
            "chapters_list": chapters_list,
            "total_lessons": total_lessons,
            "enrollment_count": enrollment_count,
            "formatted_price": formatted_price,
            "category_name": category_name,
            "reviews": reviews,
            "average_rating": average_rating,
        })

        frappe.cache().set_value(cache_key, result, expires_in_sec=CACHE_TTL)
        return frappe._dict(result)

    except frappe.DoesNotExistError:
        frappe.throw(_("Curso não encontrado"), frappe.DoesNotExistError)
    except frappe.PermissionError:
        raise
    except Exception as e:
        frappe.log_error(f"Error fetching course details: {str(e)}", "Vedium Course Details")
        frappe.throw(_("Erro ao carregar detalhes do curso. Tente novamente."))

def check_enrollment(course_name):
    """Check if current user is enrolled in the course"""
    if frappe.session.user == "Guest":
        return False
    
    return frappe.db.exists("LMS Enrollment", {
        "course": course_name,
        "member": frappe.session.user
    })

def get_related_courses(category, exclude_course, limit=3):
    """Get related courses from same category"""
    if not category:
        return []
    
    try:
        courses = frappe.get_all("LMS Course",
            filters={
                "category": category,
                "published": 1,
                "name": ["!=", exclude_course]
            },
            fields=["name", "title", "short_introduction", "image", "course_price", "currency", "paid_course"],
            limit=limit
        )
        
        for course in courses:
            if not course.image:
                course.image = "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg"
            course.url = get_course_url(course.name)
            
            if course.paid_course and course.course_price:
                course.formatted_price = _format_price(course.course_price, course.currency)
            else:
                course.formatted_price = "Gratuito"
        
        return courses
    except Exception as e:
        frappe.log_error(f"Error fetching related courses: {str(e)}", "Vedium Course Details")
        return []

def get_course_reviews(course_name):
    """Get course reviews/ratings"""
    try:
        if frappe.db.exists("DocType", "LMS Course Review"):
            # LMS Course Review (v16) não tem colunas `member` nem `published`;
            # o autor da avaliação é o `owner` do registro.
            reviews = frappe.get_all("LMS Course Review",
                filters={"course": course_name},
                fields=["rating", "review", "owner", "creation"],
                order_by="creation desc",
                limit=10
            )

            for review in reviews:
                review.member_name = frappe.db.get_value("User", review.owner, "full_name")

            return reviews
    except Exception as e:
        frappe.log_error(f"Error fetching reviews: {str(e)}", "Vedium Course Details")
    
    return []

def calculate_average_rating(reviews):
    """Calculate average rating from reviews. M-14: filter out None ratings before dividing."""
    if not reviews:
        return 0
    rated = [r for r in reviews if r.rating]
    if not rated:
        return 0
    return round(sum(r.rating for r in rated) / len(rated), 1)


def _format_price(price, currency):
    p = float(price)
    if (currency or "BRL") == "USD":
        return f"US$ {p:,.2f}"
    return f"R$ {p:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _dedupe_chapters(chapters):
    """Avoid repeated curriculum blocks when production data contains duplicates."""
    seen = set()
    unique = []
    for chapter in chapters:
        key = (chapter.get("title") or chapter.get("name") or "").strip().lower()
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        unique.append(chapter)
    return unique


def _dedupe_lessons(lessons):
    """Render a clean ordered curriculum even if the LMS has duplicate lessons."""
    seen = set()
    unique = []
    for lesson in sorted(lessons, key=lambda item: (item.get("idx") or 0, item.get("title") or "")):
        key = (lesson.get("title") or lesson.get("name") or "").strip().lower()
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        unique.append(lesson)
    return unique
