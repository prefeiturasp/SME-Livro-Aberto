from itertools import groupby

from django.db.models import Sum
from django.http import QueryDict
from django.urls import reverse
from rest_framework import serializers

from regionalizacao.constants import ETAPA_SLUGS
from regionalizacao.models import EscolaInfo


class PlacesSerializer:

    def __init__(self, map_queryset, locations_queryset, level, query_params,
                 locations_graph_type, *args, **kwargs):
        self.map_queryset = map_queryset
        self.locations_queryset = locations_queryset
        self.level = level
        self.query_params = {k: v for k, v in query_params.items() if v}
        self.locations_type = locations_graph_type

    @property
    def data(self):
        places = self.build_places_data()
        locations = self.build_locations_data()

        if self.level == 4:
            return {
                'escola': places,
                'locations': locations,
            }

        total = self.map_queryset.aggregate(total=Sum('budget_total'))['total']
        etapas = self.build_etapas_data()

        ret = {
            'total': total,
            'places': places,
            'etapas': etapas,
            'locations': locations,
        }

        return ret

    def url(self, params):
        url = reverse('regionalizacao:home')
        if params:
            qdict = QueryDict('', mutable=True)
            qdict.update(params)
            url = f'{url}?{qdict.urlencode()}&localidade={self.locations_type}'
        return url

    def build_places_data(self):
        pĺaces = []

        if self.level == 0:
            qs = self.map_queryset.order_by('distrito__zona')
            for zona_name, infos in groupby(qs, lambda i: i.distrito.zona):
                infos = list(infos)
                total_pĺaces = sum(info.budget_total for info in infos)
                params = {
                    **self.query_params,
                    'zona': zona_name,
                }
                pĺaces.append({
                    'name': zona_name,
                    'total': total_pĺaces,
                    'url': self.url(params),
                })
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        elif self.level == 1:
            qs = self.map_queryset.order_by('dre')
            for dre, infos in groupby(qs, lambda i: i.dre):
                infos = list(infos)
                total_pĺaces = sum(info.budget_total for info in infos)
                params = {
                    **self.query_params,
                    'dre': dre.code,
                }
                pĺaces.append({
                    'code': dre.code,
                    'name': dre.name,
                    'total': total_pĺaces,
                    'url': self.url(params),
                })
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        elif self.level == 2:
            qs = self.map_queryset.order_by('distrito')
            for distrito, infos in groupby(qs, lambda i: i.distrito):
                infos = list(infos)
                total_pĺaces = sum(info.budget_total for info in infos)
                params = {
                    **self.query_params,
                    'distrito': distrito.coddist,
                }
                pĺaces.append({
                    'code': distrito.coddist,
                    'name': distrito.name,
                    'total': total_pĺaces,
                    'url': self.url(params),
                })
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        elif self.level == 3:
            for info in self.map_queryset.all():
                params = {
                    **self.query_params,
                    'escola': info.escola.codesc,
                }
                pĺaces.append({
                    'code': info.escola.codesc,
                    'name': info.nomesc,
                    'total': info.budget_total,
                    'url': self.url(params),
                })
            pĺaces.sort(key=lambda z: z['total'], reverse=True)

        elif self.level == 4:
            if not self.map_queryset.count() == 1:
                raise Exception
            escola = self.map_queryset.first()
            return EscolaInfoSerializer(escola).data

        return pĺaces

    def build_etapas_data(self):
        etapas = []
        qs = self.map_queryset.order_by('tipoesc__etapa')
        for etapa, infos in groupby(qs, lambda i: i.tipoesc.etapa):
            infos = list(infos)
            total_etapas = sum(info.budget_total for info in infos)
            unidades = len(infos)
            etapas.append({
                'name': etapa,
                'unidades': unidades,
                'total': total_etapas,
                'slug': ETAPA_SLUGS.get(etapa, None),
                'tipos': self._build_tipos(infos),
            })
        etapas.sort(key=lambda e: (e['unidades'], e['total']), reverse=True)
        return etapas

    def _build_tipos(self, infos):
        tipos = []
        for tipo, infos in groupby(infos, lambda i: i.tipoesc):
            tipos.append({'code': tipo.code, 'desc': tipo.desc})
        tipos.sort(key=lambda t: t['code'])
        return tipos

    def build_locations_data(self):
        locations = []
        if self.locations_type == 'distrito':
            qs = self.locations_queryset.order_by('distrito__name')
            for distrito_name, infos in groupby(qs, lambda i: i.distrito.name):
                infos = list(infos)
                total_locations = sum(info.budget_total for info in infos)
                locations.append({
                    'name': distrito_name,
                    'total': total_locations,
                })
            locations.sort(key=lambda z: z['total'], reverse=True)
            return locations

        # locations_type == 'zona'
        qs = self.locations_queryset.order_by('distrito__zona')
        for zona_name, infos in groupby(qs, lambda i: i.distrito.zona):
            infos = list(infos)
            total_locations = sum(info.budget_total for info in infos)
            locations.append({
                'name': zona_name,
                'total': total_locations,
            })
        locations.sort(key=lambda z: z['total'], reverse=True)
        return locations


class EscolaInfoSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    total = serializers.FloatField(source='budget_total')

    class Meta:
        model = EscolaInfo
        fields = ('name', 'address', 'cep', 'total', 'recursos', 'latitude',
                  'longitude')

    def get_name(self, obj):
        return f'{obj.tipoesc.code} - {obj.nomesc}'

    def get_address(self, obj):
        return f'{obj.endereco}, {obj.numero} - {obj.bairro}'
