import pytest

from datetime import date
from decimal import Decimal
from itertools import cycle
from unittest.mock import patch

from django.db.models import Sum
from freezegun import freeze_time
from model_mommy import mommy

from budget_execution import constants
from budget_execution import exceptions
from budget_execution import services
from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import (
    Execucao,
    ExecucaoTemp,
    Orcamento,
    OrcamentoRaw,
    Empenho,
    EmpenhoRaw,
    MinimoLegal,
)


@pytest.mark.django_db
class TestLoad2003_2017ExecucoesFromJson:

    def test_load_2017_test_data(self):
        path = "budget_execution/tests/data/2017_test_data_everything.json"
        services.load_2003_2017_execucoes_from_json(path)
        assert 2 == Execucao.objects.count()


@pytest.mark.django_db
class TestLoadOrcamentoFromRawTable:

    def test_load_from_orcamento_raw_loads_only_current_year(self):
        orcamento_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2019, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        # shouldn't be loaded
        mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        assert 0 == Orcamento.objects.count()

        with freeze_time('2019-1-1'):
            services.load_data_from_orcamento_raw()

        assert 1 == Orcamento.objects.count()

        orcamento = Orcamento.objects.first()
        assert orcamento.cd_ano_execucao == orcamento_raw.cd_ano_execucao

    def test_load_everything_from_orcamento_raw_loads_after_2017(self):
        orcamento_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)
        orcamento_raw2 = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2019, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        # shouldn't be loaded
        mommy.make(
            OrcamentoRaw, cd_ano_execucao=cycle([2010, 2016, 2017]),
            cd_orgao=SME_ORGAO_ID, _fill_optional=True, _quantity=3)

        assert 0 == Orcamento.objects.count()

        services.load_data_from_orcamento_raw(load_everything=True)

        orcamentos = Orcamento.objects.all().order_by('cd_ano_execucao')
        assert 2 == len(orcamentos)
        assert orcamentos[0].cd_ano_execucao == orcamento_raw.cd_ano_execucao
        assert orcamentos[1].cd_ano_execucao == orcamento_raw2.cd_ano_execucao


@pytest.mark.django_db
class TestLoadEmpenhoFromRawTable:

    def test_load_from_empenho_raw_load_only_current_year(self):
        empenho_raw = mommy.make(
            EmpenhoRaw, an_empenho=2019, cd_orgao=SME_ORGAO_ID,
            cd_elemento='1',            # needed because this is a these are
            cd_fonte_de_recurso='5',    # text fields. this modeling came from
            cd_projeto_atividade='5',   # SME
            cd_subfuncao='5',
            cd_unidade='5',
            _fill_optional=True)

        # shouldn't be loaded
        mommy.make(
            EmpenhoRaw, an_empenho=2018, cd_orgao=SME_ORGAO_ID,
            cd_elemento='2',
            cd_fonte_de_recurso='5',
            cd_projeto_atividade='5',
            cd_subfuncao='5',
            cd_unidade='5',
            _fill_optional=True)

        assert 0 == Empenho.objects.count()

        with freeze_time('2019-1-1'):
            services.load_data_from_empenhos_raw()

        assert 1 == Empenho.objects.count()

        empenho = Empenho.objects.first()
        assert empenho.an_empenho == empenho_raw.an_empenho

    def test_load_everything_from_empenhos_raw_loads_after_2017(self):
        empenho_raw = mommy.make(
            EmpenhoRaw, an_empenho=2018, cd_orgao=SME_ORGAO_ID,
            cd_elemento='1',            # needed because this is a these are
            cd_fonte_de_recurso='5',    # text fields. this modeling came from
            cd_projeto_atividade='5',   # SME
            cd_subfuncao='5',
            cd_unidade='5',
            _fill_optional=True)
        empenho_raw2 = mommy.make(
            EmpenhoRaw, an_empenho=2019, cd_orgao=SME_ORGAO_ID,
            cd_elemento='2',
            cd_fonte_de_recurso='5',
            cd_projeto_atividade='5',
            cd_subfuncao='5',
            cd_unidade='5',
            _fill_optional=True)

        # shouldn't be loaded
        mommy.make(
            EmpenhoRaw, an_empenho=cycle([2010, 2016, 2017]),
            cd_orgao=SME_ORGAO_ID, _quantity=3)

        assert 0 == Empenho.objects.count()

        services.load_data_from_empenhos_raw(load_everything=True)

        empenhos = Empenho.objects.all().order_by('an_empenho')
        assert 2 == Empenho.objects.count()
        assert empenhos[0].an_empenho == empenho_raw.an_empenho
        assert empenhos[1].an_empenho == empenho_raw2.an_empenho


