import pytest

import responses

from analytics.client import MetricType, UmamiClientError, UmamiClient
from analytics.client import UmamiConfigurationError


@pytest.fixture
def url():
    yield "https://test.umami.is/api/"


@pytest.fixture
def website_id():
    yield "website_id"


@pytest.fixture
def client(url, website_id):
    with UmamiClient(url, "api_key", website_id=website_id) as c:
        yield c


@responses.activate
def test_active_users(client, url, website_id):
    responses.get(f"{url}websites/{website_id}/active", json={"visitors": 5})
    assert client.active_users() == 5


@responses.activate
def test_active_users_handles_errors(client, url, website_id):
    responses.get(f"{url}websites/{website_id}/active", json={}, status=401)
    with pytest.raises(UmamiClientError):
        client.active_users()


@responses.activate
def test_active_users_other_website_id(client, url):
    responses.get(f"{url}websites/other_website_id/active", json={"visitors": 5})
    assert client.active_users(website_id="other_website_id") == 5


@responses.activate
def test_stats(client, url, website_id):
    startAt = 200
    endAt = 300
    expected_response = {
        "pageviews": 10,
        "visitors": 10,
        "visits": 10,
        "bounces": 10,
        "totaltime": 10,
        "comparison": {
            "pageviews": 0,
            "visitors": 0,
            "visits": 0,
            "bounces": 0,
            "totaltime": 0,
        },
    }
    responses.get(
        f"{url}websites/{website_id}/stats",
        json=expected_response,
        match=[
            responses.matchers.query_param_matcher(
                {"startAt": str(startAt), "endAt": str(endAt)}
            )
        ],
    )
    assert client.stats(startAt, endAt) == expected_response


@responses.activate
def test_stats_handles_errors(client, url, website_id):
    startAt = 200
    endAt = 300
    responses.get(
        f"{url}websites/{website_id}/stats",
        json={},
        status=500,
        match=[
            responses.matchers.query_param_matcher(
                {"startAt": str(startAt), "endAt": str(endAt)}
            )
        ],
    )
    with pytest.raises(UmamiClientError):
        client.stats(startAt, endAt)


@responses.activate
def test_metrics(client, url, website_id):
    startAt = 200
    endAt = 300
    metric_type = MetricType.PATH
    responses.get(
        f"{url}websites/{website_id}/metrics",
        json=[{"x": "abc", "y": 10}],
        match=[
            responses.matchers.query_param_matcher(
                {
                    "startAt": str(startAt),
                    "endAt": str(endAt),
                    "type": str(metric_type),
                }
            )
        ],
    )
    assert client.metrics(startAt, endAt, metric_type) == [{"x": "abc", "y": 10}]


@responses.activate
def test_metrics_handles_errors(client, url, website_id):
    startAt = 200
    endAt = 300
    metric_type = MetricType.PATH
    responses.get(
        f"{url}websites/{website_id}/metrics",
        json={},
        status=500,
        match=[
            responses.matchers.query_param_matcher(
                {
                    "startAt": str(startAt),
                    "endAt": str(endAt),
                    "type": str(metric_type),
                }
            )
        ],
    )
    with pytest.raises(UmamiClientError):
        client.metrics(startAt, endAt, metric_type)


def test_active_users_requires_website_id(url):
    with UmamiClient(url, "api_key") as client:
        with pytest.raises(UmamiConfigurationError):
            client.active_users()


@responses.activate
def test_stats_handles_invalid_json(client, url, website_id):
    startAt = 200
    endAt = 300
    responses.get(
        f"{url}websites/{website_id}/stats",
        body="not json",
        status=200,
        content_type="application/json",
        match=[
            responses.matchers.query_param_matcher(
                {"startAt": str(startAt), "endAt": str(endAt)}
            )
        ],
    )
    with pytest.raises(UmamiClientError):
        client.stats(startAt, endAt)
