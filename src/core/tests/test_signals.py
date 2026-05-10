import pytest

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from wagtail_factories import PageFactory


@pytest.mark.django_db
def test_main_menu_cache_cleared_after_publish(site):
    cache_keys = [
        make_template_fragment_key("main_menu", [site.pk, variant])
        for variant in [True, ""]
    ]
    for cache_key in cache_keys:
        cache.set(cache_key, "Something")

    PageFactory(
        parent=site.root_page, title="Cache test page"
    ).save_revision().publish()

    for cache_key in cache_keys:
        assert cache.get(cache_key) is None
