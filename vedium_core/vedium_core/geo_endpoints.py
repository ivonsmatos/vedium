import frappe
from frappe import _
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def get_ai_summary():
    """
    GEO Endpoint: /ai/summary.json
    Returns site summary for AI systems (≤800 chars)
    """
    frappe.response['http_status_code'] = 200
    frappe.response['type'] = 'json'
    
    summary = {
        "version": "1.0",
        "lastModified": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "name": "Vedium Global Education",
        "description": "Vedium is a specialized online language learning platform offering Executive English, Tech Hebrew, Ancestral Yoruba, and Portuguese courses. We combine AI-powered 24/7 conversation practice with expert native instructors to accelerate global career development. Our industry-specific tracks serve business professionals, tech workers, cultural enthusiasts, and international students. Features include real-time AI training, certificate programs, corporate solutions, and flexible payment options including cryptocurrency (Bitcoin, Ethereum, USDC).",
        "url": "https://vediums.com",
        "contact": {
            "email": "contato@vediums.com",
            "phone": "+55 (11) 94190-6079"
        },
        "languages": ["en", "pt", "he", "yo"],
        "primaryServices": [
            "Executive English courses",
            "Tech Hebrew for programmers",
            "Ancestral Yoruba cultural courses",
            "Portuguese for international students",
            "AI-powered conversation training",
            "Corporate language training"
        ],
        "paymentMethods": ["Credit Card", "Cryptocurrency", "Corporate Invoice"]
    }
    
    frappe.response['message'] = summary
    frappe.response.headers['Content-Type'] = 'application/json'
    frappe.response.headers['Cache-Control'] = 'public, max-age=86400, stale-while-revalidate=604800'
    
    return summary

@frappe.whitelist(allow_guest=True)
def get_ai_faq():
    """
    GEO Endpoint: /ai/faq.json
    Returns frequently asked questions
    """
    frappe.response['http_status_code'] = 200
    frappe.response['type'] = 'json'
    
    faq = {
        "version": "1.0",
        "lastModified": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "faqs": [
            {
                "question": "What languages does Vedium teach?",
                "answer": "Vedium offers courses in four strategic languages: Executive English for business, Tech Hebrew for programmers, Ancestral Yoruba for cultural connection, and Portuguese for international students."
            },
            {
                "question": "How does the AI conversation training work?",
                "answer": "Our platform provides 24/7 AI-powered conversation practice that simulates real-world scenarios specific to your industry. Practice anytime, get instant feedback, and build confidence before speaking with native instructors."
            },
            {
                "question": "Do you offer certificates?",
                "answer": "Yes, students who complete 100% of a course and achieve a minimum 70% score on assessments receive a certificate of completion."
            },
            {
                "question": "Can I pay with cryptocurrency?",
                "answer": "Yes! We accept Bitcoin (BTC), Ethereum (ETH), Litecoin (LTC), USD Coin (USDC), and DAI through Coinbase Commerce. We also accept traditional payment methods like credit cards."
            },
            {
                "question": "Is there a free trial?",
                "answer": "We offer free introductory lessons for each language track. You can explore the platform and experience our teaching methodology before committing to a paid course."
            },
            {
                "question": "Do you offer corporate training?",
                "answer": "Yes, Vedium Corporate provides customized language training solutions for businesses, including bulk licensing, progress tracking, and industry-specific content."
            },
            {
                "question": "Who are the instructors?",
                "answer": "All our instructors are native speakers with specialized expertise in their teaching areas - business English, tech industry Hebrew, cultural Yoruba, or Portuguese for foreigners."
            },
            {
                "question": "How long does it take to complete a course?",
                "answer": "Course duration varies by level and intensity. Most students complete a basic level in 2-3 months with consistent practice. Our flexible format allows you to learn at your own pace."
            }
        ]
    }
    
    frappe.response['message'] = faq
    frappe.response.headers['Content-Type'] = 'application/json'
    frappe.response.headers['Cache-Control'] = 'public, max-age=86400, stale-while-revalidate=604800'
    
    return faq

