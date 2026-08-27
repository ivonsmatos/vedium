"""HomeCourseCollection -- fonte estruturada unica dos 5 blocos de curso
exibidos na secao "Nossos cursos" da Home V2 (Fase C.1.1, Parte B da missao).

Contrato explicito (ver docs/redesign/38-home-course-collection-contract.md):
esta colecao e EDITORIAL/CURADA, versionada em codigo, nao uma agregacao
dinamica por idioma vinda do LMS -- essa agregacao nao existe no sistema
(so Ingles tem curso_urls.ENGLISH_COURSE_LEVELS estruturado; os demais
idiomas nao tem uma fonte por-idioma equivalente, achado documentado desde
a Fase C, docs/redesign/26-home-v2-integration.md secao 3). Curar aqui e
uma decisao aceita explicitamente pela missao C.1.1 (Parte B, secao 10:
"CURATION IS ACCEPTABLE... desde que isso esteja explicito").

Todo copy/URL abaixo e o MESMO ja usado e validado (HTTP 200) desde a Fase
C em templates/includes/v2/home_body.html -- esta migracao NAO reescreve
texto nem muda destino de link, so move a fonte de inline-no-template para
um modulo Python testavel (ver tests/test_pure_home_course_collection.py).
"""

HOME_COURSE_COLLECTION = [
    {
        "slug": "ingles",
        "language_key": "ingles",
        "display_name": "Inglês",
        "eyebrow": "Inglês",
        "level_summary": "Do A1 ao C1",
        "headline": "Inglês para avançar no trabalho, nos estudos e na comunicação.",
        "description": "Aulas ao vivo com professor, prática de conversação e progressão clara por nível.",
        "url": "/curso-de-ingles-online",
        "cta_label": "Conheça o curso",
        "media_key": "e02-study-laptop.jpg",
        "media_alt": (
            "Pessoa adulta concentrada, usando fones de ouvido, estuda em um "
            "notebook e faz anotações em um caderno."
        ),
        "order": 1,
        "is_active": True,
        "reverse": False,
        "band_tone": "white",
        "object_position": "center",
    },
    {
        "slug": "ioruba",
        "language_key": "ioruba",
        "display_name": "Iorubá",
        "eyebrow": "Iorubá",
        "level_summary": "Básico ao avançado",
        "headline": "Língua, oralidade, literatura e história.",
        "description": (
            "Iorubá ensinado com profundidade linguística e seriedade cultural, "
            "do primeiro contato à leitura avançada."
        ),
        "url": "/curso-de-ioruba-online",
        "cta_label": "Conheça o curso",
        "media_key": "e11-ioruba-learning.jpg",
        "media_alt": "Pessoa adulta negra, em ambiente profissional, digita em um notebook.",
        "order": 2,
        "is_active": True,
        "reverse": True,
        "band_tone": "warm",
        "object_position": "center 15%",
    },
    {
        "slug": "portugues-para-estrangeiros",
        "language_key": "portugues_estrangeiros",
        "display_name": "Português para Estrangeiros",
        "eyebrow": "Português para Estrangeiros",
        "level_summary": "Portuguese for life in Brazil",
        "headline": "Português para viver, trabalhar, estudar e se comunicar no Brasil.",
        "description": "Aulas ao vivo para quem precisa se comunicar em português no dia a dia brasileiro.",
        "url": "/portugues-para-estrangeiros",
        "cta_label": "Explore o programa",
        "media_key": "e14-ple-headphones-home.jpg",
        "media_alt": (
            "Pessoa adulta usando fones de ouvido escreve em um caderno em frente "
            "a um notebook, em um ambiente doméstico claro."
        ),
        "order": 3,
        "is_active": True,
        "reverse": False,
        "band_tone": "alt",
        "object_position": "center 20%",
    },
    {
        "slug": "espanhol",
        "language_key": "espanhol",
        "display_name": "Espanhol",
        "eyebrow": "Espanhol",
        "level_summary": "Comunicação com precisão",
        "headline": "Do desenvolvimento inicial à comunicação profissional e cotidiana.",
        "description": (
            "Espanhol para quem quer sair do português misturado com espanhol e "
            "comunicar com clareza e confiança."
        ),
        "url": "/curso-de-espanhol-online",
        "cta_label": "Conheça o curso",
        "media_key": "e12-espanhol-professora.jpg",
        "media_alt": "Pessoa adulta de cabelo cacheado usa óculos, concentrada, olhando para baixo.",
        "order": 4,
        "is_active": True,
        "reverse": True,
        "band_tone": "white",
        "object_position": "center 20%",
    },
    {
        "slug": "hebraico",
        "language_key": "hebraico",
        "display_name": "Hebraico",
        "eyebrow": "Hebraico",
        "level_summary": "Escolha sua trilha",
        "headline": "Alfabetização, Hebraico Moderno e leitura bíblica orientada.",
        "description": "Aulas particulares e trilhas específicas conforme seu objetivo com o idioma.",
        "url": "/curso-de-hebraico-online",
        "cta_label": "Conheça as trilhas",
        "media_key": "e13-hebraico-headphones.jpg",
        "media_alt": (
            "Pessoa adulta usando fones de ouvido participa de uma aula online, "
            "sorrindo, em frente a um notebook."
        ),
        "order": 5,
        "is_active": True,
        "reverse": False,
        "band_tone": "alt",
        "object_position": "center",
    },
]

V2_HOME_MEDIA_BASE = "/assets/vedium_core/v2/media/home/"


def get_home_course_collection():
    """Retorna as entradas ativas, ordenadas, com o path de midia resolvido.

    Nao muta HOME_COURSE_COLLECTION -- devolve copias rasas com "media_src"
    adicionado (path completo pronto pro template, evitando repetir a base
    em cada consumidor). Hotfix de producao (media production hotfix):
    os 11 derivados aprovados vivem em public/v2/media/home/ (versionado
    no Git) -- deixaram de ser "preview" (pasta antiga v2-preview-media/
    era so local/gitignorada, nunca chegava a producao).
    """
    active = [dict(course) for course in HOME_COURSE_COLLECTION if course["is_active"]]
    active.sort(key=lambda course: course["order"])
    for course in active:
        course["media_src"] = V2_HOME_MEDIA_BASE + course["media_key"]
    return active


def get_course_index_entries():
    """Retorna [{"name", "href"}] na ordem da colecao, pro indice numerado
    (v2_course_index_intro) -- mesma ordem/rotulos ja usados desde a Fase C."""
    return [
        {"name": course["display_name"], "href": course["url"]}
        for course in get_home_course_collection()
    ]
