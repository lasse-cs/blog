from django.db.models import prefetch_related_objects

from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from core.blocks import SidebarBlock
from core.models import FeedItemMixin, FeedMixin, TaggablePage


class HomePage(FeedMixin, Page):
    intro = RichTextField(
        help_text="Intro text for the homepage.",
        default="Blog intro content.",
    )
    sidebar = StreamField(
        SidebarBlock,
        help_text="Sidebar content for the homepage.",
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("sidebar"),
    ]

    parent_page_types = ["wagtailcore.Page"]

    max_count = 1

    template = "patterns/pages/home/home_page.html"
    track_activity = True

    def get_feed_items(self):
        return (
            Page.objects.type(FeedItemMixin)
            .live()
            .public()
            .specific()
            .order_by("-first_published_at")
        )

    def get_paginated_feed_items(self, page_number):
        page, page_range = super().get_paginated_feed_items(page_number)
        taggable_items = [
            item for item in page.object_list if isinstance(item, TaggablePage)
        ]
        prefetch_related_objects(taggable_items, "tags")

        return page, page_range

    def get_context(self, request):
        context = super().get_context(request)
        page_number = request.GET.get("page", 1)
        page, page_range = self.get_paginated_feed_items(page_number)
        context["pagination_page"] = page
        context["page_range"] = page_range
        return context