@frappe.whitelist(allow_guest=True)
def get_ai_service():
    """
    GEO Endpoint: /ai/service.json
    Returns service capabilities and API information
    """
    frappe.response['http_status_code'] = 200
    frappe.response['type'] = 'json'
    
    service = {
        "version": "1.0",
        "lastModified": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "name": "Vedium Global Education",
        "description": "Online language learning platform with AI-powered training",
        "capabilities": [
            {
                "name": "Course Catalog",
                "description": "Browse available language courses",
                "endpoint": "https://vediums.com/courses",
                "methods": ["GET"]
            },
            {
                "name": "Course Enrollment",
                "description": "Enroll in language courses via checkout",
                "endpoint": "https://vediums.com/api/method/vedium_core.api.create_checkout",
                "methods": ["POST"],
                "requiresAuth": True
            },
            {
                "name": "AI Conversation Practice",
                "description": "24/7 AI-powered conversation training",
                "endpoint": "https://vediums.com/practice",
                "methods": ["GET", "POST"],
                "requiresAuth": True
            },
            {
                "name": "Progress Tracking",
                "description": "Track learning progress and payment history",
                "endpoint": "https://vediums.com/api/method/vedium_core.api.get_payment_history",
                "methods": ["GET"],
                "requiresAuth": True
            },
            {
                "name": "Certificate Generation",
                "description": "Generate course completion certificates",
                "endpoint": "https://vediums.com/api/method/vedium_core.api.issue_certificate",
                "methods": ["POST"],
                "requiresAuth": True
            }
        ],
        "authentication": {
            "type": "JWT",
            "loginEndpoint": "https://vediums.com/api/method/login",
            "signupEndpoint": "https://vediums.com/api/method/frappe.core.doctype.user.user.sign_up"
        },
        "paymentMethods": [
            {
                "name": "Credit/Debit Card",
                "providers": ["Stripe", "MercadoPago"],
                "currencies": ["BRL", "USD", "EUR"]
            },
            {
                "name": "Cryptocurrency",
                "provider": "Coinbase Commerce",
                "currencies": ["BTC", "ETH", "LTC", "USDC", "DAI"]
            }
        ],
        "supportedLanguages": ["en", "pt", "he", "yo"],
        "contactInfo": {
            "email": "contato@vediums.com",
            "phone": "+55 (11) 94190-6079",
            "website": "https://vediums.com"
        }
    }
    
    frappe.response['message'] = service
    frappe.response.headers['Content-Type'] = 'application/json'
    frappe.response.headers['Cache-Control'] = 'public, max-age=86400, stale-while-revalidate=604800'
    
    return service

@frappe.whitelist(allow_guest=True)
def get_llm_sitemap():
    """
    GEO Endpoint: /sitemap-llm.xml
    Returns LLM-optimized sitemap
    """
    frappe.response['http_status_code'] = 200
    frappe.response['type'] = 'xml'
    
    # URLs estáticas importantes para LLMs
    urls = [
        {
            'loc': 'https://vediums.com/',
            'lastmod': '2026-02-08',
            'changefreq': 'weekly',
            'priority': '1.0',
            'description': 'Homepage - Vedium Global Education platform'
        },
        {
            'loc': 'https://vediums.com/courses',
            'lastmod': '2026-02-08',
            'changefreq': 'daily',
            'priority': '0.9',
            'description': 'Course catalog - Executive English, Tech Hebrew, Ancestral Yoruba, Portuguese'
        },
        {
            'loc': 'https://vediums.com/about',
            'lastmod': '2026-02-08',
            'changefreq': 'monthly',
            'priority': '0.7',
            'description': 'About Vedium - Mission, vision, and teaching methodology'
        },
        {
            'loc': 'https://vediums.com/pricing',
            'lastmod': '2026-02-08',
            'changefreq': 'weekly',
            'priority': '0.8',
            'description': 'Pricing plans - Individual and corporate options'
        },
        {
            'loc': 'https://vediums.com/.well-known/ai.txt',
            'lastmod': '2026-02-08',
            'changefreq': 'monthly',
            'priority': '0.6',
            'description': 'AI discovery file'
        },
        {
            'loc': 'https://vediums.com/ai/summary.json',
            'lastmod': '2026-02-08',
            'changefreq': 'weekly',
            'priority': '0.6',
            'description': 'AI-readable site summary'
        },
        {
            'loc': 'https://vediums.com/ai/faq.json',
            'lastmod': '2026-02-08',
            'changefreq': 'weekly',
            'priority': '0.6',
            'description': 'Frequently asked questions in AI-readable format'
        }
    ]
    
    # Buscar cursos publicados
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "title", "modified"],
        limit=20
    )
    
    for course in courses:
        urls.append({
            'loc': f'https://vediums.com/courses/{course.name}',
            'lastmod': course.modified.strftime('%Y-%m-%d'),
            'changefreq': 'weekly',
            'priority': '0.8',
            'description': f'Course: {course.title}'
        })
    
    # Gerar XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    xml += 'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    
    for url in urls:
        xml += '  <url>\n'
        xml += f'    <loc>{url["loc"]}</loc>\n'
        xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{url["priority"]}</priority>\n'
        if 'description' in url:
            xml += f'    <!-- {url["description"]} -->\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    frappe.response['message'] = xml
    frappe.response.headers['Content-Type'] = 'application/xml'
    frappe.response.headers['Cache-Control'] = 'public, max-age=86400, stale-while-revalidate=604800'
    
    return xml
