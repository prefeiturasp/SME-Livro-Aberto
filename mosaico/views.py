from datetime import date
from urllib.parse import urlencode

from django_filters import rest_framework as filters
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from django.urls import reverse
from django.http import HttpResponseRedirect

from budget_execution.models import Grupo, Elemento, Execucao, \
    FonteDeRecursoGrupo, Programa, Subfuncao, Subgrupo
from mosaico.serializers import (
    ElementoSerializer,
    FonteDeRecursoSerializer,
    GrupoSerializer,
    ProgramaSerializer,
    ProjetoAtividadeSerializer,
    SubelementoSerializer,
    SubfuncaoSerializer,
    SubgrupoSerializer,
    TimeseriesSerializer,
)


class ExecucaoFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='year')
    fonte = filters.NumberFilter(field_name='fonte_grupo_id')

    class Meta:
        model = Execucao
        fields = ('fonte', 'year')


class SimplesViewMixin:
    tecnico = False

    def get_root_url(self):
        return reverse('mosaico:subfuncoes')


class TecnicoViewMixin:
    tecnico = True

    def get_root_url(self):
        return reverse('mosaico:grupos')


# `Simples` visualization views

class BaseListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExecucaoFilter
    template_name = 'mosaico/base.html'

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        year = self.request.query_params.get('year')
        if year:
            self.year = int(year)
            return queryset
        else:
            self.year = Execucao.objects.order_by('year').last().year.year
            return queryset.filter(year__year=self.year)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        if queryset:
            breadcrumb = self.create_breadcrumb(queryset)
        else:
            breadcrumb = []

        deflate = bool(self.request.GET.get('deflate', None))
        tseries_qs = self.get_timeseries_queryset().order_by('year')
        tseries_serializer = TimeseriesSerializer(tseries_qs, deflate=deflate)

        return Response({
            'year': self.year,
            'breadcrumb': breadcrumb,
            'execucoes': serializer.data,
            'timeseries': tseries_serializer.data,
            'tecnico': self.tecnico,
            'root_url': self.get_root_url(),
            'fontes_de_recurso': self.get_fonte_grupo_filters()
        })

    def get_fonte_grupo_filters(self):
        fontes = FonteDeRecursoGrupo.objects.all()
        return FonteDeRecursoSerializer(fontes, many=True).data

    def get_timeseries_queryset(self):
        return self.get_queryset()

    def create_breadcrumb(self, queryset):
        raise NotImplemented


def querystring(params):
    prefix = '?' if params else ''
    return prefix + params.urlencode()


class GruposListView(BaseListView, SimplesViewMixin):
    serializer_class = GrupoSerializer

    def get_queryset(self):
        return Execucao.objects.filter(subgrupo_id__isnull=False)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subgrupo__grupo_id')

    def get_timeseries_queryset(self):
        return Execucao.objects.all()

    def create_breadcrumb(self, queryset):
        params = self.request.query_params
        qs = querystring(params)
        return [
            {"name": f'Ano {self.year}',
             'url': reverse('mosaico:grupos') + qs}
        ]


class SubgruposListView(BaseListView, SimplesViewMixin):
    serializer_class = SubgrupoSerializer

    def get_queryset(self):
        grupo_id = self.kwargs['grupo_id']
        return Execucao.objects.filter(subgrupo__grupo_id=grupo_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subgrupo')

    def create_breadcrumb(self, queryset):
        execucao = queryset[0]
        subgrupo = execucao.subgrupo
        grupo = subgrupo.grupo
        year = execucao.year.year
        params = self.request.query_params
        qs = querystring(params)

        return [
            {"name": f'Ano {year}', 'url': execucao.get_url('grupos') + qs},
            {"name": grupo.desc, 'url': execucao.get_url('subgrupos') + qs}
        ]


class ElementosListView(BaseListView, SimplesViewMixin):
    serializer_class = ElementoSerializer

    def get_queryset(self):
        subgrupo_id = self.kwargs['subgrupo_id']
        return Execucao.objects.filter(subgrupo_id=subgrupo_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('elemento')

    def create_breadcrumb(self, queryset):
        execucao = queryset[0]
        subgrupo = execucao.subgrupo
        grupo = subgrupo.grupo
        year = execucao.year.year
        params = self.request.query_params
        qs = querystring(params)

        return [
            {"name": f'Ano {year}', 'url': execucao.get_url('grupos') + qs},
            {"name": grupo.desc, 'url': execucao.get_url('subgrupos') + qs},
            {"name": subgrupo.desc, 'url': execucao.get_url('elementos') + qs}
        ]


class SubelementosListView(BaseListView, SimplesViewMixin):
    serializer_class = SubelementoSerializer

    def get_queryset(self):
        subgrupo_id = self.kwargs['subgrupo_id']
        elemento_id = self.kwargs['elemento_id']
        return Execucao.objects.filter(subgrupo_id=subgrupo_id,
                elemento_id=elemento_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subelemento')

    def create_breadcrumb(self, queryset):
        execucao = queryset[0]
        subgrupo = execucao.subgrupo
        grupo = subgrupo.grupo
        elemento = execucao.elemento
        year = execucao.year.year
        params = self.request.query_params
        qs = querystring(params)

        return [
            {"name": f'Ano {year}', 'url': execucao.get_url('grupos') + qs},
            {"name": grupo.desc, 'url': execucao.get_url('subgrupos') + qs},
            {"name": subgrupo.desc, 'url': execucao.get_url('elementos') + qs},
            {"name": elemento.desc, 'url': execucao.get_url('subelementos') + qs},
        ]


# `Técnico` visualization views

class SubfuncoesListView(BaseListView, TecnicoViewMixin):
    serializer_class = SubfuncaoSerializer

    def get_queryset(self):
        return Execucao.objects.all()

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subfuncao')

    def create_breadcrumb(self, queryset):
        year = self.year
        execucao = queryset[0]
        params = self.request.query_params
        qs = querystring(params)
        return [
            {"name": f'Ano {year}', 'url': execucao.get_url('subfuncoes') + qs},
        ]


class ProgramasListView(BaseListView, TecnicoViewMixin):
    serializer_class = ProgramaSerializer

    def get_queryset(self):
        subfuncao_id = self.kwargs['subfuncao_id']
        return Execucao.objects.filter(subfuncao_id=subfuncao_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('programa')

    def create_breadcrumb(self, queryset):
        year = self.year
        execucao = queryset[0]
        subfuncao = execucao.subfuncao
        params = self.request.query_params
        qs = querystring(params)
        return [
            {"name": f'Ano {year}', 'url': execucao.get_url('subfuncoes') + qs},
            {"name": subfuncao.desc, 'url': execucao.get_url('programas') + qs},
        ]


class ProjetosAtividadesListView(BaseListView, TecnicoViewMixin):
    serializer_class = ProjetoAtividadeSerializer

    def get_queryset(self):
        subfuncao_id = self.kwargs['subfuncao_id']
        programa_id = self.kwargs['programa_id']
        return Execucao.objects.filter(subfuncao_id=subfuncao_id,
                programa_id=programa_id)

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('projeto')

    def create_breadcrumb(self, queryset):
        year = self.year
        execucao = queryset[0]
        subfuncao = execucao.subfuncao
        programa = execucao.programa
        params = self.request.query_params
        qs = querystring(params)
        return [
            {"name": f'Ano {year}', 'url': execucao.get_url('subfuncoes') + qs},
            {"name": subfuncao.desc, 'url': execucao.get_url('programas') + qs},
            {"name": programa.desc, 'url': execucao.get_url('projetos') + qs},
        ]
