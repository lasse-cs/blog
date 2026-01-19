from django.apps import apps
from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from blog import views as blog_views
from search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("sitemap.xml", sitemap),
    path("search/", search_views.search, name="search"),
    path("error-500-test/", blog_views.error_500_test, name="server_error"),
    path("", include("core.urls")),
    path("activity/", include("activity.urls")),
]

handler404 = "blog.views.page_not_found"
handler500 = "blog.views.server_error"

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Django Browser Reload
    if apps.is_installed("django_browser_reload"):
        urlpatterns += [
            path("__reload__/", include("django_browser_reload.urls")),
        ]

    # Django Debug Toolbar
    if apps.is_installed("debug_toolbar"):
        from debug_toolbar.toolbar import debug_toolbar_urls

        urlpatterns += debug_toolbar_urls()

    # Add pattern library
    if apps.is_installed("pattern_library"):
        urlpatterns = urlpatterns + [
            path("patterns/", include("pattern_library.urls")),
        ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
