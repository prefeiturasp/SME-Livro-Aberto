from datetime import date

from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

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


# `Simples` visualization views

class BaseListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    template_name = 'mosaico/base.html'

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'breadcrumb': self.breadcrumb,
                         'execucoes': serializer.data})

    @property
    def breadcrumb(self):
        raise NotImplemented


class GruposListView(BaseListView):
    serializer_class = GrupoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        return Execucao.objects.filter(year=date(year, 1, 1)) \
            .distinct('subgrupo__grupo')

    @property
    def breadcrumb(self):
        return f'Ano {self.kwargs["year"]}'


class SubgruposListView(BaseListView):
    serializer_class = SubgrupoSerializer
    _breadcrumb = ""

    def get_queryset(self):
        year = self.kwargs['year']
        grupo_id = self.kwargs['grupo_id']
        ret = Execucao.objects \
            .filter(year=date(year, 1, 1), subgrupo__grupo_id=grupo_id) \
            .distinct('subgrupo')
        if ret:
            self._breadcrumb = self.create_breadcrumb(ret[0])
        return ret

    def create_breadcrumb(self, obj):
        return (
            f'Ano {self.kwargs["year"]}/{obj.subgrupo.grupo.desc}')

    @property
    def breadcrumb(self):
        return self._breadcrumb


class ElementosListView(BaseListView):
    serializer_class = ElementoSerializer
    _breadcrumb = ""

    def get_queryset(self):
        year = self.kwargs['year']
        subgrupo_id = self.kwargs['subgrupo_id']
        ret = Execucao.objects \
            .filter(year=date(year, 1, 1), subgrupo_id=subgrupo_id) \
            .distinct('elemento')
        if ret:
            self._breadcrumb = self.create_breadcrumb(ret[0])
        return ret

    def create_breadcrumb(self, obj):
        return (
            f'Ano {self.kwargs["year"]}/{obj.subgrupo.grupo.desc}/'
            f'{obj.subgrupo.desc}')

    @property
    def breadcrumb(self):
        return self._breadcrumb


class SubelementosListView(BaseListView):
    serializer_class = SubelementoSerializer
    _breadcrumb = ""

    def get_queryset(self):
        year = self.kwargs['year']
        subgrupo_id = self.kwargs['subgrupo_id']
        elemento_id = self.kwargs['elemento_id']
        ret = Execucao.objects \
            .filter(year=date(year, 1, 1), subgrupo_id=subgrupo_id,
                    elemento_id=elemento_id) \
            .distinct('subelemento')
        if ret:
            self._breadcrumb = self.create_breadcrumb(ret[0])
        return ret

    def create_breadcrumb(self, obj):
        return (
            f'Ano {self.kwargs["year"]}/{obj.subgrupo.grupo.desc}/'
            f'{obj.subgrupo.desc}/{obj.elemento.desc}')

    @property
    def breadcrumb(self):
        return self._breadcrumb


# `Técnico` visualization views

class SubfuncoesListView(BaseListView):
    serializer_class = SubfuncaoSerializer

    def get_queryset(self):
        year = self.kwargs['year']
        return Execucao.objects.filter(year=date(year, 1, 1)) \
            .distinct('subfuncao')

    @property
    def breadcrumb(self):
        return f'Ano {self.kwargs["year"]}'


class ProgramasListView(BaseListView):
    serializer_class = ProgramaSerializer
    _breadcrumb = ""

    def get_queryset(self):
        year = self.kwargs['year']
        subfuncao_id = self.kwargs['subfuncao_id']
        ret = Execucao.objects \
            .filter(year=date(year, 1, 1), subfuncao_id=subfuncao_id) \
            .distinct('programa')
        if ret:
            self._breadcrumb = self.create_breadcrumb(ret[0])
        return ret

    def create_breadcrumb(self, obj):
        return f'Ano {self.kwargs["year"]}/{obj.subfuncao.desc}'

    @property
    def breadcrumb(self):
        return self._breadcrumb


class ProjetosAtividadesListView(BaseListView):
    serializer_class = ProjetoAtividadeSerializer
    _breadcrumb = ""

    def get_queryset(self):
        year = self.kwargs['year']
        subfuncao_id = self.kwargs['subfuncao_id']
        programa_id = self.kwargs['programa_id']
        ret = Execucao.objects \
            .filter(year=date(year, 1, 1), subfuncao_id=subfuncao_id,
                    programa_id=programa_id) \
            .distinct('projeto')
        if ret:
            self._breadcrumb = self.create_breadcrumb(ret[0])
        return ret

    def create_breadcrumb(self, obj):
        return (
            f'Ano {self.kwargs["year"]}/{obj.subfuncao.desc}/'
            f'{obj.programa.desc}')

    @property
    def breadcrumb(self):
        return self._breadcrumb
