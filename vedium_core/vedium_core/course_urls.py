"""Canonical public URLs for LMS courses.

LMS Course names are database identifiers referenced by enrollments, payments,
chapters and Raven. Public slugs may evolve independently so SEO migrations do
not require renaming those records.
"""

COURSE_PUBLIC_SLUGS = {
    "ingl-s-beginner": "ingles-basico-a1",
    "ingl-s-elementary": "ingles-elementar-a2",
    "ingl-s-pr-intermedi-rio": "ingles-pre-intermediario",
    "ingl-s-intermedi-rio": "ingles-intermediario-b1",
    "ingl-s-upper-intermedi-rio": "ingles-intermediario-superior-b2",
    "ingl-s-avan-ado": "ingles-avancado-c1",
    "iorub-b-sico": "ioruba-basico",
    "iorub-intermedi-rio": "ioruba-intermediario",
    "iorub-avan-ado": "ioruba-avancado",
    "espanhol-basico": "espanhol-basico",
    "espanhol-intermediario": "espanhol-intermediario",
    "espanhol-avancado": "espanhol-avancado",
    "hebraico-a0-alfabetizacao": "hebraico-a0-alfabetizacao",
    "hebraico-moderno-a1": "hebraico-moderno-a1",
    "hebraico-moderno-a2-b1": "hebraico-moderno-a2-b1",
    "hebraico-biblico-leitura-guiada": "hebraico-biblico-leitura-guiada",
    "hebraico-particular": "hebraico-particular",
    "portugues-para-estrangeiros-basico": "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario": "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado": "portugues-para-estrangeiros-avancado",
}

PUBLIC_TO_INTERNAL = {public: internal for internal, public in COURSE_PUBLIC_SLUGS.items()}


# A ordem desta trilha vem da própria fonte canônica de slugs. Os rótulos
# seguem a progressão CEFR aprovada pelo proprietário em 2026-08-23.
ENGLISH_COURSE_NAV_LABELS = {
    "ingl-s-beginner": "Inglês A1 — Iniciante",
    "ingl-s-elementary": "Inglês A2 — Elementar",
    "ingl-s-pr-intermedi-rio": "Inglês A2+ — Pré-Intermediário",
    "ingl-s-intermedi-rio": "Inglês B1 — Intermediário",
    "ingl-s-upper-intermedi-rio": "Inglês B2 — Intermediário Superior",
    "ingl-s-avan-ado": "Inglês C1 — Avançado",
}

ENGLISH_COURSE_LEVELS = {
    "ingl-s-beginner": "A1",
    "ingl-s-elementary": "A2",
    "ingl-s-pr-intermedi-rio": "A2+",
    "ingl-s-intermedi-rio": "B1",
    "ingl-s-upper-intermedi-rio": "B2",
    "ingl-s-avan-ado": "C1",
}

ENGLISH_COURSE_SEO_TITLES = {
    "ingl-s-beginner": "Inglês A1 Iniciante Online ao Vivo | Vedium",
    "ingl-s-elementary": "Inglês A2 Elementar Online ao Vivo | Vedium",
    "ingl-s-pr-intermedi-rio": "Inglês A2+ Pré-Intermediário Online | Vedium",
    "ingl-s-intermedi-rio": "Inglês B1 Intermediário Online ao Vivo | Vedium",
    "ingl-s-upper-intermedi-rio": "Inglês B2 Intermediário Superior Online | Vedium",
    "ingl-s-avan-ado": "Inglês C1 Avançado Online ao Vivo | Vedium",
}

PLE_LEVEL_TEST_URLS = {
    "pt-BR": "/teste-de-nivel",
    "en": "/en/portuguese-placement-test",
    "es": "/es/prueba-de-nivel-de-portugues",
    "fr": "/fr/test-de-niveau-de-portugais",
    "de": "/de/portugiesisch-einstufungstest",
}

# Trilha linear dos 3 níveis de PLE (Português para Estrangeiros). Nome
# interno == slug público pra essa família (ver COURSE_PUBLIC_SLUGS acima).
PLE_COURSE_TRACK = [
    "portugues-para-estrangeiros-basico",
    "portugues-para-estrangeiros-intermediario",
    "portugues-para-estrangeiros-avancado",
]

