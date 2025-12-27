from django.views.defaults import page_not_found as django_page_not_found


def page_not_found(request, exception):
    return django_page_not_found(
        request, exception, template_name="patterns/pages/error/404.html"
    )
