import frappe

from vedium_core.blog_content import get_blog_post_any


no_cache = 1


def get_context(context):
    context.no_cache = 1
    slug = frappe.form_dict.get("slug") or ""
    post = get_blog_post_any(slug)
    if not post:
        frappe.local.flags.redirect_location = "/blog"
        raise frappe.Redirect
    context.title = post["title"]
    context.description = post["meta_description"]
    context.post = post
    return context
