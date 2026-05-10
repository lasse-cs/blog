from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete

from wagtail.models import Page, Site
from wagtail.signals import page_published, page_unpublished


def clear_main_menu_cache(**kwargs):
    cache_keys = [
        make_template_fragment_key("main_menu", [site.pk, is_pattern_library])
        for site in Site.objects.all()
        for is_pattern_library in ["True", ""]
    ]
    cache.delete_many(cache_keys)


post_delete.connect(
    clear_main_menu_cache,
    sender=Page,
    dispatch_uid="clear_main_menu_cache_post_page_delete",
)
page_published.connect(
    clear_main_menu_cache, dispatch_uid="clear_main_menu_cache_page_published"
)
page_unpublished.connect(
    clear_main_menu_cache, dispatch_uid="clear_main_menu_cache_page_unpublished"
)
