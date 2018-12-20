from functools import lru_cache
from itertools import groupby
from urllib.parse import urlencode

from django.db.models import Sum
from rest_framework import serializers

from budget_execution.models import Execucao
from from_to_handler.models import Deflator


class TimeseriesSerializer:

    def __init__(self, queryset, deflate=False, *args, **kwargs):
        self.queryset = queryset
        self._deflate = deflate

    def deflate(self, value, year):
        if self._deflate:
            try:
                deflator = Deflator.objects.get(year=year)
                value = value / deflator.index_number
            except Deflator.DoesNotExist:
                pass
        return value

    @property
    def data(self):
        qs = self.queryset
        ret = {}
        for year, execucoes in groupby(qs, lambda e: e.year):
            execucoes = list(execucoes)
            orcado_total = sum(e.orcado_atualizado for e in execucoes)
            empenhado_total = sum(e.empenhado_liquido for e in execucoes
                                  if e.empenhado_liquido)
            ret[year.strftime('%Y')] = {
                "orcado": self.deflate(orcado_total, year),
                "empenhado": self.deflate(empenhado_total, year),
            }

        return ret


class BaseSerializer(serializers.ModelSerializer):

    orcado_total = serializers.SerializerMethodField()
    empenhado_total = serializers.SerializerMethodField()
    percentual_empenhado = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    @lru_cache(maxsize=10)
    def get_orcado_total(self, obj):
        execs = self._execucoes(obj)
        ret = execs.aggregate(total=Sum('orcado_atualizado'))
        return ret['total']

    @lru_cache(maxsize=10)
    def get_empenhado_total(self, obj):
        execs = self._execucoes(obj)
        ret = execs.aggregate(total=Sum('empenhado_liquido'))
        return ret['total']

    def get_percentual_empenhado(self, obj):
        orcado = self.get_orcado_total(obj)
        empenhado = self.get_empenhado_total(obj)

        if empenhado:
            return empenhado / orcado
        else:
            return 0

    @property
    def query_params(self):
        params = self.context['request'].query_params
        if params:
            return "?{}".format(urlencode(params))
        return ''


# `Simples` visualization serializers

class GrupoSerializer(BaseSerializer):

    grupo_id = serializers.SerializerMethodField()
    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('grupo_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_grupo_id(self, obj):
        return obj.subgrupo.grupo_id

    def get_nome(self, obj):
        return obj.subgrupo.grupo.desc

    def get_url(self, obj):
        return obj.get_url('subgrupos') + self.query_params

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo__grupo_id=obj.subgrupo.grupo_id)


class SubgrupoSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('subgrupo_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_nome(self, obj):
        return obj.subgrupo.desc

    def get_url(self, obj):
        return obj.get_url("elementos") + self.query_params

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo_id=obj.subgrupo_id)


class ElementoSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('elemento_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_nome(self, obj):
        return obj.elemento.desc

    def get_url(self, obj):
        return obj.get_url('subelementos') + self.query_params

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo_id=obj.subgrupo_id,
            elemento_id=obj.elemento_id)


class SubelementoSerializer(ElementoSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('subelemento_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado')

    def get_nome(self, obj):
        return obj.subelemento_friendly.desc


# `Técnico` visualization serializers

class SubfuncaoSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'subfuncao_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_nome(self, obj):
        return obj.subfuncao.desc

    def get_url(self, obj):
        return obj.get_url('programas') + self.query_params

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subfuncao_id=obj.subfuncao_id)


class ProgramaSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'programa_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_nome(self, obj):
        return obj.programa.desc

    def get_url(self, obj):
        return obj.get_url('projetos') + self.query_params

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subfuncao_id=obj.subfuncao_id,
            programa_id=obj.programa_id)


class ProjetoAtividadeSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'projeto_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado')

    def get_nome(self, obj):
        return obj.projeto.desc

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year,
            subfuncao_id=obj.subfuncao_id,
            programa_id=obj.programa_id,
            projeto_id=obj.projeto_id)
