import pytest

from datetime import date
from unittest.mock import Mock, patch

from model_mommy import mommy

from budget_execution.models import (
    Execucao, FonteDeRecursoGrupo, GndGealogia, Grupo, Subgrupo)
from from_to_handler.models import (
    DotacaoFromTo, FonteDeRecursoFromTo, FromTo, GNDFromTo)


@pytest.mark.django_db
class TestDotacaoGrupoSubgrupoFromTo:

    def test_apply_dotacao_fromto(self):
        assert 0 == Grupo.objects.count()
        assert 0 == Subgrupo.objects.count()

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
            subgrupo_id=None,
            _quantity=2)

        not_expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao_id=16,
            projeto_id=1011,
            categoria_id=3,
            gnd_id=3,
            modalidade_id=9,
            elemento_id=10,
            fonte_id=33,
            subgrupo_id=None)

        ft = mommy.make(DotacaoFromTo,
                        indexer='2018.16.1011.3.3.9.10.10')

        ft.apply()

        assert 1 == Grupo.objects.count()
        assert 1 == Subgrupo.objects.count()

        grupo = Grupo.objects.get(id=ft.grupo_code)
        subgrupo = Subgrupo.objects.get_by_code(
            f'{grupo.id}.{ft.subgrupo_code}')
        assert ft.grupo_desc == grupo.desc
        assert ft.subgrupo_desc == subgrupo.desc

        for ex in expected:
            ex.refresh_from_db()
            assert subgrupo == ex.subgrupo

        assert not_expected.subgrupo_id is None

    def test_apply_all_dotacoes_grupo_subgrupo_fromto_existent(self):
        fts = mommy.make(DotacaoFromTo, _quantity=3)
        for ft in fts:
            ft.apply = Mock()

        with patch.object(DotacaoFromTo.objects, 'all',
                          return_value=fts):
            DotacaoFromTo.apply_all()

        for ft in fts:
            ft.apply.assert_called_once_with()


@pytest.mark.django_db
class TestFonteDeRecursoFromToApplier:

    def test_apply_fonte_fromto(self):
        assert 0 == FonteDeRecursoGrupo.objects.count()

        expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao_id=16,
            projeto_id=1011,
            categoria_id=3,
            gnd_id=3,
            modalidade_id=9,
            elemento_id=10,
            fonte_id=4,
            fonte_grupo_id=None,
            _quantity=2)

        not_expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao_id=16,
            projeto_id=1011,
            categoria_id=3,
            gnd_id=3,
            modalidade_id=9,
            elemento_id=10,
            fonte_id=33,
            fonte_grupo_id=None)

        ft = mommy.make(
            FonteDeRecursoFromTo, code=4, grupo_code=3)
        ft.apply()

        assert 1 == FonteDeRecursoGrupo.objects.count()

        fonte_grupo = FonteDeRecursoGrupo.objects.get(id=ft.grupo_code)
        assert ft.grupo_name == fonte_grupo.desc

        for ex in expected:
            ex.refresh_from_db()
            assert fonte_grupo == ex.fonte_grupo

        assert not_expected.fonte_grupo is None

    def test_apply_all_fontes_de_recurso_fromto_existent(self):
        fts = mommy.make(FonteDeRecursoFromTo, _quantity=3)
        for ft in fts:
            ft.apply = Mock()

        with patch.object(FonteDeRecursoFromTo.objects, 'all',
                          return_value=fts):
            FonteDeRecursoFromTo.apply_all()

        for ft in fts:
            ft.apply.assert_called_once_with()


@pytest.mark.django_db
class TestGndFromToApplier:

    def test_apply_gnd_fromto(self):
        assert 0 == GndGealogia.objects.count()

        gnd_id = 1
        elemento_id = 11

        expected = mommy.make(
            Execucao,
            gnd_id=gnd_id,
            elemento_id=elemento_id,
            gnd_gealogia_id=None,
            _quantity=2)

        not_expected = mommy.make(
            Execucao,
            gnd_id=5,
            elemento_id=55,
            gnd_gealogia_id=None)

        ft = mommy.make(
            GNDFromTo, gnd_code=gnd_id, elemento_code=elemento_id)
        ft.apply()

        assert 1 == GndGealogia.objects.count()

        gnd_gealogia = GndGealogia.objects.get(id=ft.new_gnd_code)
        assert ft.new_gnd_desc == gnd_gealogia.desc

        for ex in expected:
            ex.refresh_from_db()
            assert gnd_gealogia == ex.gnd_gealogia

        assert not_expected.fonte_grupo is None

    def test_class_is_instance_of_fromto_model(self):
        assert issubclass(GNDFromTo, FromTo)
