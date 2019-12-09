from copy import deepcopy
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

        self.rede = self.map_queryset.first().rede

    @property
    def data(self):
        current_level = self.get_current_level()
        breadcrumb = self.build_breadcrumb()
        total = self.map_queryset.aggregate(total=Sum('budget_total'))['total']
        places = self.build_places_data()
        locations = self.build_locations_data()

        ret = {
            'current_level': current_level,
            'breadcrumb': breadcrumb,
            'total': total,
            'locations': locations,
            'places': places,
        }

        if self.level == 4:
            ret['escola'] = self.build_escola_data()
            return ret

        etapas = self.build_etapas_data()

        ret['etapas'] = etapas

        if self.rede == 'CON':
            vagas = self.map_queryset.aggregate(
                total=Sum('total_vagas'))['total']
            ret['vagas'] = vagas

        return ret

    def url(self, params):
        url = reverse('regionalizacao:home')
        if params:
            qdict = QueryDict('', mutable=True)
            qdict.update(params)
            url = f'{url}?{qdict.urlencode()}&localidade={self.locations_type}'
        return url

    def get_current_level(self):
        params = deepcopy(self.query_params)
        info1 = self.map_queryset.first()

        current_level = 'São Paulo'
        if 'zona' in params:
            current_level = params['zona']
        if 'dre' in params:
            current_level = info1.dre.name
        if 'distrito' in params:
            current_level = info1.distrito.name
        if 'escola' in params:
            current_level = f'{info1.tipoesc.code} - {info1.nomesc}'

        return current_level

    def build_breadcrumb(self):
        params = deepcopy(self.query_params)
        info1 = self.map_queryset.first()
        ret = []
        if 'escola' in params:
            ret.append({
                'name': f'{info1.tipoesc.code} - {info1.nomesc}',
                'url': self.url(params),
            })
            params.pop('escola')

        if 'distrito' in params:
            ret.append({
                'name': info1.distrito.name,
                'url': self.url(params),
            })
            params.pop('distrito')

        if 'dre' in params:
            ret.append({
                'name': info1.dre.name,
                'url': self.url(params),
            })
            params.pop('dre')

        if 'zona' in params:
            ret.append({
                'name': params['zona'],
                'url': self.url(params),
            })
            params.pop('zona')

        ret.append({
            'name': 'São Paulo',
            'url': self.url(params),
        })

        ret.reverse()
        return ret

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

        else:
            if self.level == 3:
                qs = self.map_queryset.all()
            else:
                info1 = self.map_queryset.first()
                qs = self.locations_queryset.filter(distrito=info1.distrito)

            for info in qs:
                params = {
                    **self.query_params,
                    'escola': info.escola.codesc,
                }
                pĺaces.append({
                    'code': info.escola.codesc,
                    'name': f'{info.tipoesc.code} - {info.nomesc}',
                    'latitude': str(info.latitude),
                    'longitude': str(info.longitude),
                    'slug': ETAPA_SLUGS.get(info.tipoesc.etapa, None),
                    'url': self.url(params),
                })
            pĺaces.sort(key=lambda z: z['name'], reverse=True)

        return pĺaces

    def build_escola_data(self):
        if not self.map_queryset.count() == 1:
            raise Exception
        escola = self.map_queryset.first()
        return EscolaInfoSerializer(escola).data

    def build_etapas_data(self):
        etapas = []
        qs = self.map_queryset.order_by('tipoesc__etapa')
        for etapa, infos in groupby(qs, lambda i: i.tipoesc.etapa):
            infos = list(infos)
            total_etapas = sum(info.budget_total for info in infos)
            unidades = len(infos)
            etapa_dict = {
                'name': etapa,
                'unidades': unidades,
                'total': total_etapas,
                'slug': ETAPA_SLUGS.get(etapa, None),
                'tipos': self._build_tipos(infos),
            }
            if self.rede == 'CON':
                vagas = sum(info.total_vagas for info in infos)
                etapa_dict['vagas'] = vagas
            etapas.append(etapa_dict)
        etapas.sort(key=lambda e: (e['unidades'], e['total']), reverse=True)
        return etapas

    def _build_tipos(self, infos):
        tipos = []
        infos.sort(key=lambda i: i.tipoesc.code)
        for tipo, infos in groupby(infos, lambda i: i.tipoesc):
            tipos.append({'code': tipo.code, 'desc': tipo.desc})
        tipos.sort(key=lambda t: t['code'])
        return tipos

    def build_locations_data(self):
        locations = []
        if self.locations_type == 'dre':
            qs = self.locations_queryset.order_by('dre__name')
            for dre_name, infos in groupby(qs, lambda i: i.dre.name):
                infos = list(infos)
                total_locations = sum(info.budget_total for info in infos)
                locations.append({
                    'name': dre_name,
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
    vagas = serializers.SerializerMethodField()

    class Meta:
        model = EscolaInfo
        fields = ('name', 'address', 'cep', 'total', 'recursos', 'latitude',
                  'longitude', 'vagas')

    def get_name(self, obj):
        return f'{obj.tipoesc.code} - {obj.nomesc}'

    def get_address(self, obj):
        return f'{obj.endereco}, {obj.numero} - {obj.bairro}'

    def get_vagas(self, obj):
        if obj.rede == 'CON':
            return obj.total_vagas
        return None
