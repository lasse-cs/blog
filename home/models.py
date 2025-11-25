from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from core.blocks import SidebarBlock
from core.models import FeedMixin


class HomePage(Page):
    intro = RichTextField(
        help_text="Intro text for the homepage.",
        default="Blog intro content.",
    )
    sidebar = StreamField(SidebarBlock, help_text="Sidebar content for the homepage.", blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("sidebar"),
    ]

    parent_page_types = ["wagtailcore.Page"]

    max_count = 1

    template = "patterns/pages/home/home_page.html"

    def get_context(self, request):
        context = super().get_context(request)
        context["feed_items"] = Page.objects.type(FeedMixin).live().public().specific()
        return context
