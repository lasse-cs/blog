from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path
from django.utils import timezone
from wagtail.admin.viewsets.base import ViewSet

from analytics.client import MetricType, Stats, UmamiClient
from analytics.models import AnalyticsSettings


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
    cache.set(cache_key, active, timeout=300)
    return active


def get_stats(website_id: str) -> dict:
    cache_key = f"analytics:stats:{website_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    start_at, end_at = _get_time_range_days(7)
    stats = _fetch_stats(start_at, end_at, website_id)
    if stats:
        cache.set(cache_key, stats)
    return stats


def get_metrics(website_id: str) -> dict:
    cache_key = f"analytics:stats_metrics:{website_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return {**cached, "warnings": []}

    start_at, end_at = _get_time_range_days(7)

    metrics = {"paths": [], "referrers": [], "countries": []}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
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
            metrics[key] = future.result()

    if metrics:
        cache.set(cache_key, metrics, timeout=1200)
    return metrics


def index(request):
    analytics_settings = AnalyticsSettings.for_request(request)
    website_id = analytics_settings.umami_id
    umami_configured = bool(
        settings.UMAMI_API_BASE and settings.UMAMI_API_KEY and website_id
    )
    return render(
        request, "analytics/index.html", {"umami_configured": umami_configured}
    )


def active_users(request):
    analytics_settings = AnalyticsSettings.for_request(request)
    website_id = analytics_settings.umami_id
    active_users = get_active_users(website_id)
    return JsonResponse({"active_users": active_users})


def stats(request):
    analytics_settings = AnalyticsSettings.for_request(request)
    website_id = analytics_settings.umami_id
    stats = get_stats(website_id)
    return JsonResponse({"stats": stats})


def metrics(request):
    analytics_settings = AnalyticsSettings.for_request(request)
    website_id = analytics_settings.umami_id
    metrics = get_metrics(website_id)
    return JsonResponse({"metrics": metrics})


class AnalyticsViewSet(ViewSet):
    add_to_admin_menu = True
    menu_label = "Analytics"
    icon = "desktop"
    name = "analytics"

    def get_urlpatterns(self):
        return [
            path("", index, name="index"),
            path("active_users/", active_users, name="active_users"),
            path("stats/", stats, name="stats"),
            path("metrics/", metrics, name="metrics"),
        ]
