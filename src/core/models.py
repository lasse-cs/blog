from django.contrib.syndication.views import Feed
from django.db import models
from django.utils.feedgenerator import Atom1Feed

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import RichTextField
from wagtail.search import index


class BaseRSSFeed(Feed):
    description_template = "patterns/feeds/description.html"

    def get_object(self, request, page):
        return page

    def title(self, obj):
        return obj.title
    
    def descripion(self, obj):
        return f"Feed for {obj.title}"

    def link(self, obj):
        return obj.url

    def items(self, obj):
        return obj.get_feed_items()[:30]
    
    def item_title(self, item):
        return item.title
    
    def item_link(self, item):
        return item.url

class BaseAtomFeed(BaseRSSFeed):
    feed_type = Atom1Feed
    
    def subtitle(self, obj):
        return self.descripion(obj)



class FeedMixin(RoutablePageMixin):
    rss_feed_instance = BaseRSSFeed()
    atom_feed_instance = BaseAtomFeed()

    @path("rss/")
    def rss_feed(self, request):
        return self.rss_feed_instance(request, self)

    @path("atom/")
    def atom_feed(self, request):
        return self.atom_feed_instance(request, self)

    def get_feed_items(self):
        return self.get_children().type(FeedItemMixin).live().public().specific().order_by('-first_published_at')


class FeedItemMixin(models.Model):
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