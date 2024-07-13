from django import template

register = template.Library()

@register.filter
def get_sum(scores):
    return sum(scores)

