from itertools import groupby

from django.db.models import Sum


class PlacesSerializer:

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset

    @property
    def data(self):
        total = self.queryset.aggregate(total=Sum('budget_total'))['total']

        zonas = []
        qs = self.queryset.order_by('distrito__zona')
        for zona_name, infos in groupby(qs, lambda i: i.distrito.zona):
            infos = list(infos)
            total_zonas = sum(info.budget_total for info in infos)
            zonas.append({'name': zona_name, 'total': total_zonas})
        zonas.sort(key=lambda z: z['total'], reverse=True)

        etapas = []
        qs = self.queryset.order_by('tipoesc__etapa')
        for etapa_name, infos in groupby(qs, lambda i: i.tipoesc.etapa):
            infos = list(infos)
            total_etapas = sum(info.budget_total for info in infos)
            unidades = len(infos)
            etapas.append({'name': etapa_name, 'unidades': unidades,
                           'total': total_etapas})
        etapas.sort(key=lambda e: e['unidades'], reverse=True)

        return {
            'total': total,
            'places': zonas,
            'etapas': etapas,
        }
