import frappe
from frappe import _

from vedium_core.course_urls import get_course_url


SITE_URL = "https://vediums.com"


@frappe.whitelist(allow_guest=True)
def get_course_schema(course_name):
    """Schema.org Course markup para uma página de curso."""
    course = frappe.get_doc("LMS Course", course_name)

    schema = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course.title,
        "description": course.short_introduction or course.description,
        "provider": {
            "@type": "Organization",
            "name": "Vedium Global Education",
            "url": SITE_URL,
        },
    }

    if course.paid_course and course.course_price:
        schema["offers"] = {
            "@type": "Offer",
            "price": str(course.course_price),
            "priceCurrency": course.currency or "BRL",
            "url": f"{SITE_URL}{get_course_url(course.name)}",
        }

    # Instrutor — Course Instructor é child table; pegar o primeiro
    instructors = frappe.get_all(
        "Course Instructor",
        filters={"parent": course.name},
        fields=["instructor"],
        limit=1,
    )
    if instructors:
        instructor = frappe.db.get_value(
            "User", instructors[0].instructor, "full_name"
        )
        if instructor:
            schema["instructor"] = {"@type": "Person", "name": instructor}

    if frappe.db.exists("DocType", "LMS Course Review"):
        avg_rating = frappe.db.get_value(
            "LMS Course Review", {"course": course.name}, "AVG(rating)"
        )
        if avg_rating:
            review_count = frappe.db.count(
                "LMS Course Review", {"course": course.name}
            )
            schema["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": str(round(avg_rating, 1)),
                "reviewCount": str(review_count),
            }

    return schema


@frappe.whitelist(allow_guest=True)
def get_organization_schema():
    """Schema.org EducationalOrganization."""
    return {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "Vedium Global Education",
        "url": SITE_URL,
        "logo": f"{SITE_URL}/assets/vedium_core/vedium_assets/images/logos/Logo-color-quadrada.png",
        "description": (
            "Escola de idiomas online com aulas ao vivo de inglês, espanhol, "
            "hebraico, iorubá e português para estrangeiros."
        ),
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "BR",
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "email": "contato@vediums.com",
            "contactType": "Customer Service",
        },
        "sameAs": [
            "https://www.instagram.com/vediumsglobal/",
            "https://www.linkedin.com/company/vediums",
        ],
    }
