from django import template
from django.conf import settings
from django.utils.html import format_html, mark_safe

register = template.Library()

plugin_dir = settings.STATIC_URL + 'plugins/'

template_file_css = '<link rel="stylesheet" href="{}" />'
template_file_js = '<script src="{}"></script>'


@register.simple_tag
def icheck_bootstrap():
    this_dir = 'icheck-bootstrap'
    return format_html(
        template_file_css, f'{plugin_dir}{this_dir}/icheck-bootstrap.css'
    )

