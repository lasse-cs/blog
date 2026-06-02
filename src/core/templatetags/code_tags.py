from django import template
from django.utils.encoding import force_str
from django.utils.html import escape
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound


register = template.Library()


@register.filter
def highlight_code(code, language):
    code = force_str(code)
    language = force_str(language)

    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        return escape(code)

    formatter = HtmlFormatter(nowrap=True)
    return mark_safe(highlight(code, lexer, formatter))
