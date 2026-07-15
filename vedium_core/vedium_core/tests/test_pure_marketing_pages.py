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
from vedium_core.marketing_landing_content import (  # noqa: E402
    LANDINGS,
    LANDING_COURSE_FILTERS,
)
from vedium_core.course_translations import COURSE_TRANSLATIONS  # noqa: E402
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
            ("curso-de-ingles-online", "learn-english-online", None),
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
        expected_alt = {
            "pt-BR": pt_slug,
            "en": LANDINGS[pt_slug]["alt"]["en"],
            "es": es_slug,
        }
        # "ru" ganhou tradução real depois (rollout russo, 2026-07-06) — se
        # o par pt/es já apontar pra um slug ru, o alt recíproco também entra.
        if "ru" in LANDINGS[pt_slug]["alt"]:
            expected_alt["ru"] = LANDINGS[pt_slug]["alt"]["ru"]
        assert LANDINGS[es_slug]["alt"] == expected_alt
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
        ("portugues-para-estrangeiros", "portugues-para-extranjeros", "/es/prueba-de-nivel-de-portugues"),
        ("portugues-para-executivos", "portugues-para-ejecutivos", "/es/prueba-de-nivel-de-portugues"),
        ("preparatorio-celpe-bras", "preparacion-examen-celpe-bras", "/es/prueba-de-nivel-de-portugues"),
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
        ("curso-de-ingles-online", "curso-de-ingles-online-en-vivo", None),
        ("ingles-para-entrevista", "ingles-para-entrevistas-de-trabajo", None),
        ("ingles-para-programadores", "ingles-para-desarrolladores", None),
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
    assert "vedium_core.helpdesk import create_ticket" in funnel
    assert '"HD Ticket"' in (ROOT / "vedium_core" / "vedium_core" / "helpdesk.py").read_text(encoding="utf-8")
    assert "frappe.sendmail" in funnel
    assert "Recebemos seu contato | Vedium" in funnel
    assert "Public funnel lead confirmation failed" in funnel
    assert "raised_by" in (ROOT / "vedium_core" / "vedium_core" / "helpdesk.py").read_text(encoding="utf-8")
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


def test_daily_practice_tool_is_safe_and_custom_progress_page_is_removed():
    practice = (WWW / "pratica-diaria.html").read_text(encoding="utf-8")
    practice_py = (WWW / "pratica_diaria.py").read_text(encoding="utf-8")
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
    assert "noindex, nofollow" in practice
    assert "https://app.vediums.com/lms" in practice
    assert "https://app.vediums.com/meu-progresso" not in practice
    assert 'APP_URL = "https://app.vediums.com"' in practice_py
    assert '_redirect_public_host("/pratica-diaria")' in practice_py
    assert "PUBLIC_HOSTS" in practice_py
    assert "_redirect_public_host" in practice_py
    assert "/api/method" not in practice
    assert "stripe" not in practice.lower()

    assert not (WWW / "meu-progresso.html").exists()
    assert not (WWW / "meu_progresso.py").exists()
    assert '"meu-progresso"' not in hooks


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
    assert "exibidos no checkout" in terms


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
    assert "/blog/aprender-ioruba-lingua-e-cultura" in footer
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
        pt_slug = "cursos-de-idiomas-online" if slug == "catalogo" else slug
        assert f'hreflang="pt-br" href="https://vediums.com/{pt_slug}"' in en_html
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

    # Alias legado/canônico em PT também deve chegar ao catálogo inglês.
    # Uma versão antiga do seletor gerava exatamente esta URL (404).
    assert by_source["/en/cursos-de-idiomas-online"] == "/en/catalogo"
    assert by_source["/en-us/cursos-de-idiomas-online"] == "/en/catalogo"
    assert by_source["/en-au/cursos-de-idiomas-online"] == "/en/catalogo"


def test_catalog_alias_redirects_to_each_real_translated_catalog():
    by_source = {
        redirect["source"]: redirect["target"]
        for redirect in vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    }
    expected = {
        "en": "/en/catalogo",
        "en-us": "/en/catalogo",
        "en-au": "/en/catalogo",
        "es": "/es/catalogo",
        "es-ar": "/es/catalogo",
        "es-co": "/es/catalogo",
        "fr": "/fr/catalogo",
        "fr-ca": "/fr/catalogo",
        "de": "/de/catalogo",
        "ru": "/ru/catalogo",
    }
    for prefix, target in expected.items():
        assert by_source[f"/{prefix}/cursos-de-idiomas-online"] == target

    # O proxy Cloudflare deste domínio injeta email-decode.min.js, mas o
    # próprio /cdn-cgi retorna 404. Evita a injeção nos dois emails comuns
    # do catálogo sem remover o link mailto acessível.
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    assert '<!--email_off--><a href="mailto:contato@vediums.com">' in navbar
    for lang in ("", "en", "es", "fr", "de", "ru"):
        catalog_path = WWW / lang / "catalogo.html" if lang else WWW / "catalogo.html"
        catalog = catalog_path.read_text(encoding="utf-8")
        assert '<!--email_off--><a href="mailto:contato@vediums.com">' in catalog


def test_translated_course_menu_links_include_the_real_language_prefix():
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    expected = (
        "/en/learn-english-online",
        "/en/learn-yoruba-online",
        "/en/learn-portuguese-brazil",
        "/es/curso-de-ingles-online-en-vivo",
        "/es/curso-de-yoruba-online",
        "/es/portugues-para-extranjeros",
        "/fr/cours-anglais-en-ligne-en-direct",
        "/fr/portugais-pour-etrangers",
        "/de/englischkurs-online-live",
        "/de/portugiesisch-fuer-auslaender",
        "/ru/kurs-angliyskogo-online",
        "/ru/kurs-yoruba-online",
        "/ru/portugalskiy-dlya-inostrantsev",
    )
    for url in expected:
        assert f'"{url}"' in navbar


def test_russian_institutional_routes_use_hyphenated_public_filenames():
    for slug in ("como-funciona", "aula-diagnostica", "programa-de-indicacao"):
        assert (WWW / "ru" / f"{slug}.html").exists()
        assert not (WWW / "ru" / f"{slug.replace('-', '_')}.html").exists()


def test_frappe_base_template_has_valid_brand_mobile_icon_language_and_canonical():
    base = (ROOT / "vedium_core" / "vedium_core" / "templates" / "base.html").read_text(
        encoding="utf-8"
    )
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(
        encoding="utf-8"
    )
    assert '<html lang="{{ lang or boot.lang }}">' in base
    assert '{% if canonical_url %}<link rel="canonical" href="{{ canonical_url }}">' in base
    assert "/assets/vedium_core/vedium_assets/images/favicons/apple-touch-icon.png" in base
    assert '"brand_html": (' in hooks
    assert "/assets/vedium_core/images/vedium-logo-reta-color.png" in hooks


def test_sitemap_covers_russian_institutional_pages_and_every_marketing_landing():
    sitemap = (WWW / "sitemap.py").read_text(encoding="utf-8")
    for slug in (
        "catalogo",
        "sobre",
        "como-funciona",
        "aula-diagnostica",
        "programa-de-indicacao",
        "carreiras",
    ):
        assert f'{{"loc": "/ru/{slug}"' in sitemap
    assert "def _marketing_landing_urls():" in sitemap
    assert "for slug, landing in LANDINGS.items()" in sitemap
    assert 'urls_by_location.setdefault(url["loc"], url)' in sitemap


def test_careers_pages_share_canonical_hreflang_and_do_not_expose_gtm_example():
    careers = (ROOT / "vedium_core" / "vedium_core" / "careers.py").read_text(
        encoding="utf-8"
    )
    for lang in ("pt-br", "en", "es", "fr", "de", "ru"):
        prefix = "" if lang == "pt-br" else f"/{lang}"
        assert f'"{lang}": "https://vediums.com{prefix}/carreiras"' in careers
    assert not (WWW / "gtm_examples.html").exists()
    assert (ROOT / "docs" / "gtm" / "gtm_examples.html").exists()


