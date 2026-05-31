from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.views.decorators.vary import vary_on_headers
from django.views.defaults import page_not_found as django_page_not_found
from django.views.defaults import server_error as django_server_error


def page_not_found(request, exception):
    return django_page_not_found(
        request, exception, template_name="patterns/pages/error/404.html"
    )


def server_error(request):
    return django_server_error(request, template_name="patterns/pages/error/500.html")


@cache_page(60 * 60)
@vary_on_headers("Host")
@require_GET
def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("sitemap"))
    response = render(
        request,
        "non_patterns/robots.txt",
        {"sitemap_url": sitemap_url},
        content_type="text/plain",
    )
    return response


@user_passes_test(lambda u: u.is_superuser)
def error_500_test(request):
    raise Exception("This is a test exception")
