import frappe

from vedium_core.blog_content import get_blog_index_context

# Blog PLE (Português para Estrangeiros) com índice próprio por idioma —
# ver templates/includes/blog_category.html e www/blog_post.py pro mesmo
# padrão de detecção de prefixo. Expandir aqui conforme fr/de/ru/zh-cn
# ganharem conteúdo (hoje só en/es têm posts reais planejados).
LANG_BLOG_PREFIXES = ("en", "es")

no_cache = 1


def get_context(context):
    context.no_cache = 1
    path = (frappe.local.path or "").lstrip("/")
    lang = next((p for p in LANG_BLOG_PREFIXES if path.startswith(f"{p}/blog")), None)
    get_blog_index_context(context, lang=lang)
    return context
