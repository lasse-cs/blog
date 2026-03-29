from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

from analytics.factories import AnalyticsSettingsFactory


def test_can_visit_analytics_dashboard(admin_client, site):
    AnalyticsSettingsFactory(site=site)
    response = admin_client.get(reverse("analytics:index"))
    assert response.status_code == 200


def test_analytics_dashboard_uses_correct_template(admin_client, site):
    AnalyticsSettingsFactory(site=site)
    response = admin_client.get(reverse("analytics:index"))
    assertTemplateUsed(response, "analytics/index.html")
