from contextlib import suppress
from operator import itemgetter

from django import template

register = template.Library()

@register.filter(name='sum_of')
def sum_of(value, attr_name):
    with suppress(KeyError):
        return sum(map(itemgetter(attr_name), value))


@register.filter(name='split')
def split(value, sep=None):
    if hasattr(value, 'split'):
        return value.split(sep=sep)
    else:
        return [value]
