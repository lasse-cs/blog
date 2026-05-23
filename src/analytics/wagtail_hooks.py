from wagtail import hooks

from analytics.views import AnalyticsViewSet


@hooks.register("register_admin_viewset")
def register_analytics_viewset():
    return AnalyticsViewSet()