# Rótulos curtos pro card de navegação e o "nível" usado no Schema Course
# (educationalLevel) e no breadcrumb. Só nos 5 idiomas com chrome próprio em
# curso.html (o dict UI de lá não tem "ru" — cursos em russo herdam o chrome
# em pt-BR, mesma lacuna pré-existente do restante da página).
PLE_COURSE_NAV_I18N = {
    "pt-BR": {
        "portugues-para-estrangeiros-basico": {"level": "Básico", "label": "PLE — Básico"},
        "portugues-para-estrangeiros-intermediario": {"level": "Intermediário", "label": "PLE — Intermediário"},
        "portugues-para-estrangeiros-avancado": {"level": "Avançado", "label": "PLE — Avançado"},
    },
    "en": {
        "portugues-para-estrangeiros-basico": {"level": "Basic", "label": "PLE — Basic"},
        "portugues-para-estrangeiros-intermediario": {"level": "Intermediate", "label": "PLE — Intermediate"},
        "portugues-para-estrangeiros-avancado": {"level": "Advanced", "label": "PLE — Advanced"},
    },
    "es": {
        "portugues-para-estrangeiros-basico": {"level": "Básico", "label": "PLE — Básico"},
        "portugues-para-estrangeiros-intermediario": {"level": "Intermedio", "label": "PLE — Intermedio"},
        "portugues-para-estrangeiros-avancado": {"level": "Avanzado", "label": "PLE — Avanzado"},
    },
    "fr": {
        "portugues-para-estrangeiros-basico": {"level": "Débutant", "label": "PLE — Débutant"},
        "portugues-para-estrangeiros-intermediario": {"level": "Intermédiaire", "label": "PLE — Intermédiaire"},
        "portugues-para-estrangeiros-avancado": {"level": "Avancé", "label": "PLE — Avancé"},
    },
    "de": {
        "portugues-para-estrangeiros-basico": {"level": "Grundstufe", "label": "PLE — Grundstufe"},
        "portugues-para-estrangeiros-intermediario": {"level": "Mittelstufe", "label": "PLE — Mittelstufe"},
        "portugues-para-estrangeiros-avancado": {"level": "Fortgeschritten", "label": "PLE — Fortgeschritten"},
    },
}

# Landing (pilar) de cada idioma pra onde a trilha de PLE aponta.
PLE_PILLAR_I18N = {
    "pt-BR": {
        "breadcrumb_label": "Português para Estrangeiros",
        "url": "/portugues-para-estrangeiros",
    },
    "en": {
        "breadcrumb_label": "Portuguese for Foreigners",
        "url": "/en/learn-portuguese-brazil",
    },
    "es": {
        "breadcrumb_label": "Portugués para Extranjeros",
        "url": "/es/portugues-para-extranjeros",
    },
    "fr": {
        "breadcrumb_label": "Portugais pour Étrangers",
        "url": "/fr/portugais-pour-etrangers",
    },
    "de": {
        "breadcrumb_label": "Portugiesisch für Ausländer",
        "url": "/de/portugiesisch-fuer-auslaender",
    },
}

# x-default: pro cluster de PLE, o público-alvo por definição não fala
# português, então o fallback pra buscas sem hreflang correspondente deve
# ser a versão em inglês (não pt-BR, que é a regra padrão dos outros
# clusters — ver get_marketing_landing() e get_context() em curso.py).
COURSE_X_DEFAULT_LANG = {
    "portugues-para-estrangeiros-basico": "en",
    "portugues-para-estrangeiros-intermediario": "en",
    "portugues-para-estrangeiros-avancado": "en",
}


def get_public_course_slug(course_name):
    return COURSE_PUBLIC_SLUGS.get(course_name, course_name)


def get_internal_course_name(public_or_internal_slug):
    return PUBLIC_TO_INTERNAL.get(public_or_internal_slug, public_or_internal_slug)


