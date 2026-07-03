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
from vedium_core.blog_content import BLOG_POSTS, get_blog_post  # noqa: E402
from vedium_core import hooks as vedium_hooks  # noqa: E402

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


def test_pillar_pages_have_real_course_grid_for_campaigns():
    """Páginas pilar reaproveitadas como destino de campanha por idioma
    (decisão do usuário: reusar /curso-de-ingles-online, /curso-de-ioruba-online
    e /portugues-para-estrangeiros em vez de criar novas URLs concorrentes)
    precisam mostrar cursos reais (nível, preço, link) — não só um preço agregado.
    """
    courses_py = (ROOT / "vedium_core" / "vedium_core" / "courses.py").read_text(encoding="utf-8")
    assert "def get_published_courses(category_prefix=None, category_exact=None)" in courses_py

    landing_content = (ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py").read_text(
        encoding="utf-8"
    )
    assert "LANDING_COURSE_FILTERS" in landing_content
    assert '"curso-de-ingles-online": {"category_prefix": "Inglês"}' in landing_content
    assert '"curso-de-ioruba-online": {"category_prefix": "Iorubá"}' in landing_content
    assert (
        '"portugues-para-estrangeiros": {"category_exact": "Português para Estrangeiros"}'
        in landing_content
    )

    template = (TPL / "marketing_landing.html").read_text(encoding="utf-8")
    assert "landing.course_grid" in template
    assert "course.formatted_price" in template
    assert "course.level_badge" in template
    assert 'href="{{ course.url }}"' in template

    # Armadilha real (achada em produção 2026-07-02): os www/*.html das páginas
    # pilar chamam get_marketing_landing() DIRETO como global do Jinja
    # ({% set landing = get_marketing_landing("slug") %}), ignorando o
    # context.landing setado pelo controller .py via apply_landing_context().
    # Qualquer dado novo em `landing` (como course_grid) só chega à página se
    # for calculado DENTRO de get_marketing_landing() — não em
    # apply_landing_context(). Trava essa posição pra não regredir.
    for slug in ("curso-de-ingles-online", "curso-de-ioruba-online", "portugues-para-estrangeiros"):
        html_path = WWW / f"{slug}.html"
        assert html_path.read_text(encoding="utf-8").strip().splitlines()[0] == (
            f'{{% set landing = get_marketing_landing("{slug}") %}}'
        )
    apply_ctx_start = landing_content.index("def apply_landing_context")
    get_landing_start = landing_content.index("def get_marketing_landing")
    course_filter_use = landing_content.index("course_filter = LANDING_COURSE_FILTERS.get(slug)")
    assert get_landing_start < course_filter_use, (
        "course_grid precisa ser calculado dentro de get_marketing_landing(), "
        "não de apply_landing_context() — o .html ignora o context.landing do .py"
    )
    assert not (apply_ctx_start < course_filter_use < get_landing_start)


def test_placement_test_cta_routes_to_the_right_language_and_subject():
    """Bug real achado em produção (2026-07-02): o CTA "teste de nível" das
    páginas pilar usava uma heurística (`slug.startswith("ingles-")`) que
    tinha 2 furos: (1) o próprio pilar "curso-de-ingles-online" não começa
    com "ingles-", então caía no teste de PORTUGUÊS por engano; (2) o
    cluster Iorubá também caía no teste de português (não existe teste de
    iorubá) e as páginas em inglês (learn-yoruba-online/learn-portuguese-brazil)
    linkavam pra testes só em português. Trava os valores explícitos de
    `test_url` que corrigem os dois problemas.
    """
    explicit_test_url = {
        "curso-de-ingles-online": "/teste-de-nivel-ingles",
        "curso-de-ioruba-online": None,
        "ioruba-para-iniciantes": None,
        "ioruba-cultura-e-ancestralidade": None,
        "learn-yoruba-online": None,
        "learn-portuguese-brazil": "/en/portuguese-placement-test",
        "portugues-para-executivos": "/teste-de-nivel",
        "preparatorio-celpe-bras": "/teste-de-nivel",
    }
    for slug, expected in explicit_test_url.items():
        assert "test_url" in LANDINGS[slug], f"{slug} precisa de test_url explícito"
        assert LANDINGS[slug]["test_url"] == expected

    # Slugs que dependem da heurística antiga (slug.startswith("ingles-") /
    # senão português) continuam sem override — a heurística já acerta pra eles.
    for slug in (
        "ingles-para-entrevista",
        "ingles-para-programadores",
        "ingles-executivo",
        "ingles-para-viagens",
        "ingles-para-atendimento-ao-cliente",
        "portugues-para-estrangeiros",
    ):
        assert "test_url" not in LANDINGS[slug]

    template = (TPL / "marketing_landing.html").read_text(encoding="utf-8")
    assert 'landing.test_url if "test_url" in landing else' in template
    # botão de teste só aparece se landing_test_url existir (Iorubá não tem teste)
    assert "{% if landing_test_url %}" in template

    # Página EN nova + reciprocidade de hreflang com a versão em português
    en_html_path = WWW / "en" / "portuguese-placement-test.html"
    en_py_path = WWW / "en" / "portuguese_placement_test.py"
    pt_html = (WWW / "teste-de-nivel.html").read_text(encoding="utf-8")
    assert en_html_path.exists()
    assert en_py_path.exists()
    en_html = en_html_path.read_text(encoding="utf-8")
    assert 'lang="en"' in en_html
    assert 'hreflang="pt-br" href="https://vediums.com/teste-de-nivel"' in en_html
    assert 'hreflang="en" href="https://vediums.com/en/portuguese-placement-test"' in pt_html
    assert "/en/portuguese-placement-test" in (
        ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
    ).read_text(encoding="utf-8")


def test_spanish_menu_and_placement_test_have_reciprocal_hreflang():
    """Primeiro idioma novo (espanhol) publicado depois da infraestrutura de
    i18n ter sido generalizada pra N idiomas (2026-07-03). Trava o rótulo
    "es" no menu principal e o par PT<->ES do teste de nível de português
    (slug pesquisado como um hispanofalante buscaria, não tradução literal
    palavra-por-palavra de "teste-de-nivel").
    """
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    assert '"es": {"home": "Inicio"' in navbar

    es_html_path = WWW / "es" / "prueba-de-nivel-de-portugues.html"
    es_py_path = WWW / "es" / "prueba_de_nivel_de_portugues.py"
    pt_html = (WWW / "teste-de-nivel.html").read_text(encoding="utf-8")
    en_html = (WWW / "en" / "portuguese-placement-test.html").read_text(encoding="utf-8")
    assert es_html_path.exists()
    assert es_py_path.exists()
    es_html = es_html_path.read_text(encoding="utf-8")
    assert 'lang="es"' in es_html
    assert 'hreflang="pt-br" href="https://vediums.com/teste-de-nivel"' in es_html
    assert 'hreflang="en" href="https://vediums.com/en/portuguese-placement-test"' in es_html
    assert 'hreflang="es" href="https://vediums.com/es/prueba-de-nivel-de-portugues"' in es_html
    assert 'hreflang="es" href="https://vediums.com/es/prueba-de-nivel-de-portugues"' in pt_html
    assert 'hreflang="es" href="https://vediums.com/es/prueba-de-nivel-de-portugues"' in en_html

    # Interface em espanhol, perguntas continuam em português (é o idioma avaliado)
    assert "Gramática y vocabulario" in es_html
    assert "Comprensión de lectura" in es_html
    assert "Comprensión auditiva" in es_html
    assert "Producción escrita" in es_html
    assert "Producción oral" in es_html
    assert "plataforma quatro às quinze horas" in es_html  # texto do áudio, em PT
    assert es_html.count("data-correct=") == 15

    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    assert '"es": "prueba-de-nivel-de-portugues"' in hooks
    assert "/es/prueba-de-nivel-de-portugues" in (
        ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
    ).read_text(encoding="utf-8")


