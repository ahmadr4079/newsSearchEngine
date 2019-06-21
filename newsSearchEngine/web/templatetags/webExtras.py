from django import template
from whoosh.highlight import HtmlFormatter

register = template.Library()

@register.filter
def resultHighlightTitle(value):
    return value.highlights("title")

@register.filter
def resultHighlightSummary(value):
    return value.highlights("summary")
