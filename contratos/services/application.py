from django.db.models import Sum


def serialize_big_number_data(queryset):
    years_sums = queryset.values('year__year').annotate(
        total_empenhado=Sum('valor_empenhado'),
        total_liquidado=Sum('valor_liquidado'))
