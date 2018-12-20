import pytest

from datetime import date
from decimal import Decimal
from itertools import cycle

from model_mommy import mommy

from budget_execution.models import Execucao
from from_to_handler.models import Deflator
from mosaico.serializers import TimeseriesSerializer


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
