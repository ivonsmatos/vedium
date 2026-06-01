import frappe
from frappe import _


def get_context(context):
    """
    Context for course details page
    Fetches specific course details and related data
    """
    # Resolve course slug from /curso/<slug> route (form_dict) or path fallback
    course_name = frappe.form_dict.get("course")
    if not course_name:
        parts = [p for p in (frappe.local.path or "").split("/") if p and p not in ("curso", "course-details")]
        course_name = parts[-1] if parts else None

    if not course_name:
        # Acesso sem curso (ex.: /curso) -> redireciona ao catálogo
        frappe.local.flags.redirect_location = "/catalogo"
        raise frappe.Redirect

    # Get course details
    context.course = get_course_details(course_name)

    # Check if user is enrolled
    context.is_enrolled = check_enrollment(course_name)

    # Get related courses
    context.related_courses = get_related_courses(context.course.category, course_name)

    # Shopping cart count
    context.cart_count = get_cart_count()

    # Page metadata (SEO) — título com nome do curso, descrição e canonical
    context.title = f"{context.course.title} — Curso de Idiomas Online ao Vivo | Vedium"
    desc = (context.course.get("short_introduction") or "").strip()
    context.description = (desc[:155] if desc else
                           f"{context.course.title}: aulas ao vivo, professores e certificado. Matricule-se na Vedium.")
    context.canonical_url = f"https://vediums.com/curso/{course_name}"
    context.og_image = (context.course.image if context.course.image and context.course.image.startswith("http")
                        else f"https://vediums.com{context.course.image}") if context.course.image else "https://vediums.com/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png"
    context.lms_url = f"/lms/courses/{course_name}"

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
    try:
        # Get course document
        course = frappe.get_doc("LMS Course", course_name)
        
        if not course.published:
            frappe.throw("Course not available", frappe.PermissionError)
        
        # Fallback image
        if not course.image:
            course.image = "/assets/vedium_core/vedium_assets/images/resources/course-details-img1.jpg"
        
        # Get instructors with details
        course.instructors_list = []
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
                course.instructors_list.append(instructor_data)
        
        # Get chapters and lessons
        course.chapters_list = []
        try:
            course.chapters_list = frappe.get_all("Course Chapter",
                filters={"course": course.name},
                fields=["name", "title"],
                order_by="idx"
            )
            for chapter in course.chapters_list:
                try:
                    chapter.lessons = frappe.get_all("Course Lesson",
                        filters={"chapter": chapter.name},
                        fields=["name", "title"],
                        order_by="idx"
                    )
                except Exception:
                    chapter.lessons = []
        except Exception:
            course.chapters_list = []
        
        # Get total lesson count and duration
        course.total_lessons = frappe.db.count("Course Lesson", {"course": course.name})
        
        # Get enrollment count
        course.enrollment_count = frappe.db.count("LMS Enrollment", {"course": course.name})
        
        # Format price
        if course.paid_course and course.course_price:
            course.formatted_price = f"{course.currency or 'BRL'} {course.course_price:.2f}"
        else:
            course.formatted_price = "Gratuito"
        
        # Category name
        if course.category:
            course.category_name = frappe.db.get_value("LMS Category", course.category, "category")
        
        # Get reviews/ratings if available
        course.reviews = get_course_reviews(course_name)
        course.average_rating = calculate_average_rating(course.reviews)
        
        return course
        
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
            course.url = f"/curso/{course.name}"
            
            if course.paid_course and course.course_price:
                course.formatted_price = f"{course.currency or 'BRL'} {course.course_price:.2f}"
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
            reviews = frappe.get_all("LMS Course Review",
                filters={"course": course_name, "published": 1},
                fields=["rating", "review", "member", "creation"],
                order_by="creation desc",
                limit=10
            )
            
            for review in reviews:
                review.member_name = frappe.db.get_value("User", review.member, "full_name")
            
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
