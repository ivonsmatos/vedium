import frappe
from frappe import _
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def generate_sitemap():
    """
    Gera sitemap XML dinâmico para SEO
    """
    # URLs estáticas
    static_urls = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': '/courses', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': '/about', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': '/contact', 'priority': '0.6', 'changefreq': 'monthly'},
    ]
    
    # Buscar cursos publicados
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "modified"]
    )
    
    # Adicionar URLs de cursos
    course_urls = []
    for course in courses:
        course_urls.append({
            'loc': f'/courses/{course.name}',
            'priority': '0.8',
            'changefreq': 'weekly',
            'lastmod': course.modified.strftime('%Y-%m-%d')
        })
    
    # Combinar todas as URLs
    all_urls = static_urls + course_urls
    
    # Gerar XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in all_urls:
        xml += '  <url>\n'
        xml += f'    <loc>https://vediums.com{url["loc"]}</loc>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        if 'lastmod' in url:
            xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    return xml

@frappe.whitelist(allow_guest=True)
def get_course_schema(course_name):
    """
    Gera schema markup (dados estruturados) para curso
    """
    course = frappe.get_doc("LMS Course", course_name)
    
    schema = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": course.title,
        "description": course.short_introduction or course.description,
        "provider": {
            "@type": "Organization",
            "name": "Vedium Global Education",
            "url": "https://vediums.com"
        }
    }
    
    # Adicionar preço se for curso pago
    if course.paid_course and course.course_price:
        schema["offers"] = {
            "@type": "Offer",
            "price": str(course.course_price),
            "priceCurrency": course.currency or "BRL",
            "url": f"https://vediums.com/courses/{course.name}"
        }
    
    # Adicionar instrutor
    if course.instructor:
        instructor = frappe.get_doc("User", course.instructor)
        schema["instructor"] = {
            "@type": "Person",
            "name": instructor.full_name
        }
    
    # Adicionar avaliação se existir
    avg_rating = frappe.db.get_value(
        "LMS Course Review",
        {"course": course.name},
        "AVG(rating)"
    )
    
    if avg_rating:
        review_count = frappe.db.count(
            "LMS Course Review",
            {"course": course.name}
        )
        
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(round(avg_rating, 1)),
            "reviewCount": str(review_count)
        }
    
    return schema

@frappe.whitelist(allow_guest=True)
def get_organization_schema():
    """
    Gera schema markup para organização
    """
    return {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": "Vedium Global Education",
        "url": "https://vediums.com",
        "logo": "https://vediums.com/assets/vedium_core/images/logo.png",
        "description": "Plataforma de cursos online de idiomas: Inglês Executivo, Hebraico Tech e Iorubá Ancestral",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "BR"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "email": "contato@vediums.com",
            "contactType": "Customer Service"
        },
        "sameAs": [
            "https://facebook.com/vedium",
            "https://linkedin.com/company/vedium",
            "https://instagram.com/vedium"
        ]
    }
