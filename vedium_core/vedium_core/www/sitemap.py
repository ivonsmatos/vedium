from urllib.parse import quote

import frappe
from frappe.utils import nowdate


no_cache = 1
base_template_path = "www/sitemap.xml"

SITE_URL = "https://vediums.com"

STATIC_URLS = [
    {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
    {"loc": "/catalogo", "priority": "0.9", "changefreq": "daily"},
    {"loc": "/sobre", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/como-funciona", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/aula-diagnostica", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/planos", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/quanto-custa-curso-de-idiomas", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/matricula", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/certificado", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/termos", "priority": "0.3", "changefreq": "monthly"},
    {"loc": "/privacidade", "priority": "0.3", "changefreq": "monthly"},
    {"loc": "/cookies", "priority": "0.3", "changefreq": "monthly"},
    {"loc": "/cancelamento-reembolso", "priority": "0.3", "changefreq": "monthly"},
    {"loc": "/gravacao-imagem-voz", "priority": "0.2", "changefreq": "monthly"},
    {"loc": "/propriedade-intelectual", "priority": "0.2", "changefreq": "monthly"},
    {"loc": "/comunidade", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/programa-de-indicacao", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/empresas", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/faq", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/diferenciais", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/metodologia", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/teste-de-nivel", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/teste-de-nivel-ingles", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/contato", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/carreiras", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/curso-de-ingles-online", "priority": "0.9", "changefreq": "monthly"},
    {"loc": "/ingles-para-entrevista", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/ingles-para-programadores", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/ingles-executivo", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/ingles-para-viagens", "priority": "0.7", "changefreq": "monthly"},
    {
        "loc": "/ingles-para-atendimento-ao-cliente",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {"loc": "/curso-de-ioruba-online", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/ioruba-para-iniciantes", "priority": "0.7", "changefreq": "monthly"},
    {
        "loc": "/ioruba-cultura-e-ancestralidade",
        "priority": "0.7",
        "changefreq": "monthly",
    },
    {"loc": "/portugues-para-estrangeiros", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/portugues-para-executivos", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/preparatorio-celpe-bras", "priority": "0.7", "changefreq": "monthly"},
    # Blog (índice; os posts individuais vêm de _blog_urls(), dinâmico —
    # cobre tanto os de código quanto os publicados pelo painel)
    {"loc": "/blog", "priority": "0.7", "changefreq": "weekly"},
    # Páginas em inglês (SEO internacional)
    {"loc": "/en", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "/en/catalogo", "priority": "0.8", "changefreq": "daily"},
    {"loc": "/en/sobre", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/como-funciona", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/en/faq", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/contato", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/en/planos", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/en/matricula", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/en/aula-diagnostica", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/en/learn-yoruba-online", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/en/learn-portuguese-brazil", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/en/portuguese-placement-test", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/yoruba-for-beginners", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/yoruba-culture-and-heritage", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/portuguese-for-executives", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/celpe-bras-exam-prep", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/learn-english-online", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/en/english-for-job-interviews", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/english-for-developers", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/business-english-online", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/english-for-travel", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/english-for-customer-service", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/en/certificado", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/en/comunidade", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/en/programa-de-indicacao", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/en/empresas", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/en/carreiras", "priority": "0.4", "changefreq": "monthly"},
    # Páginas em espanhol (SEO internacional)
    {"loc": "/es", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "/es/catalogo", "priority": "0.8", "changefreq": "daily"},
    {"loc": "/es/sobre", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/como-funciona", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/es/faq", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/contato", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/es/planos", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/es/matricula", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/es/aula-diagnostica", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/es/prueba-de-nivel-de-portugues", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/curso-de-ingles-online-en-vivo", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/es/ingles-para-entrevistas-de-trabajo", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/ingles-para-programadores", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/ingles-de-negocios", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/ingles-para-viajar", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/ingles-para-atencion-al-cliente", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/curso-de-yoruba-online", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/es/yoruba-para-principiantes", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/yoruba-cultura-y-ancestralidad", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/portugues-para-extranjeros", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/es/portugues-para-ejecutivos", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/preparacion-examen-celpe-bras", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/es/certificado", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/es/comunidade", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/es/programa-de-indicacao", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/es/empresas", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/es/carreiras", "priority": "0.4", "changefreq": "monthly"},
    # Páginas em francês (SEO internacional)
    {"loc": "/fr", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "/fr/catalogo", "priority": "0.8", "changefreq": "daily"},
    {"loc": "/fr/sobre", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/como-funciona", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/fr/faq", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/contato", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/fr/planos", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/fr/matricula", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/fr/aula-diagnostica", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/fr/test-de-niveau-de-portugais", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/portugais-pour-etrangers", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/fr/portugais-pour-cadres", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/preparation-examen-celpe-bras", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/cours-anglais-en-ligne-en-direct", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/fr/anglais-entretien-embauche", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/anglais-developpeurs-informatique", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/anglais-des-affaires", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/anglais-pour-voyager", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/anglais-service-client", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/fr/certificado", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/fr/comunidade", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/fr/programa-de-indicacao", "priority": "0.4", "changefreq": "monthly"},
    {"loc": "/fr/empresas", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/fr/carreiras", "priority": "0.4", "changefreq": "monthly"},
    # Páginas em alemão (SEO internacional)
    {"loc": "/de", "priority": "0.9", "changefreq": "weekly"},
    {"loc": "/de/catalogo", "priority": "0.8", "changefreq": "daily"},
    {"loc": "/de/sobre", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/como-funciona", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/de/faq", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/contato", "priority": "0.5", "changefreq": "monthly"},
    {"loc": "/de/planos", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/de/matricula", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/de/aula-diagnostica", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/de/portugiesisch-einstufungstest", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/portugiesisch-fuer-auslaender", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/de/portugiesisch-fuer-fuehrungskraefte", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/celpe-bras-pruefungsvorbereitung", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/englischkurs-online-live", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/de/englisch-fuer-vorstellungsgespraeche", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/englisch-fuer-entwickler", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/business-englisch-online", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/englisch-fuer-reisen", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/de/englisch-fuer-kundenservice", "priority": "0.6", "changefreq": "monthly"},
]

def _absolute_url(path):
    return f"{SITE_URL}{quote(path, safe='/-')}"


def _course_urls():
    try:
        courses = frappe.get_all(
            "LMS Course",
            filters={"published": 1},
            fields=["name", "modified"],
        )
    except Exception as exc:
        frappe.log_error(f"Sitemap: erro buscando cursos: {exc}", "Vedium.sitemap")
        return []

    from vedium_core.course_translations import COURSE_TRANSLATIONS

    urls = []
    for course in courses:
        lastmod = course.modified.strftime("%Y-%m-%d") if course.modified else nowdate()
        urls.append({
            "loc": f"/curso/{course.name}",
            "priority": "0.8",
            "changefreq": "weekly",
            "lastmod": lastmod,
        })
        if course.name in COURSE_TRANSLATIONS:
            urls.append({
                "loc": f"/en/curso/{course.name}",
                "priority": "0.6",
                "changefreq": "weekly",
                "lastmod": lastmod,
            })
    return urls


def _blog_urls():
    try:
        from vedium_core.blog_content import list_blog_posts

        return [
            {"loc": post["url"], "priority": "0.6", "changefreq": "monthly"}
            for post in list_blog_posts()
        ]
    except Exception as exc:
        frappe.log_error(f"Sitemap: erro buscando posts do blog: {exc}", "Vedium.sitemap")
        return []


def get_context(context):
    today = nowdate()
    urls = STATIC_URLS + _course_urls() + _blog_urls()

    context.no_cache = 1
    context.links = [
        {
            "loc": _absolute_url(url["loc"]),
            "lastmod": url.get("lastmod") or today,
            "changefreq": url["changefreq"],
            "priority": url["priority"],
        }
        for url in urls
    ]
    return context
