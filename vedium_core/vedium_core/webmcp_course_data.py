"""Course data service para o piloto WebMCP (Fase C.2 da missao).

Fonte UNICA -- nao cria nenhuma segunda base de dados paralela a Home.
Reutiliza tres modulos ja existentes e ja usados pela Home real:

  - home_course_collection.get_home_course_collection() (copy/URL/eyebrow
    ja aprovados, mesmos usados na secao "Cursos" da Home V2);
  - course_urls.py (ENGLISH_COURSE_LEVELS/PLE_COURSE_TRACK/
    get_course_level_destination -- a mesma logica que gera a navegacao
    real em curso.html);
  - catalog_registry.CATALOG (titulos reais dos 20 cursos -- usado aqui
    SOMENTE para os titulos de nivel de Iorubá/Espanhol/Hebraico, que nao
    tem uma trilha CEFR estruturada em course_urls.py; nenhum campo de
    preco deste catalogo e exposto).

get_webmcp_course_data() retorna um dict serializavel que e embutido como
JSON na Home (ver v2_home_data.build_home_v2_context) -- tanto a UI humana
(Pathfinder, via design-system-v2.js) quanto as WebMCP tools (webmcp.js)
leem exatamente este mesmo bloco. Ver docs/redesign/50-webmcp-pilot-architecture.md.
"""

# Enum publico das WebMCP tools (contrato da missao C.2, secao 5/19: o
# enum de idioma e uma chave em ingles para o consumidor da tool -- isso e
# DIFERENTE do locale da pagina, que continua pt-BR nesta fase piloto).
LANGUAGE_ENUM_TO_KEY = {
    "english": "ingles",
    "yoruba": "ioruba",
    "portuguese_for_foreigners": "portugues_estrangeiros",
    "spanish": "espanhol",
    "hebrew": "hebraico",
}

# course_name (internal, course_urls.COURSE_PUBLIC_SLUGS) representativo
# de cada idioma, usado so pra resolver o proximo passo (teste de nivel vs.
# contato) via course_urls.get_course_level_destination() -- a MESMA regra
# ja usada nas paginas de curso reais.
_REPRESENTATIVE_COURSE = {
    "english": "ingl-s-beginner",
    "yoruba": "iorub-b-sico",
    "portuguese_for_foreigners": "portugues-para-estrangeiros-basico",
    "spanish": "espanhol-basico",
    "hebrew": "hebraico-a0-alfabetizacao",
}

# Trilhas de curso (catalog_registry.CATALOG ids) por idioma sem estrutura
# CEFR propria em course_urls.py -- ver docstring do modulo.
_CATALOG_TRACK_COURSE_IDS = {
    "yoruba": ["iorub-b-sico", "iorub-intermedi-rio", "iorub-avan-ado"],
    "spanish": ["espanhol-basico", "espanhol-intermediario", "espanhol-avancado"],
    "hebrew": [
        "hebraico-a0-alfabetizacao",
        "hebraico-moderno-a1",
        "hebraico-moderno-a2-b1",
        "hebraico-biblico-leitura-guiada",
        "hebraico-particular",
    ],
}

# Iorubá e Espanhol sao trilhas sequenciais (Basico->Intermediario->
# Avancado, como Ingles/PLE). Hebraico NAO e sequencial -- sao produtos
# distintos (Alfabetizacao / Moderno A1 / Moderno A2-B1 / Biblico /
# Particular), confirmado no docstring de course_urls.get_course_navigation()
# ("Hebrew includes different products... need their own approved labels").
_SEQUENTIAL_LANGUAGES = {"english", "portuguese_for_foreigners", "yoruba", "spanish"}


def _english_levels():
    from vedium_core.course_urls import ENGLISH_COURSE_LEVELS, get_course_url

    return [
        {"label": level, "course_name": internal, "url": get_course_url(internal)}
        for internal, level in ENGLISH_COURSE_LEVELS.items()
    ]


