"""Camada de dados REAIS para a Home V2 (Fase C da missão de integração).

Módulo NOVO, isolado -- não modifica `blog_content.py`. Serve de ponte entre
os dados reais já existentes (posts de blog) e o formato que os macros V2
esperam (`v2e.v2_insights_editorial`), usado pelo preview
(`www/design_system_v2.py`), pela rota técnica (`www/_home_v2.py`) e, desde
a Fase C.1.4 (cutover controlado), pela própria Home real (`www/index.py`)
-- a mesma seleção real roda nos três lugares, via `build_home_v2_context()`.

Achado real desta fase: `blog_content.list_blog_posts()` combina posts de
código (`BLOG_POSTS`) com posts publicados pelo painel (doctype "Vedium
Blog Post"), mas esse doctype não está migrado neste ambiente de dev local
(`DoesNotExistError: DocType Vedium Blog Post não foi encontrado` --
confirmado via `bench console`). `get_insights_selection()` tenta a função
real primeiro (comportamento correto em produção, onde o doctype existe) e
cai para os posts de código (97 de ~100+ posts reais, não fabricados) só
se a consulta falhar -- nunca mostra dado fake, só reduz a fonte quando o
ambiente não tem a segunda fonte disponível.
"""

import frappe


def build_home_v2_context(context):
    """Monta a parte de DADOS do context compartilhada entre `/` (Home real,
    indexavel, Fase C.1.4) e `/_home_v2` (rota tecnica noindex) -- a mesma
    selecao de blog e a mesma HomeCourseCollection nos dois lugares. Cada
    chamador continua responsavel pelos campos que DIFEREM entre as duas
    rotas (robots/canonical_url/title/no_sitemap) -- ver www/index.py e
    www/_home_v2.py. "Template compartilhado + context compartilhado, minimo
    de duplicacao" (Fase C.1.4, secao 5 da missao)."""
    from vedium_core.home_course_collection import get_home_course_collection, get_course_index_entries

    featured, secondary = get_insights_selection()
    context.insights_featured = to_insight_macro_dict(featured)
    context.insights_secondary = [to_insight_macro_dict(c) for c in secondary]
    context.home_courses = get_home_course_collection()
    context.course_index_entries = get_course_index_entries()
    return context


def get_insights_selection():
    """Retorna (featured, secondary_list[2]) com os posts reais mais
    recentes em pt-BR, priorizando variedade de categoria nos 2
    secundários (regra determinística simples, sem algoritmo de
    recomendação -- ver docs/redesign/26-home-v2-integration.md)."""
    from vedium_core.blog_content import BLOG_POSTS, _post_card

    try:
        from vedium_core.blog_content import list_blog_posts

        cards = list_blog_posts()
    except Exception:
        frappe.logger("v2_home_data").info(
            "list_blog_posts() falhou (provável doctype 'Vedium Blog Post' "
            "não migrado neste ambiente) -- usando só BLOG_POSTS (posts de código)."
        )
        cards = [_post_card(slug, post) for slug, post in BLOG_POSTS.items()]

    pt_cards = [
        c for c in cards
        if c.get("lang", "pt-BR") == "pt-BR" and c.get("date") and c.get("url") and c.get("title")
    ]
    pt_cards.sort(key=lambda c: c["date"], reverse=True)

    if not pt_cards:
        return None, []

    featured = pt_cards[0]
    secondary = []
    seen_tags = {featured.get("tag")}
    for c in pt_cards[1:]:
        if c.get("tag") not in seen_tags:
            secondary.append(c)
            seen_tags.add(c.get("tag"))
        if len(secondary) == 2:
            break
    if len(secondary) < 2:
        for c in pt_cards[1:]:
            if c not in secondary and c is not featured:
                secondary.append(c)
            if len(secondary) == 2:
                break

    return featured, secondary


def to_insight_macro_dict(card):
    """Adapta o formato real de `_post_card`/`list_blog_posts()`
    (title/meta_description/url/tag/date_display) pro formato que
    `v2e.v2_insights_editorial` espera (title/summary/href/category/date)
    -- só remapeamento de chaves, nenhum dado inventado."""
    if not card:
        return None
    return {
        "title": card.get("title"),
        "summary": card.get("meta_description") or "",
        "href": card.get("url"),
        "category": card.get("tag"),
        "date": card.get("date_display") or card.get("date") or "",
    }


# Matriz de encaminhamento do Pathfinder (idioma + objetivo -> URL real).
# Fonte única de verdade documentada em
# docs/redesign/26-home-v2-integration.md -- espelhada em JS
# (design-system-v2.js, PATHFINDER_MATRIX) pra funcionar client-side sem
# round-trip ao servidor. Toda URL abaixo foi validada com HTTP 200 nesta
# fase (ver doc 26). Nunca uma URL inventada -- combinação sem página
# objetivo-específica cai na página-pilar do idioma.
PATHFINDER_MATRIX = {
    "Inglês": {
        "_pillar": "/curso-de-ingles-online",
        "Trabalho e carreira": "/ingles-executivo",
        "Comunicação cotidiana": "/curso-de-ingles-online",
        "Viagens": "/ingles-para-viagens",
        "Estudos e cultura": "/curso-de-ingles-online",
        "Viver e trabalhar no Brasil": "/curso-de-ingles-online",
    },
    "Iorubá": {
        "_pillar": "/curso-de-ioruba-online",
        "Trabalho e carreira": "/curso-de-ioruba-online",
        "Comunicação cotidiana": "/curso-de-ioruba-online",
        "Viagens": "/curso-de-ioruba-online",
        "Estudos e cultura": "/ioruba-cultura-e-ancestralidade",
        "Viver e trabalhar no Brasil": "/curso-de-ioruba-online",
    },
    "Português para Estrangeiros": {
        "_pillar": "/portugues-para-estrangeiros",
        "Trabalho e carreira": "/portugues-para-executivos",
        "Comunicação cotidiana": "/portugues-para-estrangeiros",
        "Viagens": "/portugues-para-estrangeiros",
        "Estudos e cultura": "/preparatorio-celpe-bras",
        "Viver e trabalhar no Brasil": "/portugues-para-estrangeiros",
    },
    "Espanhol": {
        "_pillar": "/curso-de-espanhol-online",
        "Trabalho e carreira": "/curso-de-espanhol-online",
        "Comunicação cotidiana": "/curso-de-espanhol-online",
        "Viagens": "/curso-de-espanhol-online",
        "Estudos e cultura": "/curso-de-espanhol-online",
        "Viver e trabalhar no Brasil": "/curso-de-espanhol-online",
    },
    "Hebraico": {
        "_pillar": "/curso-de-hebraico-online",
        "Trabalho e carreira": "/curso-de-hebraico-online",
        "Comunicação cotidiana": "/curso-de-hebraico-online",
        "Viagens": "/curso-de-hebraico-online",
        "Estudos e cultura": "/curso-de-hebraico-online",
        "Viver e trabalhar no Brasil": "/curso-de-hebraico-online",
    },
}
