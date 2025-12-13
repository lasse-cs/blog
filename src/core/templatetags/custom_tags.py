from django import template
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