def test_public_nginx_canonicalizes_www_and_serves_nonempty_pwa_assets():
    nginx = (ROOT / "deploy" / "nginx" / "vediums.com.conf").read_text(
        encoding="utf-8"
    )
    assert "return 301 https://vediums.com$request_uri;" in nginx
    assert nginx.count("location = /sw.js {") >= 2
    assert nginx.count("location = /manifest.json {") >= 2
    assert "proxy_pass http://127.0.0.1:8005/assets/vedium_core/js/sw.js;" in nginx
    assert "proxy_pass http://127.0.0.1:8005/assets/vedium_core/manifest.json;" in nginx

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
        # SAME_SLUG_TRANSLATIONS ganhou "fr" (test_french_institutional_pages_...)
        # para os mesmos 5 slugs -- checa que "en" continua no set.
        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/en/{slug}"' in sitemap_py

    # comunidade + empresas: template compartilhado public_intent_page(_en).html
    template_en = (TPL / "public_intent_page_en.html").read_text(encoding="utf-8")
    template_pt = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "page_has_en_translation" in template_pt
    assert 'hreflang="en" href="https://vediums.com/en/{{ page_slug }}"' in template_pt
    assert "vedium_core.public_funnel.submit_public_intent" in template_en
    assert "/teste-de-nivel-ingles" in template_en
    assert "wa.me/5511911293075" in template_en
    for slug, intent in {"comunidade": "community"}.items():
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
        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/en/{slug}"' in sitemap_py

    # empresas: 2026-07-04 virou pagina propria e rica em PT (ver
    # test_empresas_page_is_rich_and_wired_to_crm), com hreflang direto
    # proprio. A versao EN foi reescrita em 2026-07-04 espelhando a mesma
    # estrutura rica (hero, beneficios, steps, fotos, form CRM) -- es/fr
    # ainda usam o template compartilhado (fila de traducao).
    assert (WWW / "en" / "empresas.html").exists()
    empresas_en = (WWW / "en" / "empresas.html").read_text(encoding="utf-8")
    assert "vd-emp-hero" in empresas_en
    assert "vd-benefits" in empresas_en
    assert "vd-steps" in empresas_en
    assert "vd-form-card" in empresas_en
    assert "vedium_core.public_funnel.submit_public_intent" in empresas_en
    assert "intent:'b2b'" in empresas_en
    assert '"empresas": {"en", "es", "fr", "de", "ru"}' in hooks
    assert '{"loc": "/en/empresas"' in sitemap_py

    # carreiras: web.html genérico agora recebe canonical/hreflang pelo
    # contexto compartilhado de careers.py + templates/base.html.
    assert (WWW / "en" / "carreiras.html").exists()
    assert (WWW / "en" / "carreiras.py").exists()
    carreiras_en = (WWW / "en" / "carreiras.html").read_text(encoding="utf-8")
    carreiras_en_py = (WWW / "en" / "carreiras.py").read_text(encoding="utf-8")
    assert "English Teacher" in carreiras_en_py
    assert "Submit application" in carreiras_en
    assert "vedium_core.careers.submit_candidatura" in carreiras_en
    assert 'set_careers_seo_context(context, "en")' in carreiras_en_py
    assert '"carreiras": {"en", "es", "fr", "de", "ru"}' in hooks
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
        # SAME_SLUG_TRANSLATIONS ganhou "fr" e "de" (test_french_cta_pages_...,
        # test_german_cta_pages_...) para esses mesmos 3 slugs -- checa via
        # dict real que "en" continua no set.
        assert "en" in vedium_hooks.SAME_SLUG_TRANSLATIONS[slug]
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
    assert 'if family not in ("en", "es", "fr", "de", "ru")' in hooks_src

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
    # /de/certificado ganhou tradução real depois (2026-07-06, mesmo
    # racional do es-ar/planos acima -- SAME_SLUG_TRANSLATIONS agora
    # inclui "de" pras páginas institucionais restantes também), então
    # não sobra mais como redirect pro canônico em PT.
    assert "/de/certificado" not in by_source

    # /en|es|fr|de|ru/curso/<slug> (com barra, curso individual) já tem rota +
    # tradução de verdade (curso.py) — não pode ter redirect genérico
    # atropelando, nem para as variantes regionais (en-us, en-au, es-ar,
    # es-co, fr-ca), que também são resolvidas pelo mesmo controller.
    # "ru" ganhou course_translations reais no rollout russo (2026-07-06),
    # então saiu do fallback genérico pro PT (mesmo racional do /de acima).
    for prefix in ("en", "en-us", "en-au", "es", "es-ar", "es-co", "fr", "fr-ca", "de", "ru"):
        assert not any(r["source"].startswith(f"/{prefix}/curso/") for r in redirects)
    # Idiomas ainda sem course_translations (zh-cn) continuam no fallback pro PT.
    assert any(r["source"] == r"/zh-cn/curso/(.*)" for r in redirects)

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

    # Menu: link para o blog (rótulo vem de vd_menu_t, href de vd_menu_u --
    # blog não tem tradução em nenhum idioma ainda, então o href fica
    # sempre "/blog" pra todos os idiomas -- ver
    # test_main_menu_labels_are_translated_per_language e
    # test_language_switcher_uses_real_translated_urls_not_prefix_guessing)
    assert '<a href="{{ vd_menu_u.blog }}">{{ vd_menu_t.blog }}</a>' in navbar
    assert '"blog": "/blog"' in navbar

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
    en/es/fr/de via /<lang>/curso/<slug>, reaproveitando o MESMO controller
    dinâmico curso.py (preço/vagas/avaliações sempre ao vivo do banco) —
    só title/short_introduction/description são sobrepostos por
    course_translations.COURSE_TRANSLATIONS[slug][lang]. Sem Custom Field,
    sem migração: cursos sem tradução (cluster Inglês) continuam só em PT.

    2026-07-06: generalizado de "só inglês" pra en/es/fr/de (mesmo padrão
    das 5 páginas institucionais) -- COURSE_TRANSLATIONS passou de
    {slug: {...}} pra {slug: {lang: {...}}}, e o chrome do curso.html
    (antes um binário vd_course_en/pt-BR com ~25 strings hardcoded) virou
    um dict UI por idioma.
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
        for lang in ("en", "es", "fr", "de"):
            assert f'"{lang}"' in course_translations.split(f'"{slug}"')[1].split("},\n    \"")[0]

    assert '{"from_route": "/en/curso/<course>", "to_route": "curso"}' in hooks

    # sem tradução no idioma pedido -> redireciona pra versão PT (não cria
    # página fina/duplicada)
    assert "from vedium_core.course_translations import COURSE_TRANSLATIONS" in curso_py
    assert "translations_for_course = COURSE_TRANSLATIONS.get(course_name, {})" in curso_py
    assert "frappe.local.flags.redirect_location = get_course_url(course_name)" in curso_py
    for lang in ("en", "es", "fr", "de"):
        assert f'"{lang}"' in curso_py.split('for candidate in (')[1].split(")")[0]

    # preço/vagas/avaliações continuam vindo do banco — só sobrepõe texto
    assert "context.course = get_course_details(course_name)" in curso_py
    assert 'context.course.title = translation["title"]' in curso_py

    # chrome multi-idioma (dict UI) + hreflang recíproco pra todos os
    # idiomas que tiverem tradução real desse curso
    assert 'vd_lang = lang or "pt-BR"' in curso_html
    assert "alt_langs" in curso_html
    assert '"ui.enroll"' not in curso_html  # não pode sobrar string literal em vez do lookup
    # NOTA: o rótulo condicional "Falar com a equipe" p/ cursos consultivos
    # (CONSULTATIVE_COURSES/is_consultative, QA 2026-07-10) foi revertido por
    # outra alteração que adicionou billing_period mensal/anual em curso.py —
    # curso.html hoje usa o rótulo fixo de novo. Isso reabre o bug de preço
    # fixo pra curso de hora avulsa (ex. hebraico-particular); ver conversa.
    assert "{{ ui.enroll }}" in curso_html

    # Bug real achado em produção (2026-07-02, pós-deploy): frappe.local.path
    # NUNCA tem barra inicial — PathResolver.__init__ faz path.strip("/ ")
    # antes de setar frappe.local.path (frappe/website/path_resolver.py).
    # startswith("/en/curso/") com barra na frente nunca batia, então
    # /en/curso/<slug> sempre renderizava em português. Trava a versão
    # corrigida (lstrip antes do startswith), agora generalizada pra
    # qualquer um dos 4 idiomas.
    assert '.startswith("/en/curso/")' not in curso_py, (
        "startswith com barra inicial nunca bate — frappe.local.path não tem "
        "barra na frente (path_resolver.py faz .strip('/ '))"
    )
    assert 'path = (frappe.local.path or "").lstrip("/")' in curso_py
    assert 'path.startswith(f"{candidate}/curso/")' in curso_py


