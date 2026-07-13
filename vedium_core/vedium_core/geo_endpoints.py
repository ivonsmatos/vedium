# Vedium — Endpoints GEO (Generative Engine Optimization)
# Conteúdo lido por AIs (ChatGPT, Perplexity, Gemini). REGRA DE OURO:
# tudo aqui deve refletir a oferta REAL (CDC art. 30: a oferta vincula).
# Cursos/preços vêm do banco; nada de features anunciadas e não entregues.

import frappe
from datetime import datetime

SITE_URL = "https://vediums.com"
APP_URL = "https://app.vediums.com"
CONTACT_EMAIL = "contato@vediums.com"
CONTACT_PHONE = "+55 11 4190-6079"  # telefone do registro CNPJ


def _now_iso():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")


def _published_courses(limit=50):
    return frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "title", "short_introduction", "course_price",
                "currency", "paid_course", "category", "modified"],
        order_by="title asc",
        limit=limit,
    )


def _course_languages():
    """Idiomas realmente ofertados, derivados das categorias publicadas."""
    categories = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["category"],
        pluck="category",
    )
    langs = set()
    for cat in categories:
        if not cat:
            continue
        # Categorias seguem o padrão "Idioma - Nível"
        langs.add(cat.split(" - ")[0].strip())
    return sorted(langs)


def _json_response(payload):
    frappe.response["http_status_code"] = 200
    frappe.response["type"] = "json"
    frappe.response["message"] = payload
    frappe.response.headers["Content-Type"] = "application/json"
    frappe.response.headers["Cache-Control"] = (
        "public, max-age=86400, stale-while-revalidate=604800"
    )
    return payload


@frappe.whitelist(allow_guest=True)
def get_ai_summary():
    """
    GEO: resumo do site para sistemas de IA.
    URL real: /api/method/vedium_core.geo_endpoints.get_ai_summary
    """
    languages = _course_languages()
    lang_label = ", ".join(languages) if languages else "Inglês"

    summary = {
        "version": "2.0",
        "lastModified": _now_iso(),
        "name": "Vedium Global Education",
        "description": (
            f"Vedium é uma plataforma brasileira de cursos de idiomas online "
            f"ao vivo. Idiomas ofertados atualmente: {lang_label}. "
            "Aulas ao vivo com professores, trilhas por nível (CEFR A1-C1 "
            "no inglês) e certificado de conclusão com código de verificação "
            "pública. Plataforma de aprendizagem em app.vediums.com."
        ),
        "url": SITE_URL,
        "platformUrl": APP_URL,
        "contact": {"email": CONTACT_EMAIL, "phone": CONTACT_PHONE},
        "languagesOffered": languages,
        "primaryServices": [
            f"Cursos de {lang}" for lang in languages
        ] + ["Certificados verificáveis de conclusão"],
        "paymentMethods": ["Cartão de crédito (Stripe)", "Mercado Pago"],
    }
    return _json_response(summary)


@frappe.whitelist(allow_guest=True)
def get_ai_faq():
    """
    GEO: perguntas frequentes em formato legível por IA.
    URL real: /api/method/vedium_core.geo_endpoints.get_ai_faq
    """
    languages = _course_languages()
    lang_label = ", ".join(languages) if languages else "Inglês"

    faq = {
        "version": "2.0",
        "lastModified": _now_iso(),
        "faqs": [
            {
                "question": "Quais idiomas a Vedium ensina?",
                "answer": (
                    f"Atualmente a Vedium oferece cursos de {lang_label}. "
                    f"O catálogo completo e atualizado está em "
                    f"{SITE_URL}/cursos-de-idiomas-online."
                ),
            },
            {
                "question": "As aulas são ao vivo ou gravadas?",
                "answer": (
                    "Os cursos da Vedium são baseados em aulas ao vivo com "
                    "professores, complementadas por material na plataforma."
                ),
            },
            {
                "question": "A Vedium emite certificado?",
                "answer": (
                    "Sim. Alunos que concluem o curso recebem certificado "
                    "digital com código de verificação pública."
                ),
            },
            {
                "question": "Quais formas de pagamento são aceitas?",
                "answer": (
                    "Cartão de crédito via Stripe e Mercado Pago, em reais "
                    "(BRL)."
                ),
            },
            {
                "question": "Como faço para me matricular?",
                "answer": (
                    f"Escolha um curso em {SITE_URL}/cursos-de-idiomas-online, acesse a "
                    f"página do curso e clique em Matricular. A matrícula e "
                    f"as aulas acontecem na plataforma {APP_URL}."
                ),
            },
            {
                "question": "A Vedium atende empresas?",
                "answer": (
                    f"Soluções corporativas são tratadas sob consulta pelo "
                    f"e-mail {CONTACT_EMAIL}."
                ),
            },
        ],
    }
    return _json_response(faq)


