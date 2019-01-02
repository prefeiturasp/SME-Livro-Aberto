import pytest

from datetime import date
from decimal import Decimal
from itertools import cycle

from model_mommy import mommy

from django.test import RequestFactory
from django.urls import reverse

from budget_execution.models import Execucao
from from_to_handler.models import Deflator
from mosaico.serializers import (
    BaseExecucaoSerializer,
    GrupoSerializer,
    SubgrupoSerializer,
    ElementoSerializer,
    SubelementoSerializer,
    SubfuncaoSerializer,
    ProgramaSerializer,
    ProjetoAtividadeSerializer,

    TimeseriesSerializer,
)


@pytest.mark.django_db
class TestTimeseriesSerializer:

    @pytest.fixture(autouse=True)
    def initial(self):
        mommy.make(
            Execucao,
            orcado_atualizado=cycle([50, 100, 150]),
            empenhado_liquido=cycle([5, 10, 15]),
            year=date(2017, 1, 1),
            _quantity=3)

        mommy.make(
            Execucao,
            orcado_atualizado=cycle([10, 20, 30]),
            empenhado_liquido=cycle([1, 2, 3]),
            year=date(2018, 1, 1),
            _quantity=3)

        mommy.make(
            Deflator,
            year=date(2017, 1, 1),
            index_number=Decimal(0.2))

        mommy.make(
            Deflator,
            year=date(2018, 1, 1),
            index_number=Decimal(0.5))

    def test_serializes_data_correctly(self):
        execucoes = Execucao.objects.all()

        expected = {
            '2017': {
                "orcado": 300,
                "empenhado": 30,
            },
            '2018': {
                "orcado": 60,
                "empenhado": 6,
            },
        }

        serializer = TimeseriesSerializer(execucoes)

        assert expected == serializer.data

    def test_serializes_deflated_data(self):
        execucoes = Execucao.objects.all()

        expected = {
            '2017': {
                "orcado": 300 / 0.2,
                "empenhado": 30 / 0.2,
            },
            '2018': {
                "orcado": 60 / 0.5,
                "empenhado": 6 / 0.5,
            },
        }

        serializer = TimeseriesSerializer(execucoes, deflate=True)

        assert expected == serializer.data

    def test_serializes_normal_data_when_deflator_doesnt_exist(self):
        mommy.make(
            Execucao,
            orcado_atualizado=cycle([10, 20, 30]),
            empenhado_liquido=cycle([1, 2, 3]),
            year=date(2016, 1, 1),
            _quantity=3)

        execucoes = Execucao.objects.all()

        expected = {
            '2016': {
                "orcado": 60,
                "empenhado": 6,
            },
            '2017': {
                "orcado": 300 / 0.2,
                "empenhado": 30 / 0.2,
            },
            '2018': {
                "orcado": 60 / 0.5,
                "empenhado": 6 / 0.5,
            },
        }

        serializer = TimeseriesSerializer(execucoes, deflate=True)

        assert expected == serializer.data


@pytest.mark.django_db
class TestBaseExecucaoSerializer:

    @pytest.fixture
    def execucoes(self):
        execucoes = mommy.make(
            Execucao,
            subgrupo__grupo__id=1,
            orcado_atualizado=cycle([50, 100, 150]),
            empenhado_liquido=cycle([5, 10, 15]),
            year=date(2018, 1, 1),
            _quantity=3)
        return execucoes

    @pytest.fixture
    def serializer(self):
        factory = RequestFactory()
        request = factory.get(reverse('mosaico:grupos'))

        qs = Execucao.objects.all()
        return GrupoSerializer(qs, many=True,
                               context={'request': request})

    def test_get_orcado_total(self, execucoes, serializer):
        data = serializer.data
        expected = sum(execucao.orcado_atualizado for execucao in execucoes)
        assert expected == data[0]['orcado_total']

    def test_get_empenhado_total(self, execucoes, serializer):
        data = serializer.data
        expected = sum(execucao.empenhado_liquido for execucao in execucoes)
        assert expected == data[0]['empenhado_total']

    def test_get_percentual_empenhado(self, execucoes, serializer):
        data = serializer.data
        orcado = sum(execucao.orcado_atualizado for execucao in execucoes)
        empenhado = sum(execucao.empenhado_liquido for execucao in execucoes)
        expected = empenhado / orcado
        assert str(expected) == str(data[0]['percentual_empenhado'])

    def test_get_percentual_with_empenhado_null(self):
        mommy.make(
            Execucao,
            subgrupo__grupo__id=1,
            empenhado_liquido=None,
            year=date(2019, 1, 1),
            _quantity=3)

        data = self.serializer().data
        assert str(0) == str(data[0]['percentual_empenhado'])

    def test_serializers_are_subclasses(self):
        assert issubclass(GrupoSerializer, BaseExecucaoSerializer)
        assert issubclass(SubgrupoSerializer, BaseExecucaoSerializer)
        assert issubclass(ElementoSerializer, BaseExecucaoSerializer)
        assert issubclass(SubelementoSerializer, BaseExecucaoSerializer)
        assert issubclass(SubfuncaoSerializer, BaseExecucaoSerializer)
        assert issubclass(ProgramaSerializer, BaseExecucaoSerializer)
        assert issubclass(ProjetoAtividadeSerializer, BaseExecucaoSerializer)
