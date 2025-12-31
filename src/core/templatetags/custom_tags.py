from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html

register = template.Library()


@register.filter
def highlight_after_first_dot(value):
    if not value:
        return value

    str_value = str(value)
    split = str_value.split(".", maxsplit=1)
    if len(split) != 2:
        return value

    return format_html('{}<span class="highlight">.{}</span>', split[0], split[1])


@register.simple_tag
def svg_icon(icon_name, class_name=None):
    svg = render_to_string(f"non_patterns/svgs/{icon_name}.svg")
    if class_name:
        return format_html('<span class="{}">{}</span>', class_name, svg)
    else:
        return format_html("<span>{}</span>", svg)
