from datetime import date

import pytest

from model_mommy import mommy

from budget_execution.models import Execucao


@pytest.mark.django_db
class TestExecucaoModel:

    def test_indexer_returns_execucao(self):
        expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao_id=16,
            projeto_id=1011,
            categoria_id=3,
            gnd_id=3,
            modalidade_id=9,
            elemento_id=10,
            fonte_id=10,
            subelemento_id=99)

        mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao_id=16,
            projeto_id=1011,
            categoria_id=3,
            gnd_id=3,
            modalidade_id=9,
            elemento_id=10,
            fonte_id=10,
            subelemento_id=88)

        execucao = Execucao.objects.get_by_indexer(
            '2018.16.1011.3.3.09.10.10.99')

        assert expected == execucao
