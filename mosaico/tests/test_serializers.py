import pytest

from datetime import date
from itertools import cycle

from model_mommy import mommy

from budget_execution.models import Execucao
from mosaico.serializers import TimeseriesSerializer


@pytest.mark.django_db
class TestTimeseriesSerializer:

    def test_serializes_data_correctly(self):
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

        execucoes = Execucao.objects.all()

        expected = {
            '2017': {
                "orcado": 300,
                "empenhado": 30.00,
            },
            '2018': {
                "orcado": 60.00,
                "empenhado": 6.00,
            },
        }

        serializer = TimeseriesSerializer(execucoes)

        assert expected == serializer.data
