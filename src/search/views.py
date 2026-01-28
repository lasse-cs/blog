from django.shortcuts import render

from wagtail.models import Page

from core.utilities import paginate
from search.forms import SearchForm
from search.models import SearchItemPageMixin


def search(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        search_query = form.cleaned_data["query"]
        search_results = (
            Page.objects.type(SearchItemPageMixin).live().search(search_query)
        )
    else:
        search_query = ""
        search_results = Page.objects.none()

    page = request.GET.get("page", 1)
    page, page_range = paginate(page, search_results)
    return render(
        request,
        "patterns/pages/search/search.html",
        {
            "search_query": search_query,
            "pagination_page": page,
            "page_range": page_range,
        },
    )
