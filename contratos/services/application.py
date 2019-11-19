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
                "categoria__slug", "categoria__id") \
        .annotate(total_empenhado=Sum('valor_empenhado'),
                  total_liquidado=Sum('valor_liquidado')) \
        .order_by("categoria__name")

    year_list = []
    for cat_data in categorias_sums:
        empenhado = cat_data['total_empenhado']
        liquidado = cat_data['total_liquidado']
        percent_liquidado = liquidado / empenhado
        percent_empenhado = empenhado / total_empenhado
        cat_dict = {
            'year': cat_data['year__year'],
            'categoria_id': str(cat_data['categoria__id']),
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


def serialize_top5(queryset):
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


def serialize_date_updated():
    return ExecucaoContrato.objects.get_date_updated()
