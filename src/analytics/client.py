from enum import StrEnum
from typing import TypedDict, cast

import requests


class UmamiClientError(Exception):
    pass


class UmamiAPIError(UmamiClientError):
    def __init__(self, status_code: int, response_text: str):
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(f"Umami API error ({status_code}): {response_text}")


class UmamiConfigurationError(UmamiClientError):
    pass


class MetricType(StrEnum):
    PATH = "path"
    ENTRY = "entry"
    EXIT = "exit"
    TITLE = "title"
    QUERY = "query"
    REFERRER = "referrer"
    CHANNEL = "channel"
    DOMAIN = "domain"
    COUNTRY = "country"
    REGION = "region"
    CITY = "city"
    BROWSER = "browser"
    OS = "os"
    DEVICE = "device"
    LANGUAGE = "language"
    SCREEN = "screen"
    EVENT = "event"
    HOSTNAME = "hostname"
    TAG = "tag"
    DISTINCT_ID = "distinctId"


class Metric(TypedDict):
    x: str
    y: int


class StatsComparison(TypedDict):
    pageviews: int
    visitors: int
    visits: int
    bounces: int
    totaltime: int


class Stats(TypedDict):
    pageviews: int
    visitors: int
    visits: int
    bounces: int
    totaltime: int
    comparison: StatsComparison


class UmamiClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        website_id: str | None = None,
        timeout: int = 10,
    ):
        self.base_url = base_url.strip("/")
        self.api_key = api_key
        self.website_id = website_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"x-umami-api-key": self.api_key, "Accept": "application/json"}
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()

    def _request(self, endpoint: str, **kwargs) -> requests.Response:
        try:
            return self.session.get(
                f"{self.base_url}{endpoint}",
                timeout=self.timeout,
                **kwargs,
            )
        except requests.RequestException as e:
            raise UmamiClientError(f"Umami request failed for {endpoint}") from e

    def _handle_response(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            status_code = (
                response.status_code if e.response is None else e.response.status_code
            )
            response_text = response.text if e.response is None else e.response.text
            raise UmamiAPIError(status_code, response_text) from e
        try:
            return response.json()
        except ValueError as e:
            raise UmamiClientError("Umami API returned invalid JSON") from e

    def active_users(self, website_id: str | None = None) -> int:
        response = self._request(
            f"/websites/{self._website_id(website_id)}/active",
        )
        json_response = self._handle_response(response)
        return cast(int, json_response["visitors"])

    def _website_id(self, website_id: str | None) -> str:
        selected_website_id = website_id or self.website_id
        if not selected_website_id:
            raise UmamiConfigurationError("Umami website_id is required")
        return selected_website_id

    def metrics(
        self,
        startAt: int,
        endAt: int,
        metric_type: MetricType,
        limit: int | None = None,
        offset: int | None = None,
        website_id: str | None = None,
    ) -> list[Metric]:
        params = {
            "startAt": startAt,
            "endAt": endAt,
            "type": metric_type,
        }
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = self._request(
            f"/websites/{self._website_id(website_id)}/metrics",
            params=params,
        )
        return cast(list[Metric], self._handle_response(response))

    def stats(self, startAt: int, endAt: int, website_id: str | None = None) -> Stats:
        response = self._request(
            f"/websites/{self._website_id(website_id)}/stats",
            params={
                "startAt": startAt,
                "endAt": endAt,
            },
        )
        return cast(Stats, self._handle_response(response))