@pytest.mark.django_db
class TestImportOrcamento:

    def test_import_one_orcamento(self):
        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2019, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        with freeze_time('2019-1-1'):
            services.import_orcamentos()

        execucoes = ExecucaoTemp.objects.all()
        assert 1 == len(execucoes)
        execucao = execucoes[0]

        assert 0 == Execucao.objects.count()

        orcamento.refresh_from_db()
        assert orcamento.execucao_temp == execucao
        assert orcamento.execucao is None

    def test_load_everything_import_only_orcamentos_from_orgao_sme(self):
        # not expected. should consider only after 2017
        mommy.make(
            Orcamento, cd_ano_execucao=2017, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        orcamento1 = mommy.make(
            Orcamento, cd_ano_execucao=2018, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        orcamento2 = mommy.make(
            Orcamento, cd_ano_execucao=2019, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        # not expected
        mommy.make(
            Orcamento, cd_ano_execucao=2018, execucao=None, execucao_temp=None,
            cd_orgao=66, _fill_optional=True)

        services.import_orcamentos(load_everything=True)

        execucoes = ExecucaoTemp.objects.all().order_by('year')
        assert 2 == len(execucoes)

        assert 0 == Execucao.objects.count()

        orcamento1.refresh_from_db()
        assert orcamento1.execucao_temp == execucoes[0]
        orcamento2.refresh_from_db()
        assert orcamento2.execucao_temp == execucoes[1]

    def test_load_everything_ignores_orcamento_already_with_execucao_fk(self):
        # not expected. should consider only after 2017
        mommy.make(
            Orcamento, cd_ano_execucao=2017, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        # not expected
        mommy.make(
            Orcamento, cd_ano_execucao=2018, execucao=None, execucao_temp__id=1,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)

        services.import_orcamentos(load_everything=True)

        execucoes = ExecucaoTemp.objects.all().order_by('year')
        assert 2 == len(execucoes)
        execucao = execucoes[0]

        assert 0 == Execucao.objects.count()

        orcamento.refresh_from_db()
        assert orcamento.execucao_temp == execucao

    def test_import_only_current_year_orcamentos(self):
        # not expected. should consider only current year
        mommy.make(
            Orcamento, cd_ano_execucao=2017, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        mommy.make(
            Orcamento, cd_ano_execucao=2018, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)
        orcamento1 = mommy.make(
            Orcamento, cd_ano_execucao=2019, execucao=None, execucao_temp=None,
            cd_orgao=SME_ORGAO_ID, _fill_optional=True)

        with freeze_time('2019-1-1'):
            services.import_orcamentos()

        execucoes = ExecucaoTemp.objects.all().order_by('year')
        assert 1 == len(execucoes)

        assert 0 == Execucao.objects.count()

        orcamento1.refresh_from_db()
        assert orcamento1.execucao_temp == execucoes[0]


@pytest.mark.django_db
class TestImportEmpenho:

    @patch.object(ExecucaoTemp.objects, 'update_by_empenho')
    def test_load_everything_import_only_empenhos_from_orgao_sme(
            self, mock_update):
        mock_execucao = mommy.make(ExecucaoTemp)
        mock_update.return_value = mock_execucao

        # not expected. should consider only after 2017
        mommy.make(
            Empenho, execucao=None, execucao_temp=None, _fill_optional=True,
            an_empenho=2017, cd_orgao=SME_ORGAO_ID)

        empenhos = mommy.make(
            Empenho, execucao=None, execucao_temp=None, _fill_optional=True,
            cd_orgao=SME_ORGAO_ID, an_empenho=cycle([2018, 2019]), _quantity=3)

        not_expected = mommy.make(
            Empenho, execucao=None, execucao_temp=None, _fill_optional=True,
            cd_orgao=55)

        services.import_empenhos(load_everything=True)

        for empenho in empenhos:
            empenho.refresh_from_db()
            assert empenho.execucao_temp == mock_execucao
            assert empenho.execucao is None

        assert not_expected.execucao_temp is None
        assert not_expected.execucao is None

    @patch.object(ExecucaoTemp.objects, 'update_by_empenho')
    def test_load_only_current_year_empenhos(self, mock_update):
        mock_execucao = mommy.make(ExecucaoTemp)
        mock_update.return_value = mock_execucao

        # not expected. should consider only current year
        not_expected = mommy.make(
            Empenho, execucao=None, execucao_temp=None, _fill_optional=True,
            an_empenho=2018, cd_orgao=SME_ORGAO_ID)

        empenho = mommy.make(
            Empenho, execucao=None, execucao_temp=None, _fill_optional=True,
            cd_orgao=SME_ORGAO_ID, an_empenho=2019)

        with freeze_time('2019-1-1'):
            services.import_empenhos()

        empenho.refresh_from_db()
        assert empenho.execucao_temp == mock_execucao

        assert not_expected.execucao_temp is None

    @patch.object(ExecucaoTemp.objects, 'update_by_empenho')
    def test_ignores_when_update_by_empenho_returns_none(self, mock_update):
        mock_update.return_value = None

        empenho = mommy.make(Empenho, execucao=None, _fill_optional=True)

        services.import_empenhos()

        empenho.refresh_from_db()
        assert empenho.execucao is None


@pytest.mark.django_db
class TestUpdateExecucaoTableFromExecucaoTemp:

    def test_copies_data_from_execucao_temp_to_execucao(self):
        mommy.make(ExecucaoTemp, orgao__id=SME_ORGAO_ID, _quantity=2)
        expected_orcado_total = ExecucaoTemp.objects.all().aggregate(
            total=Sum('orcado_atualizado'))['total']

        assert 2 == ExecucaoTemp.objects.count()
        assert 0 == Execucao.objects.count()

        services.update_execucao_table_from_execucao_temp()

        assert 0 == ExecucaoTemp.objects.count()
        assert 2 == Execucao.objects.count()
        assert expected_orcado_total == Execucao.objects.all().aggregate(
            total=Sum('orcado_atualizado'))['total']

    def test_ignores_non_sme_execucoes(self):
        mommy.make(Execucao, orgao__id=1, orcado_atualizado=1)

        mommy.make(ExecucaoTemp, orgao__id=SME_ORGAO_ID, _quantity=2)
        expected_orcado_total = ExecucaoTemp.objects.all().aggregate(
            total=Sum('orcado_atualizado'))['total']

        assert 2 == ExecucaoTemp.objects.count()
        assert 1 == Execucao.objects.count()

        services.update_execucao_table_from_execucao_temp()

        assert 0 == ExecucaoTemp.objects.count()
        assert 3 == Execucao.objects.count()
        assert expected_orcado_total == Execucao.objects \
            .filter(orgao_id=SME_ORGAO_ID) \
            .aggregate(total=Sum('orcado_atualizado'))['total']


@pytest.mark.django_db
class TestVerifyTotalSum:

    def test_passes_when_orcado_limit_is_not_exceeded(self):
        percent_limit = Decimal(constants.ORCADO_DIFFERENCE_PERCENT_LIMIT)

        orcado_sum = Decimal(100)
        mommy.make(
            Execucao, orgao__id=SME_ORGAO_ID, orcado_atualizado=orcado_sum / 2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        orcado_limit = (orcado_sum * percent_limit) - 1
        mommy.make(
            ExecucaoTemp, orgao_id=SME_ORGAO_ID,
            orcado_atualizado=orcado_limit / 2,
            _quantity=2)
        execucoes_temp = ExecucaoTemp.objects.all()

        services.verify_total_sum(execucoes, execucoes_temp)

    def test_raise_exception_when_orcado_limit_is_exceeded(self):
        percent_limit = Decimal(constants.ORCADO_DIFFERENCE_PERCENT_LIMIT)

        orcado_sum = Decimal(100)
        mommy.make(
            Execucao, orgao__id=SME_ORGAO_ID, orcado_atualizado=orcado_sum / 2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        orcado_over_limit = (orcado_sum * percent_limit) + 10
        mommy.make(
            ExecucaoTemp, orgao_id=SME_ORGAO_ID,
            orcado_atualizado=orcado_over_limit / 2,
            _quantity=2)
        execucoes_temp = ExecucaoTemp.objects.all()

        with pytest.raises(exceptions.OrcadoDifferenceOverLimitException):
            services.verify_total_sum(execucoes, execucoes_temp)

    def test_passes_when_empenhado_limit_is_not_exceeded(self):
        percent_limit = Decimal(constants.EMPENHADO_DIFFERENCE_PERCENT_LIMIT)

        empenhado_sum = Decimal(100)
        mommy.make(
            Execucao,
            orgao__id=SME_ORGAO_ID,
            orcado_atualizado=10,
            empenhado_liquido=empenhado_sum / 2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        empenhado_limit = (empenhado_sum * percent_limit) - 1
        mommy.make(
            ExecucaoTemp,
            orgao_id=SME_ORGAO_ID,
            orcado_atualizado=10,
            empenhado_liquido=empenhado_limit / 2,
            _quantity=2)
        execucoes_temp = ExecucaoTemp.objects.all()

        services.verify_total_sum(execucoes, execucoes_temp)

    def test_raise_exception_when_empenhado_limit_is_exceeded(self):
        percent_limit = Decimal(constants.EMPENHADO_DIFFERENCE_PERCENT_LIMIT)

        empenhado_sum = Decimal(100)
        mommy.make(
            Execucao,
            orgao__id=SME_ORGAO_ID,
            orcado_atualizado=10,
            empenhado_liquido=empenhado_sum / 2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        empenhado_over_limit = (empenhado_sum * percent_limit) + 10
        mommy.make(
            ExecucaoTemp,
            orgao_id=SME_ORGAO_ID,
            orcado_atualizado=10,
            empenhado_liquido=empenhado_over_limit / 2,
            _quantity=2)
        execucoes_temp = ExecucaoTemp.objects.all()

        with pytest.raises(exceptions.EmpenhadoDifferenceOverLimitException):
            services.verify_total_sum(execucoes, execucoes_temp)


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
