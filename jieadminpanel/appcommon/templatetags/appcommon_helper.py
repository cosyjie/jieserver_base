from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_settings(value):
    return getattr(settings, value.upper(), "")

