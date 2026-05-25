from datetime import UTC, datetime, timedelta

from pytest_django.asserts import assertTemplateUsed

import responses

from django.urls import reverse

from analytics.factories import AnalyticsSettingsFactory


def _time_range_query_params(now: datetime) -> dict[str, str]:
    return {
        "startAt": str(int((now - timedelta(days=7)).timestamp() * 1000)),
        "endAt": str(int(now.timestamp() * 1000)),
    }


def test_can_visit_analytics_dashboard(admin_client, site, website_id):
    AnalyticsSettingsFactory(site=site, umami_id=website_id)
    response = admin_client.get(reverse("analytics:index"))
    assert response.status_code == 200


def test_analytics_dashboard_uses_correct_template(admin_client, site, website_id):
    AnalyticsSettingsFactory(site=site, umami_id=website_id)
    response = admin_client.get(reverse("analytics:index"))
    assertTemplateUsed(response, "analytics/index.html")


@responses.activate
def test_active_users_returns_503_when_umami_fails(
    admin_client, site, website_id, configured_umami_settings, umami_api_base
):
    AnalyticsSettingsFactory(site=site, umami_id=website_id)
    responses.get(
        f"{umami_api_base}websites/{website_id}/active",
        json={},
        status=500,
    )

    response = admin_client.get(reverse("analytics:active_users"))

    assert response.status_code == 503
    assert response.json() == {"error": "Umami is unavailable"}


@responses.activate
def test_stats_returns_503_when_umami_fails(
    admin_client,
    time_machine,
    site,
    website_id,
    configured_umami_settings,
    umami_api_base,
):
    AnalyticsSettingsFactory(site=site, umami_id=website_id)
    now = datetime(2026, 1, 10, 8, tzinfo=UTC)
    time_machine.move_to(now)

    responses.get(
        f"{umami_api_base}websites/{website_id}/stats",
        json={},
        status=500,
        match=[responses.matchers.query_param_matcher(_time_range_query_params(now))],
    )

    response = admin_client.get(reverse("analytics:stats"))

    assert response.status_code == 503
    assert response.json() == {"error": "Umami is unavailable"}


@responses.activate
def test_metrics_returns_503_when_umami_fails(
    admin_client,
    time_machine,
    site,
    website_id,
    configured_umami_settings,
    umami_api_base,
):
    AnalyticsSettingsFactory(site=site, umami_id=website_id)
    now = datetime(2026, 1, 10, 8, tzinfo=UTC)
    time_machine.move_to(now)
    time_range_params = _time_range_query_params(now)

    response_url = f"{umami_api_base}websites/{website_id}/metrics"
    responses.get(
        response_url,
        json=[{"x": "path", "y": 1}],
        match=[
            responses.matchers.query_param_matcher(
                {**time_range_params, "type": "path", "limit": "10"}
            )
        ],
    )
    responses.get(
        response_url,
        json={},
        status=500,
        match=[
            responses.matchers.query_param_matcher(
                {
                    **time_range_params,
                    "type": "referrer",
                    "limit": "10",
                }
            )
        ],
    )
    responses.get(
        response_url,
        json=[{"x": "country", "y": 1}],
        match=[
            responses.matchers.query_param_matcher(
                {
                    **time_range_params,
                    "type": "country",
                    "limit": "10",
                }
            )
        ],
    )

    response = admin_client.get(reverse("analytics:metrics"))

    assert response.status_code == 503
    assert response.json() == {"error": "Umami is unavailable"}
