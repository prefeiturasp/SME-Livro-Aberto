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


@register.filter(name='merge_dres')
def merge_dres(locations):
    if 'DIRETORIA REGIONAL' in locations[0]['name'] or 'DRE' in locations[0]['name']:
        total_dre_ipiranga = 0.0
        total_unidades_dre_ipiranga = 0
        total_matriculas_dre_ipiranga = 0
        total_servidores_dre_ipiranga = 0
        total_dre_pirituba_jaragua = 0.0
        total_unidades_dre_pirituba_jaragua = 0
        total_matriculas_dre_pirituba_jaragua = 0
        total_servidores_dre_pirituba_jaragua = 0
        locations_to_remove = []
        for idx, location in enumerate(locations):
            if 'IPIRANGA' in location['name']:
                total_dre_ipiranga += location['total']
                total_unidades_dre_ipiranga += location['unidades']
                total_matriculas_dre_ipiranga += location['matriculas']
                total_servidores_dre_ipiranga += location['servidores']
                locations_to_remove.append(location)
            elif 'PIRITUBA/JARAGUA' in location['name']:
                total_dre_pirituba_jaragua += location['total']
                total_unidades_dre_pirituba_jaragua += location['unidades']
                total_matriculas_dre_pirituba_jaragua += location['matriculas']
                total_servidores_dre_pirituba_jaragua += location['servidores']
                locations_to_remove.append(location)
        locations.append({'name': 'DRE IPIRANGA',
                          'total': total_dre_ipiranga,
                          'unidades': total_unidades_dre_ipiranga,
                          'matriculas': total_matriculas_dre_ipiranga,
                          'servidores': total_servidores_dre_ipiranga,
                          })
        locations.append({'name': 'DRE PIRITUBA/JARAGUA', 'total': total_dre_pirituba_jaragua,
                          'unidades': total_unidades_dre_pirituba_jaragua,
                          'matriculas': total_matriculas_dre_pirituba_jaragua,
                          'servidores': total_servidores_dre_pirituba_jaragua,
                          })
        for location in locations_to_remove:
            locations.pop(locations.index(location))
        locations = sorted(locations, key=lambda l: l['name'])
    return locations
