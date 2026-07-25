from urllib.parse import urlparse

import frappe

from vedium_core.blog_content import (
    RESERVED_CATEGORY_SLUGS,
    get_adjacent_posts,
    get_blog_post_any,
    get_category_context,
)

# Prefixos de idioma com blog PLE próprio (ver PLE_CATEGORY_BY_LANG em
# blog_content.py) — expandir aqui conforme fr/de/ru/zh-cn ganharem posts
# reais (hoje só en/es têm conteúdo planejado no calendário editorial).
LANG_BLOG_PREFIXES = ("en", "es")

no_cache = 1


def _requested_lang_prefix():
    path = (frappe.local.path or "").lstrip("/")
    for prefix in LANG_BLOG_PREFIXES:
        if path.startswith(f"{prefix}/blog/"):
            return prefix
    return None


def _normalized_path(value):
    path = urlparse(value or "").path
    return f"/{path.strip('/')}" if path.strip("/") else "/"


def get_context(context):
    context.no_cache = 1

    lang = _requested_lang_prefix()
    category = frappe.form_dict.get("category")
    slug = frappe.form_dict.get("slug")

    # A regra /blog/<slug> também recebe as páginas-pilar em PT. O Frappe
    # entrega "ioruba", "ingles" etc. no parâmetro slug, por isso é preciso
    # reconhecê-las antes de procurar um artigo com esse nome.
    if not lang and not category and slug in RESERVED_CATEGORY_SLUGS:
        return get_category_context(context, slug)

    if category and not slug:
        # /blog/<category> (PT) ou /<lang>/blog/<category> (PLE). Sob /blog/
        # sem prefixo, um valor que não é categoria reservada é, na
        # verdade, o slug de um post antigo (rota de 1 segmento é
        # compartilhada entre categoria e post plano — ver hooks.py).
        if lang or category in RESERVED_CATEGORY_SLUGS:
            return get_category_context(context, category, lang)
        slug, category = category, None

    if not slug:
        frappe.local.flags.redirect_location = f"/{lang}/blog" if lang else "/blog"
        raise frappe.Redirect

    post = get_blog_post_any(slug)
    if not post:
        frappe.local.flags.redirect_location = f"/{lang}/blog" if lang else "/blog"
        raise frappe.Redirect

    # Um artigo só pode responder na URL declarada pelo próprio conteúdo.
    # Isso elimina aliases planos, categorias arbitrárias e prefixos de idioma
    # incorretos sem afetar os posts antigos cuja canonical continua plana.
    requested_path = _normalized_path(frappe.local.path)
    canonical_path = _normalized_path(post["url"])
    if requested_path != canonical_path:
        frappe.local.flags.redirect_location = canonical_path
        raise frappe.Redirect

    context.title = post["seo_title"]
    context.description = post["meta_description"]
    context.post = post
    context.newer_post, context.older_post = get_adjacent_posts(slug)
    return context
