from django import template
from whoosh.highlight import HtmlFormatter

register = template.Library()

@register.filter
def resultHighlight(value):
    return value.highlights("title")
