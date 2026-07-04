"""Conteúdo do blog da Vedium — posts ricos (SEO/GEO) renderizados pelo
template compartilhado templates/includes/blog_post.html.

Há DUAS fontes de posts, e ambas caem no mesmo template:
1. Este dict BLOG_POSTS — posts "de código" (SEO/GEO trabalhados a fundo,
   com várias seções), editados por nós via commit/deploy.
2. O doctype "Vedium Blog Post" — posts que QUALQUER pessoa com acesso ao
   Frappe Desk publica sozinha, em /app/vedium-blog-post, sem precisar de
   código nem de deploy. É o caminho recomendado para conteúdo novo.

Toda URL /blog/<slug> passa por www/blog_post.py, que procura primeiro no
doctype (post publicado pelo painel) e só then cai neste dict. O índice em
/blog (www/blog.py) lista os dois juntos, ordenados por data.

Convenção de conteúdo: corpo em HTML controlado por nós (parágrafos,
listas e tabelas), com no mínimo ~900 palavras por post, headings H2 e
um bloco de FAQs para rich snippet.
"""

BASE_URL = "https://vediums.com"
WHATSAPP_PHONE = "5511911293075"


BLOG_POSTS = {}



def _post_card(slug, post):
    return {
        "slug": slug,
        "url": f"/blog/{slug}",
        "title": post["title"],
        "meta_description": post["meta_description"],
        "date": str(post.get("date", "")),
        "date_display": post.get("date_display", ""),
        "tag": post.get("tag", "Vedium"),
        "hero_image": post.get("hero_image", ""),
    }


def _db_post_card(row):
    return {
        "slug": row.slug,
        "url": f"/blog/{row.slug}",
        "title": row.title,
        "meta_description": row.meta_description or "",
        "date": str(row.date or ""),
        "date_display": "",
        "tag": row.tag or "Vedium",
        "hero_image": row.hero_image or "",
        "lang": row.lang or "pt-BR",
    }


def list_db_blog_posts():
    """Posts publicados via painel (doctype Vedium Blog Post, sem código/deploy)."""
    import frappe

    rows = frappe.get_all(
        "Vedium Blog Post",
        filters={"published": 1},
        fields=["name as slug", "title", "meta_description", "tag", "date", "hero_image", "lang"],
        ignore_permissions=True,
    )
    return [_db_post_card(row) for row in rows]


def list_blog_posts():
    """Lista combinada (posts do painel + posts de código), mais recente primeiro."""
    cards = [_post_card(slug, post) for slug, post in BLOG_POSTS.items()]
    cards += list_db_blog_posts()
    cards.sort(key=lambda c: c["date"], reverse=True)
    return cards


def get_blog_post(slug):
    post = dict(BLOG_POSTS[slug])
    post["slug"] = slug
    post["url"] = f"{BASE_URL}/blog/{slug}"
    return post


def get_blog_post_from_db(slug):
    """Post publicado via painel do Frappe (/app/vedium-blog-post). None se não existir/publicado."""
    import frappe

    doc = frappe.db.get_value(
        "Vedium Blog Post",
        {"slug": slug, "published": 1},
        [
            "title", "meta_description", "tag", "date", "hero_image", "hero_alt",
            "lead", "content", "cta_title", "cta_text", "cta_label", "cta_url",
        ],
        as_dict=True,
    )
    if not doc:
        return None
    faqs = frappe.get_all(
        "Vedium Blog FAQ",
        filters={"parenttype": "Vedium Blog Post", "parent": slug},
        fields=["question as q", "answer as a"],
        order_by="idx asc",
        ignore_permissions=True,
    )
    return {
        "slug": slug,
        "url": f"{BASE_URL}/blog/{slug}",
        "title": doc.title,
        "h1": doc.title,
        "meta_description": doc.meta_description or "",
        "tag": doc.tag or "Vedium",
        "date": str(doc.date or ""),
        "date_display": str(doc.date or ""),
        "hero_image": doc.hero_image or "",
        "hero_alt": doc.hero_alt or "",
        "lead": doc.lead or "",
        # content é HTML de um Text Editor (rich text) — uma seção única sem
        # heading (o template pula o <h2> quando heading está vazio).
        "sections": [{"heading": "", "body": [doc.content or ""]}],
        "faqs": faqs,
        "cta_title": doc.cta_title or "",
        "cta_text": doc.cta_text or "",
        "cta_label": doc.cta_label or "",
        "cta_url": doc.cta_url or "",
    }


def get_blog_post_any(slug):
    """Procura o post primeiro no painel (banco), depois no dict de código."""
    post = get_blog_post_from_db(slug)
    if post:
        return post
    if slug in BLOG_POSTS:
        return get_blog_post(slug)
    return None


def apply_blog_context(context, slug):
    post = get_blog_post(slug)
    context.title = post["title"]
    context.description = post["meta_description"]
    context.post = post


def get_blog_index_context(context):
    context.title = "Blog da Vedium — idiomas, cultura e aprendizado"
    context.description = (
        "Conteúdos gratuitos sobre inglês, iorubá e português para estrangeiros: "
        "guias práticos, níveis, pronúncia e cultura, escritos pela equipe da Vedium."
    )
    context.posts = list_blog_posts()
