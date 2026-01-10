import os
import pytest

from django.conf import settings

from wagtail.coreutils import get_supported_content_language_variant
from wagtail.models import Locale, Page, Site

from wagtail_factories import SiteFactory


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "1"


@pytest.fixture
def live_site(live_server):
    # Ensure that all site and page objects are deleted.
    # Wagtail will initially create ones, but we don't
    # want those
    Site.objects.all().delete()
    Page.objects.all().delete()

    # We also need a Locale
    language_code = get_supported_content_language_variant(settings.LANGUAGE_CODE)
    Locale.objects.get_or_create(language_code=language_code)

    site = SiteFactory(
        hostname=live_server.thread.host,
        port=live_server.thread.port,
        is_default_site=True,
    )
    yield site
