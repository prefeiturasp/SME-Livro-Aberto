from operator import itemgetter
from django import template

register = template.Library()

@register.filter(name='sum_of')
def sum_of(value, attr_name):
    return sum(map(itemgetter(attr_name), value))
