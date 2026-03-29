from django.templatetags.static import static
from django.utils.html import format_html_join

from wagtail import hooks

from analytics.views import AnalyticsViewSet


@hooks.register("register_admin_viewset")
def register_analytics_viewset():
    return AnalyticsViewSet()


@hooks.register("insert_global_admin_js")
def global_admin_js():
    urls = [
        static("analytics/js/controllers/content_loader_controller.js"),
        static("analytics/js/controllers/analytics_summary_controller.js"),
        static("analytics/js/controllers/analytics_metrics_controller.js"),
    ]
    return format_html_join(
        "\n",
        '<script src="{}"></script>',
        ((url,) for url in urls),
    )