def get_course_url(course_name, lang=None):
    slug = get_public_course_slug(course_name)
    prefix = f"/{lang}" if lang else ""
    return f"{prefix}/curso/{slug}"


def get_course_seo_title(course_name, course_title):
    """Return a concise title for English levels without renaming LMS data."""
    return ENGLISH_COURSE_SEO_TITLES.get(
        course_name,
        f"{course_title} — Curso de Idiomas Online ao Vivo | Vedium",
    )


def get_course_level_destination(course_name, lang="pt-BR"):
    """Return the valid diagnostic destination and whether it is contact."""
    public_slug = get_public_course_slug(course_name)
    if public_slug.startswith("ingles-"):
        return "/teste-de-nivel-ingles", False
    if public_slug.startswith("portugues-para-estrangeiros-"):
        return PLE_LEVEL_TEST_URLS.get(lang, "/teste-de-nivel"), False
    if public_slug.startswith(("ioruba-", "espanhol-", "hebraico-")):
        prefix = "" if lang == "pt-BR" else f"/{lang}"
        return f"{prefix}/contato", True
    return None, False


def get_course_navigation(course_name, lang=None):
    """Return previous/next links for a course with a defined linear trail.

    Two trails are defined here: English (A1→C1) and PLE (Básico→Avançado).
    Hebrew includes different products (modern, biblical and private), while
    the other language trails need their own approved labels before they can
    safely share this pattern. Courses without a defined trail intentionally
    return ``None``.

    ``lang`` only affects the PLE trail (English course pages only exist in
    pt-BR — there is no COURSE_TRANSLATIONS entry for them, so req_lang is
    always None when this runs for an English course).
    """
    if course_name in PLE_COURSE_TRACK:
        return _get_ple_navigation(course_name, lang)

    english_track = [
        internal
        for internal, public_slug in COURSE_PUBLIC_SLUGS.items()
        if public_slug.startswith("ingles-")
    ]
    if course_name not in english_track:
        return None

    position = english_track.index(course_name)

    def _link(index):
        internal = english_track[index]
        return {
            "label": ENGLISH_COURSE_NAV_LABELS[internal],
            "url": get_course_url(internal),
        }

    return {
        "current": {
            **_link(position),
            "level": ENGLISH_COURSE_LEVELS[course_name],
        },
        "previous": _link(position - 1) if position > 0 else None,
        "next": _link(position + 1) if position < len(english_track) - 1 else None,
        "pillar": {
            "label": "Curso de inglês online ao vivo do A1 ao C1",
            "breadcrumb_label": "Inglês",
            "url": "/curso-de-ingles-online",
        },
    }


def _get_ple_navigation(course_name, lang):
    nav_lang = lang if lang in PLE_COURSE_NAV_I18N else "pt-BR"
    labels = PLE_COURSE_NAV_I18N[nav_lang]
    url_lang = None if nav_lang == "pt-BR" else nav_lang
    position = PLE_COURSE_TRACK.index(course_name)

    def _link(index):
        internal = PLE_COURSE_TRACK[index]
        return {
            "label": labels[internal]["label"],
            "url": get_course_url(internal, url_lang),
        }

    return {
        "current": {
            **_link(position),
            "level": labels[course_name]["level"],
        },
        "previous": _link(position - 1) if position > 0 else None,
        "next": _link(position + 1) if position < len(PLE_COURSE_TRACK) - 1 else None,
        "pillar": PLE_PILLAR_I18N[nav_lang],
    }


def get_course_x_default_lang(course_name):
    """Language override for hreflang x-default on this course's detail page.

    Returns None when the family should keep the site-wide default (pt-BR).
    """
    return COURSE_X_DEFAULT_LANG.get(course_name)


def legacy_course_redirects():
    redirects = []
    for internal, public in COURSE_PUBLIC_SLUGS.items():
        if internal == public:
            continue
        redirects.append({"source": f"/curso/{internal}", "target": get_course_url(internal)})
        for lang in ("en", "es", "fr", "de", "ru"):
            redirects.append({
                "source": f"/{lang}/curso/{internal}",
                "target": get_course_url(internal, lang),
            })
    return redirects
