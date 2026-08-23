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


def get_course_navigation(course_name):
    """Return previous/next links for a course with a defined linear trail.

    Only the English A1→C1 trail is defined here. Hebrew includes different
    products (modern, biblical and private), while the other language trails
    need their own approved labels before they can safely share this pattern.
    Courses without a defined trail intentionally return ``None``.
    """
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
