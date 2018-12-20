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
    GrupoSerializer,
    ProgramaSerializer,
    ProjetoAtividadeSerializer,
    SubelementoSerializer,
    SubfuncaoSerializer,
    SubgrupoSerializer,
    TimeseriesSerializer,
)


class ExecucaoFilter(filters.FilterSet):

    class Meta:
        model = Execucao
        fields = ['fonte_grupo_id']


class HomeView(APIView):
    def get(self, request, format=None):
        year = Execucao.objects.order_by('year').last().year.year
        redirect_url = reverse('mosaico:grupos', kwargs=dict(year=year))
        return HttpResponseRedirect(redirect_url)


class SimplesViewMixin:
    tecnico = False

    def get_root_url(self):
        year = self.kwargs['year']
        return reverse('mosaico:grupos', args=[year])

    def get_toggle_mode_url(self):
        year = self.kwargs['year']
        return reverse('mosaico:subfuncoes', args=[year])


class TecnicoViewMixin:
    tecnico = True

    def get_root_url(self):
        year = self.kwargs['year']
        return reverse('mosaico:subfuncoes', args=[year])

    def get_toggle_mode_url(self):
        year = self.kwargs['year']
        return reverse('mosaico:grupos', args=[year])


# `Simples` visualization views

class BaseListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = ExecucaoFilter
    template_name = 'mosaico/base.html'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        breadcrumb = self.create_breadcrumb()

        self.deflate = bool(self.request.GET.get('deflate', None))
        tseries_qs = self.get_timeseries_queryset()
        tseries_serializer = TimeseriesSerializer(tseries_qs,
                                                  deflate=self.deflate)
        return Response(
            {
                'breadcrumb': breadcrumb,
                'tecnico': self.tecnico,
                'toggle_mode_url': self.get_toggle_mode_url(),
                'deflate': self.deflate,
                'toggle_deflator_url': self.get_deflator_url(),
                'execucoes': serializer.data,
                'timeseries': tseries_serializer.data,
            }
        )

    def get_fonte_grupo_filters(self):
        return [
            {fonte_grupo.id: fonte_grupo.desc}
            for fonte_grupo
            in FonteDeRecursoGrupo.objects.all().order_by('id')]

    def get_deflator_url(self):
        url = self.get_root_url()
        params = self.request.GET.copy()
        if self.deflate:
            params.pop('deflate')
        else:
            params['deflate'] = True

        return url

    def get_timeseries_queryset(self):
        raise NotImplemented

    def create_breadcrumb(self):
        raise NotImplemented


class GruposListView(BaseListView, SimplesViewMixin):
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

    def create_breadcrumb(self):
        year = self.kwargs["year"]
        return [
            {"name": f'Ano {year}',
             'url': reverse('mosaico:grupos', args=[year])}
        ]


class SubgruposListView(BaseListView, SimplesViewMixin):
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

    def create_breadcrumb(self):
        year = self.kwargs['year']
        grupo_id = self.kwargs['grupo_id']
        grupo = Grupo.objects.get(id=grupo_id)
        return [
            {"name": f'Ano {year}',
             'url': reverse('mosaico:grupos', args=[year])},
            {"name": grupo.desc, 'url': ''}
        ]


class ElementosListView(BaseListView, SimplesViewMixin):
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

    def create_breadcrumb(self):
        year = self.kwargs['year']
        subgrupo = Subgrupo.objects.get(id=self.kwargs['subgrupo_id'])
        return [
            {"name": f'Ano {year}',
             'url': reverse('mosaico:grupos', args=[year])},
            {"name": subgrupo.grupo.desc,
             'url': reverse('mosaico:subgrupos',
                            args=[year, subgrupo.grupo.id])},
            {"name": subgrupo.desc, 'url': ''}
        ]


class SubelementosListView(BaseListView, SimplesViewMixin):
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

    def create_breadcrumb(self):
        year = self.kwargs['year']
        subgrupo = Subgrupo.objects.get(id=self.kwargs['subgrupo_id'])
        elemento = Elemento.objects.get(id=self.kwargs['elemento_id'])
        return [
            {"name": f'Ano {year}',
             'url': reverse('mosaico:grupos', args=[year])},
            {"name": subgrupo.grupo.desc,
             'url': reverse('mosaico:subgrupos',
                            args=[year, subgrupo.grupo.id])},
            {"name": subgrupo.desc,
             'url': reverse(
                 'mosaico:elementos',
                 args=[year, subgrupo.grupo.id, subgrupo.id]
             )},
            {"name": elemento.desc, 'url': ''}
        ]


# `Técnico` visualization views

class SubfuncoesListView(BaseListView, TecnicoViewMixin):
    serializer_class = SubfuncaoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        return Execucao.objects.filter(year=date(year, 1, 1))

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        return qs.distinct('subfuncao')

    def get_timeseries_queryset(self):
        return Execucao.objects.all().order_by('year')

    def create_breadcrumb(self):
        year = self.kwargs["year"]
        return [
            {"name": f'Ano {year}', 'url': ''}
        ]


class ProgramasListView(BaseListView, TecnicoViewMixin):
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

    def create_breadcrumb(self):
        year = self.kwargs["year"]
        subfuncao = Subfuncao.objects.get(id=self.kwargs['subfuncao_id'])
        return [
            {"name": f'Ano {year}',
             'url': reverse('mosaico:subfuncoes', args=[year])},
            {"name": subfuncao.desc, 'url': ''},
        ]


class ProjetosAtividadesListView(BaseListView, TecnicoViewMixin):
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

    def create_breadcrumb(self):
        year = self.kwargs["year"]
        subfuncao = Subfuncao.objects.get(id=self.kwargs['subfuncao_id'])
        programa = Programa.objects.get(id=self.kwargs['programa_id'])
        return [
            {"name": f'Ano {year}',
             'url': reverse('mosaico:subfuncoes', args=[year])},
            {"name": subfuncao.desc,
             'url': reverse('mosaico:programas',
                            args=[year, subfuncao.id])},
            {"name": programa.desc, 'url': ''},
        ]
