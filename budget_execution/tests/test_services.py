import pytest

from datetime import date
from unittest.mock import patch

from model_mommy import mommy

from budget_execution import services
from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import (
    Execucao,
    Orcamento,
    OrcamentoRaw,
    Empenho,
    EmpenhoRaw,
    MinimoLegal,
)


@pytest.mark.django_db
class TestLoadOrcamentoFromRawTable:

    def test_load_from_orcamento_raw(self):
        orcamento_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        assert 0 == Orcamento.objects.count()

        services.load_data_from_orcamento_raw()

        assert 1 == Orcamento.objects.count()

        orcamento = Orcamento.objects.first()
        assert orcamento.cd_ano_execucao == orcamento_raw.cd_ano_execucao


@pytest.mark.django_db
class TestLoadEmpenhoFromRawTable:

    def test_load_from_empenho_raw(self):
        empenho_raw = mommy.make(
            EmpenhoRaw, an_empenho=2018, cd_orgao=SME_ORGAO_ID,
            cd_elemento='1',            # needed because this is a these are
            cd_fonte_de_recurso='5',    # text fields. this modeling came from
            cd_projeto_atividade='5',   # SME
            cd_subfuncao='5',
            cd_unidade='5',
            _fill_optional=True)

        assert 0 == Empenho.objects.count()

        services.load_data_from_empenho_raw()

        assert 1 == Empenho.objects.count()

        empenho = Empenho.objects.first()
        assert empenho.an_empenho == empenho_raw.an_empenho


@pytest.mark.django_db
class TestImportOrcamento:

    def test_import_one_orcamento(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                               cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        services.import_orcamentos()

        execucoes = Execucao.objects.all()
        assert 1 == len(execucoes)
        execucao = execucoes[0]

        orcamento.refresh_from_db()
        assert orcamento.execucao == execucao

    def test_import_only_orcamentos_from_orgao_sme(self):
        orcamento1 = mommy.make(Orcamento, cd_ano_execucao=2017, execucao=None,
                                cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        orcamento2 = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                                cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        # not expected
        mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                   cd_orgao=66, _fill_optional=True)
        services.import_orcamentos()

        execucoes = Execucao.objects.all().order_by('year')
        assert 2 == len(execucoes)

        orcamento1.refresh_from_db()
        assert orcamento1.execucao == execucoes[0]
        orcamento2.refresh_from_db()
        assert orcamento2.execucao == execucoes[1]

    def test_ignores_orcamento_already_with_execucao_fk(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2017, execucao=None,
                               cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        # not expected
        mommy.make(Orcamento, cd_ano_execucao=2018, execucao__id=1,
                   cd_orgao=SME_ORGAO_ID, _fill_optional=True)

        services.import_orcamentos()

        execucoes = Execucao.objects.all().order_by('year')
        assert 2 == len(execucoes)
        execucao = execucoes[0]

        orcamento.refresh_from_db()
        assert orcamento.execucao == execucao


@pytest.mark.django_db
class TestImportEmpenho:

    @patch.object(Execucao.objects, 'update_by_empenho')
    def test_import_only_empenhos_from_orgao_sme(self, mock_update):
        mock_execucao = mommy.make(Execucao)
        mock_update.return_value = mock_execucao

        empenhos = mommy.make(Empenho, execucao=None, _fill_optional=True,
                              cd_orgao=SME_ORGAO_ID, _quantity=3)

        not_expected = mommy.make(Empenho, execucao=None, _fill_optional=True,
                                  cd_orgao=55)

        services.import_empenhos()

        for empenho in empenhos:
            empenho.refresh_from_db()
            assert empenho.execucao == mock_execucao

        assert not_expected.execucao is None

    @patch.object(Execucao.objects, 'update_by_empenho')
    def test_ignores_when_update_by_empenho_returns_none(self, mock_update):
        mock_update.return_value = None

        empenho = mommy.make(Empenho, execucao=None, _fill_optional=True)

        services.import_empenhos()

        empenho.refresh_from_db()
        assert empenho.execucao is None


@pytest.mark.django_db
class TestImportMinimoLegal:

    def test_import_minimo_legal(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2017, execucao=None,
                               _fill_optional=True)
        orcamento2 = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                                _fill_optional=True)

        ml = mommy.make(MinimoLegal, year=date(2017, 1, 1), execucao=None,
                        projeto_id=orcamento.cd_projeto_atividade,
                        _fill_optional=True)
        ml2 = mommy.make(MinimoLegal, year=date(2018, 1, 1), execucao=None,
                         projeto_id=orcamento2.cd_projeto_atividade,
                         _fill_optional=True)

        services.import_minimo_legal()

        execucoes = Execucao.objects.all().order_by('year')
        assert 2 == len(execucoes)

        orcamento.refresh_from_db()
        ml.refresh_from_db()
        assert orcamento.execucao == execucoes[0]
        assert ml.execucao == execucoes[0]

        orcamento2.refresh_from_db()
        ml2.refresh_from_db()
        assert orcamento2.execucao == execucoes[1]
        assert ml2.execucao == execucoes[1]
