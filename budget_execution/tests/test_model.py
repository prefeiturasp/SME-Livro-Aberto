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
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=10,
            subelemento__id=99)

        # not expected
        mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=10,
            subelemento__id=88)

        execucao = Execucao.objects.get_by_indexer(
            '2018.16.1011.3.3.09.10.10.99')

        assert expected == execucao

    def test_filter_by_indexer(self):
        expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=10,
            _quantity=2)

        # not expected
        mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=20)

        # using indexer without subelemento_id
        ret = Execucao.objects.filter_by_indexer(
            '2018.16.1011.3.3.09.10.10')

        assert 2 == len(ret)
        for e in expected:
            assert e in ret

    def test_filter_by_subelemento_fromto_code(self):
        expected = mommy.make(
            Execucao,
            categoria__id=1,
            gnd__id=1,
            modalidade__id=10,
            elemento__id=10,
            subelemento__id=1,
            _quantity=2)

        # not expected
        mommy.make(
            Execucao,
            categoria__id=1,
            gnd__id=1,
            modalidade__id=10,
            elemento__id=10,
            subelemento__id=55)

        # using indexer without subelemento_id
        ret = Execucao.objects.filter_by_subelemento_fromto_code(
            '1.1.10.10.01')

        assert 2 == len(ret)
        for e in expected:
            assert e in ret


@pytest.mark.django_db
class TestSubgrupoQueryset:

    def test_get_by_code(self):
        grupo = mommy.make(Grupo, id=10)
        expected = mommy.make(Subgrupo, code=5, grupo=grupo)
        # not expected
        mommy.make(Subgrupo, code=4, grupo=grupo)

        assert expected == Subgrupo.objects.get_by_code('10.5')


@pytest.mark.django_db
class TestSubgrupoModel:

    def test_full_code_property(self):
        grupo = mommy.make(Grupo, id=10)
        subgrupo = mommy.make(Subgrupo, code=5, grupo=grupo)

        assert '10.5' == subgrupo.full_code
