from django.shortcuts import get_object_or_404, render

from core.models import PageTag, TaggablePage
from core.utilities import paginate


def tagged_pages(request, tag_slug):
    tag = get_object_or_404(PageTag, slug=tag_slug)
    taggable_pages = (
        TaggablePage.objects.filter(tags__slug=tag_slug)
        .live()
        .public()
        .specific()
        .order_by("-first_published_at")
        .prefetch_related("tags")
    )
    page_number = request.GET.get("page", 1)
    page, page_range = paginate(page_number, taggable_pages)
    context = {"pagination_page": page, "page_range": page_range, "tag": tag}
    return render(request, "patterns/pages/core/tagged_pages.html", context)
