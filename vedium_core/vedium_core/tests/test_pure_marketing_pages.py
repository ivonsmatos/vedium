"""Testes puros para melhorias públicas de marketing.

Estes testes rodam sem Frappe/bench e protegem o pacote seguro de produção:
não validam banco, Stripe, LMS, professores, alunos ou assinaturas.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WWW = ROOT / "vedium_core" / "vedium_core" / "www"
TPL = ROOT / "vedium_core" / "vedium_core" / "templates" / "includes"
PUBLIC_JS = ROOT / "vedium_core" / "vedium_core" / "public" / "js"
PUBLIC_CSS = ROOT / "vedium_core" / "vedium_core" / "public" / "css"
GTM_IMPORT = ROOT / "docs" / "gtm" / "vedium-gtm-container-import.json"
REVIEWS_PROCESS = ROOT / "docs" / "reviews" / "VERIFIED_REVIEWS_PROCESS.md"
REVIEWS_TEMPLATE = ROOT / "docs" / "reviews" / "verified_reviews_template.csv"
CATALOG_AUDIT = ROOT / "vedium_core" / "vedium_core" / "catalog_audit.py"
CATALOG_AUDIT_WORKFLOW = ROOT / ".github" / "workflows" / "catalog-audit.yml"
PUBLIC_FUNNEL = ROOT / "vedium_core" / "vedium_core" / "public_funnel.py"
PUBLIC_E2E_WORKFLOW = ROOT / ".github" / "workflows" / "e2e-public.yml"
API = ROOT / "vedium_core" / "vedium_core" / "api.py"

sys.path.insert(0, str(ROOT / "vedium_core"))
from vedium_core.marketing_landing_content import LANDINGS  # noqa: E402

SEO_SLUGS = [
    "curso-de-ingles-online",
    "ingles-para-entrevista",
    "ingles-para-programadores",
    "ingles-executivo",
    "ingles-para-viagens",
    "ingles-para-atendimento-ao-cliente",
    "curso-de-ioruba-online",
    "ioruba-para-iniciantes",
    "ioruba-cultura-e-ancestralidade",
    "portugues-para-estrangeiros",
    "portugues-para-executivos",
    "preparatorio-celpe-bras",
]

COMMERCIAL_SLUGS = [
    "como-funciona",
    "aula-diagnostica",
    "planos",
    "matricula",
    "faq",
]

PUBLIC_INTENT_SLUGS = [
    "certificado",
    "comunidade",
    "programa-de-indicacao",
    "empresas",
]

PLATFORM_SLUGS = [
    "meu-progresso",
    "pratica-diaria",
]


def read_public_text():
    files = list(WWW.glob("*.html")) + list(TPL.glob("*.html")) + [WWW / "llms.txt"]
    return "\n".join(p.read_text(encoding="utf-8") for p in files if p.exists())


def test_seo_objective_pages_exist_and_link_to_existing_funnel():
    template = (TPL / "marketing_landing.html").read_text(encoding="utf-8")
    assert "O que você vai aprender" in template
    assert "Perguntas frequentes" in template
    assert "seo_landing_whatsapp_click" in template
    assert "landing_test_url" in template
    assert "/teste-de-nivel-ingles" in template
    assert 'href="{{ landing_test_url }}" class="thm-btn"' in template
    assert "seo_landing_test_click" not in template
    # Infra SEO/GEO: FAQPage schema, offers no Course, prosa longa e preço
    assert '"@type": "FAQPage"' in template
    assert '"offers"' in template
    assert "landing.seo_sections" in template
    assert "landing.price_display" in template
    # scripts com defer (performance no mobile)
    assert "<script defer src=" in template
    assert template.count("<script src=") == 0


def test_english_pillar_page_is_rich_for_seo():
    landing = LANDINGS["curso-de-ingles-online"]
    # prosa longa de verdade (SEO/GEO exige corpo de texto substancial)
    prose = " ".join(
        block
        for sec in landing["seo_sections"]
        for block in sec["body"]
    )
    word_count = len(re.sub(r"<[^>]+>", " ", prose).split())
    assert word_count >= 700, f"prosa muito curta: {word_count} palavras"
    assert len(landing["seo_sections"]) >= 4
    assert landing["price_from"] == "240"
    assert "240" in landing["price_display"]
    # links internos para o cluster de inglês (link building interno)
    assert "/ingles-para-entrevista" in prose
    assert "/teste-de-nivel-ingles" in prose

    for slug in SEO_SLUGS:
        html_path = WWW / f"{slug}.html"
        # Controller www: Frappe converte hífen→underscore no nome do módulo
        # Python (template_page.set_pymodule) — o .py DEVE usar underscore.
        py_path = WWW / f"{slug.replace('-', '_')}.py"
        assert html_path.exists()
        assert py_path.exists()
        html = html_path.read_text(encoding="utf-8")
        py = py_path.read_text(encoding="utf-8")
        landing = LANDINGS[slug]
        assert f'get_marketing_landing("{slug}")' in html
        assert 'marketing_landing.html' in html
        assert slug in py
        assert len(landing["lead"]) > 120
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4


def test_commercial_pages_exist_and_drive_to_public_ctas():
    for slug in COMMERCIAL_SLUGS:
        html_path = WWW / f"{slug}.html"
        # Controller www: Frappe converte hífen→underscore no nome do módulo
        # Python (template_page.set_pymodule) — o .py DEVE usar underscore.
        py_path = WWW / f"{slug.replace('-', '_')}.py"
        assert html_path.exists()
        assert py_path.exists()
        html = html_path.read_text(encoding="utf-8")
        assert f"https://vediums.com/{slug}" in html
        assert "/teste-de-nivel" in html
        assert "wa.me/5511911293075" in html
        assert "public_cta_click" in html


def test_diagnostic_scheduling_is_public_and_checkout_safe():
    html = (WWW / "aula-diagnostica.html").read_text(encoding="utf-8")
    assert "Pré-agendamento" in html
    assert "diagnostic_schedule_click" in html
    assert "diagnostic_slot_click" in html
    assert "get_available_diagnostic_slots" in html
    assert 'data-vd-diagnostic="english"' in html
    assert 'data-vd-diagnostic="portuguese_foreigners"' in html
    assert 'data-vd-diagnostic="yoruba"' in html
    assert html.count("https://wa.me/5511911293075") >= 4
    assert "não cria reserva automática, matrícula, cobrança ou alteração de plano" in html
    assert "vedium_core.public_funnel.get_available_diagnostic_slots" in html
    assert "stripe" not in html.lower()


def test_public_plan_selection_tracks_funnel_without_checkout_mutation():
    html = (WWW / "planos.html").read_text(encoding="utf-8")
    assert "plan_select_click" in html
    assert "plan_platform_click" in html
    assert "Escolher plano leve" in html
    assert "Escolher plano recomendado" in html
    assert "Escolher plano intensivo" in html
    assert "/matricula" in html
    assert html.count("https://wa.me/5511911293075") >= 4
    assert "/api/method" not in html


def test_public_enrollment_intent_page_keeps_checkout_on_platform():
    html = (WWW / "matricula.html").read_text(encoding="utf-8")
    py = (WWW / "matricula.py").read_text(encoding="utf-8")
    assert "https://vediums.com/matricula" in html
    assert "Continuar na plataforma" in html
    assert "https://app.vediums.com/lms/courses/" in html
    assert "source=public_funnel" in html
    assert "enrollment_intent_click" in html
    assert "enrollment_whatsapp_click" in html
    assert "Stripe preservado" in html
    assert "get_context" in py
    assert "/api/method" not in html


def test_certificate_verification_page_and_public_funnel_endpoints_are_safe():
    html = (WWW / "certificado.html").read_text(encoding="utf-8")
    py = (WWW / "certificado.py").read_text(encoding="utf-8")
    funnel = PUBLIC_FUNNEL.read_text(encoding="utf-8")
    assert "https://vediums.com/certificado" in html
    assert "verify_certificate" in html
    assert "vedium_core.public_funnel.verify_certificate" in html
    assert "Verificar certificado" in html
    assert "quickchart.io/qr" in html
    assert "QR Code verificável" in html
    assert "URLSearchParams(location.search)" in html
    assert "?code=" in html
    assert "vendors/fontawesome/css/all.min.css" in html
    assert "vendors/icomoon-icons/style.css" in html
    assert "vedium-responsive.css" in html
    assert 'img[src*="logo-color-reta"]' in html
    assert '.footer-one img[src*="logo-branca-reta"]' in html
    assert "vedium.js" in html
    assert "get_context" in py
    assert "submit_public_intent" in funnel
    assert "request_diagnostic_class" in funnel
    assert "get_available_diagnostic_slots" in funnel
    assert "verify_certificate" in funnel
    for intent in ["lead", "diagnostic", "community", "referral", "b2b", "review"]:
        assert f'"{intent}"' in funnel
    assert '"doctype": "Support Ticket"' in funnel
    assert "frappe.sendmail" in funnel
    assert "Recebemos seu contato | Vedium" in funnel
    assert "Public funnel lead confirmation failed" in funnel
    assert '"opened_by"' in funnel
    assert "LMS Certificate" in funnel
    assert "Lesson Slot" in funnel
    assert "create_checkout" not in funnel
    assert "Stripe" not in funnel
    assert "LMS Enrollment" not in funnel
    api = API.read_text(encoding="utf-8")
    assert 'verify_url": f"/certificado?code={code}"' in api


def test_public_interest_pages_create_support_tickets_without_checkout_touch():
    template = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "vedium_core.public_funnel.submit_public_intent" in template
    assert "public_intent_submit" in template
    assert "public_cta_click" in template
    assert "vendors/fontawesome/css/all.min.css" in template
    assert "vendors/icomoon-icons/style.css" in template
    assert "vedium-responsive.css" in template
    assert 'img[src*="logo-color-reta"]' in template
    assert '.footer-one img[src*="logo-branca-reta"]' in template
    assert "vedium.js" in template
    assert "wa.me/5511911293075" in template
    assert "/teste-de-nivel" in template
    assert 'https://vediums.com/{{ page_slug }}' in template
    assert "Enviando..." in template
    assert "create_checkout" not in template
    assert "stripe" not in template.lower()

    expectations = {
        "comunidade": "community",
        "empresas": "b2b",
    }
    for slug, intent in expectations.items():
        html = (WWW / f"{slug}.html").read_text(encoding="utf-8")
        py = (WWW / f"{slug}.py").read_text(encoding="utf-8")
        assert f'page_slug = "{slug}"' in html
        assert f'page_intent = "{intent}"' in html
        assert 'public_intent_page.html' in html
        assert "get_context" in py


def test_referral_program_links_to_authenticated_dashboard():
    html = (WWW / "programa-de-indicacao.html").read_text(encoding="utf-8")
    py = (WWW / "programa_de_indicacao.py").read_text(encoding="utf-8")
    assert "https://vediums.com/programa-de-indicacao" in html
    assert "Dentro da plataforma" in html
    # Programa agora é funcional: CTA leva ao painel autenticado, não a um
    # login genérico — a página pública em si não gera cupom/coleta dados,
    # isso acontece em minhas-indicacoes.py (sessão logada obrigatória).
    assert "https://app.vediums.com/minhas-indicacoes" in html
    assert "referral_platform_click" in html
    assert "Gerar link de indicação" not in html
    assert "Registrar indicação" not in html
    assert "utm_source=referral" not in html
    assert "referral_link_copy" not in html
    assert "referral_register_submit" not in html
    assert "vedium_core.public_funnel.submit_public_intent" not in html


def test_referral_dashboard_requires_login_and_uses_referrals_module():
    py = (WWW / "minhas_indicacoes.py").read_text(encoding="utf-8")
    html = (WWW / "minhas-indicacoes.html").read_text(encoding="utf-8")
    assert 'frappe.session.user == "Guest"' in py
    assert "app.vediums.com/login?redirect-to=/minhas-indicacoes" in py
    assert "from vedium_core.referrals import get_my_referral, get_my_referral_conversions" in py
    assert 'noindex, nofollow' in html
    assert "referral.referral_code" in html
    assert "referral.whatsapp_link" in html
    assert "create_checkout" not in html
    assert "stripe" not in html.lower()


def test_daily_practice_tool_and_student_progress_dashboard_are_safe():
    practice = (WWW / "pratica-diaria.html").read_text(encoding="utf-8")
    practice_py = (WWW / "pratica_diaria.py").read_text(encoding="utf-8")
    progress_html = (WWW / "meu-progresso.html").read_text(encoding="utf-8")
    progress_py = (WWW / "meu_progresso.py").read_text(encoding="utf-8")
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(
        encoding="utf-8"
    )

    assert "SpeechSynthesisUtterance" in practice
    assert "SpeechRecognition" in practice
    assert "daily_practice_listen" in practice
    assert "daily_practice_speak" in practice
    assert "similarity" in practice
    assert "yo-NG" in practice
    assert 'location.replace("https://app.vediums.com/pratica-diaria"' in practice
    assert 'location.replace("https://app.vediums.com/meu-progresso"' in progress_html
    assert "noindex, nofollow" in practice
    assert "https://app.vediums.com/meu-progresso" in practice
    assert "https://app.vediums.com/pratica-diaria" in progress_html
    assert 'APP_URL = "https://app.vediums.com"' in practice_py
    assert 'APP_URL = "https://app.vediums.com"' in progress_py
    assert '_redirect_public_host("/pratica-diaria")' in practice_py
    assert '_redirect_public_host("/meu-progresso")' in progress_py
    assert "PUBLIC_HOSTS" in practice_py
    assert "PUBLIC_HOSTS" in progress_py
    assert "_redirect_public_host" in practice_py
    assert "_redirect_public_host" in progress_py
    assert "/api/method" not in practice
    assert "stripe" not in practice.lower()

    assert "Meu progresso Vedium" in progress_html
    assert "noindex, nofollow" in progress_html
    assert "Streak" in progress_html
    assert "CEFR" in progress_html
    assert "LMS Enrollment" in progress_py
    assert "LMS Flashcard" in progress_py
    assert "LMS Badge Log" in progress_py
    # Lesson Slot é doctype legado (0 registros para sempre em produção) —
    # a leitura morta foi removida 2026-07-01; só resta o comentário
    # explicando a remoção, não uma query real.
    assert 'frappe.get_all(\n        "Lesson Slot"' not in progress_py
    assert "context.slots" not in progress_py
    assert "Aulas e tarefas" not in progress_html
    assert "redirect-to=/meu-progresso" in progress_py
    assert '"meu-progresso"' in hooks
    assert "create_checkout" not in progress_py
    assert "stripe" not in progress_py.lower()


def test_verified_reviews_process_exists_without_fake_public_reviews():
    process = REVIEWS_PROCESS.read_text(encoding="utf-8")
    template = REVIEWS_TEMPLATE.read_text(encoding="utf-8")
    assert "Só publicar depoimento quando houver autorização explícita" in process
    assert "Depoimento de template" in process
    assert "Review ligado a professor individual" in process
    assert "public_name,course_or_goal,collection_date" in template
    assert "approved_quote" in template
    assert "authorization_evidence" in template


def test_production_catalog_audit_is_read_only_and_checks_b1_b2():
    audit = CATALOG_AUDIT.read_text(encoding="utf-8")
    workflow = CATALOG_AUDIT_WORKFLOW.read_text(encoding="utf-8")
    assert "def audit_course_levels" in audit
    assert "frappe.get_all" in audit
    assert "filters={\"published\": 1}" in audit
    assert "Upper Intermediario appears with B1" in audit
    assert "Intermediario appears with B2" in audit
    assert ".save(" not in audit
    assert ".insert(" not in audit
    assert "frappe.db.set_value" not in audit
    assert "workflow_dispatch" in workflow
    assert "bench --site" in workflow
    assert "vedium_core.catalog_audit.audit_course_levels" in workflow


def test_level_test_ctas_use_native_navigation_only():
    files = [
        WWW / "index.html",
        TPL / "site_navbar.html",
        TPL / "marketing_landing.html",
        WWW / "como-funciona.html",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    assert re.search(r'href="(?:\{\{ landing_test_url \}\}|/teste-de-nivel(?:-ingles)?)"', combined)
    assert not re.search(
        r'href="(?:\{\{ landing_test_url \}\}|/teste-de-nivel(?:-ingles)?)"[^>]*\sonclick=',
        combined,
    )
    assert "seo_landing_test_click" not in combined
    assert "cta:'level_test'" not in combined


def test_public_level_test_exists_without_backend_dependency():
    html_path = WWW / "teste-de-nivel.html"
    english_html_path = WWW / "teste-de-nivel-ingles.html"
    py_path = WWW / "teste_de_nivel.py"
    english_py_path = WWW / "teste_de_nivel_ingles.py"
    assert html_path.exists()
    assert english_html_path.exists()
    assert py_path.exists()
    assert english_py_path.exists()
    html = html_path.read_text(encoding="utf-8")
    english_html = english_html_path.read_text(encoding="utf-8")
    assert "https://vediums.com/teste-de-nivel" in html
    assert "Teste de Nível de Português para Estrangeiros" in html
    assert "portuguese-level-test" in html
    assert html.count("data-correct=") == 15
    assert "/teste-de-nivel-ingles" in html
    assert "Gramática e vocabulário" in html
    assert "Compreensão de leitura" in html
    assert "Compreensão auditiva" in html
    assert "Produção escrita" in html
    assert "Produção oral" in html
    assert "Atenção passageiros" in html
    assert "médico de resgate" in html
    assert "SpeechSynthesisUtterance" in html
    assert "level_test_completed" in html
    assert "level_test_plan_click" in html
    assert "level_test_catalog_click" in html
    assert "/aula-diagnostica" in html
    assert "/planos" in html
    assert "portuguese_foreigners" in html
    assert "Diagnóstico:" in html
    assert "Recomendação:" in html
    assert "recommendation" in html
    assert "wa.me/5511911293075" in html
    assert "A1" in html and "C1" in html
    assert "/api/method" not in html
    assert "stripe" not in html.lower()
    assert "https://vediums.com/teste-de-nivel-ingles" in english_html
    assert "Teste de Nível de Inglês" in english_html
    assert "english-level-test" in english_html
    assert english_html.count("data-correct=") == 15
    assert "/teste-de-nivel" in english_html
    assert "Grammar and vocabulary" in english_html
    assert "Reading comprehension" in english_html
    assert "Listening comprehension" in english_html
    assert "Writing" in english_html
    assert "Speaking" in english_html
    assert "Flight 204 to London" in english_html
    assert "project was successful" in english_html
    assert "SpeechSynthesisUtterance" in english_html
    assert "level_test_completed" in english_html
    assert "level_test_plan_click" in english_html
    assert "level_test_catalog_click" in english_html
    assert "/aula-diagnostica" in english_html
    assert "/planos" in english_html
    assert "english_learners" in english_html
    assert "Diagnóstico:" in english_html
    assert "Recomendação:" in english_html
    assert "wa.me/5511911293075" in english_html
    assert "A1" in english_html and "C1" in english_html
    assert "/api/method" not in english_html
    assert "stripe" not in english_html.lower()


def test_public_pages_do_not_reintroduce_template_residue():
    text = read_public_text()
    forbidden = [
        "Lorem ipsum",
        "Amazing Courses",
        "Kevin Martin",
        "666 888 0000",
        "[email protected]",
        "testimonials-one",
        "Prova Social",
        "Prova social",
        "Ana Oliveira",
        "Dra. Juliana Costa",
        "pravatar.cc",
        "Company-Logos",
        "Who Will You Learn With?",
        'href="/mentores"',
        'href="/professores"',
        'href="/professor-busayo-frank-alonge"',
    ]
    for item in forbidden:
        assert item not in text
    assert not (WWW / "mentores.html").exists()
    assert not (WWW / "professores.html").exists()
    assert not (WWW / "professores.py").exists()
    assert not (WWW / "professor-busayo-frank-alonge.html").exists()
    assert not (WWW / "professor-busayo-frank-alonge.py").exists()


def test_company_legal_data_is_visible_without_touching_checkout():
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    terms = (WWW / "termos.html").read_text(encoding="utf-8")
    privacy = (WWW / "privacidade.html").read_text(encoding="utf-8")
    for text in [footer, terms, privacy]:
        assert "VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA" in text
        assert "58.434.869/0001-24" in text
    assert "Stripe" in terms
    assert "Stripe" in privacy
    assert "Direito de arrependimento" in terms
    assert "7 (sete) dias corridos" in terms
    assert "não altera o checkout" in terms


def test_rich_footer_matches_public_site_structure():
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    assert "vd-rich-footer" in footer
    assert "--vd-footer-bg: #164f86" in footer
    assert "vd-rich-footer__language" not in footer
    assert ".vd-rich-footer .swiper-pagination" in footer
    assert ".vd-rich-footer .owl-dots" in footer
    assert "display: none !important" in footer
    assert "Cursos de Idiomas" in footer
    assert "Objetivos" in footer
    assert "Vedium online para você" in footer
    assert "Conteúdos gratuitos" in footer
    assert "Conteúdos e oportunidades" in footer
    assert "FAQ & Suporte" in footer
    assert "/ingles-para-entrevista" in footer
    assert "/portugues-para-estrangeiros" in footer
    assert "/curso-de-ioruba-online" in footer
    assert "/blog/niveis-de-ingles-a1-c1" in footer
    assert "/teste-de-nivel-ingles" in footer
    assert "https://www.instagram.com/vediumsglobal/" in footer
    assert "https://www.linkedin.com/company/vediums" in footer
    assert "wa.me/5511911293075" in footer
    assert "VEDIUM GLOBAL EDUCACAO E TECNOLOGIA LTDA" in footer
    assert "58.434.869/0001-24" in footer
    assert "/mentores" not in footer
    assert "/professores" not in footer
    assert "/professor-busayo-frank-alonge" not in footer


def test_llms_txt_has_current_course_level_and_objective_pages():
    llms = (WWW / "llms.txt").read_text(encoding="utf-8")
    assert "Upper Intermediário (B2)" in llms
    assert "Upper Intermediário (B1)" not in llms
    for slug in SEO_SLUGS + COMMERCIAL_SLUGS + PUBLIC_INTENT_SLUGS:
        assert f"https://vediums.com/{slug}" in llms
    for slug in PLATFORM_SLUGS:
        assert f"https://vediums.com/{slug}" not in llms
    assert "https://vediums.com/mentores" not in llms


def test_app_domain_redirect_and_catalog_level_guards_are_in_place():
    index_html = (WWW / "index.html").read_text(encoding="utf-8")
    index_py = (WWW / "index.py").read_text(encoding="utf-8")
    catalogo_py = (WWW / "catalogo.py").read_text(encoding="utf-8")
    curso_py = (WWW / "curso.py").read_text(encoding="utf-8")
    static_index = (ROOT / "deploy" / "site" / "index.html").read_text(encoding="utf-8")
    nginx_primary = (ROOT / "deploy" / "nginx" / "vediums.com.conf").read_text(encoding="utf-8")
    nginx_legacy = (ROOT / "deploy" / "vediums.com.nginx").read_text(encoding="utf-8")
    assert "app.vediums.com" in index_py
    assert 'redirect_location = "/login"' in index_py
    assert "raise frappe.Redirect" in index_py
    for html in [index_html, static_index]:
        assert "app.vediums.com" in html
        assert "window.location.replace('/login')" in html
    assert ".main-slider .swiper-slide { display: flex !important; align-items: center !important; pointer-events: none; }" in index_html
    assert ".main-slider .swiper-slide-active { pointer-events: auto; }" in index_html
    assert "testimonials-pagination" not in index_html
    assert "pagination: { el: '.testimonials-pagination'" not in index_html
    assert "blog-one__single-content-overlay-mata-info" not in index_html
    assert "2 de junho de 2026" not in index_html
    for nginx in [nginx_primary, nginx_legacy]:
        assert "location = /" in nginx
        assert "return 302 /login;" in nginx
    assert catalogo_py.index('"Upper Intermediário": "B2"') < catalogo_py.index('"Intermediário": "B1"')
    assert index_py.index('"Upper Intermediário": "B2"') < index_py.index('"Intermediário": "B1"')
    assert "_dedupe_chapters" in curso_py
    assert "_dedupe_lessons" in curso_py
    assert "chapter.lessons = _dedupe_lessons" in curso_py


def test_dynamic_sitemap_lists_public_marketing_pages():
    sitemap_page = (WWW / "sitemap.xml").read_text(encoding="utf-8")
    sitemap_context = (WWW / "sitemap.py").read_text(encoding="utf-8")
    # public/robots.txt removido (duplicata) — o canônico é www/robots.txt
    robots_page = (WWW / "robots.txt").read_text(encoding="utf-8")
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(
        encoding="utf-8"
    )
    for slug in (
        SEO_SLUGS
        + COMMERCIAL_SLUGS
        + PUBLIC_INTENT_SLUGS
        + ["teste-de-nivel", "teste-de-nivel-ingles"]
    ):
        # seo_utils.generate_sitemap() foi removido (órfão); checar www/sitemap.py
        assert f'"loc": "/{slug}"' in sitemap_context
        assert f'"{slug}"' in hooks
    assert '"meu-progresso"' in hooks
    assert '"pratica-diaria"' in hooks
    assert '"loc": "/meu-progresso"' not in sitemap_context
    assert '"loc": "/pratica-diaria"' not in sitemap_context
    for prefix in ["pt-br", "en-us", "es-ar", "de", "zh-cn"]:
        # LANGUAGE_ROUTE_PREFIXES vive somente em hooks.py e em vedium-language.js
        assert f'"{prefix}"' in hooks
    assert "urlset" in sitemap_page
    assert "links" in sitemap_page
    assert "Sitemap: https://vediums.com/sitemap.xml" in robots_page
    assert "sitemap-courses.xml" not in robots_page
    assert "sitemap-llm.xml" not in robots_page
    assert "User-agent: *" in robots_page
    assert '{"from_route": "/sw.js", "to_route": "sw"}' in hooks
    e2e = PUBLIC_E2E_WORKFLOW.read_text(encoding="utf-8")
    assert "python -m playwright install --with-deps chromium" in e2e
    assert "VEDIUM_RUN_PUBLIC_E2E" in e2e
    assert "test_pure_public_e2e_playwright.py" in e2e


def test_public_language_selector_and_gtm_import_are_available():
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    lang_js = (PUBLIC_JS / "vedium-language.js").read_text(encoding="utf-8")
    pwa_js = (PUBLIC_JS / "pwa-register.js").read_text(encoding="utf-8")
    sw_js = (PUBLIC_JS / "sw.js").read_text(encoding="utf-8")
    # www/sw.js removido (duplicata) — sw.py serve public/js/sw.js diretamente
    sw_py = (WWW / "sw.py").read_text(encoding="utf-8")
    cookie_js = (PUBLIC_JS / "cookie-consent.js").read_text(encoding="utf-8")
    theme_css = (PUBLIC_CSS / "luxo_theme.css").read_text(encoding="utf-8")
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(
        encoding="utf-8"
    )
    manifest = json.loads(
        (ROOT / "vedium_core" / "vedium_core" / "public" / "vedium_assets" / "images" / "favicons" / "site.webmanifest").read_text(
            encoding="utf-8"
        )
    )
    static_index = (ROOT / "deploy" / "site" / "index.html").read_text(encoding="utf-8")
    static_sw = (ROOT / "deploy" / "site" / "sw.js").read_text(encoding="utf-8")
    static_manifest_raw = (ROOT / "deploy" / "site" / "manifest.json").read_text(
        encoding="utf-8"
    )
    for locale in ["pt-br", "en-us", "es-ar", "fr", "de", "ru", "zh-cn"]:
        assert f'data-vd-locale="{locale}"' in navbar
    for href in ["/pt-br/", "/en-us/", "/es-ar/", "/de/", "/zh-cn/"]:
        assert f'href="{href}"' in navbar
    assert "data-vd-language-open" in navbar
    assert "Select your region and language" in navbar
    assert "BRASIL | PORTUGUÊS" in navbar
    assert "vedium-language-chips" not in navbar
    assert ".vedium-language-chips" in theme_css
    assert "display: none !important" in theme_css
    assert "flagcdn.com/w20/br.png" in navbar
    assert "flagcdn.com/w20/us.png" in navbar
    assert "flagcdn.com/w20/cn.png" in navbar
    assert "GTM-P6Q2FXLK" in footer
    assert "vedium-language.js?v=editorial-v6-skipgrids" in footer
    assert "pwa-register.js?v=static-v4" in footer
    assert "/assets/vedium_core/js/pwa-register.js?v=static-v4" in hooks
    assert "/assets/vedium_core/js/cookie-consent.js?v=mobile-pwa-fix" in hooks
    assert "vediumGoToLevelTest" not in footer
    assert "document.addEventListener('touchend'" not in footer
    assert "window.location.href = link.href" not in footer
    assert "wa.me/5511911293075" in footer
    # Botão flutuante removido a pedido do usuário (2026-06-30) — travava o
    # site no mobile ao tentar abrir o app do WhatsApp.
    assert "vedium-whatsapp-float" not in footer
    assert "data-vd-location=\"floating_whatsapp\"" not in footer
    assert "navigator.language" not in lang_js
    assert "language_selected" in lang_js
    assert "vedium_preferred_locale" not in lang_js
    assert "window.location.assign" not in lang_js
    assert 'var current = getLocaleFromPath() || "pt-br";' in lang_js
    assert "localeCopy" in lang_js
    assert "editorialCopy" in lang_js
    assert "Verify certificate" in lang_js
    assert "Verificar certificado" in lang_js
    assert "Vérifier le certificat" in lang_js
    assert "Zertifikat prüfen" in lang_js
    assert "Проверить сертификат" in lang_js
    assert "验证证书" in lang_js
    assert "English for job interviews with real speaking practice" in lang_js
    assert "Inglés para entrevistas laborales con práctica real de conversación" in lang_js
    assert "Anglais pour entretien d'embauche avec vraie pratique orale" in lang_js
    assert "面试英语，真实口语训练" in lang_js
    assert "translateTextNodes" in lang_js
    assert "updateLocaleLinks" in lang_js
    assert "Take the free placement test" in lang_js
    assert "Kostenlosen Einstufungstest machen" in lang_js
    assert "Diagnostic class" in lang_js
    assert "Clase diagnóstica" in lang_js
    assert "Diagnosestunde" in lang_js
    assert "诊断课" in lang_js
    assert "Choose recommended plan" in lang_js
    assert "Continue on the platform" in lang_js
    assert "Configura tu intención de matrícula" in lang_js
    assert "Zur Anmeldung" in lang_js
    assert 'prefix: "/pt-br/"' in lang_js
    assert 'prefix: "/es-ar/"' in lang_js
    assert 'prefix: "/de/"' in lang_js
    assert "setModalOpen" in lang_js
    assert "flagcdn.com/w20/br.png" in lang_js
    assert "switchLanguage(detected" not in lang_js
    assert "switchLanguage(" not in lang_js
    assert "translate.google.com" not in lang_js
    assert "loadGoogleTranslate" not in lang_js
    assert "vediumInitGoogleTranslate" not in lang_js
    assert "google_translate_element" not in navbar
    assert "googtrans=" not in lang_js
    assert "target.closest" in lang_js
    assert "navigator.serviceWorker.register('/sw.js'" in pwa_js
    assert "fetch('/sw.js', { method: 'HEAD', cache: 'no-store' })" in pwa_js
    assert "PUBLIC_HOSTS" in pwa_js
    assert "app.vediums.com" not in pwa_js
    assert "request.mode === 'navigate'" in sw_js
    assert "request.mode === 'navigate'" in static_sw
    assert "application/javascript; charset=utf-8" in sw_py
    assert 'frappe.response["type"] = "binary"' in sw_py
    assert "'/api/'" in sw_js
    assert "'/lms'" in sw_js
    assert "'/checkout'" in sw_js
    assert "caches.match('/index.html')" not in sw_js
    assert "caches.match('/index.html')" not in static_sw
    assert "serviceWorker.register('/sw.js')" not in static_index
    assert "@media(max-width:767px)" in cookie_js
    assert "top:12px" in cookie_js
    assert "bottom:auto" in cookie_js
    assert manifest["name"] == "Vedium"
    assert manifest["short_name"] == "Vedium"
    assert manifest["start_url"] == "/"
    assert manifest["icons"][0]["src"].startswith("/assets/vedium_core/")

    # /manifest.json na raiz — mesmo padrão do /sw.js (achado do QA 2026-07-01:
    # nginx tinha alias fixo para pasta inexistente /opt/vedium/pwa/, 404
    # sempre). Servido via Frappe contornando o problema dentro do repo; ver
    # docs/plataforma/pendente-pwa-marketing-404.md para a parte que ainda
    # depende de mexer no nginx (fora do repo).
    manifest_py = (WWW / "manifest.py").read_text(encoding="utf-8")
    assert '{"from_route": "/manifest.json", "to_route": "manifest"}' in hooks
    assert "application/manifest+json; charset=utf-8" in manifest_py
    assert 'frappe.response["type"] = "binary"' in manifest_py
    root_manifest = json.loads(
        (ROOT / "vedium_core" / "vedium_core" / "public" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    assert root_manifest["theme_color"] == "#2E6DA4"
    static_manifest = json.loads(static_manifest_raw)
    assert static_manifest["theme_color"] == "#2E6DA4"
    assert "Inteligência Cultural" not in static_manifest_raw

    gtm = json.loads(GTM_IMPORT.read_text(encoding="utf-8"))
    raw_gtm = GTM_IMPORT.read_text(encoding="utf-8")
    assert '"type": "template"' not in raw_gtm
    assert '"type": "boolean"' not in raw_gtm
    assert '"type": "integer"' not in raw_gtm
    assert '"tagFiringOption": "ONCE_PER_PAGE"' not in raw_gtm
    assert '"tagFiringOption": "oncePerLoad"' not in raw_gtm
    assert '"tagFiringOption": "ONCE_PER_EVENT"' in raw_gtm
    names = {tag["name"] for tag in gtm["containerVersion"]["tag"]}
    triggers = {trigger["name"] for trigger in gtm["containerVersion"]["trigger"]}
    assert "GA4 - Base Config" in names
    assert "GA4 - Event - Public CTA Click" in names
    assert "GA4 - Event - Level Test Completed" in names
    assert "GA4 - Event - Level Test Plan Click" in names
    assert "GA4 - Event - Level Test Catalog Click" in names
    assert "GA4 - Event - Diagnostic Schedule Click" in names
    assert "GA4 - Event - Plan Select Click" in names
    assert "GA4 - Event - Plan Platform Click" in names
    assert "GA4 - Event - Enrollment Intent Click" in names
    assert "GA4 - Event - Course Enrollment Intent Click" in names
    assert "CE - public_cta_click" in triggers
    assert "CE - language_selected" in triggers
    assert "CE - level_test_plan_click" in triggers
    assert "CE - level_test_catalog_click" in triggers
    assert "CE - diagnostic_schedule_click" in triggers
    assert "CE - plan_select_click" in triggers
    assert "CE - plan_platform_click" in triggers
    assert "CE - enrollment_intent_click" in triggers
    assert "CE - course_enrollment_intent_click" in triggers


def test_blog_has_self_service_panel_and_dynamic_route():
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    blog_content = (ROOT / "vedium_core" / "vedium_core" / "blog_content.py").read_text(encoding="utf-8")
    blog_post_py = (WWW / "blog_post.py").read_text(encoding="utf-8")
    blog_post_html = (WWW / "blog_post.html").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    # Menu: link para o blog
    assert '<a href="/blog">Blog</a>' in navbar

    # Rota dinâmica /blog/<slug> — substitui os arquivos www/blog/<slug>.html
    # individuais (removidos: route rules do Frappe têm prioridade sobre
    # arquivos estáticos, então mantê-los seria código morto e confuso).
    assert '{"from_route": "/blog/<slug>", "to_route": "blog_post"}' in hooks
    assert not (WWW / "blog").exists()

    # Doctype self-service: qualquer um com acesso ao Desk publica sem
    # depender de código/deploy.
    doctype_json = (
        ROOT / "vedium_core" / "vedium_core" / "vedium_core" / "doctype"
        / "vedium_blog_post" / "vedium_blog_post.json"
    )
    assert doctype_json.exists()
    doctype = json.loads(doctype_json.read_text(encoding="utf-8"))
    assert doctype["autoname"] == "field:slug"
    field_names = {f["fieldname"] for f in doctype["fields"]}
    assert {"title", "slug", "published", "content", "meta_description"} <= field_names
    roles = {p["role"] for p in doctype["permissions"]}
    assert "System Manager" in roles
    assert "All" not in roles  # publicação é só via Desk, não REST pública

    # blog_post.py procura primeiro no painel (banco), depois no código
    assert "get_blog_post_any" in blog_post_py
    assert "get_blog_post_from_db" in blog_content
    assert "def list_db_blog_posts" in blog_content
    assert '{% include "templates/includes/blog_post.html" %}' in blog_post_html

    # Sitemap lista os posts dinamicamente (inclui os publicados pelo painel)
    assert "_blog_urls" in sitemap_py
    assert "list_blog_posts" in sitemap_py


def test_lesson_slot_doctype_is_not_world_writable():
    """O agendamento aluno<->professor usa o fluxo NATIVO do Frappe LMS
    (Course Evaluator + Google Meet / LMS Live Class), não páginas custom.
    O doctype legado Lesson Slot só alimenta a exibição de aulas em
    meu-progresso/aula-diagnóstica, mas seguia com a role "All" tendo
    CRUD total via REST API padrão — expondo horários e dados pessoais.
    Esta trava de permissão é mantida como correção de segurança."""
    slot_json = json.loads(
        (
            ROOT / "vedium_core" / "vedium_core" / "vedium_core" / "doctype"
            / "lesson_slot" / "lesson_slot.json"
        ).read_text(encoding="utf-8")
    )
    perms_by_role = {p["role"]: p for p in slot_json["permissions"]}
    assert perms_by_role["All"]["write"] == 0
    assert perms_by_role["All"]["create"] == 0
    assert perms_by_role["All"]["delete"] == 0
    assert perms_by_role["All"]["read"] == 1
    assert perms_by_role["System Manager"]["write"] == 1
    assert perms_by_role["LMS Moderator"]["write"] == 1

    # As páginas custom de agendamento foram removidas em favor do fluxo nativo.
    assert not (WWW / "agendar-aula.html").exists()
    assert not (WWW / "minha-agenda.html").exists()
    assert not (ROOT / "vedium_core" / "vedium_core" / "scheduling.py").exists()


def test_pricing_value_page_has_real_prices_and_no_stale_redirect():
    html_path = WWW / "quanto-custa-curso-de-idiomas.html"
    py_path = WWW / "quanto_custa_curso_de_idiomas.py"
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")

    assert html_path.exists()
    assert py_path.exists()
    html = html_path.read_text(encoding="utf-8")

    # Preços reais (confirmados em produção), não achismo.
    assert "R$ 240" in html
    assert "R$ 320" in html
    assert "US$ 120" in html

    # Honesto sobre não ser a mais barata — não pode prometer isso.
    assert "não somos a opção mais barata" in html.lower() or "não afirmamos isso" in html.lower()

    # FAQ schema para rich snippet.
    assert '"@type": "FAQPage"' in html

    # Word count mínimo (padrão do projeto: 900+ palavras de conteúdo real).
    body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    assert len(text.split()) >= 900

    # O redirect temporário /planos foi removido — a página real existe agora.
    assert '{"source": "/quanto-custa-curso-de-idiomas", "target": "/planos"}' not in hooks

    # Sitemap e footer apontam pra ela.
    assert '"/quanto-custa-curso-de-idiomas"' in sitemap_py
    assert '<a href="/quanto-custa-curso-de-idiomas">' in footer
