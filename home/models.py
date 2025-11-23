from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    intro = RichTextField(
        help_text="Intro text for the homepage.",
        default="Blog intro content.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    parent_page_types = ["wagtailcore.Page"]

    max_count = 1

    template = "patterns/pages/home/home_page.html"
