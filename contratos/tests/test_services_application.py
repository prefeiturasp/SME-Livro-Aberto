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
        execucoes2018 = mommy.make(
            ExecucaoContrato, year=date(2018, 1, 1),
            valor_empenhado=cycle([111, 222]), valor_liquidado=cycle([10, 20]),
            _quantity=2)
        execucoes2019 = mommy.make(
            ExecucaoContrato, year=date(2019, 1, 1),
            valor_empenhado=cycle([100, 200]), valor_liquidado=cycle([1, 2]),
            _quantity=2)

        queryset = ExecucaoContrato.objects.all()

        ret = services.serialize_big_number_data(queryset)
