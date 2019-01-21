import pytest

from unittest.mock import patch

from model_mommy import mommy

from budget_execution import services
from budget_execution.models import (
    Execucao,
    Orcamento,
    Empenho,
)


@pytest.mark.django_db
class TestImportOrcamento:

    def test_import_one_orcamento(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                               _fill_optional=True)
        services.import_orcamentos()

        execucoes = Execucao.objects.all()
        assert 1 == len(execucoes)
        execucao = execucoes[0]

        orcamento.refresh_from_db()
        assert orcamento.execucao == execucao

    def test_import_all_orcamentos(self):
        orcamento1 = mommy.make(Orcamento, cd_ano_execucao=2017, execucao=None,
                                _fill_optional=True)
        orcamento2 = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                                _fill_optional=True)
        services.import_orcamentos()

        execucoes = Execucao.objects.all().order_by('year')
        assert 2 == len(execucoes)

        orcamento1.refresh_from_db()
        assert orcamento1.execucao == execucoes[0]
        orcamento2.refresh_from_db()
        assert orcamento2.execucao == execucoes[1]

    def test_ignores_orcamento_already_with_execucao_fk(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2017, execucao=None,
                               _fill_optional=True)
        # not expected
        mommy.make(Orcamento, cd_ano_execucao=2018, execucao__id=1,
                   _fill_optional=True)

        services.import_orcamentos()

        execucoes = Execucao.objects.all().order_by('year')
        assert 2 == len(execucoes)
        execucao = execucoes[0]

        orcamento.refresh_from_db()
        assert orcamento.execucao == execucao


@pytest.mark.django_db
class TestImportEmpenho:

    @patch.object(Execucao.objects, 'update_by_empenho')
    def test_import_empenhos(self, mock_update):
        mock_execucao = mommy.make(Execucao)
        mock_update.return_value = mock_execucao

        empenhos = mommy.make(Empenho, execucao=None, _fill_optional=True,
                              _quantity=3)

        services.import_empenhos()

        for empenho in empenhos:
            empenho.refresh_from_db()
            assert empenho.execucao == mock_execucao
