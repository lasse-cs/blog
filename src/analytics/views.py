from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta
import logging

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from wagtail.admin.viewsets.base import ViewSet

from analytics.client import MetricType, Stats, UmamiClient, UmamiClientError
from analytics.models import AnalyticsSettings


logger = logging.getLogger(__name__)


def _get_client():
    return UmamiClient(
        base_url=settings.UMAMI_API_BASE,
        api_key=settings.UMAMI_API_KEY,
    )


def _get_time_range_days(days: int = 7) -> tuple[int, int]:
    now = timezone.now()
    start = now - timedelta(days=days)
    return int(start.timestamp() * 1000), int(now.timestamp() * 1000)


def _fetch_stats(start_at: int, end_at: int, website_id: str) -> Stats:
    with _get_client() as client:
        return client.stats(start_at, end_at, website_id=website_id)


def _fetch_metrics(
    start_at: int, end_at: int, metric_type: MetricType, website_id: str
) -> list:
    with _get_client() as client:
        return client.metrics(
            start_at, end_at, metric_type, limit=10, website_id=website_id
        )


def get_active_users(website_id: str) -> dict:
    cache_key = f"analytics:active_users:{website_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    with _get_client() as client:
        active = client.active_users(website_id=website_id)

    data = {"value": active, "fetched_at": timezone.now()}
    cache.set(cache_key, data, timeout=300)
    return data


def get_stats_metrics(website_id: str) -> dict:
    cache_key = f"analytics:stats_metrics:{website_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return {**cached, "warnings": []}

    start_at, end_at = _get_time_range_days(7)

    results = {"stats": None, "paths": [], "referrers": [], "countries": []}
    warnings: list[str] = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(_fetch_stats, start_at, end_at, website_id): "stats",
            executor.submit(
                _fetch_metrics, start_at, end_at, MetricType.PATH, website_id
            ): "paths",
            executor.submit(
                _fetch_metrics, start_at, end_at, MetricType.REFERRER, website_id
            ): "referrers",
            executor.submit(
                _fetch_metrics, start_at, end_at, MetricType.COUNTRY, website_id
            ): "countries",
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except UmamiClientError as e:
                warnings.append(key)
                logger.warning("Unable to fetch analytics %s: %s", key, e)
            except Exception:
                warnings.append(key)
                logger.exception("Unexpected runtime error fetching analytics %s", key)

    data = {
        "stats": results["stats"],
        "metrics": {
            "paths": results["paths"],
            "referrers": results["referrers"],
            "countries": results["countries"],
        },
        "fetched_at": timezone.now(),
        "warnings": warnings,
    }

    if (
        results["stats"]
        or results["paths"]
        or results["referrers"]
        or results["countries"]
    ):
        cache.set(
            cache_key,
            {
                "stats": data["stats"],
                "metrics": data["metrics"],
                "fetched_at": data["fetched_at"],
            },
            timeout=1200,
        )

    return data


def index(request):
    website_id = None
    try:
        analytics_settings = AnalyticsSettings.for_request(request)
        website_id = analytics_settings.umami_id
    except Exception:
        logger.exception("Failed to read analytics settings for request")

    umami_configured = bool(
        settings.UMAMI_API_BASE and settings.UMAMI_API_KEY and website_id
    )

    context = {
        "active_users": None,
        "stats": None,
        "metrics": None,
        "fetched_at": None,
        "warnings": [],
        "has_umami_config": umami_configured,
    }

    if umami_configured:
        try:
            active_data = get_active_users(website_id)
            context["active_users"] = active_data["value"]
            stats_metrics = get_stats_metrics(website_id)
            context["stats"] = stats_metrics["stats"]
            context["metrics"] = stats_metrics["metrics"]
            context["fetched_at"] = stats_metrics["fetched_at"]
            context["warnings"] = stats_metrics["warnings"]
        except UmamiClientError as e:
            logger.warning("Unable to fetch analytics dashboard data: %s", e)

    return render(request, "analytics/index.html", context)


class AnalyticsViewSet(ViewSet):
    add_to_admin_menu = True
    menu_label = "Analytics"
    icon = "desktop"
    name = "analytics"

    def get_urlpatterns(self):
        return [
            path("", index, name="index"),
        ]
