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
    {"loc": "/professores", "priority": "0.7", "changefreq": "monthly"},
    {
        "loc": "/professor-busayo-frank-alonge",
        "priority": "0.6",
        "changefreq": "monthly",
    },
    {"loc": "/faq", "priority": "0.7", "changefreq": "monthly"},
    {"loc": "/teste-de-nivel", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/teste-de-nivel-ingles", "priority": "0.8", "changefreq": "monthly"},
    {"loc": "/contato", "priority": "0.6", "changefreq": "monthly"},
    {"loc": "/carreiras", "priority": "0.5", "changefreq": "monthly"},
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
]

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


def _absolute_url(path):
    return f"{SITE_URL}{quote(path, safe='/-')}"


def _localized_urls():
    for prefix in LANGUAGE_ROUTE_PREFIXES:
        for url in STATIC_URLS:
            loc = f"/{prefix}/" if url["loc"] == "/" else f"/{prefix}{url['loc']}"
            yield {
                **url,
                "loc": loc,
                "priority": "0.6" if url["loc"] == "/" else "0.5",
            }


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

    return [
        {
            "loc": f"/curso/{course.name}",
            "priority": "0.8",
            "changefreq": "weekly",
            "lastmod": course.modified.strftime("%Y-%m-%d")
            if course.modified
            else nowdate(),
        }
        for course in courses
    ]


def get_context(context):
    today = nowdate()
    urls = STATIC_URLS + list(_localized_urls()) + _course_urls()

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
