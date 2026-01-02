from django.template import Library

from core.models import PageTag

register = Library()


@register.simple_tag
def tag_list():
    return PageTag.objects.all()
