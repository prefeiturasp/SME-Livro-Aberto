import pytest

from datetime import date
from unittest.mock import call, patch

from model_mommy import mommy

from budget_execution.models import Execucao, Grupo, Subgrupo
from from_to_handler import services
from from_to_handler.models import DotacaoFromTo


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

        services.apply_dotacao_fromto(ft)

        assert 1 == Grupo.objects.count()
        assert 1 == Subgrupo.objects.count()

        grupo = Grupo.objects.get(id=ft.grupo_code)
        subgrupo = Subgrupo.objects.get_by_code(
            f'{grupo.id}.{ft.subgrupo_code}')
        assert ft.grupo_desc == grupo.desc
        assert ft.subgrupo_desc == subgrupo.desc

        for ex in expected:
            ex.refresh_from_db()
            assert ft.grupo_code == ex.subgrupo.grupo_id
            assert ft.subgrupo_code == ex.subgrupo.code

        assert not_expected.subgrupo_id is None

    @patch('from_to_handler.services.apply_dotacao_fromto')
    def test_apply_dotacoes_applies_every_dotacao_fromto_existent(
            self, mock_fromto):
        fts = mommy.make(DotacaoFromTo, _quantity=3)

        services.apply_dotacoes_grupo_subgrupo_fromto()

        for ft in fts:
            assert call(ft) in mock_fromto.call_args_list