def _ple_levels():
    from vedium_core.course_urls import PLE_COURSE_TRACK, PLE_COURSE_NAV_I18N, get_course_url

    labels = PLE_COURSE_NAV_I18N["pt-BR"]
    return [
        {"label": labels[internal]["level"], "course_name": internal, "url": get_course_url(internal)}
        for internal in PLE_COURSE_TRACK
    ]


def _catalog_track_levels(course_ids):
    from vedium_core.catalog_registry import CATALOG
    from vedium_core.course_urls import get_course_url

    return [
        {"label": CATALOG[course_id]["title"], "course_name": course_id, "url": get_course_url(course_id)}
        for course_id in course_ids
    ]


def _get_levels_for(language_enum):
    if language_enum == "english":
        return _english_levels()
    if language_enum == "portuguese_for_foreigners":
        return _ple_levels()
    return _catalog_track_levels(_CATALOG_TRACK_COURSE_IDS[language_enum])


def _get_next_step(language_enum):
    """Reutiliza course_urls.get_course_level_destination() -- a MESMA regra
    que decide, nas paginas de curso reais, se o proximo passo e um teste de
    nivel self-service ou contato. Nunca inventa disponibilidade."""
    from vedium_core.course_urls import get_course_level_destination

    course_name = _REPRESENTATIVE_COURSE[language_enum]
    url, requires_contact = get_course_level_destination(course_name, "pt-BR")
    if requires_contact:
        return {
            "kind": "contact",
            "url": url,
            "text": "O próximo passo recomendado é entrar em contato para uma avaliação inicial.",
        }
    return {
        "kind": "level_test",
        "url": url,
        "text": "O próximo passo recomendado é realizar o teste de nível.",
    }


def get_webmcp_course_data():
    """Monta o bloco de dados compartilhado (courses + pathfinder matrix).

    Retorna um dict JSON-serializavel puro (sem objetos Frappe) -- pronto
    pra `frappe.as_json()` e embutido na Home como data island. Nao muta
    nenhuma das fontes originais.
    """
    from vedium_core.home_course_collection import get_home_course_collection
    from vedium_core import v2_home_data

    by_key = {c["language_key"]: c for c in get_home_course_collection()}

    courses = {}
    for enum, key in LANGUAGE_ENUM_TO_KEY.items():
        home = by_key[key]
        next_step = _get_next_step(enum)
        courses[enum] = {
            "language": enum,
            "display_name": home["display_name"],
            "course_name": home["display_name"],
            "summary": home["description"],
            "level_summary": home["level_summary"],
            "delivery_mode": "Aulas ao vivo, online, com professor.",
            "teacher_profile": "Professores nativos e/ou especialistas, conforme o idioma.",
            "progression": home["level_summary"],
            "url": home["url"],
            "cta_label": home["cta_label"],
            "levels": _get_levels_for(enum),
            "levels_are_sequential": enum in _SEQUENTIAL_LANGUAGES,
            "next_step": next_step,
        }

    language_enum_to_display_name = {enum: courses[enum]["display_name"] for enum in LANGUAGE_ENUM_TO_KEY}

    # Mesmo dict, mesmas chaves (display_name) de v2_home_data.PATHFINDER_MATRIX
    # -- os radios do form humano (v2_pathfinder) ja usam esses display_name
    # como `value`, entao a UI le esta estrutura sem nenhuma conversao.
    pathfinder_matrix_by_display_name = v2_home_data.PATHFINDER_MATRIX

    # Lista de objetivos derivada das proprias chaves da matriz (exclui
    # "_pillar") -- nunca uma segunda lista hardcoded da mesma taxonomia.
    sample_entry = next(iter(pathfinder_matrix_by_display_name.values()))
    pathfinder_goals = [k for k in sample_entry.keys() if k != "_pillar"]

    return {
        "courses": courses,
        "language_enum_to_display_name": language_enum_to_display_name,
        "pathfinder_matrix_by_display_name": pathfinder_matrix_by_display_name,
        "pathfinder_goals": pathfinder_goals,
    }
