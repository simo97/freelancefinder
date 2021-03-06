"""Markdown template filter."""

from django import template
from django.utils.safestring import mark_safe

import bleach
import markdown as markdown_

register = template.Library()

ADDITIONAL_TAGS = ['p', 'br', 'pre']


@register.filter(name='markdown')
def markdown_filter(value):
    """Convert markdown value to html."""
    if value.count('<') > 5:
        # Assume this is HTML and not markdown
        rendered_html = value
    else:
        rendered_html = markdown_.markdown(value)
    bleached_html = bleach.clean(rendered_html, tags=bleach.ALLOWED_TAGS + ADDITIONAL_TAGS, strip=True)
    return mark_safe(bleached_html)
