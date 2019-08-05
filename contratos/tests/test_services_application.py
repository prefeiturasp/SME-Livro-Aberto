import pytest

from datetime import date
from itertools import cycle
from unittest import TestCase

from model_mommy import mommy

from contratos.models import ExecucaoContrato
from contratos.services import application as services


@pytest.mark.django_db
class TestApplicationServices(TestCase):

    def test_serialize_big_number_data(self):
        mommy.make(
            ExecucaoContrato, year=date(2018, 1, 1),
            valor_empenhado=cycle([100, 200]), valor_liquidado=cycle([10, 20]),
            _quantity=2)
        mommy.make(
            ExecucaoContrato, year=date(2019, 1, 1),
            valor_empenhado=cycle([200, 400]),
            valor_liquidado=cycle([120, 180]),
            _quantity=2)

        queryset = ExecucaoContrato.objects.all()

        expected = [
            {
                "year": 2018,
                "empenhado": 300,
                "liquidado": 30,
                "percent_liquidado": 10,
            },
            {
                "year": 2019,
                "empenhado": 600,
                "liquidado": 300,
                "percent_liquidado": 50,
            },
        ]

        ret = services.serialize_big_number_data(queryset)

        assert expected == ret
