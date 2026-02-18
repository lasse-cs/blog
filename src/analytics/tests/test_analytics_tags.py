import pytest

from core.factories import AnalyticsSettingsFactory
from analytics.templatetags.analytics_tags import analytics_tracker


@pytest.mark.django_db
def test_valid_analytics(site, settings, rf):
    settings.UMAMI_HOST = "http://localhost:3000/"
    analytics_settings = AnalyticsSettingsFactory(site=site)
    context = {"request": rf.get("/", headers={"host": site.hostname})}
    result = analytics_tracker(context)
    assert (
        result
        == f'<script defer src="http://localhost:3000/script.js" data-website-id="{analytics_settings.umami_id}"></script>'
    )


@pytest.mark.django_db
def test_no_umami_host(site, settings, rf):
    settings.UMAMI_HOST = ""
    AnalyticsSettingsFactory(site=site)
    context = {"request": rf.get("/", headers={"host": site.hostname})}
    result = analytics_tracker(context)
    assert result == ""


@pytest.mark.django_db
def test_no_umami_id(site, settings, rf):
    settings.UMAMI_HOST = "http://localhost:3000/"
    AnalyticsSettingsFactory(site=site, umami_id="")
    context = {"request": rf.get("/", headers={"host": site.hostname})}
    result = analytics_tracker(context)
    assert result == ""


@pytest.mark.django_db
def test_in_preview(site, settings, rf):
    settings.UMAMI_HOST = "http://localhost:3000/"
    AnalyticsSettingsFactory(site=site)
    request = rf.get("/", headers={"host": site.hostname})
    request.is_preview = True
    context = {"request": request}
    result = analytics_tracker(context)
    assert result == ""


@pytest.mark.django_db
def test_in_pattern_library(site, settings, rf):
    settings.UMAMI_HOST = "http://localhost:3000/"
    AnalyticsSettingsFactory(site=site)
    request = rf.get("/", headers={"host": site.hostname})
    context = {"request": request, "is_pattern_library": True}
    result = analytics_tracker(context)
    assert result == ""
