import frappe
from frappe import _


SITE_URL = "https://vediums.com"
LANGUAGE_ROUTE_PREFIXES = (
    "pt-br",
    "en",
    "en-us",
    "en-au",
    "es",
    "es-ar",
    "es-co",
    "fr",
    "fr-ca",
    "de",
    "ru",
    "zh-cn",
)


@frappe.whitelist(allow_guest=True)
def generate_sitemap():
    """
    Gera sitemap XML dinâmico para SEO.

    Retorna o XML cru com Content-Type correto (não envolve em JSON do Frappe).
    Para servir em /sitemap.xml, mapear no nginx para esta whitelisted route.
    """
    static_urls = [
        {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": "/catalogo", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/sobre", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/como-funciona", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/faq", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/teste-de-nivel", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/contato", "priority": "0.6", "changefreq": "monthly"},
        {"loc": "/carreiras", "priority": "0.5", "changefreq": "monthly"},
        {"loc": "/ingles-para-entrevista", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/ingles-para-programadores", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/ingles-executivo", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/ingles-para-viagens", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/ingles-para-atendimento-ao-cliente", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/curso-de-ioruba-online", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/ioruba-para-iniciantes", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/ioruba-cultura-e-ancestralidade", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/portugues-para-estrangeiros", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/portugues-para-executivos", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/preparatorio-celpe-bras", "priority": "0.7", "changefreq": "monthly"},
    ]

    try:
        courses = frappe.get_all(
            "LMS Course",
            filters={"published": 1},
            fields=["name", "modified"],
        )
    except Exception as e:
        frappe.log_error(f"Sitemap: erro buscando cursos: {e}", "Vedium.seo.sitemap")
        courses = []

    course_urls = [
        {
            "loc": f"/curso/{c.name}",
            "priority": "0.8",
            "changefreq": "weekly",
            "lastmod": c.modified.strftime("%Y-%m-%d") if c.modified else None,
        }
        for c in courses
    ]

    localized_static_urls = [
        {
            **url,
            "loc": f"/{prefix}/" if url["loc"] == "/" else f"/{prefix}{url['loc']}",
            "priority": "0.6" if url["loc"] == "/" else "0.5",
        }
        for prefix in LANGUAGE_ROUTE_PREFIXES
        for url in static_urls
    ]

    all_urls = static_urls + localized_static_urls + course_urls

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in all_urls:
        parts.append("  <url>")
        parts.append(f"    <loc>{SITE_URL}{url['loc']}</loc>")
        parts.append(f"    <priority>{url['priority']}</priority>")
        parts.append(f"    <changefreq>{url['changefreq']}</changefreq>")
        if url.get("lastmod"):
            parts.append(f"    <lastmod>{url['lastmod']}</lastmod>")
        parts.append("  </url>")
    parts.append("</urlset>")

    xml = "\n".join(parts)

    # Devolver XML cru (sem JSON wrap do Frappe)
    frappe.response["type"] = "binary"
    frappe.response["filecontent"] = xml.encode("utf-8")
    frappe.response["filename"] = "sitemap.xml"
    frappe.response["content_type"] = "application/xml; charset=utf-8"


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
            "url": f"{SITE_URL}/curso/{course.name}",
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
            "Plataforma de cursos online de idiomas: Inglês Executivo, "
            "Iorubá Ancestral e Português para Estrangeiros."
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
