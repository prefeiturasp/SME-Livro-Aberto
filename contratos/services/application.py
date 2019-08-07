from datetime import date

from django.db.models import Sum

from contratos.constants import CONTRATOS_INITIAL_YEAR


def serialize_big_number_data(queryset):
    years_sums = queryset.order_by('year').values('year__year').annotate(
        total_empenhado=Sum('valor_empenhado'),
        total_liquidado=Sum('valor_liquidado'))

    ret = []
    for year_data in years_sums:
        empenhado = year_data['total_empenhado']
        liquidado = year_data['total_liquidado']
        percent_liquidado = liquidado * 100 / empenhado
        year_dict = {
            'year': year_data['year__year'],
            'empenhado': empenhado,
            'liquidado': liquidado,
            'percent_liquidado': percent_liquidado,
        }
        ret.append(year_dict)

    return ret


def serialize_destinies(queryset):
    current_year = date.today().year
    years = list(range(CONTRATOS_INITIAL_YEAR, current_year + 1))

    ret = {}
    for year in years:
        categorias_sums = queryset.filter(year__year=year) \
            .values("categoria__name", "categoria__desc").annotate(
                total_empenhado=Sum('valor_empenhado'),
                total_liquidado=Sum('valor_liquidado'))

        year_list = []
        for cat_data in categorias_sums:
            empenhado = cat_data['total_empenhado']
            liquidado = cat_data['total_liquidado']
            percent_liquidado = liquidado * 100 / empenhado
            cat_dict = {
                'categoria_name': cat_data['categoria__name'],
                'categoria_desc': cat_data['categoria__desc'],
                'empenhado': empenhado,
                'liquidado': liquidado,
                'percent_liquidado': percent_liquidado,
            }
            year_list.append(cat_dict)

        ret[year] = year_list

    return ret
