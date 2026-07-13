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


def get_public_course_slug(course_name):
    return COURSE_PUBLIC_SLUGS.get(course_name, course_name)


def get_internal_course_name(public_or_internal_slug):
    return PUBLIC_TO_INTERNAL.get(public_or_internal_slug, public_or_internal_slug)


def get_course_url(course_name, lang=None):
    slug = get_public_course_slug(course_name)
    prefix = f"/{lang}" if lang else ""
    return f"{prefix}/curso/{slug}"


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
