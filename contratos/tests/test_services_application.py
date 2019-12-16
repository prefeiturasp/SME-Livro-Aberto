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
            "percent_liquidado": .5,
        }

        ret = services.serialize_big_number_data(queryset)

        assert expected == ret

    def test_serialize_destinations(self):
        category1 = mommy.make(CategoriaContrato, id=3, name='cat1',
                desc='desc 1', slug='slug_1')
        category2 = mommy.make(CategoriaContrato, id=4, name='cat2',
                desc='desc 1', slug='slug_2')

        empenhado1 = 200
        empenhado2 = 400
        empenhado_total = empenhado1 + empenhado2
        mommy.make(
            ExecucaoContrato, year=date(2019, 1, 1),
            valor_empenhado=cycle([empenhado1, empenhado2]),
            valor_liquidado=cycle([120, 180]),
            categoria=cycle([category1, category2]), _quantity=2)

        queryset = ExecucaoContrato.objects.all()

        expected = [
            {
                'year': 2019,
                'categoria_id': '3',
                'categoria_name': 'cat1',
                'categoria_desc': 'desc 1',
                'categoria_slug': 'slug_1',
                'empenhado': 200.0,
                'liquidado': 120.0,
                'percent_liquidado': .6,
                'percent_empenhado': empenhado1 / empenhado_total,
            },
            {
                'year': 2019,
                'categoria_id': '4',
                'categoria_name': 'cat2',
                'categoria_desc': 'desc 1',
                'categoria_slug': 'slug_2',
                'empenhado': 400.0,
                'liquidado': 180.0,
                'percent_liquidado': 0.45,
                'percent_empenhado': empenhado2 / empenhado_total,
            },
        ]

        ret = services.serialize_destinations(queryset)

        assert expected == ret

    def test_serialize_top5(self):
        exec_pos3 = mommy.make(ExecucaoContrato, valor_empenhado=300.0,
                               _fill_optional=True)
        exec_pos1 = mommy.make(ExecucaoContrato, valor_empenhado=500.0,
                               _fill_optional=True)
        exec_pos2 = mommy.make(ExecucaoContrato, valor_empenhado=400.0,
                               _fill_optional=True)
        exec_pos5 = mommy.make(ExecucaoContrato, valor_empenhado=100.0,
                               _fill_optional=True)
        exec_pos4 = mommy.make(ExecucaoContrato, valor_empenhado=200.0,
                               _fill_optional=True)
        execucoes_top5 = [exec_pos1, exec_pos2, exec_pos3, exec_pos4, exec_pos5]
        # not expected
        mommy.make(ExecucaoContrato, valor_empenhado=50, _fill_optional=True)

        expected = []
        for execucao in execucoes_top5:
            expected.append(
                {
                    'year': execucao.year.year,
                    'cod_contrato': execucao.cod_contrato,
                    'categoria_name': execucao.categoria.name,
                    'categoria_desc': execucao.categoria.desc,
                    'fornecedor': execucao.fornecedor.razao_social,
                    'objeto_contrato': execucao.objeto_contrato.desc,
                    'modalidade': execucao.modalidade.desc,
                    'empenhado': execucao.valor_empenhado,
                }
            )

        queryset = ExecucaoContrato.objects.all()
        ret = services.serialize_top5(queryset)

        assert expected == ret
