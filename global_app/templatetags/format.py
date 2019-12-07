from django import template

register = template.Library()

@register.filter(name='format')
def format(value, fmt):
    return fmt.format(value)

@register.filter(name='percentage')
def percentage(value):
    return value * 100