def test_foreign_audience_clusters_have_english_pages_with_reciprocal_hreflang():
    """Público de Iorubá e Português-para-estrangeiros (PLE) inclui gente que
    não fala PT (diáspora, expats, executivos estrangeiros) — decisão do
    usuário: traduzir esses 2 clusters pra inglês primeiro. Cada par PT/EN
    precisa apontar um pro outro via `alt` (hreflang bidirecional).

    Checagem por subconjunto (não igualdade exata): o cluster Iorubá já
    ganhou uma 3ª entrada "es" no mesmo `alt` (par PT/ES paralelo, ver
    test_yoruba_cluster_has_spanish_pages_with_reciprocal_hreflang) — o
    dict `alt` é compartilhado entre todos os idiomas daquele slug, então
    exigir igualdade exata quebraria assim que qualquer 3º idioma chegasse.
    """
    pairs = [
        ("ioruba-para-iniciantes", "yoruba-for-beginners", None),
        ("ioruba-cultura-e-ancestralidade", "yoruba-culture-and-heritage", None),
        ("portugues-para-executivos", "portuguese-for-executives", "/en/portuguese-placement-test"),
        ("preparatorio-celpe-bras", "celpe-bras-exam-prep", "/en/portuguese-placement-test"),
    ]
    for pt_slug, en_slug, expected_test_url in pairs:
        expected_pair = {"pt-BR": pt_slug, "en": en_slug}
        assert LANDINGS[pt_slug]["alt"].items() >= expected_pair.items()
        assert LANDINGS[en_slug]["alt"].items() >= expected_pair.items()
        assert LANDINGS[en_slug]["lang"] == "en"
        assert "test_url" in LANDINGS[en_slug], f"{en_slug} precisa de test_url explícito"
        assert LANDINGS[en_slug]["test_url"] == expected_test_url

        en_html = (WWW / "en" / f"{en_slug}.html").read_text(encoding="utf-8")
        en_py = (WWW / "en" / f"{en_slug.replace('-', '_')}.py").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{en_slug}")' in en_html
        assert en_slug in en_py

        # conteúdo real, não placeholder (mesmo padrão de profundidade das outras landings)
        landing = LANDINGS[en_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/en/{en_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")


def test_english_cluster_has_english_pages_with_reciprocal_hreflang():
    """Cluster de Inglês (pilar curso-de-ingles-online + 5 sub-páginas) --
    item 4 de prioridade do agente translator-en, a única parte do cluster
    de idiomas que ainda faltava (Iorubá e PLE já tinham inglês publicado
    antes). Mesmo padrão dos outros clusters: slug em inglês pensado como
    um falante nativo buscaria (não tradução literal), alt recíproco nos
    dois idiomas, paridade de profundidade de conteúdo.
    """
    pairs = [
        ("curso-de-ingles-online", "learn-english-online", "/teste-de-nivel-ingles"),
        ("ingles-para-entrevista", "english-for-job-interviews", None),
        ("ingles-para-programadores", "english-for-developers", None),
        ("ingles-executivo", "business-english-online", None),
        ("ingles-para-viagens", "english-for-travel", None),
        ("ingles-para-atendimento-ao-cliente", "english-for-customer-service", None),
    ]
    for pt_slug, en_slug, expected_test_url in pairs:
        expected_pair = {"pt-BR": pt_slug, "en": en_slug}
        assert LANDINGS[pt_slug]["alt"].items() >= expected_pair.items()
        assert LANDINGS[en_slug]["alt"].items() >= expected_pair.items()
        assert LANDINGS[en_slug]["lang"] == "en"
        if expected_test_url:
            assert "test_url" in LANDINGS[en_slug], f"{en_slug} precisa de test_url explícito"
            assert LANDINGS[en_slug]["test_url"] == expected_test_url

        en_html = (WWW / "en" / f"{en_slug}.html").read_text(encoding="utf-8")
        en_py_path = WWW / "en" / f"{en_slug.replace('-', '_')}.py"
        assert en_py_path.exists(), f"falta www/en/{en_slug.replace('-', '_')}.py (underscore!)"
        en_py = en_py_path.read_text(encoding="utf-8")
        assert f'get_marketing_landing("{en_slug}")' in en_html
        assert en_slug in en_py

        # conteúdo real, não placeholder (mesmo padrão de profundidade das outras landings)
        landing = LANDINGS[en_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/en/{en_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # Pilar em inglês: mesma riqueza de SEO/GEO que o pilar em PT (prosa
    # longa, preço em US$, grid de cursos ao vivo do banco filtrado por
    # categoria "Inglês", link building interno pro cluster).
    pillar = LANDINGS["learn-english-online"]
    prose = " ".join(block for sec in pillar["seo_sections"] for block in sec["body"])
    word_count = len(re.sub(r"<[^>]+>", " ", prose).split())
    assert word_count >= 700, f"prosa muito curta: {word_count} palavras"
    assert len(pillar["seo_sections"]) >= 4
    assert pillar["price_from"] == "120"
    assert "US$ 120" in pillar["price_display"]
    assert "R$" not in pillar["price_display"]
    assert "/ingles-para-entrevista" in prose
    assert "/teste-de-nivel-ingles" in prose

    landing_content = (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")
    assert '"learn-english-online": {"category_prefix": "Inglês"}' in landing_content

    pillar_html = (WWW / "en" / "learn-english-online.html").read_text(encoding="utf-8")
    assert pillar_html.strip().splitlines()[0] == (
        '{% set landing = get_marketing_landing("learn-english-online") %}'
    )


def test_yoruba_cluster_has_spanish_pages_with_reciprocal_hreflang():
    """Cluster Iorubá traduzido pro espanhol (2026-07-03, mesmo racional do
    inglês: público inclui diáspora hispanofalante, não fala PT). Trava par
    PT<->ES via `alt` (que agora carrega 3 idiomas nesses 3 slugs — pt-BR,
    en, es — todos apontando um pro outro), slugs pesquisados como um
    hispanofalante buscaria (não tradução literal palavra-por-palavra) e
    paridade de profundidade de conteúdo com as versões PT/EN existentes.
    """
    pairs = [
        ("curso-de-ioruba-online", "curso-de-yoruba-online", None),
        ("ioruba-para-iniciantes", "yoruba-para-principiantes", None),
        ("ioruba-cultura-e-ancestralidade", "yoruba-cultura-y-ancestralidad", None),
    ]
    for pt_slug, es_slug, expected_test_url in pairs:
        assert LANDINGS[pt_slug]["alt"]["es"] == es_slug
        assert LANDINGS[es_slug]["alt"] == {
            "pt-BR": pt_slug,
            "en": LANDINGS[pt_slug]["alt"]["en"],
            "es": es_slug,
        }
        assert LANDINGS[es_slug]["lang"] == "es"
        assert "test_url" in LANDINGS[es_slug], f"{es_slug} precisa de test_url explícito"
        assert LANDINGS[es_slug]["test_url"] == expected_test_url

        es_html = (WWW / "es" / f"{es_slug}.html").read_text(encoding="utf-8")
        es_py = (WWW / "es" / f"{es_slug.replace('-', '_')}.py").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{es_slug}")' in es_html
        assert es_slug in es_py

        # conteúdo real, não placeholder (mesmo padrão de profundidade das outras landings)
        landing = LANDINGS[es_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/es/{es_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # Curso-de-yoruba-online é a landing pilar em ES: precisa do mesmo grid
    # de cursos reais (preço, aulas, link) que os outros pilares já têm.
    assert '"curso-de-yoruba-online": {"category_prefix": "Iorubá"}' in (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")


def test_ple_cluster_has_spanish_pages_with_reciprocal_hreflang():
    """Cluster PLE (Português para Estrangeiros) traduzido pro espanhol --
    público de PLE é 100% estrangeiro e inclui muitos hispanofalantes,
    prioridade alta na retomada do trabalho em ES (mesma ordem de
    prioridade que o inglês, item 4). Mesmo padrão do cluster Iorubá em
    espanhol: `alt` com 3 idiomas, slugs pesquisados como um hispanofalante
    buscaria. test_url aponta pro único teste de nível real que existe
    (inglês) -- não inventa um teste de espanhol que não existe.
    """
    pairs = [
        ("portugues-para-estrangeiros", "portugues-para-extranjeros", "/en/portuguese-placement-test"),
        ("portugues-para-executivos", "portugues-para-ejecutivos", "/en/portuguese-placement-test"),
        ("preparatorio-celpe-bras", "preparacion-examen-celpe-bras", "/en/portuguese-placement-test"),
    ]
    for pt_slug, es_slug, expected_test_url in pairs:
        assert LANDINGS[pt_slug]["alt"]["es"] == es_slug
        # Checagem por subconjunto (não igualdade exata): o cluster PLE
        # ganhou francês depois (ver test_ple_cluster_has_french_pages_...),
        # então esses "alt" legitimamente têm uma chave "fr" a mais agora.
        assert LANDINGS[es_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[es_slug]["alt"]["en"] == LANDINGS[pt_slug]["alt"]["en"]
        assert LANDINGS[es_slug]["alt"]["es"] == es_slug
        assert LANDINGS[es_slug]["lang"] == "es"
        assert "test_url" in LANDINGS[es_slug], f"{es_slug} precisa de test_url explícito"
        assert LANDINGS[es_slug]["test_url"] == expected_test_url

        es_html = (WWW / "es" / f"{es_slug}.html").read_text(encoding="utf-8")
        es_py = (WWW / "es" / f"{es_slug.replace('-', '_')}.py").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{es_slug}")' in es_html
        assert es_slug in es_py

        # conteúdo real, não placeholder (mesmo padrão de profundidade das outras landings)
        landing = LANDINGS[es_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/es/{es_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # portugues-para-extranjeros é a landing pilar em ES: precisa do mesmo
    # grid de cursos reais (preço, aulas, link) que os outros pilares já têm.
    assert '"portugues-para-extranjeros": {"category_exact": "Português para Estrangeiros"}' in (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")


def test_english_cluster_has_spanish_pages_with_reciprocal_hreflang():
    """Cluster de Inglês (pilar curso-de-ingles-online-en-vivo + 5
    sub-páginas) traduzido pro espanhol -- último item da ordem de
    prioridade corrigida (item 5): hispanohablantes que querem aprender
    inglês com a Vedium. Mesmo padrão de
    test_english_cluster_has_english_pages_with_reciprocal_hreflang: slug em
    espanhol pensado como um hispanofalante buscaria (não tradução literal
    do português nem do inglês), `alt` recíproco nos 3 idiomas, paridade de
    profundidade de conteúdo.
    """
    pairs = [
        ("curso-de-ingles-online", "curso-de-ingles-online-en-vivo", "/en/portuguese-placement-test"),
        ("ingles-para-entrevista", "ingles-para-entrevistas-de-trabajo", None),
        ("ingles-para-programadores", "ingles-para-programadores", None),
        ("ingles-executivo", "ingles-de-negocios", None),
        ("ingles-para-viagens", "ingles-para-viajar", None),
        ("ingles-para-atendimento-ao-cliente", "ingles-para-atencion-al-cliente", None),
    ]
    for pt_slug, es_slug, expected_test_url in pairs:
        assert LANDINGS[pt_slug]["alt"]["es"] == es_slug
        # Checagem por subconjunto (não igualdade exata): o cluster de
        # inglês ganhou francês depois (test_english_cluster_has_french_...),
        # então esses "alt" legitimamente têm uma chave "fr" a mais agora.
        assert LANDINGS[es_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[es_slug]["alt"]["en"] == LANDINGS[pt_slug]["alt"]["en"]
        assert LANDINGS[es_slug]["alt"]["es"] == es_slug
        assert LANDINGS[es_slug]["lang"] == "es"
        if expected_test_url:
            assert "test_url" in LANDINGS[es_slug], f"{es_slug} precisa de test_url explícito"
            assert LANDINGS[es_slug]["test_url"] == expected_test_url

        es_html = (WWW / "es" / f"{es_slug}.html").read_text(encoding="utf-8")
        es_py_path = WWW / "es" / f"{es_slug.replace('-', '_')}.py"
        assert es_py_path.exists(), f"falta www/es/{es_slug.replace('-', '_')}.py (underscore!)"
        es_py = es_py_path.read_text(encoding="utf-8")
        assert f'get_marketing_landing("{es_slug}")' in es_html
        assert es_slug in es_py

        # conteúdo real, não placeholder (mesmo padrão de profundidade das outras landings)
        landing = LANDINGS[es_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/es/{es_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # Pilar em espanhol: mesma riqueza de SEO/GEO que os pilares em PT/EN
    # (prosa longa, preço em US$, grid de cursos ao vivo do banco filtrado
    # por categoria "Inglês", link building interno pro cluster).
    pillar = LANDINGS["curso-de-ingles-online-en-vivo"]
    prose = " ".join(block for sec in pillar["seo_sections"] for block in sec["body"])
    word_count = len(re.sub(r"<[^>]+>", " ", prose).split())
    assert word_count >= 700, f"prosa muito curta: {word_count} palavras"
    assert len(pillar["seo_sections"]) >= 4
    assert pillar["price_from"] == "120"
    assert "US$ 120" in pillar["price_display"]
    assert "R$" not in pillar["price_display"]
    assert "/es/ingles-para-entrevistas-de-trabajo" in prose

    landing_content = (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")
    assert '"curso-de-ingles-online-en-vivo": {"category_prefix": "Inglês"}' in landing_content

    pillar_html = (WWW / "es" / "curso-de-ingles-online-en-vivo.html").read_text(encoding="utf-8")
    assert pillar_html.strip().splitlines()[0] == (
        '{% set landing = get_marketing_landing("curso-de-ingles-online-en-vivo") %}'
    )


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


def test_english_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang():
    """Páginas do menu principal (catalogo, sobre, como-funciona, faq,
    contato) traduzidas pro inglês -- 2a prioridade do agente translator-en
    depois da home. Diferente das landings (LANDINGS) e do teste de nível
    (slug diferente), essas páginas mantêm o MESMO slug sob /en/ (ex.
    /en/catalogo) -- ver SAME_SLUG_TRANSLATIONS em hooks.py, que existe
    justamente pra este caso: sem essa entrada, LANGUAGE_ROUTE_RULES força
    o controller PT mesmo com www/en/<slug>.html existindo, e o redirect de
    en-us/en-au cairia de volta pro PT em vez de usar a tradução real.
    """
    menu_slugs = ["catalogo", "sobre", "como-funciona", "faq", "contato"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in menu_slugs:
        en_html_path = WWW / "en" / f"{slug}.html"
        pt_html_path = WWW / f"{slug}.html"
        assert en_html_path.exists(), f"falta www/en/{slug}.html"
        assert pt_html_path.exists()

        en_html = en_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")

        assert 'lang="en"' in en_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in en_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in en_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in pt_html

        # SAME_SLUG_TRANSLATIONS registrado, senão o roteamento força PT
        assert f'"{slug}": {{"en"}}' in hooks or f'"{slug}": {{"en"' in hooks

        assert f'{{"loc": "/en/{slug}"' in sitemap_py

    # catalogo/sobre/como-funciona/faq têm controller próprio (title/description
    # dinâmicos ou lógica de cursos); contato não tem .py em nenhum idioma
    # (conteúdo 100% estático no .html) -- não regride esse padrão.
    for slug in ["catalogo", "como-funciona", "faq"]:
        en_py_path = WWW / "en" / f"{slug.replace('-', '_')}.py"
        assert en_py_path.exists(), f"falta www/en/{slug.replace('-', '_')}.py"
    assert not (WWW / "en" / "contato.py").exists()
    assert not (WWW / "contato.py").exists()

    # sobre.py nunca existiu em nenhum idioma (conteúdo estático) — não
    # inventa um controller que o PT também não tem.
    assert not (WWW / "sobre.py").exists()
    assert not (WWW / "en" / "sobre.py").exists()

    # Roteamento: /en/catalogo não pode ser interceptado pelo controller PT
    # (bug que existiria se SAME_SLUG_TRANSLATIONS não tivesse sido criado)
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in menu_slugs:
        assert f"/en/{slug}" not in by_source  # sem self-redirect
        assert by_source[f"/en-us/{slug}"] == f"/en/{slug}"

    rules_by_from = {r["from_route"]: r["to_route"] for r in vedium_hooks.LANGUAGE_ROUTE_RULES}
    for slug in menu_slugs:
        assert rules_by_from.get(f"/en/{slug}") is None
        assert rules_by_from.get(f"/en-us/{slug}") is None

    # Conteúdo real (adaptação, não tradução literal) — CTAs apontam pro
    # teste de nível de inglês e pro catálogo em inglês, não pro PT.
    catalogo_en = (WWW / "en" / "catalogo.html").read_text(encoding="utf-8")
    sobre_en = (WWW / "en" / "sobre.html").read_text(encoding="utf-8")
    como_funciona_en = (WWW / "en" / "como-funciona.html").read_text(encoding="utf-8")
    faq_en = (WWW / "en" / "faq.html").read_text(encoding="utf-8")
    contato_en = (WWW / "en" / "contato.html").read_text(encoding="utf-8")

    assert "/teste-de-nivel-ingles" in como_funciona_en
    assert "/teste-de-nivel-ingles" in faq_en
    assert "/en/catalogo" in sobre_en
    assert "Study from anywhere in the world" in sobre_en
    assert "Explore Our Courses" in catalogo_en
    assert "Send Message" in contato_en
    assert "Message sent!" in contato_en


def test_english_institutional_pages_exist_with_reciprocal_hreflang():
    """Restante das páginas institucionais (item 5 do translator-en):
    certificado, comunidade, programa-de-indicacao, empresas, carreiras.
    Mesmo padrão de slug das páginas de menu/CTA -- mesmo slug sob /en/.
    comunidade e empresas reaproveitam o template compartilhado
    public_intent_page.html (agora com hreflang condicional via
    page_has_en_translation, pra não quebrar páginas desse template que
    ainda não têm tradução, ex. futuras). carreiras usa templates/web.html
    (tema genérico do Frappe, sem controle de <head> customizado -- por
    isso não tem hreflang, mesma limitação da versão em PT).

    Checagem de SAME_SLUG_TRANSLATIONS por subconjunto (não igualdade
    exata): espanhol ganhou as mesmas páginas depois (ver
    test_spanish_institutional_pages_exist_with_reciprocal_hreflang), então
    esses sets legitimamente têm {"en", "es"} agora.
    """
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    # certificado + programa-de-indicacao: página própria, com hreflang direto
    for slug in ["certificado", "programa-de-indicacao"]:
        en_html_path = WWW / "en" / f"{slug}.html"
        en_py_path = WWW / "en" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert en_html_path.exists(), f"falta www/en/{slug}.html"
        assert en_py_path.exists(), f"falta www/en/{slug.replace('-', '_')}.py"
        en_html = en_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")
        assert 'lang="en"' in en_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in en_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in en_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in pt_html
        assert f'"{slug}": {{"en", "es"}}' in hooks
        assert f'{{"loc": "/en/{slug}"' in sitemap_py

    # comunidade + empresas: template compartilhado public_intent_page(_en).html
    template_en = (TPL / "public_intent_page_en.html").read_text(encoding="utf-8")
    template_pt = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "page_has_en_translation" in template_pt
    assert 'hreflang="en" href="https://vediums.com/en/{{ page_slug }}"' in template_pt
    assert "vedium_core.public_funnel.submit_public_intent" in template_en
    assert "/teste-de-nivel-ingles" in template_en
    assert "wa.me/5511911293075" in template_en
    for slug, intent in {"comunidade": "community", "empresas": "b2b"}.items():
        en_html_path = WWW / "en" / f"{slug}.html"
        en_py_path = WWW / "en" / f"{slug.replace('-', '_')}.py"
        pt_html = (WWW / f"{slug}.html").read_text(encoding="utf-8")
        assert en_html_path.exists()
        assert en_py_path.exists()
        en_html = en_html_path.read_text(encoding="utf-8")
        en_py = en_py_path.read_text(encoding="utf-8")
        assert f'page_slug = "{slug}"' in en_html
        assert f'page_intent = "{intent}"' in en_html
        assert 'public_intent_page_en.html' in en_html
        assert "page_has_en_translation = true" in pt_html
        assert "get_context" in en_py
        assert f'"{slug}": {{"en", "es"}}' in hooks
        assert f'{{"loc": "/en/{slug}"' in sitemap_py

    # carreiras: web.html generico, sem hreflang (mesma limitacao do PT)
    assert (WWW / "en" / "carreiras.html").exists()
    assert (WWW / "en" / "carreiras.py").exists()
    carreiras_en = (WWW / "en" / "carreiras.html").read_text(encoding="utf-8")
    carreiras_en_py = (WWW / "en" / "carreiras.py").read_text(encoding="utf-8")
    assert "English Teacher" in carreiras_en_py
    assert "Submit application" in carreiras_en
    assert "vedium_core.careers.submit_candidatura" in carreiras_en
    assert 'context.canonical_url = "https://vediums.com/en/carreiras"' in carreiras_en_py
    assert '"carreiras": {"en", "es"}' in hooks
    assert '{"loc": "/en/carreiras"' in sitemap_py

    # Roteamento: sem self-redirect, en-us cai na traducao real
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in ["certificado", "comunidade", "programa-de-indicacao", "empresas", "carreiras"]:
        assert f"/en/{slug}" not in by_source
        assert by_source[f"/en-us/{slug}"] == f"/en/{slug}"


def test_english_cta_pages_exist_and_preserve_public_funnel_safety():
    """Páginas de CTA/conversão (planos, matricula, aula-diagnostica) --
    3a prioridade do agente translator-en. Mesmo slug sob /en/ (como as
    páginas de menu). Preserva as garantias de segurança do funil público
    já testadas em PT: sem alteração de checkout, CTAs corretos pro
    público internacional (teste de nível em inglês, não o de português).
    """
    cta_slugs = ["planos", "matricula", "aula-diagnostica"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in cta_slugs:
        en_html_path = WWW / "en" / f"{slug}.html"
        en_py_path = WWW / "en" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert en_html_path.exists(), f"falta www/en/{slug}.html"
        assert en_py_path.exists(), f"falta www/en/{slug.replace('-', '_')}.py"

        en_html = en_html_path.read_text(encoding="utf-8")
        en_py = en_py_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")

        assert 'lang="en"' in en_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in en_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in en_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in pt_html
        # SAME_SLUG_TRANSLATIONS ganhou "fr" (test_french_cta_pages_...)
        # para esses mesmos 3 slugs -- checa que "en" continua no set.
        assert f'"{slug}": {{"en", "es", "fr"}}' in hooks
        assert f'{{"loc": "/en/{slug}"' in sitemap_py

        # Funil publico continua seguro: sem endpoint de checkout real (matricula
        # MENCIONA "Stripe" como copy informativo -- "Stripe preserved" --
        # igual a versao em PT, entao so exige ausencia nas outras 2 paginas)
        if slug != "matricula":
            assert "stripe" not in en_html.lower()
        assert "create_checkout" not in en_html
        assert 'context.lang = "en"' in en_py
        assert f'context.canonical_url = "https://vediums.com/en/{slug}"' in en_py

    # planos: CTA final aponta pro teste de nivel em ingles e pro
    # matricula/catalogo em ingles, nao pros equivalentes em PT.
    planos_en = (WWW / "en" / "planos.html").read_text(encoding="utf-8")
    assert "/teste-de-nivel-ingles" in planos_en
    assert "/en/matricula" in planos_en
    assert "/en/catalogo" in planos_en
    assert "Choose the light plan" in planos_en
    assert "Choose the recommended plan" in planos_en
    assert "Choose the intensive plan" in planos_en
    assert "wa.me/5511911293075" in planos_en

    # matricula: dropdown com valores de curso intactos (slugs de banco,
    # nunca traduzidos), so os LABELS mudam pro ingles.
    matricula_en = (WWW / "en" / "matricula.html").read_text(encoding="utf-8")
    assert 'value="ingl-s-beginner"' in matricula_en
    assert 'value="iorub-b-sico"' in matricula_en
    assert "English Beginner (A1)" in matricula_en
    assert "Continue on the platform" in matricula_en
    assert "app.vediums.com/lms/courses/" in matricula_en
    assert "source=public_funnel" in matricula_en
    assert "enrollment_intent_click" in matricula_en
    assert "/api/method" not in matricula_en

    # aula-diagnostica: pre-agendamento nao cria reserva automatica,
    # mesma garantia da versao em PT, com CTAs em ingles.
    diagnostica_en = (WWW / "en" / "aula-diagnostica.html").read_text(encoding="utf-8")
    assert "diagnostic_schedule_click" in diagnostica_en
    assert "diagnostic_slot_click" in diagnostica_en
    assert "get_available_diagnostic_slots" in diagnostica_en
    assert 'data-vd-diagnostic="english"' in diagnostica_en
    assert 'data-vd-diagnostic="portuguese_foreigners"' in diagnostica_en
    assert 'data-vd-diagnostic="yoruba"' in diagnostica_en
    assert "doesn't create an automatic booking, enrollment, charge or plan change" in diagnostica_en
    assert "vedium_core.public_funnel.get_available_diagnostic_slots" in diagnostica_en

    # Roteamento: sem self-redirect, en-us cai na traducao real
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in cta_slugs:
        assert f"/en/{slug}" not in by_source
        assert by_source[f"/en-us/{slug}"] == f"/en/{slug}"


def test_english_home_page_exists_and_routes_correctly():
    """Home (/) traduzida pro inglês (www/en/index.html) — a página mais
    visitada do site, primeira prioridade do agente translator-en (ver
    .claude/agents/translator-en.md). Diferente das landings do dict
    LANDINGS, a home é página própria (hero com swiper, grid de cursos ao
    vivo do banco, planos, depoimentos, blog) sem infraestrutura de
    tradução prévia — por isso trava aqui: existência dos arquivos,
    conteúdo real (não placeholder), roteamento (/en não pode mais cair no
    redirect antigo pra PT) e reciprocidade de hreflang.
    """
    en_html_path = WWW / "en" / "index.html"
    en_py_path = WWW / "en" / "index.py"
    assert en_html_path.exists()
    assert en_py_path.exists()

    en_html = en_html_path.read_text(encoding="utf-8")
    en_py = en_py_path.read_text(encoding="utf-8")
    pt_html = (WWW / "index.html").read_text(encoding="utf-8")

    assert 'lang="en"' in en_html
    assert "Vedium - Live Online Language Courses" in en_html
    assert 'hreflang="pt-br" href="https://vediums.com/"' in en_html
    assert 'hreflang="en" href="https://vediums.com/en"' in en_html
    assert 'link rel="canonical" href="https://vediums.com/en"' in en_html

    # Hero traduzido (above-the-fold), CTAs apontam pro teste de inglês
    assert "Accelerate Your" in en_html
    assert "Take the free placement test" in en_html
    assert '/teste-de-nivel-ingles" class="thm-btn"' in en_html
    assert "Chat on WhatsApp" in en_html
    assert "wa.me/5511911293075" in en_html

    # Preço em US$, não R$ (público internacional)
    assert "US$ 120" in en_html
    assert "R$" not in en_html

    # Teasers do blog apontam pros posts em inglês existentes (não pros
    # slugs em português, que o leitor de inglês não conseguiria ler)
    assert "/blog/yoruba-language-and-culture" in en_html
    assert "/blog/yoruba-greetings" in en_html
    assert "/blog/yoruba-numbers-1-to-20" in en_html
    assert "/blog/niveis-de-ingles-a1-c1" not in en_html
    assert "/blog/como-funcionam-as-aulas-ao-vivo" not in en_html

    # Controller: contexto de idioma pro seletor (site_navbar.html) +
    # mesma lógica de negócio da home em PT (cursos ao vivo do banco,
    # redirect app.vediums.com -> /login)
    assert 'context.lang = "en"' in en_py
    assert 'context.canonical_url = "https://vediums.com/en"' in en_py
    assert 'context.alt_lang_url = "https://vediums.com/"' in en_py
    assert "def get_courses()" in en_py
    assert "app.vediums.com" in en_py
    assert 'redirect_location = "/login"' in en_py

    # PT ganha o hreflang de volta (reciprocidade)
    assert 'hreflang="en" href="https://vediums.com/en"' in pt_html

    # Roteamento: /en não pode mais cair no redirect antigo pra PT (bug
    # que existiria se a home nova não tivesse sido conectada em hooks.py)
    hooks_src = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    assert by_source["/en-us"] == "/en"
    assert by_source["/en-au"] == "/en"
    assert "/en" not in by_source  # sem self-redirect /en -> /en
    assert 'if prefix != "en"' in hooks_src

    # Sitemap lista a home em inglês
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    assert '{"loc": "/en", "priority"' in sitemap_py


def test_app_domain_redirect_and_catalog_level_guards_are_in_place():
    index_html = (WWW / "index.html").read_text(encoding="utf-8")
    index_py = (WWW / "index.py").read_text(encoding="utf-8")
    courses_py = (ROOT / "vedium_core" / "vedium_core" / "courses.py").read_text(encoding="utf-8")
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
    assert courses_py.index('"Upper Intermediário": "B2"') < courses_py.index('"Intermediário": "B1"')
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


def test_language_switcher_uses_real_translated_urls_not_prefix_guessing():
    """Bug real achado pelo usuário em produção (2026-07-03): o seletor de
    idioma (bandeiras) fazia troca burra de PREFIXO na URL atual — em
    /en/portuguese-for-executives, clicar na bandeira dos EUA gerava
    /en-us/portuguese-for-executives (404), porque o slug em inglês só
    existe sob /en/, nunca existiu sob /en-us/. site_navbar.html agora
    calcula o mapa REAL {idioma: URL} (landing/post/curso) e expõe via
    data-vd-nav-urls (JSON) no <header>; vedium-language.js usa ele quando
    existe, em vez de adivinhar. Generalizado (2026-07-03, mesma sessão)
    pra N idiomas — não hardcoded só en/pt — depois do usuário pedir pra
    rodar tradução em espanhol/francês/alemão/russo/chinês em paralelo:
    sem isso, cada idioma novo bateria no MESMO bug que o inglês bateu.
    """
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    lang_js = (PUBLIC_JS / "vedium-language.js").read_text(encoding="utf-8")

    assert "data-vd-nav-urls=" in navbar
    assert "data-vd-nav-current=" in navbar
    assert "vd_nav.urls | tojson" in navbar
    # landing (marketing_landing.html), post (blog_post.html) e curso
    # (curso.html) — as 3 famílias de página com tradução de verdade
    assert "landing is defined and landing" in navbar
    assert "post is defined and post" in navbar
    assert "lang is defined and canonical_url is defined" in navbar
    # landing.lang_code já é o hreflang normalizado (LANG_HREFLANG no
    # Python) — não reimplementa a normalização em Jinja
    assert "landing.lang_code" in navbar

    assert "function getPageNavUrls()" in lang_js
    assert "var family = LOCALE_LANG_FAMILY[locale] || locale;" in lang_js
    assert 'var realUrl = pageNav.urls[family] || pageNav.urls.en || pageNav.urls["pt-br"];' in lang_js
    # sem tradução real (a maioria das páginas), continua com o comportamento
    # antigo (troca de prefixo) — não regride nada fora do escopo traduzido
    assert "meta.prefix + cleanPath" in lang_js


def test_language_switcher_remembers_which_regional_flag_was_clicked():
    """Segundo bug achado pelo usuário na mesma sessão (2026-07-03): Global,
    United States e Australia têm o MESMO conteúdo real (só existe um
    /en/... por página) — depois do fix anterior, clicar em "United States"
    levava pra essa única URL, mas o indicador do cabeçalho sempre voltava
    a mostrar "Global" (perdia qual bandeira a pessoa realmente escolheu).
    Corrigido com ?locale=en-us na própria URL (não localStorage — removido
    antes por decisão do time, commit "Use native locale links"). Generalizado
    pra QUALQUER família com mais de uma bandeira regional (en/en-us/en-au,
    es/es-ar/es-co, fr/fr-ca) — não só inglês, já que espanhol e francês têm
    o mesmo problema estrutural assim que ganharem conteúdo real. Idiomas
    sem tradução pra uma página específica caem no inglês real (se existir)
    e mostram o indicador correspondente (honesto — não finge estar naquele
    idioma).
    """
    lang_js = (PUBLIC_JS / "vedium-language.js").read_text(encoding="utf-8")

    assert "var LOCALE_LANG_FAMILY = {" in lang_js
    assert '"es-ar": "es", "es-co": "es", "es": "es",' in lang_js
    assert "var MULTI_REGION_LOCALES = {" in lang_js
    assert "function getPreferredLocaleFromQuery()" in lang_js
    assert 'var localeParam = MULTI_REGION_LOCALES[locale] ? "?locale=" + locale : "";' in lang_js
    assert "var preferredFamily = LOCALE_LANG_FAMILY[preferredLocale] || \"\";" in lang_js
    assert (
        'var current = (pageNav.current && preferredFamily === pageNav.current && preferredLocale)\n'
        '      || pageNav.current\n'
        '      || getLocaleFromPath()\n'
        '      || "pt-br";'
    ) in lang_js
    # não reintroduz o padrão removido antes (localStorage) — usa querystring
    assert "localStorage." not in lang_js
    assert "vedium_preferred_locale" not in lang_js


def test_main_menu_labels_are_translated_per_language():
    """Pedido explícito do usuário (2026-07-03): "linkado no menu correto"
    — o menu principal do cabeçalho (Início, Cursos, Blog, FAQ, Contato)
    estava sempre em português, mesmo nas páginas já traduzidas pra
    inglês. vd_menu_t (dict por idioma, mesmo padrão de vd_i18n em
    marketing_landing.html) traduz os RÓTULOS visíveis — os links
    continuam apontando pro destino em português (catálogo/sobre/como-
    funciona/FAQ/contato ainda não têm tradução; isso é conteúdo, não
    infraestrutura, fica pros agentes de tradução). Cada agente novo
    (.claude/agents/translator-*.md) deve adicionar sua entrada em
    vd_menu_i18n ao publicar a primeira página no idioma dele.
    """
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")

    assert "vd_menu_i18n" in navbar
    assert '"pt-br": {"home": "Início"' in navbar
    assert '"en": {"home": "Home"' in navbar
    assert "vd_menu_t = vd_menu_i18n.get(vd_nav.current, vd_menu_i18n[\"pt-br\"])" in navbar
    for label in ("home", "how", "about", "courses", "blog", "faq", "contact", "login", "signup", "free_test"):
        assert f"vd_menu_t.{label}" in navbar


def test_legacy_language_prefixes_redirect_instead_of_serving_wrong_language():
    """Terceiro bug achado pelo usuário na mesma sessão (2026-07-03),
    screenshot em mãos: /en-us/contato (URL em inglês, conteúdo 100% em
    português) e tentativa de /en-us/portuguese-for-executives (nem existe
    nesse sistema antigo). Causa: LANGUAGE_ROUTE_RULES serve a MESMA
    página em português sob QUALQUER prefixo de idioma — dependia do JS
    (desligado) pra "traduzir" depois de carregar. Isso vale pros 12
    prefixos × 30 páginas da lista PUBLIC_LANGUAGE_ROUTES, não é caso
    isolado.

    Fix: website_redirects intercepta essas URLs ANTES da resolução de
    website_route_rules (frappe/website/path_resolver.py chama
    resolve_redirect() antes de resolve_path()). Se existe tradução real
    (LANDINGS[...]["alt"]["en"] ou o mapa manual de páginas fora do dict
    LANDINGS), redireciona pra ela; senão, redireciona pro canônico em
    português — nunca mais serve conteúdo desalinhado da URL.
    """
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}

    # Casos exatos reportados pelo usuário — /contato ganhou tradução real
    # depois (www/en/contato.html, SAME_SLUG_TRANSLATIONS), então o
    # redirect hoje aponta pra ela em vez de cair no canônico em PT.
    assert by_source["/en-us/contato"] == "/en/contato"
    # /en (e mesma família en-us/en-au) tem home real traduzida agora
    # (www/en/index.html) — não volta mais pro PT.
    assert by_source["/en-us"] == "/en"
    assert "/en" not in by_source

    # Prefixo /en/ TAMBÉM precisa cair no redirect — a página pilar de
    # Iorubá em PT (curso-de-ioruba-online) tem tradução real, mas sob um
    # slug diferente (learn-yoruba-online); sem o redirect, /en/curso-de-
    # ioruba-online serviria a MESMA página em português por baixo do
    # mesmo bug, só que com o prefixo "correto".
    assert by_source["/en/curso-de-ioruba-online"] == "/en/learn-yoruba-online"
    assert by_source["/en-us/teste-de-nivel"] == "/en/portuguese-placement-test"
    # Cluster de Inglês ganhou tradução real depois (mesmo racional do Iorubá
    # acima: slug diferente, learn-english-online) -- redireciona pra ela.
    assert by_source["/en/curso-de-ingles-online"] == "/en/learn-english-online"
    # Espanhol ganhou tradução real depois (mesmo slug, SAME_SLUG_TRANSLATIONS
    # agora inclui "es") -- /es-ar/planos (família es) cai na página real em
    # espanhol, não mais no canônico em PT.
    assert by_source["/es-ar/planos"] == "/es/planos"
    # Sem tradução real (idiomas ainda sem conteúdo) -> PT
    assert by_source["/de/contato"] == "/contato"

    # /en/curso/<slug> (com barra, curso individual) já tem rota + tradução
    # de verdade (curso.py) — não pode ter redirect genérico atropelando.
    assert not any(r["source"].startswith("/en/curso/") for r in redirects)
    assert any(r["source"] == r"/en-us/curso/(.*)" for r in redirects)

    hooks_src = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    assert "*LANGUAGE_PREFIX_REDIRECTS," in hooks_src
    assert hooks_src.index("website_redirects = [") > hooks_src.index(
        "LANGUAGE_PREFIX_REDIRECTS = _build_language_prefix_redirects()"
    )


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
    assert "vedium-language.js?v=v11-n-languages" in footer
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

    # Menu: link para o blog (rótulo agora vem de vd_menu_t, traduzido por
    # idioma — ver test_main_menu_labels_are_translated_per_language)
    assert '<a href="/blog">{{ vd_menu_t.blog }}</a>' in navbar

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


def test_yoruba_blog_cluster_has_english_translations():
    """4 posts do cluster Iorubá traduzidos pro inglês (mesmo /blog/<slug>
    flat, sem prefixo /en/ — blog_post.py é uma rota dinâmica única, não os
    arquivos estáticos .py/.html das páginas pilar). Trava par PT/EN,
    hreflang recíproco e paridade de profundidade de conteúdo.
    """
    pairs = [
        ("alfabeto-ioruba", "yoruba-alphabet-guide"),
        ("saudacoes-em-ioruba", "yoruba-greetings"),
        ("numeros-em-ioruba", "yoruba-numbers-1-to-20"),
        ("aprender-ioruba-lingua-e-cultura", "yoruba-language-and-culture"),
    ]
    for pt_slug, en_slug in pairs:
        assert BLOG_POSTS[pt_slug]["alt"] == {"pt-BR": pt_slug, "en": en_slug}
        assert BLOG_POSTS[en_slug]["alt"] == {"pt-BR": pt_slug, "en": en_slug}
        assert BLOG_POSTS[en_slug]["lang"] == "en"

        pt_post = get_blog_post(pt_slug)
        en_post = get_blog_post(en_slug)
        pt_words = len(re.sub(r"<[^>]+>", " ", " ".join(
            b for sec in pt_post["sections"] for b in sec["body"]
        )).split())
        en_words = len(re.sub(r"<[^>]+>", " ", " ".join(
            b for sec in en_post["sections"] for b in sec["body"]
        )).split())
        # tradução fiel, não resumo nem expansão — tamanho deve ficar próximo
        assert abs(en_words - pt_words) / max(pt_words, 1) < 0.25, (
            f"{en_slug}: {en_words} palavras vs {pt_slug}: {pt_words} — "
            "desvio grande demais para uma tradução fiel"
        )
        assert len(en_post["sections"]) == len(pt_post["sections"])
        assert len(en_post["faqs"]) == len(pt_post["faqs"])

    template = (TPL / "blog_post.html").read_text(encoding="utf-8")
    assert "post.lang or 'pt-BR'" in template
    assert "post.alt" in template
    assert '"Frequently asked questions" if vd_bp_en else' in template


def test_individual_course_pages_have_english_translation():
    """6 páginas de curso individuais (3 Iorubá + 3 PLE) ganham versão em
    inglês via /en/curso/<slug>, reaproveitando o MESMO controller
    dinâmico curso.py (preço/vagas/avaliações sempre ao vivo do banco) —
    só title/short_introduction/description são sobrepostos por
    course_translations.COURSE_TRANSLATIONS. Sem Custom Field, sem
    migração: cursos sem tradução (cluster Inglês) continuam só em PT.
    """
    course_translations = (
        ROOT / "vedium_core" / "vedium_core" / "course_translations.py"
    ).read_text(encoding="utf-8")
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    curso_py = (WWW / "curso.py").read_text(encoding="utf-8")
    curso_html = (WWW / "curso.html").read_text(encoding="utf-8")

    translated_slugs = [
        "iorub-b-sico",
        "iorub-intermedi-rio",
        "iorub-avan-ado",
        "portugues-para-estrangeiros-basico",
        "portugues-para-estrangeiros-intermediario",
        "portugues-para-estrangeiros-avancado",
    ]
    for slug in translated_slugs:
        assert f'"{slug}"' in course_translations

    assert '{"from_route": "/en/curso/<course>", "to_route": "curso"}' in hooks

    # sem tradução -> redireciona pra versão PT (não cria página fina/duplicada)
    assert "from vedium_core.course_translations import COURSE_TRANSLATIONS" in curso_py
    assert "has_translation = course_name in COURSE_TRANSLATIONS" in curso_py
    assert 'frappe.local.flags.redirect_location = f"/curso/{course_name}"' in curso_py

    # preço/vagas/avaliações continuam vindo do banco — só sobrepõe texto
    assert "context.course = get_course_details(course_name)" in curso_py
    assert 'context.course.title = translation["title"]' in curso_py

    # chrome bilíngue + hreflang recíproco
    assert 'lang="{{ lang or \'pt-BR\' }}"' in curso_html
    assert "alt_lang_url" in curso_html
    assert '"Enroll now" if vd_course_en else "Matricular agora"' in curso_html

    # Bug real achado em produção (2026-07-02, pós-deploy): frappe.local.path
    # NUNCA tem barra inicial — PathResolver.__init__ faz path.strip("/ ")
    # antes de setar frappe.local.path (frappe/website/path_resolver.py).
    # startswith("/en/curso/") com barra na frente nunca batia, então
    # /en/curso/<slug> sempre renderizava em português. Trava a versão
    # corrigida (lstrip antes do startswith).
    assert '.startswith("/en/curso/")' not in curso_py, (
        "startswith com barra inicial nunca bate — frappe.local.path não tem "
        "barra na frente (path_resolver.py faz .strip('/ '))"
    )
    assert '.lstrip("/").startswith("en/curso/")' in curso_py


def test_english_pillar_course_grid_links_to_english_course_pages():
    """As páginas pilar EN (learn-yoruba-online, learn-portuguese-brazil)
    ganham o mesmo grid de cursos das PT (task #38), mas linkando pra
    /en/curso/<slug> com título traduzido — não faz sentido levar quem
    está lendo em inglês pra uma ficha de curso 100% em português.
    """
    landing_content = (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")
    assert '"learn-yoruba-online": {"category_prefix": "Iorubá"}' in landing_content
    assert (
        '"learn-portuguese-brazil": {"category_exact": "Português para Estrangeiros"}'
        in landing_content
    )
    assert "LANDING_COURSE_GRID_USES_EN_COURSE_URL" in landing_content
    assert 'course.url = f"/en/curso/{course.name}"' in landing_content


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


def test_spanish_home_page_exists_and_routes_correctly():
    """Home (/) traduzida pro espanhol (www/es/index.html) — retomando o
    trabalho de tradução em ES na MESMA ordem de prioridade usada pelo
    agente de inglês (home primeiro). Espelha
    test_english_home_page_exists_and_routes_correctly: existência dos
    arquivos, conteúdo real (não placeholder), roteamento (/es não pode
    cair no redirect antigo pra PT) e reciprocidade de hreflang.
    """
    es_html_path = WWW / "es" / "index.html"
    es_py_path = WWW / "es" / "index.py"
    assert es_html_path.exists()
    assert es_py_path.exists()

    es_html = es_html_path.read_text(encoding="utf-8")
    es_py = es_py_path.read_text(encoding="utf-8")
    pt_html = (WWW / "index.html").read_text(encoding="utf-8")
    en_html = (WWW / "en" / "index.html").read_text(encoding="utf-8")

    assert 'lang="es"' in es_html
    assert "Vedium - Cursos de Idiomas Online en Vivo" in es_html
    assert 'hreflang="pt-br" href="https://vediums.com/"' in es_html
    assert 'hreflang="es" href="https://vediums.com/es"' in es_html
    assert 'link rel="canonical" href="https://vediums.com/es"' in es_html

    # Hero traduzido (above-the-fold), CTAs apontam pro teste de inglês
    # (único teste de nível formal que existe hoje -- mesmo padrão do EN)
    assert "Acelera Tu" in es_html
    assert "Haz la prueba de nivel gratis" in es_html
    assert '/teste-de-nivel-ingles" class="thm-btn"' in es_html
    assert "Escríbenos por WhatsApp" in es_html
    assert "wa.me/5511911293075" in es_html

    # Preço em US$, não R$ (público internacional, mesmo padrão do EN)
    assert "US$ 120" in es_html
    assert "R$" not in es_html

    # Teasers do blog apontam pros posts em inglês existentes (ainda não há
    # blog em espanhol) -- não pros slugs em português, que o leitor de
    # espanhol não conseguiria ler.
    assert "/blog/yoruba-language-and-culture" in es_html
    assert "/blog/yoruba-greetings" in es_html
    assert "/blog/yoruba-numbers-1-to-20" in es_html
    assert "/blog/niveis-de-ingles-a1-c1" not in es_html

    # Controller: contexto de idioma pro seletor (site_navbar.html) + mesma
    # lógica de negócio da home em PT/EN (cursos ao vivo do banco, redirect
    # app.vediums.com -> /login)
    assert 'context.lang = "es"' in es_py
    assert 'context.canonical_url = "https://vediums.com/es"' in es_py
    assert 'context.alt_lang_url = "https://vediums.com/"' in es_py
    assert "def get_courses()" in es_py
    assert "app.vediums.com" in es_py
    assert 'redirect_location = "/login"' in es_py

    # PT e EN ganham o hreflang de volta (reciprocidade)
    assert 'hreflang="es" href="https://vediums.com/es"' in pt_html
    assert 'hreflang="es" href="https://vediums.com/es"' in en_html

    # Roteamento: /es não pode cair no redirect antigo pra PT (bug que
    # existiria se a home nova não tivesse sido conectada em hooks.py)
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    assert by_source["/es-ar"] == "/es"
    assert by_source["/es-co"] == "/es"
    assert "/es" not in by_source  # sem self-redirect /es -> /es
    assert "LANGUAGES_WITH_OWN_HOME" in (
        ROOT / "vedium_core" / "vedium_core" / "hooks.py"
    ).read_text(encoding="utf-8")

    # Sitemap lista a home em espanhol
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    assert '{"loc": "/es", "priority"' in sitemap_py


def test_spanish_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang():
    """Páginas do menu principal (catalogo, sobre, como-funciona, faq,
    contato) traduzidas pro espanhol -- mesmo padrão de
    test_english_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang:
    mantêm o MESMO slug sob /es/ (ex. /es/catalogo), registrado em
    SAME_SLUG_TRANSLATIONS.
    """
    menu_slugs = ["catalogo", "sobre", "como-funciona", "faq", "contato"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in menu_slugs:
        es_html_path = WWW / "es" / f"{slug}.html"
        pt_html_path = WWW / f"{slug}.html"
        en_html_path = WWW / "en" / f"{slug}.html"
        assert es_html_path.exists(), f"falta www/es/{slug}.html"
        assert pt_html_path.exists()

        es_html = es_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")
        en_html = en_html_path.read_text(encoding="utf-8")

        assert 'lang="es"' in es_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in es_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in pt_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in en_html

        # SAME_SLUG_TRANSLATIONS ganhou "fr" (test_french_main_menu_pages_...)
        # para os mesmos 5 slugs -- checa que "es" continua presente no set,
        # sem travar o conjunto exato (que agora inclui mais idiomas).
        assert f'"{slug}": {{"en", "es", "fr"}}' in hooks
        assert f'{{"loc": "/es/{slug}"' in sitemap_py

    # catalogo/como-funciona/faq têm controller próprio; contato e sobre não
    # têm .py em nenhum idioma (conteúdo estático) -- não regride o padrão.
    for slug in ["catalogo", "como-funciona", "faq"]:
        es_py_path = WWW / "es" / f"{slug.replace('-', '_')}.py"
        assert es_py_path.exists(), f"falta www/es/{slug.replace('-', '_')}.py"
    assert not (WWW / "es" / "contato.py").exists()
    assert not (WWW / "es" / "sobre.py").exists()

    # Roteamento: /es/catalogo não pode ser interceptado pelo controller PT
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in menu_slugs:
        assert f"/es/{slug}" not in by_source  # sem self-redirect
        assert by_source[f"/es-ar/{slug}"] == f"/es/{slug}"
        assert by_source[f"/es-co/{slug}"] == f"/es/{slug}"

    rules_by_from = {r["from_route"]: r["to_route"] for r in vedium_hooks.LANGUAGE_ROUTE_RULES}
    for slug in menu_slugs:
        assert rules_by_from.get(f"/es/{slug}") is None
        assert rules_by_from.get(f"/es-ar/{slug}") is None

    # Conteúdo real (adaptación editorial, não tradução literal) — CTAs
    # apontam pro teste de nível de inglês (único formal) e pro catálogo em
    # espanhol, não pro PT.
    catalogo_es = (WWW / "es" / "catalogo.html").read_text(encoding="utf-8")
    sobre_es = (WWW / "es" / "sobre.html").read_text(encoding="utf-8")
    como_funciona_es = (WWW / "es" / "como-funciona.html").read_text(encoding="utf-8")
    faq_es = (WWW / "es" / "faq.html").read_text(encoding="utf-8")
    contato_es = (WWW / "es" / "contato.html").read_text(encoding="utf-8")

    assert "/teste-de-nivel-ingles" in como_funciona_es
    assert "/teste-de-nivel-ingles" in faq_es
    assert "/es/catalogo" in sobre_es
    assert "Explora Nuestros Cursos" in catalogo_es
    assert "Enviar Mensaje" in contato_es
    assert "¡Mensaje enviado!" in contato_es


def test_spanish_cta_pages_exist_and_preserve_public_funnel_safety():
    """Páginas de CTA/conversão (planos, matricula, aula-diagnostica)
    traduzidas pro espanhol -- mesmo padrão de
    test_english_cta_pages_exist_and_preserve_public_funnel_safety. Mesmo
    slug sob /es/. Preserva as garantias de segurança do funil público já
    testadas em PT/EN: sem alteração de checkout.
    """
    cta_slugs = ["planos", "matricula", "aula-diagnostica"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in cta_slugs:
        es_html_path = WWW / "es" / f"{slug}.html"
        es_py_path = WWW / "es" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert es_html_path.exists(), f"falta www/es/{slug}.html"
        assert es_py_path.exists(), f"falta www/es/{slug.replace('-', '_')}.py"

        es_html = es_html_path.read_text(encoding="utf-8")
        es_py = es_py_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")

        assert 'lang="es"' in es_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in pt_html
        # SAME_SLUG_TRANSLATIONS ganhou "fr" (test_french_cta_pages_...)
        # para esses mesmos 3 slugs -- checa que "es" continua no set.
        assert f'"{slug}": {{"en", "es", "fr"}}' in hooks
        assert f'{{"loc": "/es/{slug}"' in sitemap_py

        if slug != "matricula":
            assert "stripe" not in es_html.lower()
        assert "create_checkout" not in es_html
        assert 'context.lang = "es"' in es_py
        assert f'context.canonical_url = "https://vediums.com/es/{slug}"' in es_py

    # planos: CTA final aponta pro teste de nivel em ingles e pro
    # matricula/catalogo em espanhol, nao pros equivalentes em PT.
    planos_es = (WWW / "es" / "planos.html").read_text(encoding="utf-8")
    assert "/teste-de-nivel-ingles" in planos_es
    assert "/es/matricula" in planos_es
    assert "/es/catalogo" in planos_es
    assert "Elegir el plan ligero" in planos_es
    assert "Elegir el plan recomendado" in planos_es
    assert "Elegir el plan intensivo" in planos_es
    assert "wa.me/5511911293075" in planos_es

    # matricula: dropdown com valores de curso intactos (slugs de banco,
    # nunca traduzidos), so os LABELS mudam pro espanhol.
    matricula_es = (WWW / "es" / "matricula.html").read_text(encoding="utf-8")
    assert 'value="ingl-s-beginner"' in matricula_es
    assert 'value="iorub-b-sico"' in matricula_es
    assert "Continuar en la plataforma" in matricula_es
    assert "app.vediums.com/lms/courses/" in matricula_es
    assert "source=public_funnel" in matricula_es
    assert "enrollment_intent_click" in matricula_es
    assert "/api/method" not in matricula_es

    # aula-diagnostica: pre-agendamento nao cria reserva automatica.
    diagnostica_es = (WWW / "es" / "aula-diagnostica.html").read_text(encoding="utf-8")
    assert "diagnostic_schedule_click" in diagnostica_es
    assert "diagnostic_slot_click" in diagnostica_es
    assert "get_available_diagnostic_slots" in diagnostica_es
    assert 'data-vd-diagnostic="english"' in diagnostica_es
    assert 'data-vd-diagnostic="portuguese_foreigners"' in diagnostica_es
    assert 'data-vd-diagnostic="yoruba"' in diagnostica_es
    assert "no crea una reserva automática, matrícula, cargo o cambio de plan" in diagnostica_es
    assert "vedium_core.public_funnel.get_available_diagnostic_slots" in diagnostica_es

    # Roteamento: sem self-redirect, es-ar cai na traducao real
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in cta_slugs:
        assert f"/es/{slug}" not in by_source
        assert by_source[f"/es-ar/{slug}"] == f"/es/{slug}"


def test_spanish_institutional_pages_exist_with_reciprocal_hreflang():
    """Páginas institucionais restantes (certificado, comunidade,
    programa-de-indicacao, empresas, carreiras) traduzidas pro espanhol --
    mesmo padrão de test_english_institutional_pages_exist_with_reciprocal_hreflang.
    """
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    # certificado + programa-de-indicacao: página própria, com hreflang direto
    for slug in ["certificado", "programa-de-indicacao"]:
        es_html_path = WWW / "es" / f"{slug}.html"
        es_py_path = WWW / "es" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert es_html_path.exists(), f"falta www/es/{slug}.html"
        assert es_py_path.exists(), f"falta www/es/{slug.replace('-', '_')}.py"
        es_html = es_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")
        assert 'lang="es"' in es_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in pt_html
        assert f'"{slug}": {{"en", "es"}}' in hooks
        assert f'{{"loc": "/es/{slug}"' in sitemap_py

    # comunidade + empresas: template compartilhado public_intent_page(_es).html
    template_es = (TPL / "public_intent_page_es.html").read_text(encoding="utf-8")
    template_pt = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "page_has_es_translation" in template_pt
    assert 'hreflang="es" href="https://vediums.com/es/{{ page_slug }}"' in template_pt
    assert "vedium_core.public_funnel.submit_public_intent" in template_es
    assert "/teste-de-nivel-ingles" in template_es
    assert "wa.me/5511911293075" in template_es
    for slug, intent in {"comunidade": "community", "empresas": "b2b"}.items():
        es_html_path = WWW / "es" / f"{slug}.html"
        es_py_path = WWW / "es" / f"{slug.replace('-', '_')}.py"
        pt_html = (WWW / f"{slug}.html").read_text(encoding="utf-8")
        assert es_html_path.exists()
        assert es_py_path.exists()
        es_html = es_html_path.read_text(encoding="utf-8")
        es_py = es_py_path.read_text(encoding="utf-8")
        assert f'page_slug = "{slug}"' in es_html
        assert f'page_intent = "{intent}"' in es_html
        assert 'public_intent_page_es.html' in es_html
        assert "page_has_es_translation = true" in pt_html
        assert "get_context" in es_py
        assert f'"{slug}": {{"en", "es"}}' in hooks
        assert f'{{"loc": "/es/{slug}"' in sitemap_py

    # carreiras: web.html generico, sem hreflang (mesma limitacao do PT/EN)
    assert (WWW / "es" / "carreiras.html").exists()
    assert (WWW / "es" / "carreiras.py").exists()
    carreiras_es = (WWW / "es" / "carreiras.html").read_text(encoding="utf-8")
    carreiras_es_py = (WWW / "es" / "carreiras.py").read_text(encoding="utf-8")
    assert "Profesor de Inglés" in carreiras_es_py
    assert "Enviar postulación" in carreiras_es
    assert "vedium_core.careers.submit_candidatura" in carreiras_es
    assert 'context.canonical_url = "https://vediums.com/es/carreiras"' in carreiras_es_py
    assert '"carreiras": {"en", "es"}' in hooks
    assert '{"loc": "/es/carreiras"' in sitemap_py

    # Roteamento: sem self-redirect, es-ar cai na traducao real
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in ["certificado", "comunidade", "programa-de-indicacao", "empresas", "carreiras"]:
        assert f"/es/{slug}" not in by_source
        assert by_source[f"/es-ar/{slug}"] == f"/es/{slug}"


def test_french_home_page_exists_and_routes_correctly():
    """Home (/) traduzida pro francês (www/fr/index.html) — 3º idioma do
    rollout sequencial (en -> es -> fr -> de -> ru -> zh). Espelha
    test_spanish_home_page_exists_and_routes_correctly: existência dos
    arquivos, conteúdo real (não placeholder), roteamento (/fr não pode
    cair no redirect antigo pra PT) e reciprocidade de hreflang.
    """
    fr_html_path = WWW / "fr" / "index.html"
    fr_py_path = WWW / "fr" / "index.py"
    assert fr_html_path.exists()
    assert fr_py_path.exists()

    fr_html = fr_html_path.read_text(encoding="utf-8")
    fr_py = fr_py_path.read_text(encoding="utf-8")
    pt_html = (WWW / "index.html").read_text(encoding="utf-8")
    en_html = (WWW / "en" / "index.html").read_text(encoding="utf-8")
    es_html = (WWW / "es" / "index.html").read_text(encoding="utf-8")

    assert 'lang="fr"' in fr_html
    assert "Vedium - Cours de Langues en Ligne en Direct" in fr_html
    assert 'hreflang="pt-br" href="https://vediums.com/"' in fr_html
    assert 'hreflang="fr" href="https://vediums.com/fr"' in fr_html
    assert 'link rel="canonical" href="https://vediums.com/fr"' in fr_html

    # Hero traduzido (above-the-fold), CTAs apontam pro teste de inglês
    # (único teste de nível formal que existe hoje -- mesmo padrão do EN/ES)
    assert "Accélérez Votre" in fr_html
    assert "Faites le test de niveau gratuit" in fr_html
    assert '/teste-de-nivel-ingles" class="thm-btn"' in fr_html
    assert "Écrivez-nous sur WhatsApp" in fr_html
    assert "wa.me/5511911293075" in fr_html

    # Preço em EUR, não R$ nem US$ (público francofalante, adaptação própria
    # do agente de francês -- mesmo espírito do padrão EN/ES)
    assert "110 €" in fr_html
    assert "R$" not in fr_html
    assert "US$" not in fr_html

    # Teasers do blog apontam pros posts em inglês existentes (ainda não há
    # blog em francês) -- não pros slugs em português, que o leitor de
    # francês não conseguiria ler.
    assert "/blog/yoruba-language-and-culture" in fr_html
    assert "/blog/yoruba-greetings" in fr_html
    assert "/blog/yoruba-numbers-1-to-20" in fr_html
    assert "/blog/niveis-de-ingles-a1-c1" not in fr_html

    # Controller: contexto de idioma pro seletor (site_navbar.html) + mesma
    # lógica de negócio da home em PT/EN/ES (cursos ao vivo do banco,
    # redirect app.vediums.com -> /login)
    assert 'context.lang = "fr"' in fr_py
    assert 'context.canonical_url = "https://vediums.com/fr"' in fr_py
    assert 'context.alt_lang_url = "https://vediums.com/"' in fr_py
    assert "def get_courses()" in fr_py
    assert "app.vediums.com" in fr_py
    assert 'redirect_location = "/login"' in fr_py

    # PT, EN e ES ganham o hreflang de volta (reciprocidade)
    assert 'hreflang="fr" href="https://vediums.com/fr"' in pt_html
    assert 'hreflang="fr" href="https://vediums.com/fr"' in en_html
    assert 'hreflang="fr" href="https://vediums.com/fr"' in es_html

    # Roteamento: /fr não pode cair no redirect antigo pra PT (bug que
    # existiria se a home nova não tivesse sido conectada em hooks.py)
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    assert by_source["/fr-ca"] == "/fr"
    assert "/fr" not in by_source  # sem self-redirect /fr -> /fr
    assert "LANGUAGES_WITH_OWN_HOME" in (
        ROOT / "vedium_core" / "vedium_core" / "hooks.py"
    ).read_text(encoding="utf-8")

    # Menu principal traduzido (rótulos, ver site_navbar.html vd_menu_i18n)
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    assert '"fr": {"home"' in navbar

    # Sitemap lista a home em francês
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    assert '{"loc": "/fr", "priority"' in sitemap_py


def test_french_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang():
    """Páginas do menu principal (catalogo, sobre, como-funciona, faq,
    contato) traduzidas pro francês -- mesmo padrão de
    test_spanish_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang:
    mantêm o MESMO slug sob /fr/ (ex. /fr/catalogo), registrado em
    SAME_SLUG_TRANSLATIONS.
    """
    menu_slugs = ["catalogo", "sobre", "como-funciona", "faq", "contato"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in menu_slugs:
        fr_html_path = WWW / "fr" / f"{slug}.html"
        pt_html_path = WWW / f"{slug}.html"
        en_html_path = WWW / "en" / f"{slug}.html"
        es_html_path = WWW / "es" / f"{slug}.html"
        assert fr_html_path.exists(), f"falta www/fr/{slug}.html"
        assert pt_html_path.exists()

        fr_html = fr_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")
        en_html = en_html_path.read_text(encoding="utf-8")
        es_html = es_html_path.read_text(encoding="utf-8")

        assert 'lang="fr"' in fr_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in fr_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in fr_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in pt_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in en_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in es_html

        assert f'"{slug}": {{"en", "es", "fr"}}' in hooks
        assert f'{{"loc": "/fr/{slug}"' in sitemap_py

    # catalogo/como-funciona/faq têm controller próprio; contato e sobre não
    # têm .py em nenhum idioma (conteúdo estático) -- não regride o padrão.
    for slug in ["catalogo", "como-funciona", "faq"]:
        fr_py_path = WWW / "fr" / f"{slug.replace('-', '_')}.py"
        assert fr_py_path.exists(), f"falta www/fr/{slug.replace('-', '_')}.py"
    assert not (WWW / "fr" / "contato.py").exists()
    assert not (WWW / "fr" / "sobre.py").exists()

    # Roteamento: /fr/catalogo não pode ser interceptado pelo controller PT
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in menu_slugs:
        assert f"/fr/{slug}" not in by_source  # sem self-redirect
        assert by_source[f"/fr-ca/{slug}"] == f"/fr/{slug}"

    rules_by_from = {r["from_route"]: r["to_route"] for r in vedium_hooks.LANGUAGE_ROUTE_RULES}
    for slug in menu_slugs:
        assert rules_by_from.get(f"/fr/{slug}") is None
        assert rules_by_from.get(f"/fr-ca/{slug}") is None

    # Conteúdo real (adaptação editorial, não tradução literal) — CTAs
    # apontam pro teste de nível de inglês (único formal) e pro catálogo em
    # francês, não pro PT.
    catalogo_fr = (WWW / "fr" / "catalogo.html").read_text(encoding="utf-8")
    sobre_fr = (WWW / "fr" / "sobre.html").read_text(encoding="utf-8")
    como_funciona_fr = (WWW / "fr" / "como-funciona.html").read_text(encoding="utf-8")
    faq_fr = (WWW / "fr" / "faq.html").read_text(encoding="utf-8")
    contato_fr = (WWW / "fr" / "contato.html").read_text(encoding="utf-8")

    assert "/teste-de-nivel-ingles" in como_funciona_fr
    assert "/teste-de-nivel-ingles" in faq_fr
    assert "/fr/catalogo" in sobre_fr
    assert "Explorez Nos Cours" in catalogo_fr
    assert "Envoyer le Message" in contato_fr
    assert "Message envoyé !" in contato_fr


def test_french_cta_pages_exist_and_preserve_public_funnel_safety():
    """Páginas de CTA/conversão (planos, matricula, aula-diagnostica)
    traduzidas pro francês -- mesmo padrão de
    test_spanish_cta_pages_exist_and_preserve_public_funnel_safety. Mesmo
    slug sob /fr/. Preserva as garantias de segurança do funil público já
    testadas em PT/EN/ES: sem alteração de checkout.
    """
    cta_slugs = ["planos", "matricula", "aula-diagnostica"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in cta_slugs:
        fr_html_path = WWW / "fr" / f"{slug}.html"
        fr_py_path = WWW / "fr" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert fr_html_path.exists(), f"falta www/fr/{slug}.html"
        assert fr_py_path.exists(), f"falta www/fr/{slug.replace('-', '_')}.py"

        fr_html = fr_html_path.read_text(encoding="utf-8")
        fr_py = fr_py_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")

        assert 'lang="fr"' in fr_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in pt_html
        assert f'"{slug}": {{"en", "es", "fr"}}' in hooks
        assert f'{{"loc": "/fr/{slug}"' in sitemap_py

        if slug != "matricula":
            assert "stripe" not in fr_html.lower()
        assert "create_checkout" not in fr_html
        assert 'context.lang = "fr"' in fr_py
        assert f'context.canonical_url = "https://vediums.com/fr/{slug}"' in fr_py

    # planos: CTA final aponta pro teste de nivel em ingles e pro
    # matricula/catalogo em frances, nao pros equivalentes em PT.
    planos_fr = (WWW / "fr" / "planos.html").read_text(encoding="utf-8")
    assert "/teste-de-nivel-ingles" in planos_fr
    assert "/fr/matricula" in planos_fr
    assert "/fr/catalogo" in planos_fr
    assert "Choisir le forfait léger" in planos_fr
    assert "Choisir le forfait recommandé" in planos_fr
    assert "Choisir le forfait intensif" in planos_fr
    assert "wa.me/5511911293075" in planos_fr

    # matricula: dropdown com valores de curso intactos (slugs de banco,
    # nunca traduzidos), so os LABELS mudam pro frances.
    matricula_fr = (WWW / "fr" / "matricula.html").read_text(encoding="utf-8")
    assert 'value="ingl-s-beginner"' in matricula_fr
    assert 'value="iorub-b-sico"' in matricula_fr
    assert "Continuer sur la plateforme" in matricula_fr
    assert "app.vediums.com/lms/courses/" in matricula_fr
    assert "source=public_funnel" in matricula_fr
    assert "enrollment_intent_click" in matricula_fr
    assert "/api/method" not in matricula_fr

    # aula-diagnostica: pre-agendamento nao cria reserva automatica.
    diagnostica_fr = (WWW / "fr" / "aula-diagnostica.html").read_text(encoding="utf-8")
    assert "diagnostic_schedule_click" in diagnostica_fr
    assert "diagnostic_slot_click" in diagnostica_fr
    assert "get_available_diagnostic_slots" in diagnostica_fr
    assert 'data-vd-diagnostic="english"' in diagnostica_fr
    assert 'data-vd-diagnostic="portuguese_foreigners"' in diagnostica_fr
    assert 'data-vd-diagnostic="yoruba"' in diagnostica_fr
    assert "ne crée pas de réservation automatique" in diagnostica_fr
    assert "vedium_core.public_funnel.get_available_diagnostic_slots" in diagnostica_fr

    # Roteamento: sem self-redirect, fr-ca cai na traducao real
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in cta_slugs:
        assert f"/fr/{slug}" not in by_source
        assert by_source[f"/fr-ca/{slug}"] == f"/fr/{slug}"


def test_ple_cluster_has_french_pages_with_reciprocal_hreflang():
    """Cluster PLE (Português para Estrangeiros) traduzido pro francês --
    público francófono pode ter interesse real (diáspora, expatriados,
    profissionais com operação no Brasil), 4a prioridade do
    translator-fr (mesma ordem usada em en/es). Mesmo padrão do cluster
    PLE em espanhol: `alt` com 4 idiomas agora (pt-BR, en, es, fr), slugs
    pesquisados como um francófono buscaria. Diferente do padrão ES: o
    francês GANHOU sua própria página de teste de nível
    (/fr/test-de-niveau-de-portugais), então test_url aponta pra ela, não
    pro teste em inglês.
    """
    pairs = [
        ("portugues-para-estrangeiros", "portugais-pour-etrangers"),
        ("portugues-para-executivos", "portugais-pour-cadres"),
        ("preparatorio-celpe-bras", "preparation-examen-celpe-bras"),
    ]
    expected_test_url = "/fr/test-de-niveau-de-portugais"
    for pt_slug, fr_slug in pairs:
        assert LANDINGS[pt_slug]["alt"]["fr"] == fr_slug
        assert LANDINGS[fr_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[fr_slug]["alt"]["en"] == LANDINGS[pt_slug]["alt"]["en"]
        assert LANDINGS[fr_slug]["alt"]["es"] == LANDINGS[pt_slug]["alt"]["es"]
        assert LANDINGS[fr_slug]["alt"]["fr"] == fr_slug
        assert LANDINGS[fr_slug]["lang"] == "fr"
        assert "test_url" in LANDINGS[fr_slug], f"{fr_slug} precisa de test_url explícito"
        assert LANDINGS[fr_slug]["test_url"] == expected_test_url

        fr_html = (WWW / "fr" / f"{fr_slug}.html").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{fr_slug}")' in fr_html

        # conteúdo real, não placeholder (mesma paridade de profundidade
        # exigida do cluster PT/EN/ES)
        landing = LANDINGS[fr_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/fr/{fr_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # portugais-pour-etrangers é a landing pilar em FR: precisa do mesmo
    # grid de cursos reais (preço, aulas, link) que os outros pilares já têm.
    assert '"portugais-pour-etrangers": {"category_exact": "Português para Estrangeiros"}' in (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")

    # Página de teste de nível em francês: existência, roteamento (via
    # hooks._build_language_prefix_redirects -> pt_to_lang_slug) e
    # reciprocidade de hreflang com PT/EN/ES.
    test_html_path = WWW / "fr" / "test-de-niveau-de-portugais.html"
    test_py_path = WWW / "fr" / "test_de_niveau_de_portugais.py"
    assert test_html_path.exists()
    assert test_py_path.exists()

    test_html = test_html_path.read_text(encoding="utf-8")
    assert 'lang="fr"' in test_html
    assert 'hreflang="pt-br" href="https://vediums.com/teste-de-nivel"' in test_html
    assert 'hreflang="en" href="https://vediums.com/en/portuguese-placement-test"' in test_html
    assert 'hreflang="es" href="https://vediums.com/es/prueba-de-nivel-de-portugues"' in test_html
    assert 'hreflang="fr" href="https://vediums.com/fr/test-de-niveau-de-portugais"' in test_html

    # As perguntas de múltipla escolha continuam em português (o idioma
    # avaliado nunca muda) -- só as instruções ao redor mudam pra francês.
    assert "O supermercado fica _ lado da farmácia." in test_html
    assert "Découvrez votre niveau de portugais du Brésil" in test_html
    assert "Voir mon résultat CECR" in test_html

    # Reciprocidade nos 3 idiomas existentes
    pt_test_html = (WWW / "teste-de-nivel.html").read_text(encoding="utf-8")
    en_test_html = (WWW / "en" / "portuguese-placement-test.html").read_text(encoding="utf-8")
    es_test_html = (WWW / "es" / "prueba-de-nivel-de-portugues.html").read_text(encoding="utf-8")
    assert 'hreflang="fr" href="https://vediums.com/fr/test-de-niveau-de-portugais"' in pt_test_html
    assert 'hreflang="fr" href="https://vediums.com/fr/test-de-niveau-de-portugais"' in en_test_html
    assert 'hreflang="fr" href="https://vediums.com/fr/test-de-niveau-de-portugais"' in es_test_html

    # Roteamento: /fr/teste-de-nivel redireciona pra tradução real, sem
    # self-redirect, fr-ca cai na tradução também.
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    assert by_source["/fr/teste-de-nivel"] == "/fr/test-de-niveau-de-portugais"
    assert by_source["/fr-ca/teste-de-nivel"] == "/fr/test-de-niveau-de-portugais"

    assert '{"loc": "/fr/test-de-niveau-de-portugais"' in (
        ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
    ).read_text(encoding="utf-8")


def test_english_cluster_has_french_pages_with_reciprocal_hreflang():
    """Cluster de Inglês (pilar cours-anglais-en-ligne-en-direct + 5
    sub-páginas) traduzido pro francês -- 5a prioridade do translator-fr
    (mesma ordem usada em en/es): francófonos que querem aprender inglês
    com a Vedium, adaptado pro público francofalante. Mesmo padrão de
    test_english_cluster_has_spanish_pages_with_reciprocal_hreflang: slug
    em francês pensado como um francófono buscaria (não tradução literal
    do português nem do inglês), `alt` recíproco nos 4 idiomas, paridade
    de profundidade de conteúdo.
    """
    pairs = [
        ("curso-de-ingles-online", "cours-anglais-en-ligne-en-direct", "/teste-de-nivel-ingles"),
        ("ingles-para-entrevista", "anglais-entretien-embauche", None),
        ("ingles-para-programadores", "anglais-developpeurs-informatique", None),
        ("ingles-executivo", "anglais-des-affaires", None),
        ("ingles-para-viagens", "anglais-pour-voyager", None),
        ("ingles-para-atendimento-ao-cliente", "anglais-service-client", None),
    ]
    for pt_slug, fr_slug, expected_test_url in pairs:
        assert LANDINGS[pt_slug]["alt"]["fr"] == fr_slug
        assert LANDINGS[fr_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[fr_slug]["alt"]["en"] == LANDINGS[pt_slug]["alt"]["en"]
        assert LANDINGS[fr_slug]["alt"]["es"] == LANDINGS[pt_slug]["alt"]["es"]
        assert LANDINGS[fr_slug]["alt"]["fr"] == fr_slug
        assert LANDINGS[fr_slug]["lang"] == "fr"
        if expected_test_url:
            assert "test_url" in LANDINGS[fr_slug], f"{fr_slug} precisa de test_url explícito"
            assert LANDINGS[fr_slug]["test_url"] == expected_test_url

        fr_html = (WWW / "fr" / f"{fr_slug}.html").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{fr_slug}")' in fr_html

        # conteúdo real, não placeholder (mesma paridade de profundidade
        # exigida do cluster PT/EN/ES)
        landing = LANDINGS[fr_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/fr/{fr_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # cours-anglais-en-ligne-en-direct é a landing pilar em FR: precisa do
    # mesmo grid de cursos reais (preço, aulas, link) que os outros
    # pilares já têm, e preço em EUR (não R$ nem US$).
    assert '"cours-anglais-en-ligne-en-direct": {"category_prefix": "Inglês"}' in (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")
    pilar = LANDINGS["cours-anglais-en-ligne-en-direct"]
    assert "€" in pilar["price_display"]
    assert "R$" not in pilar["price_display"]
    assert "US$" not in pilar["price_display"]
