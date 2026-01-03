from datetime import datetime

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
        "first_published_at": datetime(2023, 10, 24, 10, 0, 0),
        "intro": "Article intro text",
        "get_summary_template": "patterns/components/article/article_summary.html",
        "get_tag_summary_template": "patterns/components/article/article_summary.html",
    },
    {
        "title": "Another Title",
        "first_published_at": datetime(2023, 10, 23, 10, 0, 0),
        "intro": "Intro text for <em>another</em> article.",
        "get_summary_template": "patterns/components/article/article_summary.html",
        "get_tag_summary_template": "patterns/components/article/article_summary.html",
        "tags": {
            "all": {
                "name": "Tag1",
                "slug": "tag1",
                "get_absolute_url": "#",
            },
        },
    },
]

BOOKS = [
    {
        "title": "Clean Code",
        "blurb": "<p>A handbook of agile software craftsmanship that explores professionalism, naming, error handling, and how to write maintainable software.</p>",
        "progess": 80,
        "intro": "<p>“Clean Code” delves into what it means to write code that is understandable, tidy, and resilient to change. It’s a practical, disciplined guide for developers who care about craftsmanship over shortcuts.</p>",
        "book_authors": {
            "all": [
                {"author": {"name": "Robert C. Martin"}},
                {"author": {"name": "Lasse Schmieding"}},
            ]
        },
        "cover_image": "dummy",
        "get_summary_template": "patterns/components/book/book_summary.html",
    },
    {
        "title": "Clean Code",
        "blurb": "<p>A handbook of agile software craftsmanship that explores professionalism, naming, error handling, and how to write maintainable software.</p>",
        "progess": 80,
        "intro": "<p>“Clean Code” delves into what it means to write code that is understandable, tidy, and resilient to change. It’s a practical, disciplined guide for developers who care about craftsmanship over shortcuts.</p>",
        "book_authors": {
            "all": [
                {"author": {"name": "Robert C. Martin"}},
                {"author": {"name": "Lasse Schmieding"}},
            ]
        },
        "cover_image": "dummy",
        "get_summary_template": "patterns/components/book/book_summary.html",
    },
    {
        "title": "Clean Code",
        "blurb": "<p>A handbook of agile software craftsmanship that explores professionalism, naming, error handling, and how to write maintainable software.</p>",
        "progess": 80,
        "intro": "<p>“Clean Code” delves into what it means to write code that is understandable, tidy, and resilient to change. It’s a practical, disciplined guide for developers who care about craftsmanship over shortcuts.</p>",
        "book_authors": {
            "all": [
                {"author": {"name": "Robert C. Martin"}},
                {"author": {"name": "Lasse Schmieding"}},
            ]
        },
        "cover_image": "dummy",
        "get_summary_template": "patterns/components/book/book_summary.html",
    },
    {
        "title": "Clean Code",
        "blurb": "<p>A handbook of agile software craftsmanship that explores professionalism, naming, error handling, and how to write maintainable software.</p>",
        "progess": 80,
        "intro": "<p>“Clean Code” delves into what it means to write code that is understandable, tidy, and resilient to change. It’s a practical, disciplined guide for developers who care about craftsmanship over shortcuts.</p>",
        "book_authors": {
            "all": [
                {"author": {"name": "Robert C. Martin"}},
                {"author": {"name": "Lasse Schmieding"}},
            ]
        },
        "cover_image": "dummy",
        "get_summary_template": "patterns/components/book/book_summary.html",
    },
    {
        "title": "Clean Code",
        "blurb": "<p>A handbook of agile software craftsmanship that explores professionalism, naming, error handling, and how to write maintainable software.</p>",
        "progess": 80,
        "intro": "<p>“Clean Code” delves into what it means to write code that is understandable, tidy, and resilient to change. It’s a practical, disciplined guide for developers who care about craftsmanship over shortcuts.</p>",
        "book_authors": {
            "all": [
                {"author": {"name": "Robert C. Martin"}},
                {"author": {"name": "Lasse Schmieding"}},
            ]
        },
        "cover_image": "dummy",
        "get_summary_template": "patterns/components/book/book_summary.html",
    },
    {
        "title": "Clean Code",
        "blurb": "<p>A handbook of agile software craftsmanship that explores professionalism, naming, error handling, and how to write maintainable software.</p>",
        "progess": 80,
        "intro": "<p>“Clean Code” delves into what it means to write code that is understandable, tidy, and resilient to change. It’s a practical, disciplined guide for developers who care about craftsmanship over shortcuts.</p>",
        "book_authors": {
            "all": [
                {"author": {"name": "Robert C. Martin"}},
                {"author": {"name": "Lasse Schmieding"}},
            ]
        },
        "cover_image": "dummy",
        "get_summary_template": "patterns/components/book/book_summary.html",
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
    items = [*ARTICLES, *BOOKS]
    items.extend([None] * 22)
    page, page_range = paginate(1, items, per_page=4)
    context["pagination_page"] = page
    context["page_range"] = page_range


@register_context_modifier(template="patterns/pages/book/book_index_page.html")
def add_book_index_paginator(context, request):
    books = list(BOOKS)
    books.extend([None] * 22)
    page, page_range = paginate(1, books, per_page=6)
    context["pagination_page"] = page
    context["page_range"] = page_range


@register_context_modifier(template="patterns/pages/core/tagged_pages.html")
def add_tags_paginator(context, request):
    items = list(ARTICLES)
    page, page_range = paginate(1, items, per_page=3)
    context["pagination_page"] = page
    context["page_range"] = page_range
