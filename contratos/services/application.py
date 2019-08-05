from django.db.models import Sum


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
