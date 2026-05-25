import pytest

from analytics.client import UmamiClient


@pytest.fixture
def umami_api_base():
    return "https://test.umami.is/api/"


@pytest.fixture
def umami_api_key():
    return "api_key"


@pytest.fixture
def website_id():
    return "website_id"


@pytest.fixture
def umami_client(umami_api_base, umami_api_key, website_id):
    with UmamiClient(umami_api_base, umami_api_key, website_id=website_id) as client:
        yield client


@pytest.fixture
def configured_umami_settings(settings, umami_api_base, umami_api_key):
    settings.UMAMI_API_BASE = umami_api_base
    settings.UMAMI_API_KEY = umami_api_key
    return settings
