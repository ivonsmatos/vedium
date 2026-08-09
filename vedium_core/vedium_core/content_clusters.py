"""Clusters de autoridade SEO (P9) — mapa hub-and-spoke.

Estratégia: cada idioma tem uma **página pilar** (`/curso-de-<idioma>-online`)
ligada a um **cluster** de conteúdos (`/blog/<idioma>/...`), e cada peça aponta o
próximo passo: **teste de nível → curso → lead → matrícula**.

Este módulo é a FONTE do mapa + um helper Jinja (`cluster_for_category`) que
qualquer template (blog, curso, landing) chama para renderizar a linkagem
interna spoke → pilar → conversão. Registrado em hooks `jinja.methods`.

O que falta (conteúdo, não plataforma): escrever os artigos do cluster (via
agente `blog-publisher`) e cruzar os links pilar → spokes. Ver doc 17.
"""

from __future__ import annotations

# Chaveado pelo slug de categoria do blog (ver blog_content.CATEGORY_PAGES).
CLUSTERS = {
    "ingles": {
        "label": "Inglês",
        "pillar_url": "/curso-de-ingles-online",
        "teste_url": "/teste-de-nivel-ingles",
    },
    "ioruba": {
        "label": "Iorubá",
        "pillar_url": "/curso-de-ioruba-online",
        "teste_url": "/teste-de-nivel",
    },
    "hebraico": {
        "label": "Hebraico",
        "pillar_url": "/curso-de-hebraico-online",
        "teste_url": "/teste-de-nivel",
    },
    "espanhol": {
        "label": "Espanhol",
        "pillar_url": "/curso-de-espanhol-online",
        "teste_url": "/teste-de-nivel",
    },
    "ple": {
        "label": "Português para Estrangeiros",
        "pillar_url": "/portugues-para-estrangeiros",
        "teste_url": "/teste-de-nivel",
    },
}

# Sinônimos de categoria → chave canônica do cluster.
_ALIASES = {
    "portugues": "ple",
    "portugues-para-estrangeiros": "ple",
    "português": "ple",
    "yoruba": "ioruba",
    "iorubá": "ioruba",
    "inglês": "ingles",
    "español": "espanhol",
    "hebrew": "hebraico",
}


def cluster_for_category(category: str | None) -> dict | None:
    """Retorna {label, pillar_url, teste_url} do cluster da categoria, ou None.
    Seguro para chamar de qualquer template (nunca lança)."""
    if not category:
        return None
    key = str(category).strip().lower()
    key = _ALIASES.get(key, key)
    return CLUSTERS.get(key)
