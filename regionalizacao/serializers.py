from itertools import groupby

from django.db.models import Sum


class PlacesSerializer:

    def __init__(self, queryset, level, *args, **kwargs):
        self.queryset = queryset
        self.level = level

    @property
    def data(self):
        total = self.queryset.aggregate(total=Sum('budget_total'))['total']

        return {
            'total': total,
            'places': self.build_places_data(),
            'etapas': self.build_etapas_data(),
        }

    def build_places_data(self):
        pĺaces = []

        if self.level == 0:
            qs = self.queryset.order_by('distrito__zona')
            for zona_name, infos in groupby(qs, lambda i: i.distrito.zona):
                infos = list(infos)
                total_pĺaces = sum(info.budget_total for info in infos)
                pĺaces.append({'name': zona_name, 'total': total_pĺaces})
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        elif self.level == 1:
            qs = self.queryset.order_by('dre')
            for dre, infos in groupby(qs, lambda i: i.dre):
                infos = list(infos)
                total_pĺaces = sum(info.budget_total for info in infos)
                pĺaces.append({'code': dre.code, 'name': dre.name,
                               'total': total_pĺaces})
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        elif self.level == 2:
            qs = self.queryset.order_by('distrito')
            for distrito, infos in groupby(qs, lambda i: i.distrito):
                infos = list(infos)
                total_pĺaces = sum(info.budget_total for info in infos)
                pĺaces.append({'code': distrito.coddist, 'name': distrito.name,
                               'total': total_pĺaces})
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        return pĺaces

    def build_etapas_data(self):
        etapas = []
        qs = self.queryset.order_by('tipoesc__etapa')
        for etapa_name, infos in groupby(qs, lambda i: i.tipoesc.etapa):
            infos = list(infos)
            total_etapas = sum(info.budget_total for info in infos)
            unidades = len(infos)
            etapas.append({'name': etapa_name, 'unidades': unidades,
                           'total': total_etapas})
        etapas.sort(key=lambda e: (e['unidades'], e['total']), reverse=True)
        return etapas
