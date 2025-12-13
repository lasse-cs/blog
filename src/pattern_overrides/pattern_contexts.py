from pattern_library import register_context_modifier

from core.utilities import paginate


@register_context_modifier(template="patterns/components/pagination/pagination.html")
def add_paginator(context, request):
    objects = 24 * [None]
    page, page_range = paginate(1, objects, per_page=2)
    context["pagination_page"] = page
    context["page_range"] = page_range


ARTICLES = [
    {
        "title": "Article Title",
        "first_published_at": "2023-10-24T10:00:00Z",
        "intro": "Article intro text",
        "get_summary_template": "patterns/components/article/article_summary.html",
    },
    {
        "title": "Another Title",
        "first_published_at": "2023-10-23T10:00:00Z",
        "intro": "Intro text for <em>another</em> article.",
        "get_summary_template": "patterns/components/article/article_summary.html",
    },
]


@register_context_modifier(template="patterns/pages/article/article_index_page.html")
def add_article_index_paginator(context, request):
    articles = list(ARTICLES)
    articles.extend([None] * 22)
    page, page_range = paginate(1, articles, per_page=2)
    context["pagination_page"] = page
    context["page_range"] = page_range


@register_context_modifier(template="patterns/pages/home/home_page.html")
def add_home_page_paginator(context, request):
    articles = list(ARTICLES)
    articles.extend([None] * 22)
    page, page_range = paginate(1, articles, per_page=2)
    context["pagination_page"] = page
    context["page_range"] = page_range
