import pytest

from datetime import date
from itertools import cycle
from unittest import TestCase

from model_mommy import mommy

from contratos.models import CategoriaContrato, ExecucaoContrato
from contratos.services import application as services


@pytest.mark.django_db
class TestApplicationServices(TestCase):

    def test_serialize_big_number_data(self):
        mommy.make(
            ExecucaoContrato, year=date(2019, 1, 1),
            valor_empenhado=cycle([200, 400]),
            valor_liquidado=cycle([120, 180]),
            _quantity=2)

        queryset = ExecucaoContrato.objects.all()

        expected = {
            "year": 2019,
            "empenhado": 600,
            "liquidado": 300,
            "percent_liquidado": 50,
        }

        ret = services.serialize_big_number_data(queryset)

        assert expected == ret

    def test_serialize_destinations(self):
        category1 = mommy.make(CategoriaContrato, name='cat1', desc='desc 1')
        category2 = mommy.make(CategoriaContrato, name='cat2', desc='desc 1')

        mommy.make(
            ExecucaoContrato, year=date(2019, 1, 1),
            valor_empenhado=cycle([200, 400]),
            valor_liquidado=cycle([120, 180]),
            categoria=cycle([category1, category2]), _quantity=2)

        queryset = ExecucaoContrato.objects.all()

        expected = [
            {
                'year': 2019,
                'categoria_name': 'cat1',
                'categoria_desc': 'desc 1',
                'empenhado': 200.0,
                'liquidado': 120.0,
                'percent_liquidado': 60.0,
            },
            {
                'year': 2019,
                'categoria_name': 'cat2',
                'categoria_desc': 'desc 1',
                'empenhado': 400.0,
                'liquidado': 180.0,
                'percent_liquidado': 45.0,
            },
        ]

        ret = services.serialize_destinations(queryset)

        assert expected == ret