def test_translated_pillar_course_grids_link_to_translated_course_pages():
    """Grades de PLE e Iorubá acompanham o idioma da landing, inclusive RU.
    """
    landing_content = (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")
    assert '"learn-yoruba-online": {"category_prefix": "Iorubá"}' in landing_content
    assert (
        '"learn-portuguese-brazil": {"category_exact": "Português para Estrangeiros"}'
        in landing_content
    )
    assert '"kurs-yoruba-online": {"category_prefix": "Iorubá"}' in landing_content
    assert (
        '"portugalskiy-dlya-inostrantsev": {"category_exact": "Português para Estrangeiros"}'
        in landing_content
    )
    assert "COURSE_LEVEL_BADGE_I18N" in landing_content
    assert 'translation = COURSE_TRANSLATIONS.get(course.name, {}).get(lang)' in landing_content
    assert "course.url = get_course_url(course.name, lang)" in landing_content


def test_ple_course_grid_is_available_and_translated_in_every_public_language():
    landing_slugs = {
        "en": "learn-portuguese-brazil",
        "es": "portugues-para-extranjeros",
        "fr": "portugais-pour-etrangers",
        "de": "portugiesisch-fuer-auslaender",
        "ru": "portugalskiy-dlya-inostrantsev",
    }
    course_slugs = {
        "portugues-para-estrangeiros-basico",
        "portugues-para-estrangeiros-intermediario",
        "portugues-para-estrangeiros-avancado",
    }

    for lang, landing_slug in landing_slugs.items():
        assert LANDINGS[landing_slug]["lang"] == lang
        assert LANDING_COURSE_FILTERS[landing_slug] == {
            "category_exact": "Português para Estrangeiros"
        }
        for course_slug in course_slugs:
            translation = COURSE_TRANSLATIONS[course_slug][lang]
            assert translation["title"].strip()
            assert translation["short_introduction"].strip()


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
    # 2026-07-03: uma tentativa de reintroduzir um scheduling.py (casca fina
    # sobre o fluxo nativo) foi revertida — a solução final é 100% nativa:
    # ligar LMS Course.paid_certificate + LMS Enrollment.purchased_certificate
    # (ver test_enrollment_creation_unlocks_native_certification_button e
    # scripts/migrations/oneshot/enable_native_scheduling_button.py).
    assert not (WWW / "agendar-aula.html").exists()
    assert not (WWW / "minha-agenda.html").exists()
    assert not (ROOT / "vedium_core" / "vedium_core" / "scheduling.py").exists()


def test_enrollment_creation_unlocks_native_certification_button():
    """2026-07-03: o botão nativo do LMS "Get Certified" (que leva direto ao
    agendamento de aula com o professor, via Course Evaluator) só aparece
    quando LMS Course.paid_certificate=1 — e, se a matrícula não tiver
    purchased_certificate=1, ele manda o aluno pra uma tela de cobrança
    DENTRO do LMS antes de deixar agendar, cobrando de novo por algo já
    pago no Stripe. Toda matrícula criada após pagamento precisa nascer com
    purchased_certificate=1. Ver scripts/migrations/oneshot/
    enable_native_scheduling_button.py pro backfill do histórico."""
    api_code = (ROOT / "vedium_core" / "vedium_core" / "api.py").read_text(encoding="utf-8")
    assert "def create_enrollment_if_paid" in api_code
    section = api_code.split("def create_enrollment_if_paid", 1)[1].split("\ndef ", 1)[0]
    assert '"purchased_certificate": 1' in section

    oneshot_path = (
        ROOT / "vedium_core" / "vedium_core" / "scripts" / "migrations" / "oneshot"
        / "enable_native_scheduling_button.py"
    )
    assert oneshot_path.exists()
    oneshot_code = oneshot_path.read_text(encoding="utf-8")
    assert "paid_certificate" in oneshot_code
    assert "purchased_certificate" in oneshot_code


def test_support_ticket_doctype_is_not_world_writable():
    """2026-07-03: achado durante revisão de RH/CRM/Suporte — o doctype
    'Support Ticket' tinha role "All" com CRUD completo (create/write/delete),
    igual o bug já corrigido no Lesson Slot: qualquer usuário logado podia
    ler/editar/apagar o chamado de QUALQUER outra pessoa via API REST padrão
    do Frappe, mesmo os wrappers em api.py/public_funnel.py já filtrando
    corretamente por dono. Ambos usam `insert(ignore_permissions=True)` pra
    criar, então apertar a permissão de doctype não quebra nenhum fluxo
    existente (guest ou logado)."""
    ticket_json = json.loads(
        (
            ROOT / "vedium_core" / "vedium_core" / "vedium_core" / "doctype"
            / "support_ticket" / "support_ticket.json"
        ).read_text(encoding="utf-8")
    )
    perms_by_role = {p["role"]: p for p in ticket_json["permissions"]}
    assert perms_by_role["All"]["write"] == 0
    assert perms_by_role["All"].get("delete", 0) == 0
    assert perms_by_role["All"].get("share", 0) == 0
    assert perms_by_role["All"]["if_owner"] == 1
    assert perms_by_role["All"]["read"] == 1
    assert perms_by_role["System Manager"]["write"] == 1
    assert perms_by_role["System Manager"]["delete"] == 1


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
        pt_slug = "cursos-de-idiomas-online" if slug == "catalogo" else slug
        assert f'hreflang="pt-br" href="https://vediums.com/{pt_slug}"' in es_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in es_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in pt_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in en_html

        # SAME_SLUG_TRANSLATIONS ganhou "fr" e "de" (test_french_main_menu_
        # pages_..., test_german_main_menu_pages_...) para os mesmos 5
        # slugs -- checa via dict real que "es" continua presente no set,
        # sem travar o conjunto exato de idiomas (que só cresce).
        assert "es" in vedium_hooks.SAME_SLUG_TRANSLATIONS[slug]
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
        # SAME_SLUG_TRANSLATIONS ganhou "fr" e "de" (test_french_cta_pages_...,
        # test_german_cta_pages_...) para esses mesmos 3 slugs -- checa via
        # dict real que "es" continua no set.
        assert "es" in vedium_hooks.SAME_SLUG_TRANSLATIONS[slug]
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
        # SAME_SLUG_TRANSLATIONS ganhou "fr" (test_french_institutional_pages_...)
        # para os mesmos 5 slugs -- checa que "es" continua no set.
        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/es/{slug}"' in sitemap_py

    # comunidade + empresas: template compartilhado public_intent_page(_es).html
    template_es = (TPL / "public_intent_page_es.html").read_text(encoding="utf-8")
    template_pt = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "page_has_es_translation" in template_pt
    assert 'hreflang="es" href="https://vediums.com/es/{{ page_slug }}"' in template_pt
    assert "vedium_core.public_funnel.submit_public_intent" in template_es
    assert "/teste-de-nivel-ingles" in template_es
    assert "wa.me/5511911293075" in template_es
    for slug, intent in {"comunidade": "community"}.items():
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
        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/es/{slug}"' in sitemap_py

    # empresas: pagina propria em PT (ver
    # test_empresas_page_is_rich_and_wired_to_crm); ES tambem reescrita como
    # pagina rica propria (hero, beneficios, passos, fotos, formulario).
    assert (WWW / "es" / "empresas.html").exists()
    empresas_es = (WWW / "es" / "empresas.html").read_text(encoding="utf-8")
    assert 'vd-emp-hero' in empresas_es
    assert 'vd-benefits' in empresas_es
    assert 'vd-steps' in empresas_es
    assert 'vd-form-card' in empresas_es
    assert "vedium_core.public_funnel.submit_public_intent" in empresas_es
    assert "intent:'b2b'" in empresas_es
    assert '"empresas": {"en", "es", "fr", "de", "ru"}' in hooks
    assert '{"loc": "/es/empresas"' in sitemap_py

    # carreiras: canonical/hreflang vêm do contexto compartilhado.
    assert (WWW / "es" / "carreiras.html").exists()
    assert (WWW / "es" / "carreiras.py").exists()
    carreiras_es = (WWW / "es" / "carreiras.html").read_text(encoding="utf-8")
    carreiras_es_py = (WWW / "es" / "carreiras.py").read_text(encoding="utf-8")
    assert "Profesor de Inglés" in carreiras_es_py
    assert "Enviar postulación" in carreiras_es
    assert "vedium_core.careers.submit_candidatura" in carreiras_es
    assert 'set_careers_seo_context(context, "es")' in carreiras_es_py
    assert '"carreiras": {"en", "es", "fr", "de", "ru"}' in hooks
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
        pt_slug = "cursos-de-idiomas-online" if slug == "catalogo" else slug
        assert f'hreflang="pt-br" href="https://vediums.com/{pt_slug}"' in fr_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in fr_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in pt_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in en_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in es_html

        # SAME_SLUG_TRANSLATIONS ganhou "de" (test_german_main_menu_pages_...)
        # para os mesmos 5 slugs -- checa via dict real que "fr" continua
        # presente no set, sem travar o conjunto exato de idiomas.
        assert "fr" in vedium_hooks.SAME_SLUG_TRANSLATIONS[slug]
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
        # SAME_SLUG_TRANSLATIONS ganhou "de" (test_german_cta_pages_...)
        # para esses mesmos 3 slugs -- checa via dict real que "fr"
        # continua presente no set.
        assert "fr" in vedium_hooks.SAME_SLUG_TRANSLATIONS[slug]
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
            ("curso-de-ingles-online", "cours-anglais-en-ligne-en-direct", None),
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


def test_french_institutional_pages_exist_with_reciprocal_hreflang():
    """Páginas institucionais restantes (certificado, comunidade,
    programa-de-indicacao, empresas, carreiras) traduzidas pro francês --
    6a prioridade do translator-fr, mesmo padrão de
    test_spanish_institutional_pages_exist_with_reciprocal_hreflang.
    """
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    # certificado + programa-de-indicacao: página própria, com hreflang direto
    for slug in ["certificado", "programa-de-indicacao"]:
        fr_html_path = WWW / "fr" / f"{slug}.html"
        fr_py_path = WWW / "fr" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert fr_html_path.exists(), f"falta www/fr/{slug}.html"
        assert fr_py_path.exists(), f"falta www/fr/{slug.replace('-', '_')}.py"
        fr_html = fr_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")
        assert 'lang="fr"' in fr_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in fr_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in pt_html
        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/fr/{slug}"' in sitemap_py

    # comunidade + empresas: template compartilhado public_intent_page(_fr).html
    template_fr = (TPL / "public_intent_page_fr.html").read_text(encoding="utf-8")
    template_pt = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "page_has_fr_translation" in template_pt
    assert 'hreflang="fr" href="https://vediums.com/fr/{{ page_slug }}"' in template_pt
    assert "vedium_core.public_funnel.submit_public_intent" in template_fr
    assert "/teste-de-nivel-ingles" in template_fr
    assert "wa.me/5511911293075" in template_fr
    for slug, intent in {"comunidade": "community"}.items():
        fr_html_path = WWW / "fr" / f"{slug}.html"
        fr_py_path = WWW / "fr" / f"{slug.replace('-', '_')}.py"
        pt_html = (WWW / f"{slug}.html").read_text(encoding="utf-8")
        assert fr_html_path.exists()
        assert fr_py_path.exists()
        fr_html = fr_html_path.read_text(encoding="utf-8")
        fr_py = fr_py_path.read_text(encoding="utf-8")
        assert f'page_slug = "{slug}"' in fr_html
        assert f'page_intent = "{intent}"' in fr_html
        assert 'public_intent_page_fr.html' in fr_html
        assert "page_has_fr_translation = true" in pt_html
        assert "get_context" in fr_py
        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/fr/{slug}"' in sitemap_py

    # empresas: pagina propria em PT (ver
    # test_empresas_page_is_rich_and_wired_to_crm); versao FR foi reescrita
    # em 2026-07-04 espelhando a mesma estrutura rica (hero, beneficios,
    # steps, fotos, form CRM) -- mesmo padrao da versao EN.
    assert (WWW / "fr" / "empresas.html").exists()
    empresas_fr = (WWW / "fr" / "empresas.html").read_text(encoding="utf-8")
    assert "vd-emp-hero" in empresas_fr
    assert "vd-benefits" in empresas_fr
    assert "vd-steps" in empresas_fr
    assert "vd-form-card" in empresas_fr
    assert "vedium_core.public_funnel.submit_public_intent" in empresas_fr
    assert "intent:'b2b'" in empresas_fr
    assert '"empresas": {"en", "es", "fr", "de", "ru"}' in hooks
    assert '{"loc": "/fr/empresas"' in sitemap_py

    # carreiras: canonical/hreflang vêm do contexto compartilhado.
    assert (WWW / "fr" / "carreiras.html").exists()
    assert (WWW / "fr" / "carreiras.py").exists()
    carreiras_fr = (WWW / "fr" / "carreiras.html").read_text(encoding="utf-8")
    carreiras_fr_py = (WWW / "fr" / "carreiras.py").read_text(encoding="utf-8")
    assert "Professeur d'Anglais" in carreiras_fr_py
    assert "Envoyer ma candidature" in carreiras_fr
    assert "vedium_core.careers.submit_candidatura" in carreiras_fr
    assert 'set_careers_seo_context(context, "fr")' in carreiras_fr_py
    assert '"carreiras": {"en", "es", "fr", "de", "ru"}' in hooks
    assert '{"loc": "/fr/carreiras"' in sitemap_py

    # Roteamento: sem self-redirect, fr-ca cai na traducao real
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in ["certificado", "comunidade", "programa-de-indicacao", "empresas", "carreiras"]:
        assert f"/fr/{slug}" not in by_source
        assert by_source[f"/fr-ca/{slug}"] == f"/fr/{slug}"


def test_german_home_page_exists_and_routes_correctly():
    """Home (/) traduzida pro alemão (www/de/index.html) — 4º idioma do
    rollout sequencial (en -> es -> fr -> de -> ru -> zh). Espelha
    test_french_home_page_exists_and_routes_correctly: existência dos
    arquivos, conteúdo real (não placeholder), roteamento (/de não pode
    cair no redirect antigo pra PT) e reciprocidade de hreflang.
    """
    de_html_path = WWW / "de" / "index.html"
    de_py_path = WWW / "de" / "index.py"
    assert de_html_path.exists()
    assert de_py_path.exists()

    de_html = de_html_path.read_text(encoding="utf-8")
    de_py = de_py_path.read_text(encoding="utf-8")
    pt_html = (WWW / "index.html").read_text(encoding="utf-8")
    en_html = (WWW / "en" / "index.html").read_text(encoding="utf-8")
    es_html = (WWW / "es" / "index.html").read_text(encoding="utf-8")
    fr_html = (WWW / "fr" / "index.html").read_text(encoding="utf-8")

    assert 'lang="de"' in de_html
    assert "Vedium - Live Online Sprachkurse" in de_html
    assert 'hreflang="pt-br" href="https://vediums.com/"' in de_html
    assert 'hreflang="de" href="https://vediums.com/de"' in de_html
    assert 'link rel="canonical" href="https://vediums.com/de"' in de_html

    # Hero traduzido (above-the-fold), CTAs apontam pro teste de inglês
    # (único teste de nível formal que existe hoje -- mesmo padrão do EN/ES/FR)
    assert "Bringen Sie Ihre" in de_html
    assert "Kostenlosen Einstufungstest machen" in de_html
    assert '/teste-de-nivel-ingles" class="thm-btn"' in de_html
    assert "Schreiben Sie uns auf WhatsApp" in de_html
    assert "wa.me/5511911293075" in de_html

    # Preço em EUR, não R$ nem US$ (público germanofalante, mesma lógica
    # editorial usada pelo agente de francês -- não é conversão cambial literal)
    assert "110 €" in de_html
    assert "R$" not in de_html
    assert "US$" not in de_html

    # Teasers do blog apontam pros posts em inglês existentes (ainda não há
    # blog em alemão) -- não pros slugs em português, que o leitor de
    # alemão não conseguiria ler.
    assert "/blog/yoruba-language-and-culture" in de_html
    assert "/blog/yoruba-greetings" in de_html
    assert "/blog/yoruba-numbers-1-to-20" in de_html
    assert "/blog/niveis-de-ingles-a1-c1" not in de_html

    # Controller: contexto de idioma pro seletor (site_navbar.html) + mesma
    # lógica de negócio da home em PT/EN/ES/FR (cursos ao vivo do banco,
    # redirect app.vediums.com -> /login)
    assert 'context.lang = "de"' in de_py
    assert 'context.canonical_url = "https://vediums.com/de"' in de_py
    assert 'context.alt_lang_url = "https://vediums.com/"' in de_py
    assert "def get_courses()" in de_py
    assert "app.vediums.com" in de_py
    assert 'redirect_location = "/login"' in de_py

    # PT, EN, ES e FR ganham o hreflang de volta (reciprocidade)
    assert 'hreflang="de" href="https://vediums.com/de"' in pt_html
    assert 'hreflang="de" href="https://vediums.com/de"' in en_html
    assert 'hreflang="de" href="https://vediums.com/de"' in es_html
    assert 'hreflang="de" href="https://vediums.com/de"' in fr_html

    # Roteamento: /de não pode cair no redirect antigo pra PT (bug que
    # existiria se a home nova não tivesse sido conectada em hooks.py)
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    assert "/de" not in by_source  # sem self-redirect /de -> /de
    assert "LANGUAGES_WITH_OWN_HOME" in (
        ROOT / "vedium_core" / "vedium_core" / "hooks.py"
    ).read_text(encoding="utf-8")
    assert "de" in vedium_hooks.LANGUAGES_WITH_OWN_HOME

    # Menu principal traduzido (rótulos, ver site_navbar.html vd_menu_i18n)
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")
    assert '"de": {"home"' in navbar

    # Sitemap lista a home em alemão
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    assert '{"loc": "/de", "priority"' in sitemap_py


def test_german_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang():
    """Páginas do menu principal (catalogo, sobre, como-funciona, faq,
    contato) traduzidas pro alemão -- mesmo padrão de
    test_french_main_menu_pages_exist_with_same_slug_and_reciprocal_hreflang:
    mantêm o MESMO slug sob /de/ (ex. /de/catalogo), registrado em
    SAME_SLUG_TRANSLATIONS.
    """
    menu_slugs = ["catalogo", "sobre", "como-funciona", "faq", "contato"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in menu_slugs:
        de_html_path = WWW / "de" / f"{slug}.html"
        pt_html_path = WWW / f"{slug}.html"
        en_html_path = WWW / "en" / f"{slug}.html"
        es_html_path = WWW / "es" / f"{slug}.html"
        fr_html_path = WWW / "fr" / f"{slug}.html"
        assert de_html_path.exists(), f"falta www/de/{slug}.html"
        assert pt_html_path.exists()

        de_html = de_html_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")
        en_html = en_html_path.read_text(encoding="utf-8")
        es_html = es_html_path.read_text(encoding="utf-8")
        fr_html = fr_html_path.read_text(encoding="utf-8")

        assert 'lang="de"' in de_html
        pt_slug = "cursos-de-idiomas-online" if slug == "catalogo" else slug
        assert f'hreflang="pt-br" href="https://vediums.com/{pt_slug}"' in de_html
        assert f'hreflang="en" href="https://vediums.com/en/{slug}"' in de_html
        assert f'hreflang="es" href="https://vediums.com/es/{slug}"' in de_html
        assert f'hreflang="fr" href="https://vediums.com/fr/{slug}"' in de_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in de_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in pt_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in en_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in es_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in fr_html

        assert f'"{slug}": {{"en", "es", "fr", "de", "ru"}}' in hooks
        assert f'{{"loc": "/de/{slug}"' in sitemap_py

    # catalogo/como-funciona/faq têm controller próprio; contato e sobre não
    # têm .py em nenhum idioma (conteúdo estático) -- não regride o padrão.
    for slug in ["catalogo", "como-funciona", "faq"]:
        de_py_path = WWW / "de" / f"{slug.replace('-', '_')}.py"
        assert de_py_path.exists(), f"falta www/de/{slug.replace('-', '_')}.py"
    assert not (WWW / "de" / "contato.py").exists()
    assert not (WWW / "de" / "sobre.py").exists()

    # Roteamento: /de/catalogo não pode ser interceptado pelo controller PT
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in menu_slugs:
        assert f"/de/{slug}" not in by_source  # sem self-redirect

    rules_by_from = {r["from_route"]: r["to_route"] for r in vedium_hooks.LANGUAGE_ROUTE_RULES}
    for slug in menu_slugs:
        assert rules_by_from.get(f"/de/{slug}") is None

    # Conteúdo real (adaptação editorial, não tradução literal) — CTAs
    # apontam pro teste de nível de inglês (único formal) e pro catálogo em
    # alemão, não pro PT.
    catalogo_de = (WWW / "de" / "catalogo.html").read_text(encoding="utf-8")
    sobre_de = (WWW / "de" / "sobre.html").read_text(encoding="utf-8")
    como_funciona_de = (WWW / "de" / "como-funciona.html").read_text(encoding="utf-8")
    faq_de = (WWW / "de" / "faq.html").read_text(encoding="utf-8")
    contato_de = (WWW / "de" / "contato.html").read_text(encoding="utf-8")

    assert "/teste-de-nivel-ingles" in como_funciona_de
    assert "/teste-de-nivel-ingles" in faq_de
    assert "/de/catalogo" in sobre_de
    assert "Entdecken Sie Unsere Kurse" in catalogo_de
    assert "Nachricht Senden" in contato_de
    assert "Nachricht gesendet!" in contato_de


def test_german_cta_pages_exist_and_preserve_public_funnel_safety():
    """Páginas de CTA/conversão (planos, matricula, aula-diagnostica)
    traduzidas pro alemão -- mesmo padrão de
    test_french_cta_pages_exist_and_preserve_public_funnel_safety. Mesmo
    slug sob /de/. Preserva as garantias de segurança do funil público já
    testadas em PT/EN/ES/FR: sem alteração de checkout.
    """
    cta_slugs = ["planos", "matricula", "aula-diagnostica"]
    hooks = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")

    for slug in cta_slugs:
        de_html_path = WWW / "de" / f"{slug}.html"
        de_py_path = WWW / "de" / f"{slug.replace('-', '_')}.py"
        pt_html_path = WWW / f"{slug}.html"
        assert de_html_path.exists(), f"falta www/de/{slug}.html"
        assert de_py_path.exists(), f"falta www/de/{slug.replace('-', '_')}.py"

        de_html = de_html_path.read_text(encoding="utf-8")
        de_py = de_py_path.read_text(encoding="utf-8")
        pt_html = pt_html_path.read_text(encoding="utf-8")

        assert 'lang="de"' in de_html
        assert f'hreflang="pt-br" href="https://vediums.com/{slug}"' in de_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in de_html
        assert f'hreflang="de" href="https://vediums.com/de/{slug}"' in pt_html
        assert "de" in vedium_hooks.SAME_SLUG_TRANSLATIONS[slug]
        assert f'{{"loc": "/de/{slug}"' in sitemap_py

        if slug != "matricula":
            assert "stripe" not in de_html.lower()
        assert "create_checkout" not in de_html
        assert 'context.lang = "de"' in de_py
        assert f'context.canonical_url = "https://vediums.com/de/{slug}"' in de_py

    # planos: CTA final aponta pro teste de nivel em ingles e pro
    # matricula/catalogo em alemão, nao pros equivalentes em PT.
    planos_de = (WWW / "de" / "planos.html").read_text(encoding="utf-8")
    assert "/teste-de-nivel-ingles" in planos_de
    assert "/de/matricula" in planos_de
    assert "/de/catalogo" in planos_de
    assert "Leichtes Paket wählen" in planos_de
    assert "Empfohlenes Paket wählen" in planos_de
    assert "Intensives Paket wählen" in planos_de
    assert "wa.me/5511911293075" in planos_de

    # matricula: dropdown com valores de curso intactos (slugs de banco,
    # nunca traduzidos), so os LABELS mudam pro alemão.
    matricula_de = (WWW / "de" / "matricula.html").read_text(encoding="utf-8")
    assert 'value="ingl-s-beginner"' in matricula_de
    assert 'value="iorub-b-sico"' in matricula_de
    assert "Weiter auf der Plattform" in matricula_de
    assert "app.vediums.com/lms/courses/" in matricula_de
    assert "source=public_funnel" in matricula_de
    assert "enrollment_intent_click" in matricula_de
    assert "/api/method" not in matricula_de

    # aula-diagnostica: pre-agendamento nao cria reserva automatica.
    diagnostica_de = (WWW / "de" / "aula-diagnostica.html").read_text(encoding="utf-8")
    assert "diagnostic_schedule_click" in diagnostica_de
    assert "diagnostic_slot_click" in diagnostica_de
    assert "get_available_diagnostic_slots" in diagnostica_de
    assert 'data-vd-diagnostic="english"' in diagnostica_de
    assert 'data-vd-diagnostic="portuguese_foreigners"' in diagnostica_de
    assert 'data-vd-diagnostic="yoruba"' in diagnostica_de
    assert "erstellt keine automatische Reservierung" in diagnostica_de
    assert "vedium_core.public_funnel.get_available_diagnostic_slots" in diagnostica_de

    # Roteamento: sem self-redirect
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    for slug in cta_slugs:
        assert f"/de/{slug}" not in by_source


def test_ple_cluster_has_german_pages_with_reciprocal_hreflang():
    """Cluster PLE (Português para Estrangeiros) traduzido pro alemão --
    público germanofalante pode ter interesse real (DACH: Alemanha,
    Áustria, Suíça -- diáspora, expatriados, profissionais com operação no
    Brasil), 4a prioridade do rollout de alemão (mesma ordem usada em
    en/es/fr). Mesmo padrão do cluster PLE em francês: `alt` com 5 idiomas
    agora (pt-BR, en, es, fr, de), slugs pensados como um germanofalante
    buscaria (transliteração ASCII padrão de ü/ö/ä -> ue/oe/ae). O alemão
    GANHOU sua própria página de teste de nível
    (/de/portugiesisch-einstufungstest), então test_url aponta pra ela,
    não pro teste em inglês.
    """
    pairs = [
        ("portugues-para-estrangeiros", "portugiesisch-fuer-auslaender"),
        ("portugues-para-executivos", "portugiesisch-fuer-fuehrungskraefte"),
        ("preparatorio-celpe-bras", "celpe-bras-pruefungsvorbereitung"),
    ]
    expected_test_url = "/de/portugiesisch-einstufungstest"
    for pt_slug, de_slug in pairs:
        assert LANDINGS[pt_slug]["alt"]["de"] == de_slug
        assert LANDINGS[de_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[de_slug]["alt"]["en"] == LANDINGS[pt_slug]["alt"]["en"]
        assert LANDINGS[de_slug]["alt"]["es"] == LANDINGS[pt_slug]["alt"]["es"]
        assert LANDINGS[de_slug]["alt"]["fr"] == LANDINGS[pt_slug]["alt"]["fr"]
        assert LANDINGS[de_slug]["alt"]["de"] == de_slug
        assert LANDINGS[de_slug]["lang"] == "de"
        assert "test_url" in LANDINGS[de_slug], f"{de_slug} precisa de test_url explícito"
        assert LANDINGS[de_slug]["test_url"] == expected_test_url

        de_html = (WWW / "de" / f"{de_slug}.html").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{de_slug}")' in de_html

        # conteúdo real, não placeholder (mesma paridade de profundidade
        # exigida do cluster PT/EN/ES/FR)
        landing = LANDINGS[de_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/de/{de_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # portugiesisch-fuer-auslaender é a landing pilar em DE: precisa do
    # mesmo grid de cursos reais (preço, aulas, link) que os outros
    # pilares já têm.
    assert '"portugiesisch-fuer-auslaender": {"category_exact": "Português para Estrangeiros"}' in (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")

    # Página de teste de nível em alemão: existência, roteamento (via
    # hooks._build_language_prefix_redirects -> pt_to_lang_slug) e
    # reciprocidade de hreflang com PT/EN/ES/FR.
    test_html_path = WWW / "de" / "portugiesisch-einstufungstest.html"
    test_py_path = WWW / "de" / "portugiesisch_einstufungstest.py"
    assert test_html_path.exists()
    assert test_py_path.exists()

    test_html = test_html_path.read_text(encoding="utf-8")
    assert 'lang="de"' in test_html
    assert 'hreflang="pt-br" href="https://vediums.com/teste-de-nivel"' in test_html
    assert 'hreflang="en" href="https://vediums.com/en/portuguese-placement-test"' in test_html
    assert 'hreflang="es" href="https://vediums.com/es/prueba-de-nivel-de-portugues"' in test_html
    assert 'hreflang="fr" href="https://vediums.com/fr/test-de-niveau-de-portugais"' in test_html
    assert 'hreflang="de" href="https://vediums.com/de/portugiesisch-einstufungstest"' in test_html

    # As perguntas de múltipla escolha continuam em português (o idioma
    # avaliado nunca muda) -- só as instruções ao redor mudam pro alemão.
    assert "O supermercado fica _ lado da farmácia." in test_html
    assert "Erfahren Sie Ihr Niveau in brasilianischem Portugiesisch" in test_html
    assert "Mein GER-Ergebnis ansehen" in test_html

    # Reciprocidade nos 4 idiomas existentes
    pt_test_html = (WWW / "teste-de-nivel.html").read_text(encoding="utf-8")
    en_test_html = (WWW / "en" / "portuguese-placement-test.html").read_text(encoding="utf-8")
    es_test_html = (WWW / "es" / "prueba-de-nivel-de-portugues.html").read_text(encoding="utf-8")
    fr_test_html = (WWW / "fr" / "test-de-niveau-de-portugais.html").read_text(encoding="utf-8")
    assert 'hreflang="de" href="https://vediums.com/de/portugiesisch-einstufungstest"' in pt_test_html
    assert 'hreflang="de" href="https://vediums.com/de/portugiesisch-einstufungstest"' in en_test_html
    assert 'hreflang="de" href="https://vediums.com/de/portugiesisch-einstufungstest"' in es_test_html
    assert 'hreflang="de" href="https://vediums.com/de/portugiesisch-einstufungstest"' in fr_test_html

    # Roteamento: /de/teste-de-nivel redireciona pra tradução real, sem
    # self-redirect.
    redirects = vedium_hooks.LANGUAGE_PREFIX_REDIRECTS
    by_source = {r["source"]: r["target"] for r in redirects}
    assert by_source["/de/teste-de-nivel"] == "/de/portugiesisch-einstufungstest"

    assert '{"loc": "/de/portugiesisch-einstufungstest"' in (
        ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
    ).read_text(encoding="utf-8")


def test_english_cluster_has_german_pages_with_reciprocal_hreflang():
    """Cluster de Inglês (pilar englischkurs-online-live + 5 sub-páginas)
    traduzido pro alemão -- 5a prioridade do rollout de alemão (mesma
    ordem usada em en/es/fr): germanofalantes que querem aprender inglês
    com a Vedium, adaptado pro público da região DACH. Mesmo padrão de
    test_english_cluster_has_french_pages_with_reciprocal_hreflang: slug
    em alemão pensado como um germanofalante buscaria (transliteração
    ASCII de ü/ö/ä), `alt` recíproco nos 5 idiomas, paridade de
    profundidade de conteúdo.
    """
    pairs = [
            ("curso-de-ingles-online", "englischkurs-online-live", None),
        ("ingles-para-entrevista", "englisch-fuer-vorstellungsgespraeche", None),
        ("ingles-para-programadores", "englisch-fuer-entwickler", None),
        ("ingles-executivo", "business-englisch-online", None),
        ("ingles-para-viagens", "englisch-fuer-reisen", None),
        ("ingles-para-atendimento-ao-cliente", "englisch-fuer-kundenservice", None),
    ]
    for pt_slug, de_slug, expected_test_url in pairs:
        assert LANDINGS[pt_slug]["alt"]["de"] == de_slug
        assert LANDINGS[de_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[de_slug]["alt"]["en"] == LANDINGS[pt_slug]["alt"]["en"]
        assert LANDINGS[de_slug]["alt"]["es"] == LANDINGS[pt_slug]["alt"]["es"]
        assert LANDINGS[de_slug]["alt"]["fr"] == LANDINGS[pt_slug]["alt"]["fr"]
        assert LANDINGS[de_slug]["alt"]["de"] == de_slug
        assert LANDINGS[de_slug]["lang"] == "de"
        if expected_test_url:
            assert "test_url" in LANDINGS[de_slug], f"{de_slug} precisa de test_url explícito"
            assert LANDINGS[de_slug]["test_url"] == expected_test_url

        de_html = (WWW / "de" / f"{de_slug}.html").read_text(encoding="utf-8")
        assert f'get_marketing_landing("{de_slug}")' in de_html

        # conteúdo real, não placeholder (mesma paridade de profundidade
        # exigida do cluster PT/EN/ES/FR)
        landing = LANDINGS[de_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100

        assert f"/de/{de_slug}" in (
            ROOT / "vedium_core" / "vedium_core" / "www" / "sitemap.py"
        ).read_text(encoding="utf-8")

    # englischkurs-online-live é a landing pilar em DE: precisa do mesmo
    # grid de cursos reais (preço, aulas, link) que os outros pilares já
    # têm, e preço em EUR (não R$ nem US$).
    assert '"englischkurs-online-live": {"category_prefix": "Inglês"}' in (
        ROOT / "vedium_core" / "vedium_core" / "marketing_landing_content.py"
    ).read_text(encoding="utf-8")
    pilar = LANDINGS["englischkurs-online-live"]
    assert "€" in pilar["price_display"]
    assert "R$" not in pilar["price_display"]
    assert "US$" not in pilar["price_display"]


def test_legal_pages_publish_pdf_of_full_document_not_just_summary():
    """2026-07-03: os 6 documentos legais externos (docx completos, escritos
    fora do repo) são densos demais (100-270 linhas cada) pra transcrever
    em HTML sem risco de erro jurídico. Cada página do site é um RESUMO
    + link pro PDF completo (fidelidade total ao documento original),
    não uma reescrita. PDFs ficam em public/legal/ (exceção ao *.pdf do
    .gitignore, que existe pra bloquear material de aula com direito
    autoral de terceiro — estes são documentos próprios da Vedium)."""
    legal_dir = ROOT / "vedium_core" / "vedium_core" / "public" / "legal"
    pages_and_pdfs = {
        "termos.html": "termos-de-uso-e-contratacao.pdf",
        "privacidade.html": "politica-de-privacidade.pdf",
        "cookies.html": "politica-de-cookies.pdf",
        "cancelamento-reembolso.html": "politica-de-cancelamento-reembolso.pdf",
        "gravacao-imagem-voz.html": "termo-de-gravacao-imagem-voz.pdf",
        "propriedade-intelectual.html": "politica-de-propriedade-intelectual.pdf",
    }
    for page, pdf in pages_and_pdfs.items():
        page_path = WWW / page
        assert page_path.exists(), f"{page} não existe"
        html = page_path.read_text(encoding="utf-8")
        assert f"/assets/vedium_core/legal/{pdf}" in html
        assert '{% extends "templates/web.html" %}' not in html, (
            f"{page} não pode usar o layout web.html (amador) — "
            "precisa do tema unificado (site_navbar/site_footer)"
        )
        assert "site_navbar.html" in html
        assert "site_footer.html" in html
        pdf_path = legal_dir / pdf
        assert pdf_path.exists(), f"PDF {pdf} não existe em public/legal/"
        assert pdf_path.stat().st_size > 10_000, f"PDF {pdf} parece vazio/corrompido"

    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    assert '<a href="/cookies">' in footer
    assert '<a href="/cancelamento-reembolso">' in footer

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "!vedium_core/vedium_core/public/legal/*.pdf" in gitignore


def test_diferenciais_and_metodologia_pages_exist():
    """2026-07-04: novas páginas /diferenciais e /metodologia, inspiradas na
    estrutura da WiseUp mas com claims reais da Vedium (sem estatística
    inventada tipo '500+ horas' — só o que já está provado em outras
    páginas: aulas ao vivo de 1h, sem fidelidade, certificado, teste de
    nível grátis). PT-only por enquanto (tradução vem depois via agentes)."""
    for slug in ["diferenciais", "metodologia"]:
        py_path = WWW / f"{slug}.py"
        html_path = WWW / f"{slug}.html"
        assert py_path.exists(), f"falta www/{slug}.py"
        assert html_path.exists(), f"falta www/{slug}.html"
        html = html_path.read_text(encoding="utf-8")
        assert 'lang="pt-BR"' in html
        assert "site_navbar.html" in html
        assert "site_footer.html" in html
        assert f'<link rel="canonical" href="https://vediums.com/{slug}" />' in html

    diferenciais = (WWW / "diferenciais.html").read_text(encoding="utf-8")
    assert "Sem contrato de fidelidade" in diferenciais or "sem contrato de fidelidade" in diferenciais.lower()
    assert "/teste-de-nivel" in diferenciais
    assert "/metodologia" in diferenciais

    metodologia = (WWW / "metodologia.html").read_text(encoding="utf-8")
    assert "/teste-de-nivel" in metodologia
    assert "/diferenciais" in metodologia
    assert "HowTo" in metodologia


def test_aulas_ao_vivo_and_parcerias_pages_exist():
    """2026-07-14: páginas institucionais Aulas ao Vivo e Parcerias, com
    conteúdo baseado nos documentos internos revisados da empresa (Método
    Pedagógico e Produtos, Personas e Jornada, Parcerias Estratégicas) e nas
    políticas já publicadas (Termos, Termo de Gravação/Imagem/Voz) — sem
    estatística ou promessa comercial inventada. PT-only por enquanto,
    mesmo padrão de diferenciais/metodologia. O controller de Aulas ao Vivo
    usa underscore (aulas_ao_vivo.py) porque Frappe não resolve módulo com
    hífen no nome do arquivo."""
    pages = [("aulas-ao-vivo", "aulas_ao_vivo"), ("parcerias", "parcerias")]
    for slug, py_name in pages:
        py_path = WWW / f"{py_name}.py"
        html_path = WWW / f"{slug}.html"
        assert py_path.exists(), f"falta www/{py_name}.py"
        assert html_path.exists(), f"falta www/{slug}.html"
        html = html_path.read_text(encoding="utf-8")
        assert 'lang="pt-BR"' in html
        assert "site_navbar.html" in html
        assert "site_footer.html" in html
        assert f'<link rel="canonical" href="https://vediums.com/{slug}" />' in html
        assert "FAQPage" in html

    aulas = (WWW / "aulas-ao-vivo.html").read_text(encoding="utf-8")
    assert "180 dias" in aulas
    assert "18 anos" in aulas
    assert "/metodologia" in aulas
    assert "/gravacao-imagem-voz" in aulas
    assert "/teste-de-nivel" in aulas

    parcerias = (WWW / "parcerias.html").read_text(encoding="utf-8")
    assert "/empresas" in parcerias
    assert "/programa-de-indicacao" in parcerias
    assert "/contato" in parcerias

    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    assert '{"loc": "/aulas-ao-vivo"' in sitemap_py
    assert '{"loc": "/parcerias"' in sitemap_py

    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    assert "vd_footer_t.live_classes" in footer
    assert "vd_footer_t.partnerships" in footer
    assert "'aulas-ao-vivo'" in footer
    assert "'parcerias'" in footer

    sitemap_py = (WWW / "sitemap.py").read_text(encoding="utf-8")
    assert '{"loc": "/diferenciais"' in sitemap_py
    assert '{"loc": "/metodologia"' in sitemap_py

    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")
    assert "vd_footer_u.diferenciais" in footer
    assert "vd_footer_u.metodologia" in footer


def test_institutional_pages_have_breadcrumb():
    """2026-07-15: auditoria Semana 2 achou que só curso.html tinha
    Schema.org BreadcrumbList; blog só tinha o visual, sem schema; e várias
    páginas institucionais não tinham breadcrumb nenhum (nem visual, nem
    schema). Trava BreadcrumbList nessas páginas pra não regredir."""
    pages = [
        "faq.html", "planos.html", "matricula.html", "aula-diagnostica.html",
        "diferenciais.html", "metodologia.html", "aulas-ao-vivo.html",
        "parcerias.html", "empresas.html", "carreiras.html", "blog.html",
    ]
    for slug in pages:
        html = (WWW / slug).read_text(encoding="utf-8")
        assert "BreadcrumbList" in html, f"{slug} sem Schema.org BreadcrumbList"

    public_intent = (TPL / "public_intent_page.html").read_text(encoding="utf-8")
    assert "BreadcrumbList" in public_intent

    blog_post = (TPL / "blog_post.html").read_text(encoding="utf-8")
    blog_category = (TPL / "blog_category.html").read_text(encoding="utf-8")
    assert "BreadcrumbList" in blog_post
    assert "BreadcrumbList" in blog_category


def test_sobre_page_has_mission_vision_values():
    """2026-07-15: usuário apontou que /sobre era rasa demais -- faltava
    propósito, missão, visão e valores, baseados nos documentos internos
    reais (Identidade Organizacional v1/v2, Modelo de Negócio v2), não
    inventados."""
    sobre = (WWW / "sobre.html").read_text(encoding="utf-8")
    assert "Propósito" in sobre
    assert "Missão" in sobre
    assert "Visão" in sobre
    assert "Manifesto" in sobre
    assert "AboutPage" in sobre
    assert "EducationalOrganization" in sobre
    # tabela de valores (fazemos / não fazemos), mesmo padrão de diferenciais.html
    for valor in ("Presença", "Respeito cultural", "Acessibilidade", "Evolução real", "Verdade"):
        assert valor in sobre


def test_blog_posts_have_alt_text_and_internal_links():
    """2026-07-15: usuário apontou 2 regras de SEO que precisam valer pra
    QUALQUER post do blog, não só os de hoje: (1) toda imagem de capa
    precisa ter ALT (acessibilidade + SEO de imagem); (2) o corpo do post
    precisa ter link interno de verdade pra página relacionada (curso, FAQ
    etc.), não só o botão de CTA no fim. Trava as duas regras pra sempre no
    dict BLOG_POSTS, e confirma que os grids de listagem (blog.html,
    blog_category.html) renderizam <img alt> de verdade em vez de <div>
    com background-image (que não tem alt nenhum)."""
    import vedium_core.blog_content as bc

    missing_alt = []
    low_links = []
    for slug, post in bc.BLOG_POSTS.items():
        if not (post.get("hero_alt") or "").strip():
            missing_alt.append(slug)

        body_html = "".join(
            "".join(sec.get("body", [])) for sec in post.get("sections", [])
        )
        internal_links = re.findall(r'href="(/[^"#]*)"', body_html)
        if len(internal_links) < 2:
            low_links.append(slug)

    assert not missing_alt, f"posts sem hero_alt: {missing_alt}"
    assert not low_links, f"posts com menos de 2 links internos no corpo: {low_links}"

    blog_html = (WWW / "blog.html").read_text(encoding="utf-8")
    assert '<img src="{{ p.hero_image }}" alt="{{ p.hero_alt }}"' in blog_html

    blog_category_html = (TPL / "blog_category.html").read_text(encoding="utf-8")
    assert '<img src="{{ p.hero_image }}" alt="{{ p.hero_alt }}"' in blog_category_html


def test_faq_enriched_with_course_specific_questions():
    """2026-07-04: /faq ganhou perguntas segmentadas por curso (inglês,
    iorubá, português para estrangeiros) além das gerais — mantendo a
    mesma página única (schema FAQPage + hreflang já existentes, decisão
    consciente de não fragmentar em sub-páginas como a WiseUp faz)."""
    faq_html = (WWW / "faq.html").read_text(encoding="utf-8")
    assert "Ingles" in faq_html or "Inglês" in faq_html
    assert "Ioruba" in faq_html or "Iorubá" in faq_html
    assert "estrangeiros" in faq_html.lower()
    assert faq_html.count('"@type":"Question"') >= 8


def test_blog_index_has_pagination_search_and_category_filter():
    """2026-07-04: usuário notou que o /blog carregava os 40+ posts de uma
    vez e as imagens de capa se repetiam. Adiciona paginação (12/página,
    ?page=N, rel=prev/next, canonical por página, noindex quando filtrado
    por busca/categoria para não indexar combinações infinitas de query) +
    busca por texto + filtro por categoria (reaproveitando o campo `tag`
    que os posts já têm, sem inventar taxonomia nova)."""
    import vedium_core.blog_content as bc

    assert bc.POSTS_PER_PAGE == 12
    assert hasattr(bc, "get_blog_categories")
    assert hasattr(bc, "get_adjacent_posts")

    blog_html = (WWW / "blog.html").read_text(encoding="utf-8")
    assert 'name="q"' in blog_html
    assert 'name="category"' in blog_html
    assert "vd-bl-pager" in blog_html
    assert 'rel="prev"' in blog_html and 'rel="next"' in blog_html
    assert "noindex, follow" in blog_html  # páginas filtradas não indexam

    blog_py = (WWW / "blog.py").read_text(encoding="utf-8")
    assert "get_blog_index_context" in blog_py

    blog_content_src = (ROOT / "vedium_core" / "vedium_core" / "blog_content.py").read_text(encoding="utf-8")
    assert "frappe.form_dict.get(\"page\")" in blog_content_src
    assert "frappe.form_dict.get(\"category\")" in blog_content_src
    assert "frappe.form_dict.get(\"q\")" in blog_content_src


def test_blog_post_has_prev_next_navigation():
    """2026-07-04: ao ler um post, o usuário pode navegar pro artigo
    anterior/próximo (ordem cronológica da lista combinada) sem voltar
    pro índice."""
    blog_post_py = (WWW / "blog_post.py").read_text(encoding="utf-8")
    assert "get_adjacent_posts" in blog_post_py
    assert "context.newer_post, context.older_post" in blog_post_py

    template = (TPL / "blog_post.html").read_text(encoding="utf-8")
    assert "vd-bp-nav" in template
    assert "newer_post" in template and "older_post" in template


def test_empresas_page_is_rich_and_wired_to_crm():
    """2026-07-04: /empresas era 12 linhas genéricas do template
    public_intent_page.html; usuário pediu conteúdo mais rico (inspirado
    na OpenEnglish para-empresas: ícones, "como funciona", fotos
    humanizadas) e que o formulário caia direto no CRM (não só em Support
    Ticket, que era o comportamento anterior de TODOS os formulários de
    /public_funnel.submit_public_intent)."""
    empresas_html = (WWW / "empresas.html").read_text(encoding="utf-8")
    empresas_py = (WWW / "empresas.py").read_text(encoding="utf-8")

    # conteudo rico: beneficios com icone, "como funciona" em etapas,
    # fotos humanizadas (nao so texto)
    assert empresas_html.count('<i class="fa') >= 6
    assert "vd-steps" in empresas_html
    assert empresas_html.count("<img") >= 3  # hero + 2 fotos humanizadas
    assert "vd-photo-row" in empresas_html

    # formulario com campos de empresa (o que o CRM Lead precisa pra B2B)
    assert 'id="company"' in empresas_html
    assert 'id="team_size"' in empresas_html
    assert "intent:'b2b'" in empresas_html
    # cai no mesmo endpoint que ja tinha, mas agora esse endpoint valida
    # e cria CRM Lead pra intent b2b (ver testes de public_funnel abaixo)
    assert "vedium_core.public_funnel.submit_public_intent" in empresas_html
    # checa r.ok antes de considerar sucesso (bug corrigido nesta mudanca)
    assert "if(!r.ok)" in empresas_html

    # hreflang proprio (pagina deixou de depender do template compartilhado)
    assert 'hreflang="en" href="https://vediums.com/en/empresas"' in empresas_html
    assert 'hreflang="es" href="https://vediums.com/es/empresas"' in empresas_html
    assert 'hreflang="fr" href="https://vediums.com/fr/empresas"' in empresas_html
    assert "site_navbar.html" in empresas_html
    assert "site_footer.html" in empresas_html
    assert "get_context" in empresas_py


def test_public_intent_validates_fields_and_creates_crm_lead_for_b2b():
    """2026-07-04: submit_public_intent (usado por /empresas, /comunidade
    etc.) não validava nada (nome/e-mail podiam vir vazios) nem tinha
    rate-limit — diferente do formulário de contato, que já tinha os dois.
    Também não criava CRM Lead, só ticket. Agora: valida
    nome+e-mail obrigatórios e formato de e-mail, tem rate-limit, e cria/
    atualiza um CRM Lead pra QUALQUER intent (não só b2b -- usuário pediu
    pra garantir que os módulos se enxerguem), com organization/
    no_of_employees setados de forma defensiva (não quebra se o schema do
    CRM Lead instalado não tiver esses campos)."""
    funnel = (ROOT / "vedium_core" / "vedium_core" / "public_funnel.py").read_text(encoding="utf-8")
    assert "rate_limit_by_ip(\"public_intent\"" in funnel
    assert "Nome e e-mail são obrigatórios" in funnel
    assert "EMAIL_RE" in funnel
    assert "_upsert_crm_lead_from_public_intent" in funnel
    assert "lead.organization" in funnel
    assert "lead.no_of_employees" in funnel
    assert "CRM Lead" in funnel
    # nao fica restrito a b2b -- todo intent vira lead, so o texto de
    # origem/nota que muda por intent_label
    submit_body = funnel.split("def submit_public_intent")[1]
    assert 'if intent == "b2b"' not in submit_body


def test_candidatura_doctype_has_resume_attachment_field():
    """2026-07-04: campo de anexo de currículo, além do link, no doctype
    que já capturava candidaturas de /carreiras (nome, e-mail, telefone,
    vaga, currículo, mensagem, status) -- espelha o que um ATS/HR real
    captura, sem precisar instalar o app hrms inteiro."""
    careers_py = (ROOT / "vedium_core" / "vedium_core" / "careers.py").read_text(encoding="utf-8")
    assert '"resume_attachment"' in careers_py
    assert "resume_attachment" in careers_py.split("def submit_candidatura")[1].split("\n\n")[0]


def test_referral_conversion_also_creates_crm_lead():
    """2026-07-04: usuário perguntou pra onde vai o programa de indicação
    e pediu visibilidade no CRM. O mecanismo de recompensa já sabia quem
    indicou quem (o código de indicação, gerado só pra usuário logado,
    carrega essa identidade -- não há "compartilhamento anônimo"). O que
    faltava era o time de vendas ENXERGAR essa atividade no CRM. Agora
    record_referral_conversion cria/atualiza um CRM Lead pro indicado
    (referee) com nota de quem indicou, sem mudar o fluxo de recompensa
    automática que já funcionava."""
    referrals_py = (ROOT / "vedium_core" / "vedium_core" / "referrals.py").read_text(encoding="utf-8")
    assert "_upsert_crm_lead_from_referral_conversion" in referrals_py
    assert '"doctype": "CRM Lead"' not in referrals_py  # usa frappe.new_doc, nao dict cru
    assert "lead.source = " in referrals_py
    assert "Indicado por:" in referrals_py
    # nunca pode derrubar a recompensa/cupom se o CRM falhar
    body = referrals_py.split("def record_referral_conversion")[1]
    assert "_upsert_crm_lead_from_referral_conversion" in body.split("def _upsert_crm_lead_from_referral_conversion")[0]
    assert "except Exception" in body.split("_upsert_crm_lead_from_referral_conversion(")[1][:200]


def test_careers_form_also_creates_native_hrms_job_applicant():
    """2026-07-04: usuário instalou o app hrms (Frappe HR) e pediu pra
    /carreiras usar o módulo nativo. O formulário continua criando o
    doctype custom Candidatura (histórico existente, não descartado), e
    agora TAMBÉM cria um Job Applicant nativo, ligado a um Job Opening
    real (não hardcoded) via job_title. Nunca quebra se o hrms não
    estiver instalado (checagem defensiva) nem se o Job Opening
    correspondente não existir ainda."""
    careers_py = (ROOT / "vedium_core" / "vedium_core" / "careers.py").read_text(encoding="utf-8")
    assert "_create_hrms_job_applicant" in careers_py
    assert 'frappe.db.exists("DocType", "Job Applicant")' in careers_py
    assert 'frappe.new_doc("Job Applicant")' in careers_py
    assert "applicant.applicant_name" in careers_py
    assert "applicant.email_id" in careers_py
    assert "applicant.job_title" in careers_py
    body = careers_py.split("def submit_candidatura")[1]
    assert "_create_hrms_job_applicant" in body.split("def _create_hrms_job_applicant")[0]
    assert "except Exception" in body.split("_create_hrms_job_applicant(")[1][:200]

    oneshot = (
        ROOT / "vedium_core" / "vedium_core" / "scripts" / "migrations" / "oneshot"
        / "setup_hrms_job_openings.py"
    )
    assert oneshot.exists()
    oneshot_src = oneshot.read_text(encoding="utf-8")
    assert "Professor(a) de Ingles" in oneshot_src
    assert "Professor(a) de Ioruba" in oneshot_src
    assert '"doctype": "Job Opening"' in oneshot_src
    assert '"doctype": "Designation"' in oneshot_src
    assert 'COMPANY = "Vedium"' in oneshot_src


def test_certificate_pdf_push_and_onboarding_are_wired_correctly():
    """2026-07-06: certificate_pdf.py, push_notifications.py e onboarding.py
    ficaram órfãos (nunca commitados/wireados) depois do outage de
    2026-07-05. Ao finalizá-los, achamos dois bugs reais:

    1. Todo `frappe.call`/URL que chamava esses 3 módulos usava
       "vedium_core.vedium_core.<modulo>.<metodo>" (3 segmentos) quando o
       caminho de import correto é "vedium_core.<modulo>.<metodo>" (2
       segmentos) -- os arquivos estão em vedium_core/vedium_core/*.py,
       não dentro do subpacote vedium_core/vedium_core/vedium_core/.
       Isso derrubaria QUALQUER chamada com 404 "method not found".
    2. hooks.py tinha `scheduler_events` definido DUAS vezes -- a segunda
       atribuição sobrescrevia a primeira, silenciosamente cancelando o
       cron do resumo semanal. Os jobs de trial.expire_trials e
       lgpd._audit_pending_requests também usavam o path de 3 segmentos
       errado (mesma classe de bug do item 1), então nunca rodavam.
    """
    hooks_src = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    certificado_html = (WWW / "certificado.html").read_text(encoding="utf-8")
    onboarding_html = (WWW / "onboarding.html").read_text(encoding="utf-8")
    push_js = (PUBLIC_JS / "push-notifications.js").read_text(encoding="utf-8")

    # Nenhum caminho de 3 segmentos sobrando pros módulos de nível superior.
    for bad in [
        "vedium_core.vedium_core.certificate_pdf.",
        "vedium_core.vedium_core.push_notifications.",
        "vedium_core.vedium_core.onboarding.",
        "vedium_core.vedium_core.trial.",
        "vedium_core.vedium_core.lgpd.",
    ]:
        assert bad not in certificado_html
        assert bad not in onboarding_html
        assert bad not in push_js
        assert bad not in hooks_src

    assert "vedium_core.certificate_pdf.generate_pdf" in certificado_html
    assert "vedium_core.onboarding.save_onboarding" in onboarding_html
    assert "vedium_core.push_notifications.save_subscription" in push_js
    assert "vedium_core.push_notifications.remove_subscription" in push_js
    assert "vedium_core.push_notifications.get_vapid_public_key" in push_js

    # scheduler_events aparece só 1 vez como atribuição (não duplicado).
    assert hooks_src.count("scheduler_events = {") == 1
    assert "vedium_core.trial.expire_trials" in vedium_hooks.scheduler_events["daily"]
    assert "vedium_core.lgpd._audit_pending_requests" in vedium_hooks.scheduler_events["weekly"]
    assert "vedium_core.reports.send_weekly_digest" in vedium_hooks.scheduler_events["cron"]["0 11 * * 1"]

    # DocType custom de push subscription precisa existir e estar plugado
    # no install.py (mesmo padrão de ensure_candidatura_doctype).
    push_py = (ROOT / "vedium_core" / "vedium_core" / "push_notifications.py").read_text(encoding="utf-8")
    install_py = (ROOT / "vedium_core" / "vedium_core" / "install.py").read_text(encoding="utf-8")
    assert "def ensure_push_subscription_doctype" in push_py
    assert "ensure_push_subscription_doctype" in install_py

    # Custom fields de onboarding e VAPID precisam estar no setup idempotente.
    custom_setup_py = (ROOT / "vedium_core" / "vedium_core" / "custom_setup.py").read_text(encoding="utf-8")
    for fieldname in [
        "custom_preferred_language",
        "custom_learning_goal",
        "custom_study_frequency",
        "custom_onboarding_done",
        "custom_vedium_vapid_public_key",
        "custom_vedium_vapid_private_key",
    ]:
        assert fieldname in custom_setup_py

    # push-notifications.js precisa estar carregado no site inteiro.
    assert "js/push-notifications.js" in hooks_src


def test_menu_links_respect_current_language_not_just_labels():
    """Bug real reportado pelo usuário (2026-07-03, ver memória
    project_i18n_language_switcher_reset_bug): em /en/sobre (ou qualquer
    página traduzida), clicar em um link do menu (ex. FAQ) voltava pra
    versão em português (href="/faq") em vez de ir pra /en/faq -- só o
    RÓTULO do menu era traduzido (vd_menu_t), o HREF continuava
    hardcoded em PT. Corrigido em 2026-07-06 com um segundo dict
    (vd_menu_u) que resolve o href certo por idioma, e generalizando a
    detecção de vd_nav.current pra além do binário en/pt-br (agora
    também es/fr/de, e aceita tanto o alt_langs dict de curso.py quanto
    o alt_lang_url singular das páginas institucionais).
    """
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")

    # vd_nav.current generalizado -- não mais só "en"/"pt-br"
    assert 'lang if lang in ("en", "es", "fr", "de", "ru") else "pt-br"' in navbar
    assert "alt_langs" in navbar

    # Cada link do menu usa vd_menu_u (href por idioma), não mais um
    # caminho PT fixo -- e o rótulo continua vindo de vd_menu_t.
    for key in ("home", "how", "about", "courses", "blog", "faq", "contact"):
        assert f'href="{{{{ vd_menu_u.{key} }}}}"' in navbar

    assert 'href="{{ vd_menu_u.free_test }}"' in navbar

    # Dict de URLs por idioma cobre as 5 famílias e cada uma resolve pro
    # slug certo (mesmo slug em en/es/fr/de para as páginas institucionais
    # com tradução real; blog fica sempre em PT, teste de nível usa um
    # slug DIFERENTE por idioma).
    links_dict = navbar.split("vd_menu_links = {")[1].split("\n} %}")[0]
    for lang, home, faq_path, free_test in [
        ("pt-br", "/", "/faq", "/teste-de-nivel"),
        ("en", "/en/", "/en/faq", "/en/portuguese-placement-test"),
        ("es", "/es/", "/es/faq", "/es/prueba-de-nivel-de-portugues"),
        ("fr", "/fr/", "/fr/faq", "/fr/test-de-niveau-de-portugais"),
        ("de", "/de/", "/de/faq", "/de/portugiesisch-einstufungstest"),
    ]:
        block = links_dict.split(f'"{lang}": {{')[1].split("},\n")[0]
        assert f'"home": "{home}"' in block
        assert f'"faq": "{faq_path}"' in block
        assert f'"free_test": "{free_test}"' in block


def test_footer_links_and_labels_respect_current_language():
    """Mesma classe de bug do menu (ver
    test_menu_links_respect_current_language_not_just_labels), mas no
    rodapé (site_footer.html): título, rótulos de link e hrefs eram
    100% hardcoded em português, mesmo em páginas já traduzidas -- o
    menu tinha sido corrigido primeiro (2026-07-06) e o rodapé nunca
    tinha NENHUMA lógica de idioma, nem pros rótulos.

    Corrigido: vd_footer_i18n traduz título/rótulos por idioma;
    vd_footer_urls corrige o href SÓ pras rotas com tradução real de
    mesmo slug (mesmo racional do menu) -- páginas de nicho (clusters
    SEO, blog, termos/privacidade/cookies) continuam apontando pro PT
    de propósito, porque não existe tradução real pra apontar.
    """
    footer = (TPL / "site_footer.html").read_text(encoding="utf-8")

    # vd_footer_lang recalculado de forma independente (não reaproveita
    # vd_nav do navbar -- includes Jinja não compartilham "set" entre si).
    assert "vd_footer_lang" in footer
    assert 'lang in ("en", "es", "fr", "de", "ru")' in footer

    # Rótulos traduzidos pras 5 famílias, incluindo o título de cada coluna.
    i18n_dict = footer.split("vd_footer_i18n = {")[1].split("\n} %}")[0]
    for lang, courses_title, support_title in [
        ("pt-br", "Cursos de Idiomas", "Suporte"),
        ("en", "Language Courses", "Support"),
        ("es", "Cursos de Idiomas", "Soporte"),
        ("fr", "Cours de Langues", "Assistance"),
        ("de", "Sprachkurse", "Support"),
    ]:
        block = i18n_dict.split(f'"{lang}": {{')[1].split("},\n")[0]
        assert f'"courses_title": "{courses_title}"' in block
        assert f'"support_title": "{support_title}"' in block

    # Hrefs corrigidos por idioma pras rotas com tradução real.
    urls_dict = footer.split("vd_footer_urls = {")[1].split("\n} %}")[0]
    for lang, faq_path, empresas_path in [
        ("pt-br", "/faq", "/empresas"),
        ("en", "/en/faq", "/en/empresas"),
        ("es", "/es/faq", "/es/empresas"),
        ("fr", "/fr/faq", "/fr/empresas"),
        ("de", "/de/faq", "/de/empresas"),
    ]:
        block = urls_dict.split(f'"{lang}": {{')[1].split("},\n")[0]
        assert f'"faq": "{faq_path}"' in block
        assert f'"empresas": "{empresas_path}"' in block

    # 2026-07-06 (2ª rodada): links de nicho (páginas pilar SEO tipo
    # curso-de-ingles-online) TAMBÉM têm tradução real, só que com um
    # slug DIFERENTE por idioma (LANDINGS[...]["alt"], não
    # SAME_SLUG_TRANSLATIONS) -- resolvidos via vd_footer_u.get(chave,
    # fallback pt) pra não quebrar quando a tradução não existir
    # (ex.: ioruba-cultura-e-ancestralidade não tem fr/de ainda).
    cluster_urls = footer.split("vd_footer_urls = {")[1].split("\n} %}")[0]
    for lang, english_online, yoruba_online in [
        ("pt-br", "/curso-de-ingles-online", "/curso-de-ioruba-online"),
        ("en", "/en/learn-english-online", "/en/learn-yoruba-online"),
        ("es", "/es/curso-de-ingles-online-en-vivo", "/es/curso-de-yoruba-online"),
        ("fr", "/fr/cours-anglais-en-ligne-en-direct", None),
        ("de", "/de/englischkurs-online-live", None),
    ]:
        block = cluster_urls.split(f'"{lang}": {{')[1].split("},\n")[0]
        assert f'"cluster-english-online": "{english_online}"' in block
        if yoruba_online:
            assert f'"cluster-yoruba-online": "{yoruba_online}"' in block
        else:
            # fr/de não têm tradução real desse cluster ainda -- a chave
            # não deve existir (o .get() no template cai pro PT sozinho).
            assert '"cluster-yoruba-online"' not in block

    # Blog index e termos/privacidade/cookies continuam sem tradução real
    # em nenhum idioma -- ficam sempre em PT, comportamento intencional.
    assert '<a href="/blog">' in footer
    assert '<a href="/termos">' in footer
    assert '<a href="/quanto-custa-curso-de-idiomas">' in footer
    assert '<a href="/teste-de-nivel-ingles">' in footer
    assert '"courses_title": "Языковые курсы"' in footer
    assert '"cluster-ple": "/ru/portugalskiy-dlya-inostrantsev"' in footer


def test_translated_landings_translate_shared_chrome_and_keep_header_on_one_row():
    landing_tpl = (TPL / "marketing_landing.html").read_text(encoding="utf-8")
    navbar = (TPL / "site_navbar.html").read_text(encoding="utf-8")

    for lang in ("en", "es", "fr", "de", "ru"):
        assert f'"{lang}": {{' in landing_tpl

    # Rótulos que antes apareciam em português nas páginas ES/FR/DE/RU.
    for translated_label in (
        '"summary": "Resumen del programa"',
        '"summary": "Résumé du parcours"',
        '"summary": "Kursübersicht"',
        '"summary": "Кратко о программе"',
    ):
        assert translated_label in landing_tpl

    # Uma landing estrangeira sem teste traduzido não pode cair no teste PT.
    assert '(landing.lang or "pt-BR") == "pt-BR"' in landing_tpl
    assert '"es": {"home": "/es/", "courses": "/es/catalogo"}' in landing_tpl
    assert '"ru": {"home": "/ru/", "courses": "/ru/catalogo"}' in landing_tpl

    # Evita o CTA espanhol cair na segunda linha do cabeçalho desktop.
    assert ".main-menu__inner { flex-wrap: nowrap; gap: 16px; }" in navbar
    assert "margin-left: clamp(16px, 1.55vw, 30px)" in navbar
    assert '"ru": {"home": "Главная"' in navbar

    cookie_js = (ROOT / "vedium_core" / "vedium_core" / "public" / "js" / "cookie-consent.js").read_text(encoding="utf-8")
    for lang in ("pt", "en", "es", "fr", "de", "ru"):
        assert f"    {lang}: {{" in cookie_js
    assert "Usamos cookies para mejorar tu experiencia" in cookie_js
    assert "Мы используем файлы cookie" in cookie_js


def test_russian_cluster_has_reciprocal_hreflang_and_real_pages():
    """Rollout russo (5º idioma da sequência en->es->fr->de->ru->zh,
    2026-07-06): 12 landings novas cobrindo os 3 clusters (Inglês, Iorubá,
    Português para Estrangeiros). Trava par PT<->RU via `alt` (que agora
    também carrega "ru" nas entradas pt-BR/en/es/fr/de correspondentes),
    slugs em transliteração/inglês (não em cirílico, por suporte de
    ferramentas), test_url coerente com a convenção (só Inglês/PLE têm
    teste formal; Iorubá usa None) e paridade de profundidade de conteúdo.
    """
    # Só as landings principais (curso "guarda-chuva" de cada cluster e as
    # que citam explicitamente teste-de-nivel/portugiesisch-einstufungstest
    # no PT/DE de origem) setam "test_url" explícito; as landings de nicho
    # (entrevista, programadores, executivo, viagens, atendimento) herdam o
    # fallback do template `marketing_landing.html`, sem chave própria —
    # mesmo padrão já usado no cluster alemão de origem.
    pairs_with_explicit_test_url = [
        ("curso-de-ingles-online", "kurs-angliyskogo-online", None),
        ("curso-de-ioruba-online", "kurs-yoruba-online", None),
        ("ioruba-para-iniciantes", "yoruba-dlya-nachinayushchikh", None),
        ("ioruba-cultura-e-ancestralidade", "yoruba-kultura-i-nasledie", None),
        ("portugues-para-estrangeiros", "portugalskiy-dlya-inostrantsev", None),
        ("portugues-para-executivos", "portugalskiy-dlya-rukovoditeley", None),
    ]
    pairs_without_explicit_test_url = [
        ("ingles-para-entrevista", "angliyskiy-dlya-sobesedovaniy"),
        ("ingles-para-programadores", "angliyskiy-dlya-programmistov"),
        ("ingles-executivo", "biznes-angliyskiy-online"),
        ("ingles-para-viagens", "angliyskiy-dlya-puteshestviy"),
        ("ingles-para-atendimento-ao-cliente", "angliyskiy-dlya-podderzhki-klientov"),
        ("preparatorio-celpe-bras", "podgotovka-k-celpe-bras"),
    ]
    pairs = [(pt, ru, url) for pt, ru, url in pairs_with_explicit_test_url]
    for pt_slug, ru_slug, expected_test_url in pairs:
        assert LANDINGS[pt_slug]["alt"]["ru"] == ru_slug
        assert LANDINGS[ru_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[ru_slug]["alt"]["ru"] == ru_slug
        assert LANDINGS[ru_slug]["lang"] == "ru"
        assert "test_url" in LANDINGS[ru_slug], f"{ru_slug} precisa de test_url explícito"
        assert LANDINGS[ru_slug]["test_url"] == expected_test_url

    for pt_slug, ru_slug in pairs_without_explicit_test_url:
        assert LANDINGS[pt_slug]["alt"]["ru"] == ru_slug
        assert LANDINGS[ru_slug]["alt"]["pt-BR"] == pt_slug
        assert LANDINGS[ru_slug]["alt"]["ru"] == ru_slug
        assert LANDINGS[ru_slug]["lang"] == "ru"
        pairs.append((pt_slug, ru_slug, None))

        ru_html = (WWW / "ru" / f"{ru_slug}.html").read_text(encoding="utf-8")
        assert ru_html.strip().splitlines()[0] == (
            f'{{% set landing = get_marketing_landing("{ru_slug}") %}}'
        )
        assert '{% include "templates/includes/marketing_landing.html" %}' in ru_html

        # conteúdo real, não placeholder (mesmo padrão de profundidade das outras landings)
        landing = LANDINGS[ru_slug]
        assert len(landing["pain_points"]) >= 4
        assert len(landing["outcomes"]) >= 4
        assert len(landing["modules"]) >= 6
        assert len(landing["faqs"]) >= 4
        assert len(landing["lead"]) > 100


def test_russian_course_translations_exist_for_yoruba_and_ple():
    """Cursos individuais de Iorubá e PLE (público não-lusófono) ganharam
    bloco "ru" em COURSE_TRANSLATIONS no rollout russo. www/curso.py precisa
    reconhecer o prefixo /ru/curso/<slug> e ter a rota registrada em
    hooks.py (mesmo padrão de en/es/fr/de)."""
    from vedium_core.course_translations import COURSE_TRANSLATIONS

    course_slugs = [
        "iorub-b-sico",
        "iorub-intermedi-rio",
        "iorub-avan-ado",
        "portugues-para-estrangeiros-basico",
        "portugues-para-estrangeiros-intermediario",
        "portugues-para-estrangeiros-avancado",
    ]
    for slug in course_slugs:
        assert "ru" in COURSE_TRANSLATIONS[slug], f"{slug} precisa de tradução ru"
        entry = COURSE_TRANSLATIONS[slug]["ru"]
        assert entry["title"]
        assert entry["short_introduction"]
        assert entry["description"]

    curso_py = (WWW / "curso.py").read_text(encoding="utf-8")
    assert '"en", "es", "fr", "de", "ru"' in curso_py

    hooks_src = (ROOT / "vedium_core" / "vedium_core" / "hooks.py").read_text(encoding="utf-8")
    assert '{"from_route": "/ru/curso/<course>", "to_route": "curso"}' in hooks_src


def test_russian_carreiras_page_matches_pt_structure_with_reciprocal_hreflang():
    """2026-07-15: ru/carreiras.html estava desatualizada (extends web.html +
    frappe.call(), sem breadcrumb/title/description próprios). Reescrita no
    mesmo padrão estrutural do par PT (fetch() nativo, hreflang de 6 idiomas,
    BreadcrumbList, título/descrição via contexto) -- trava aqui pra não
    regredir pro modelo antigo."""
    ru_html = (WWW / "ru" / "carreiras.html").read_text(encoding="utf-8")
    ru_py = (WWW / "ru" / "carreiras.py").read_text(encoding="utf-8")

    assert '{% extends "templates/web.html" %}' not in ru_html
    assert "frappe.call(" not in ru_html
    assert '<html lang="ru">' in ru_html

    for lang, prefix in (
        ("pt-br", ""), ("en", "/en"), ("es", "/es"), ("fr", "/fr"),
        ("de", "/de"), ("ru", "/ru"),
    ):
        assert f'hreflang="{lang}" href="https://vediums.com{prefix}/carreiras"' in ru_html
    assert 'hreflang="x-default" href="https://vediums.com/carreiras"' in ru_html
    assert '<link rel="canonical" href="https://vediums.com/ru/carreiras" />' in ru_html

    assert '"item":"https://vediums.com/ru"' in ru_html
    assert '"item":"https://vediums.com/ru/carreiras"' in ru_html

    assert "vedium_core.careers.submit_candidatura" in ru_html
    assert "fetch(" in ru_html
    assert "X-Frappe-CSRF-Token" in ru_html

    # rótulos/mensagens já traduzidos preservados
    assert "Полное имя *" in ru_html
    assert "Отправить заявку" in ru_html
    assert "Заявка отправлена!" in ru_html
    assert "Пожалуйста, заполните имя и email." in ru_html

    # links internos novos apontando pro cluster ru já existente
    assert 'href="/ru/sobre"' in ru_html
    assert 'href="/ru/como-funciona"' in ru_html
    assert 'href="/ru/faq"' in ru_html
    assert 'href="/ru/contato"' in ru_html

    assert 'set_careers_seo_context(context, "ru")' in ru_py
    assert "context.title" in ru_py
    assert "context.description" in ru_py
    assert "Преподаватель йоруба" in ru_py
