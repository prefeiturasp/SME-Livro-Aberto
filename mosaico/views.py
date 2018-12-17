from datetime import date
from itertools import groupby

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from django.urls import reverse
from django.http import HttpResponseRedirect

from budget_execution.models import Execucao
from mosaico.serializers import (
    ElementoSerializer,
    GrupoSerializer,
    ProgramaSerializer,
    ProjetoAtividadeSerializer,
    SubelementoSerializer,
    SubfuncaoSerializer,
    SubgrupoSerializer,
)


class HomeView(APIView):
    def get(self, request, format=None):
        year = Execucao.objects.order_by('year').last().year.year
        redirect_url = reverse('mosaico:home_simples', kwargs=dict(year=year))
        return HttpResponseRedirect(redirect_url)


# `Simples` visualization views

class BaseListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'mosaico/base.html'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        breadcrumb = self.create_breadcrumb(queryset[0])

        tseries_qs = self.get_timeseries_queryset()
        tseries_data = self.prepare_timeseries_data(tseries_qs)
        return Response({'breadcrumb': breadcrumb,
                         'execucoes': serializer.data,
                         'timeseries': tseries_data})

    # TODO: move this logic to somewhere else
    def prepare_timeseries_data(self, qs):
        ret = {}
        for year, execucoes in groupby(qs, lambda e: e.year):
            execucoes = list(execucoes)
            orcado_total = sum(e.orcado_atualizado for e in execucoes)
            empenhado_total = sum(e.empenhado_liquido for e in execucoes
                                  if e.empenhado_liquido)
            ret[year.strftime('%Y')] = {
                "orcado": orcado_total,
                "empenhado": empenhado_total,
            }

        return ret

    def get_timeseries_queryset(self):
        raise NotImplemented

    def create_breadcrumb(self, obj):
        raise NotImplemented


class GruposListView(BaseListView):
    serializer_class = GrupoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        return Execucao.objects.filter(year=date(year, 1, 1),
                                       subgrupo_id__isnull=False)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subgrupo__grupo_id')

    def get_timeseries_queryset(self):
        return Execucao.objects.all().order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_simples')}
        ]


class SubgruposListView(BaseListView):
    serializer_class = SubgrupoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        grupo_id = self.kwargs['grupo_id']
        return Execucao.objects \
            .filter(year=date(year, 1, 1), subgrupo__grupo_id=grupo_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subgrupo')

    def get_timeseries_queryset(self):
        grupo_id = self.kwargs['grupo_id']
        return Execucao.objects.filter(subgrupo__grupo_id=grupo_id) \
            .order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_simples')},
            {"name": obj.subgrupo.grupo.desc, 'url': obj.get_url('grupo')}
        ]


class ElementosListView(BaseListView):
    serializer_class = ElementoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        subgrupo_id = self.kwargs['subgrupo_id']
        return Execucao.objects \
            .filter(year=date(year, 1, 1), subgrupo_id=subgrupo_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('elemento')

    def get_timeseries_queryset(self):
        subgrupo_id = self.kwargs['subgrupo_id']
        return Execucao.objects.filter(subgrupo_id=subgrupo_id) \
            .order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_simples')},
            {"name": obj.subgrupo.grupo.desc, 'url': obj.get_url('grupo')},
            {"name": obj.subgrupo.desc, 'url': obj.get_url('subgrupo')}
        ]


class SubelementosListView(BaseListView):
    serializer_class = SubelementoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        subgrupo_id = self.kwargs['subgrupo_id']
        elemento_id = self.kwargs['elemento_id']
        return Execucao.objects \
            .filter(year=date(year, 1, 1), subgrupo_id=subgrupo_id,
                    elemento_id=elemento_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subelemento')

    def get_timeseries_queryset(self):
        subgrupo_id = self.kwargs['subgrupo_id']
        elemento_id = self.kwargs['elemento_id']
        return Execucao.objects \
            .filter(subgrupo_id=subgrupo_id, elemento_id=elemento_id) \
            .order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_simples')},
            {"name": obj.subgrupo.grupo.desc, 'url': obj.get_url('grupo')},
            {"name": obj.subgrupo.desc, 'url': obj.get_url('subgrupo')},
            {"name": obj.elemento.desc, 'url': obj.get_url('elemento')}
        ]


# `Técnico` visualization views

class SubfuncoesListView(BaseListView):
    serializer_class = SubfuncaoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        return Execucao.objects.filter(year=date(year, 1, 1))

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subfuncao')

    def get_timeseries_queryset(self):
        return Execucao.objects.all().order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_tecnico')},
        ]


class ProgramasListView(BaseListView):
    serializer_class = ProgramaSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        subfuncao_id = self.kwargs['subfuncao_id']
        return Execucao.objects \
            .filter(year=date(year, 1, 1), subfuncao_id=subfuncao_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('programa')

    def get_timeseries_queryset(self):
        subfuncao_id = self.kwargs['subfuncao_id']
        return Execucao.objects \
            .filter(subfuncao_id=subfuncao_id) \
            .order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_tecnico')},
            {"name": obj.subfuncao.desc, 'url': obj.get_url('subfuncao')},
        ]


class ProjetosAtividadesListView(BaseListView):
    serializer_class = ProjetoAtividadeSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        subfuncao_id = self.kwargs['subfuncao_id']
        programa_id = self.kwargs['programa_id']
        return Execucao.objects \
            .filter(year=date(year, 1, 1), subfuncao_id=subfuncao_id,
                    programa_id=programa_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('projeto')

    def get_timeseries_queryset(self):
        subfuncao_id = self.kwargs['subfuncao_id']
        programa_id = self.kwargs['programa_id']
        return Execucao.objects \
            .filter(subfuncao_id=subfuncao_id, programa_id=programa_id) \
            .order_by('year')

    def create_breadcrumb(self, obj):
        return [
            {"name": f'Ano {self.kwargs["year"]}',
             'url': obj.get_url('home_tecnico')},
            {"name": obj.subfuncao.desc, 'url': obj.get_url('subfuncao')},
            {"name": obj.programa.desc, 'url': obj.get_url('programa')},
        ]
