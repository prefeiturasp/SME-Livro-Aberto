from datetime import date

import pytest

from model_mommy import mommy

from budget_execution.models import Execucao, Grupo, Subgrupo


@pytest.mark.django_db
class TestExecucaoQuerySet:

    def test_get_by_indexer(self):
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

        # not expected
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

    def test_filter_by_indexer(self):
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
            _quantity=2)

        # not expected
        mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao_id=16,
            projeto_id=1011,
            categoria_id=3,
            gnd_id=3,
            modalidade_id=9,
            elemento_id=10,
            fonte_id=20)

        # using indexer without subelemento_id
        ret = Execucao.objects.filter_by_indexer(
            '2018.16.1011.3.3.09.10.10')

        assert 2 == len(ret)
        for e in expected:
            assert e in ret


@pytest.mark.django_db
class TestSubgrupoModel:

    def test_code_property(self):
        grupo = mommy.make(Grupo, id=10)
        subgrupo = mommy.make(Subgrupo, _code=5, grupo=grupo)

        assert '10.5' == subgrupo.code
