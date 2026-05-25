from wagtail import hooks

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import register_setting
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from wagtail_umami_analytics.models import UmamiAnalyticsSetting
from wagtail_umami_analytics.views import UmamiAnalyticsViewSet

from core.models import PageTag


class PageTagsSnippetViewSet(SnippetViewSet):
    panels = [FieldPanel("name")]  # only show the name field
    model = PageTag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Page Tags"
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ["name", "slug"]
    search_fields = ("name",)


register_snippet(PageTagsSnippetViewSet)


register_setting(UmamiAnalyticsSetting)


@hooks.register("register_admin_viewset")
def umami_dashboard():
    return UmamiAnalyticsViewSet()
