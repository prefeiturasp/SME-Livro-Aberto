from django import template
from django.template import defaultfilters
from django.contrib.humanize.templatetags.humanize import intword
from django.utils.translation import ngettext

register = template.Library()


@register.filter(name='format')
def format(value, fmt):
    return fmt.format(value)


@register.filter(name='percentage')
def percentage(value):
    return value * 100


@register.filter(name='small_intword')
def small_intword(value):
    if 1000 < value < 1000000:
        new_value = value / 1000
        formated = defaultfilters.floatformat(new_value, 1)
        return '%(value)s mil' % dict(value=formated)

    return intword(value)
