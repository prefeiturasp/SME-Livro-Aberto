from functools import lru_cache

from django.db.models import Sum
from rest_framework import serializers

from budget_execution.models import Execucao


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


# `Simples` visualization serializers

class GrupoSerializer(BaseSerializer):

    grupo_id = serializers.SerializerMethodField()
    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'grupo_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_grupo_id(self, obj):
        return obj.subgrupo.grupo_id

    def get_nome(self, obj):
        return obj.subgrupo.grupo.desc

    def get_url(self, obj):
        return obj.get_url('grupo')

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo__grupo_id=obj.subgrupo.grupo_id)


class SubgrupoSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'subgrupo_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_nome(self, obj):
        return obj.subgrupo.desc

    def get_url(self, obj):
        return obj.get_url("subgrupo")

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo_id=obj.subgrupo_id)


class ElementoSerializer(BaseSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'elemento_id', 'nome', 'orcado_total',
                  'empenhado_total', 'percentual_empenhado', 'url')

    def get_nome(self, obj):
        return obj.elemento.desc

    def get_url(self, obj):
        return obj.get_url('elemento')

    @lru_cache(maxsize=10)
    def _execucoes(self, obj):
        return Execucao.objects.filter(
            year=obj.year, subgrupo_id=obj.subgrupo_id,
            elemento_id=obj.elemento_id)


class SubelementoSerializer(ElementoSerializer):

    nome = serializers.SerializerMethodField()

    class Meta:
        model = Execucao
        fields = ('id', 'subelemento_id', 'nome', 'orcado_total',
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
        return obj.get_url('subfuncao')

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
        return obj.get_url('programa')

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
