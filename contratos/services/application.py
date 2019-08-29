from contextlib import suppress

from django.db.models import Sum

from contratos.models import ExecucaoContrato


def serialize_big_number_data(queryset):
    year_sum_qs = queryset.values('year__year').annotate(
        total_empenhado=Sum('valor_empenhado'),
        total_liquidado=Sum('valor_liquidado'))

    if year_sum_qs:
        year_sum = year_sum_qs[0]
    else:
        return {}

    empenhado = year_sum['total_empenhado']
    liquidado = year_sum['total_liquidado']
    percent_liquidado = liquidado / empenhado
    year_dict = {
        'year': year_sum['year__year'],
        'empenhado': empenhado,
        'liquidado': liquidado,
        'percent_liquidado': percent_liquidado,
    }

    return year_dict


def serialize_destinations(queryset):
    empenhado_qs = queryset.values('year__year')\
        .annotate(total_empenhado=Sum('valor_empenhado')) \
        .distinct()
    if empenhado_qs:
        total_empenhado = empenhado_qs[0]['total_empenhado']
    else:
        return []

    categorias_sums = queryset \
        .values("year__year", "categoria__name", "categoria__desc",
                "categoria__slug") \
        .annotate(total_empenhado=Sum('valor_empenhado'),
                  total_liquidado=Sum('valor_liquidado'))

    year_list = []
    for cat_data in categorias_sums:
        empenhado = cat_data['total_empenhado']
        liquidado = cat_data['total_liquidado']
        percent_liquidado = liquidado / empenhado
        percent_empenhado = empenhado / total_empenhado
        cat_dict = {
            'year': cat_data['year__year'],
            'categoria_name': cat_data['categoria__name'],
            'categoria_desc': cat_data['categoria__desc'],
            'categoria_slug': cat_data['categoria__slug'],
            'empenhado': empenhado,
            'liquidado': liquidado,
            'percent_liquidado': percent_liquidado,
            'percent_empenhado': percent_empenhado,
        }
        year_list.append(cat_dict)

    return year_list


def serialize_top5(queryset, categoria_id=None):
    if categoria_id:
        queryset = queryset.filter(categoria_id=categoria_id)

    top5_contratos = queryset \
        .values("year__year", "cod_contrato", "fornecedor__razao_social",
                "categoria__name", "categoria__desc", "modalidade__desc",
                "objeto_contrato__desc") \
        .annotate(total_empenhado=Sum('valor_empenhado')) \
        .order_by('-valor_empenhado')[:5]

    top5_list = []
    for contrato in top5_contratos:
        exec_dict = {
            'year': contrato['year__year'],
            'cod_contrato': contrato['cod_contrato'],
            'categoria_name': contrato['categoria__name'],
            'categoria_desc': contrato['categoria__desc'],
            'fornecedor': contrato['fornecedor__razao_social'],
            'objeto_contrato': contrato['objeto_contrato__desc'],
            'modalidade': contrato['modalidade__desc'],
            'empenhado': contrato['total_empenhado'],
        }
        top5_list.append(exec_dict)
    return top5_list


def cast_to_int(value):
    with suppress(TypeError, ValueError):
        return int(value)


def serialize_filters(queryset, categoria_id, year):
    years = ExecucaoContrato.objects.all().values('year__year').distinct() \
        .order_by('year')
    categorias = queryset.values('categoria__id', 'categoria__name'). distinct()

    ret = {
        # TODO: A better solution may be serialize the filter form
        'selected_year': cast_to_int(year),
        'selected_categoria': cast_to_int(categoria_id),
        'years': [year_qs['year__year'] for year_qs in years]
    }

    categorias_list = []
    for categoria_qs in categorias:
        categoria_dict = {
            'id': categoria_qs['categoria__id'],
            'name': categoria_qs['categoria__name'],
        }
        categorias_list.append(categoria_dict)
    ret['categorias'] = categorias_list
    return ret
