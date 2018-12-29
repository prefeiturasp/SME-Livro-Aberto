from urllib.parse import urlencode

from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

from django.urls import reverse

from budget_execution.models import Execucao, FonteDeRecursoGrupo
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


SERIALIZERS_BY_SECTION = {
    'grupos': GrupoSerializer,
    'subgrupos': SubgrupoSerializer,
    'elementos': ElementoSerializer,
    'subelementos': SubelementoSerializer,
    'subfuncoes': SubfuncaoSerializer,
    'programas': ProgramaSerializer,
    'projetos': ProjetoAtividadeSerializer,
}

DISTINCT_FIELD_BY_SECTION = {
    'grupos': 'subgrupo__grupo_id',
    'subgrupos': 'subgrupo',
    'elementos': 'elemento',
    'subelementos': 'subelemento',
    'subfuncoes': 'subfuncao',
    'programas': 'programa',
    'projetos': 'projeto',
}


class ExecucaoFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='year', lookup_expr='year')
    fonte = filters.NumberFilter(field_name='fonte_grupo_id')
    grupo_id = filters.CharFilter(method='filter_grupo')

    def filter_grupo(self, queryset, name, value):
        qs = queryset.filter(subgrupo__grupo_id=int(value))
        return qs

    class Meta:
        model = Execucao
        fields = ['year', 'grupo_id', 'subgrupo_id', 'elemento_id',
                  'subfuncao_id', 'programa_id', 'fonte']


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
        self.filters = self.request.query_params.dict()
        year = self.request.query_params.get('year')
        if year:
            self.year = int(year)
            return queryset
        else:
            self.year = Execucao.objects.order_by('year').last().year.year
            self.filters['year'] = self.year
            return queryset.filter(year__year=self.year)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['filters'] = self.filters
        return context

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
            'fontes_de_recurso': self.get_fonte_grupo_filters(),
            'download_full_csv_url': self.get_download_csv_url(),
            'download_filtered_csv_url': self.get_download_csv_url(
                filtered=True),
        })

    def get_fonte_grupo_filters(self):
        fontes = FonteDeRecursoGrupo.objects.all()
        context = {'request': self.request}
        return FonteDeRecursoSerializer(fontes, many=True, context=context).data

    def get_download_csv_url(self, filtered=False):
        csv_url = reverse('mosaico:download', args=[self.name])
        url_params = self.kwargs.copy()

        if filtered:
            filters = self.filters
            filters.pop('deflate', None)
            filters.pop('format', None)
            params = {**url_params, **filters}
            params['filter'] = True
        else:
            params = {**url_params}

        if params:
            csv_url += "?{}".format(urlencode(params))

        return csv_url

    def get_timeseries_queryset(self):
        return self.get_queryset()

    def create_breadcrumb(self, queryset):
        raise NotImplemented


def querystring(params):
    prefix = '?' if params else ''
    return prefix + params.urlencode()


class GruposListView(BaseListView, SimplesViewMixin):
    name = 'grupos'
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
    name = 'subgrupos'
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
    name = 'elementos'
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
    name = 'subelementos'
    serializer_class = SubelementoSerializer

    def get_queryset(self):
        subgrupo_id = self.kwargs['subgrupo_id']
        elemento_id = self.kwargs['elemento_id']
        return Execucao.objects.filter(
            subgrupo_id=subgrupo_id, elemento_id=elemento_id)

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
            {"name": elemento.desc,
             'url': execucao.get_url('subelementos') + qs},
        ]


# `Técnico` visualization views

class SubfuncoesListView(BaseListView, TecnicoViewMixin):
    name = 'subfuncoes'
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
    name = 'programas'
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
    name = 'projetos'
    serializer_class = ProjetoAtividadeSerializer

    def get_queryset(self):
        subfuncao_id = self.kwargs['subfuncao_id']
        programa_id = self.kwargs['programa_id']
        return Execucao.objects.filter(
            subfuncao_id=subfuncao_id, programa_id=programa_id)

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


class DownloadView(generics.ListAPIView):
    renderer_classes = [CSVRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExecucaoFilter

    def get_serializer_class(self):
        return SERIALIZERS_BY_SECTION[self.section]

    def get_queryset(self):
        return Execucao.objects.filter(subgrupo_id__isnull=False) \
            .order_by(self.distinct_field, 'year')

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        if self.section == 'subelementos':
            qs = qs.filter(subelemento__isnull=False)
        return qs.distinct(self.distinct_field)

    def list(self, request, *args, **kwargs):
        self.section = self.kwargs['section']
        self.distinct_field = self._get_distinct_field_name()

        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        filename = f'mosaico_{self.kwargs["section"]}'
        if self.request.GET.get('filter'):
            filename += "_filtrado"

        headers = {
            'Content-Disposition': f'attachment; filename={filename}.csv'
        }
        response = Response(serializer.data, headers=headers)
        return response

    def _get_distinct_field_name(self):
        return DISTINCT_FIELD_BY_SECTION[self.section]
