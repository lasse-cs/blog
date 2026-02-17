import pytest
import responses
import json

from urllib.parse import parse_qs, urlparse

from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from core.factories import AnalyticsSettingsFactory


UMAMI_API_BASE = "https://umami.example/api"
WEBSITE_ID = "website-id"


def _register_active_users_response(visitors: int):
    responses.get(
        f"{UMAMI_API_BASE}/websites/{WEBSITE_ID}/active",
        json={"visitors": visitors},
    )


def _register_stats_and_metrics_responses(
    metric_payloads: dict[str, list[dict]],
    failed_metrics: set[str] | None = None,
    stats_payload: dict | None = None,
):
    responses.get(
        f"{UMAMI_API_BASE}/websites/{WEBSITE_ID}/stats",
        json=stats_payload
        or {
            "pageviews": 10,
            "visitors": 4,
            "visits": 5,
            "bounces": 1,
            "totaltime": 120,
            "comparison": {
                "pageviews": 8,
                "visitors": 3,
                "visits": 4,
                "bounces": 1,
                "totaltime": 100,
            },
        },
    )

    failed_metrics = failed_metrics or set()

    def metrics_callback(request):
        metric_type = parse_qs(urlparse(request.url).query).get("type", [""])[0]
        if metric_type in failed_metrics:
            return (500, {"Content-Type": "application/json"}, json.dumps({}))

        body = json.dumps(metric_payloads.get(metric_type, []))
        return (200, {"Content-Type": "application/json"}, body)

    responses.add_callback(
        responses.GET,
        f"{UMAMI_API_BASE}/websites/{WEBSITE_ID}/metrics",
        callback=metrics_callback,
        content_type="application/json",
    )


def test_can_visit_analytics_dashboard(admin_client):
    response = admin_client.get(reverse("analytics:index"))
    assert response.status_code == 200


def test_analytics_dashboard_uses_correct_template(admin_client):
    response = admin_client.get(reverse("analytics:index"))
    assertTemplateUsed(response, "analytics/index.html")


@pytest.mark.django_db
@responses.activate
def test_analytics_dashboard_shows_partial_data_warning(admin_client, settings, site):
    settings.UMAMI_API_BASE = UMAMI_API_BASE
    settings.UMAMI_API_KEY = "test-api-key"
    AnalyticsSettingsFactory(site=site, umami_id=WEBSITE_ID)
    _register_active_users_response(visitors=3)
    _register_stats_and_metrics_responses(
        metric_payloads={
            "path": [{"x": "/", "y": 10}],
            "referrer": [{"x": "google.com", "y": 5}],
            "country": [{"x": "US", "y": 2}],
        },
        failed_metrics={"referrer"},
    )

    response = admin_client.get(reverse("analytics:index"))
    assert response.status_code == 200
    assert b"Some analytics sections could not be loaded" in response.content


@pytest.mark.django_db
@responses.activate
def test_analytics_dashboard_happy_path(admin_client, settings, site):
    settings.UMAMI_API_BASE = UMAMI_API_BASE
    settings.UMAMI_API_KEY = "test-api-key"
    AnalyticsSettingsFactory(site=site, umami_id=WEBSITE_ID)
    _register_active_users_response(visitors=7)
    _register_stats_and_metrics_responses(
        metric_payloads={
            "path": [{"x": "/", "y": 22}],
            "referrer": [{"x": "google.com", "y": 11}],
            "country": [{"x": "US", "y": 8}],
        },
        stats_payload={
            "pageviews": 100,
            "visitors": 40,
            "visits": 50,
            "bounces": 10,
            "totaltime": 1200,
            "comparison": {
                "pageviews": 90,
                "visitors": 35,
                "visits": 45,
                "bounces": 9,
                "totaltime": 1100,
            },
        },
    )

    response = admin_client.get(reverse("analytics:index"))
    assert response.status_code == 200
    assert b"Some analytics sections could not be loaded" not in response.content
