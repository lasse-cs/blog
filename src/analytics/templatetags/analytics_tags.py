from django import template
from django.conf import settings
from django.utils.html import format_html

from analytics.models import AnalyticsSettings

register = template.Library()


@register.simple_tag(takes_context=True)
def analytics_tracker(context):
    if "request" not in context:
        return ""
    if getattr(context["request"], "is_preview", False):
        return ""
    if context.get("is_pattern_library", False):
        return ""
    try:
        analytics_settings = AnalyticsSettings.for_request(request=context["request"])
    except Exception:
        return ""
    if not settings.UMAMI_HOST or not analytics_settings.umami_id:
        return ""
    umami_script = settings.UMAMI_HOST.rstrip("/") + "/script.js"
    return format_html(
        '<script defer src="{}" data-website-id="{}"></script>',
        umami_script,
        analytics_settings.umami_id,
    )
