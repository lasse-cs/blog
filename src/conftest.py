import pytest
from django.conf import settings
from wagtail.coreutils import get_supported_content_language_variant
from wagtail.models import Locale, Page, Site
from wagtail_factories import SiteFactory


@pytest.fixture
def site():
    # Ensure that all site and page objects are deleted.
    # Wagtail will initially create ones, but we don't
    # want those
    Site.objects.all().delete()
    Page.objects.all().delete()

    # We also need a Locale
    language_code = get_supported_content_language_variant(settings.LANGUAGE_CODE)
    Locale.objects.get_or_create(language_code=language_code)

    yield SiteFactory(is_default_site=True)


@pytest.fixture
def root_page(site: Site):
    yield site.root_page