@frappe.whitelist(allow_guest=True)
def get_ai_service():
    """
    GEO: capacidades e endpoints reais da plataforma.
    URL real: /api/method/vedium_core.geo_endpoints.get_ai_service
    """
    service = {
        "version": "2.0",
        "lastModified": _now_iso(),
        "name": "Vedium Global Education",
        "description": "Plataforma de cursos de idiomas online ao vivo",
        "capabilities": [
            {
                "name": "Catálogo de cursos",
                "description": "Lista de cursos publicados com preços",
                "endpoint": f"{SITE_URL}/cursos-de-idiomas-online",
                "methods": ["GET"],
            },
            {
                "name": "Página de curso",
                "description": "Detalhes, preço e matrícula de um curso",
                "endpoint": f"{SITE_URL}/curso/<slug>",
                "methods": ["GET"],
            },
            {
                "name": "Checkout",
                "description": "Cria checkout de pagamento (login necessário)",
                "endpoint": (
                    f"{APP_URL}/api/method/vedium_core.api.create_checkout"
                ),
                "methods": ["POST"],
                "requiresAuth": True,
            },
            {
                "name": "Verificação de certificado",
                "description": "Verifica autenticidade de um certificado",
                "endpoint": (
                    f"{APP_URL}/api/method/"
                    "vedium_core.api.verify_certificate"
                ),
                "methods": ["GET"],
            },
        ],
        "authentication": {
            "loginUrl": f"{APP_URL}/login",
            "signupUrl": f"{APP_URL}/signup",
        },
        "paymentMethods": [
            {
                "name": "Cartão de crédito / débito",
                "providers": ["Stripe", "MercadoPago"],
                "currencies": ["BRL"],
            }
        ],
        "contactInfo": {
            "email": CONTACT_EMAIL,
            "phone": CONTACT_PHONE,
            "website": SITE_URL,
        },
    }
    return _json_response(service)


@frappe.whitelist(allow_guest=True)
def get_llm_sitemap():
    """
    GEO: sitemap otimizado para LLMs com as URLs REAIS do site.
    URL real: /api/method/vedium_core.geo_endpoints.get_llm_sitemap
    """
    today = datetime.now().strftime("%Y-%m-%d")

    urls = [
        {"loc": f"{SITE_URL}/", "lastmod": today, "changefreq": "weekly",
         "priority": "1.0", "description": "Homepage Vedium"},
        {"loc": f"{SITE_URL}/cursos-de-idiomas-online", "lastmod": today,
         "changefreq": "daily", "priority": "0.9",
         "description": "Catálogo de cursos de idiomas"},
        {"loc": f"{SITE_URL}/sobre", "lastmod": today,
         "changefreq": "monthly", "priority": "0.7",
         "description": "Sobre a Vedium"},
        {"loc": f"{SITE_URL}/imprensa", "lastmod": today,
         "changefreq": "monthly", "priority": "0.6",
         "description": "Informações institucionais e imprensa"},
        {"loc": f"{SITE_URL}/contato", "lastmod": today,
         "changefreq": "monthly", "priority": "0.6",
         "description": "Contato"},
        {"loc": f"{SITE_URL}/carreiras", "lastmod": today,
         "changefreq": "monthly", "priority": "0.5",
         "description": "Trabalhe conosco"},
    ]

    from vedium_core.course_urls import get_course_url

    for course in _published_courses(limit=20):
        urls.append({
            "loc": f"{SITE_URL}{get_course_url(course.name)}",
            "lastmod": course.modified.strftime("%Y-%m-%d"),
            "changefreq": "weekly",
            "priority": "0.8",
            "description": f"Curso: {course.title}",
        })

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += "  <url>\n"
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        if "description" in url:
            xml += f'    <!-- {url["description"]} -->\n'
        xml += "  </url>\n"
    xml += "</urlset>"

    frappe.response["http_status_code"] = 200
    frappe.response["type"] = "xml"
    frappe.response["message"] = xml
    frappe.response.headers["Content-Type"] = "application/xml"
    frappe.response.headers["Cache-Control"] = (
        "public, max-age=86400, stale-while-revalidate=604800"
    )
    return xml
