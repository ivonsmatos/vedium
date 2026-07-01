from vedium_core.blog_content import get_blog_index_context


no_cache = 1


def get_context(context):
    context.no_cache = 1
    get_blog_index_context(context)
    return context
