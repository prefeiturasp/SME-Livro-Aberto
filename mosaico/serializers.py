from datetime import date, datetime
from decimal import Decimal
from functools import lru_cache
from itertools import groupby
from urllib.parse import urlencode

from django.db.models import Manager, Sum
from rest_framework import serializers

from budget_execution.models import Execucao, FonteDeRecurso
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


class ExecucaoListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        iterable = data.distinct(self.child.Meta.distinct_field)

        return [
            self.child.to_representation(item) for item in iterable
        ]


class BaseExecucaoSerializer(serializers.ModelSerializer):

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

        current_date = datetime.now().date()
        if obj.year.year == current_date.year:
            current_month = current_date.month
            proportion_factor = Decimal(current_month / 12)
        else:
            proportion_factor = 1

        if empenhado:
            return empenhado / (proportion_factor * orcado)
        else:
            return 0

    def get_url(self, obj):
        next_level = getattr(self.Meta, 'next_level')
        return obj.get_url(next_level) + self._query_params

    @property
    def _query_params(self):
        params = self.context['request'].GET
        if params:
            return '?{}'.format(urlencode(params))
        return ''


# `Simples` visualization serializers

class GrupoSerializer(BaseExecucaoSerializer):

    grupo_id = serializers.IntegerField(source='subgrupo.grupo_id',
                                        read_only=True)
    nome = serializers.CharField(source='subgrupo.grupo.desc', read_only=True)

    class Meta:
        model = Execucao
        fields = ('grupo_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')
        next_level = 'subgrupos'
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'subgrupo__grupo'

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        execs = self.instance
        return execs.filter(
            subgrupo__grupo_id=obj.subgrupo.grupo_id)


class SubgrupoSerializer(BaseExecucaoSerializer):

    nome = serializers.CharField(source='subgrupo.desc', read_only=True)

    class Meta:
        model = Execucao
        fields = ('subgrupo_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')
        next_level = 'elementos'
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'subgrupo'

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        execs = self.instance
        return execs.filter(
            subgrupo_id=obj.subgrupo_id)


class ElementoSerializer(BaseExecucaoSerializer):

    nome = serializers.CharField(source='elemento.desc', read_only=True)

    class Meta:
        model = Execucao
        fields = ('elemento_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')
        next_level = 'subelementos'
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'elemento'

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        execs = self.instance
        return execs.filter(
            subgrupo_id=obj.subgrupo_id,
            elemento_id=obj.elemento_id)


class SubelementoSerializer(ElementoSerializer):

    nome = serializers.CharField(source='subelemento_friendly.desc',
                                 read_only=True)

    class Meta:
        model = Execucao
        fields = ('subelemento_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado')
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'subelemento'


# `Técnico` visualization serializers

class SubfuncaoSerializer(BaseExecucaoSerializer):

    nome = serializers.CharField(source='subfuncao.desc', read_only=True)

    class Meta:
        model = Execucao
        fields = ('subfuncao_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')
        next_level = 'programas'
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'subfuncao'

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        execs = self.instance
        return execs.filter(subfuncao_id=obj.subfuncao_id)


class ProgramaSerializer(BaseExecucaoSerializer):

    nome = serializers.CharField(source='programa.desc', read_only=True)

    class Meta:
        model = Execucao
        fields = ('programa_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')
        next_level = 'projetos'
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'programa'

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        execs = self.instance
        return execs.filter(
            subfuncao_id=obj.subfuncao_id,
            programa_id=obj.programa_id)


class ProjetoAtividadeSerializer(BaseExecucaoSerializer):

    nome = serializers.CharField(source='projeto.desc', read_only=True)

    class Meta:
        model = Execucao
        fields = ('projeto_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado')
        list_serializer_class = ExecucaoListSerializer
        distinct_field = 'projeto'

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        execs = self.instance
        return execs.filter(
            subfuncao_id=obj.subfuncao_id,
            programa_id=obj.programa_id,
            projeto_id=obj.projeto_id)


class FonteDeRecursoSerializer(serializers.ModelSerializer):
    selecionado = serializers.SerializerMethodField()

    class Meta:
        model = FonteDeRecurso
        fields = ('id', 'desc', 'selecionado')

    def get_selecionado(self, obj):
        request = self.context['request']
        param = request.query_params.get('fonte', False)
        return param and obj.id == int(param)
