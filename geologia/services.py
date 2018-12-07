from django.db.models import Sum


def prepare_gnd_data(queryset):
    years = queryset.values('year').distinct()

    ret = {
        'orcado': [],
        'empenhado': [],
    }
    for year_dict in years:
        year = year_dict['year']
        year_qs = queryset.filter(year=year)

        ret['orcado'].append(get_gnd_orcado_data(year_qs))
        ret['empenhado'].append(get_gnd_empenhado_data(year_qs))

    return ret


def get_gnd_orcado_data(queryset):
    year = queryset[0].year

    orcado_by_gnd = queryset.values('gnd_gealogia__desc') \
        .annotate(orcado=Sum('orcado_atualizado'))
    orcado_total = queryset.aggregate(total=Sum('orcado_atualizado'))

    orcado_gnds = [
        {
            "name": gnd['gnd_gealogia__desc'],
            "value": gnd['orcado'],
            "percent": gnd['orcado'] / orcado_total['total'],
        }
        for gnd in orcado_by_gnd
    ]

    return {
        "year": year.strftime("%Y"),
        "total": orcado_total['total'],
        "gnds": orcado_gnds,
    }


def get_gnd_empenhado_data(queryset):
    year = queryset[0].year

    empenhado_by_gnd = queryset.values('gnd_gealogia__desc') \
        .annotate(empenhado=Sum('empenhado_liquido'))
    empenhado_total = queryset.aggregate(total=Sum('empenhado_liquido'))

    empenhado_gnds = []
    for gnd in empenhado_by_gnd:
        if gnd['empenhado'] is None:
            gnd['empenhado'] = 0

        empenhado_gnds.append({
            "name": gnd['gnd_gealogia__desc'],
            "value": gnd['empenhado'],
            "percent": gnd['empenhado'] / empenhado_total['total'],
        })

    return {
        "year": year.strftime("%Y"),
        "total": empenhado_total['total'],
        "gnds": empenhado_gnds,
    }
