from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.search import index


class FeedMixin(models.Model):
    """
    Mixin to specify that a model can be included in a Feed.
    """
    intro = RichTextField(
        help_text="Intro text for the page, used also in summaries.",
        default="Intro content.",
    )

    panels = [
        FieldPanel("intro"),
    ]

    search_fields = [
        index.SearchField("intro"),
    ]

    def get_summary_template(self):
        if hasattr(self, "summary_template"):
            return self.summary_template
        raise NotImplementedError("You must define summary_template on the model.")

    class Meta:
        abstract = True


@register_setting
class SiteFooter(BaseSiteSetting):
    content = RichTextField("Footer Content", max_length=255, features=["italic", "link", "bold"])