import os

import pytest

from unittest import TestCase
from unittest.mock import patch

from django.conf import settings
from django.core.files import File

from freezegun import freeze_time
from model_mommy import mommy

from contratos.dao import sof_api as sof_api_dao
from contratos.dao.dao import EmpenhosFailedRequestsDao
from contratos.models import (
    CategoriaContratoFromTo, CategoriaContratoFromToSpreadsheet,
)
from contratos.tests.fixtures import (
    EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA,
    SOF_API_REQUEST_RETURN_DICT)


class EmpenhoDAOTestCase(TestCase):

    @patch('contratos.dao.sof_api.get_by_ano_empenho')
    def test_get_by_codcontrato_and_anoexercicio(self, mock_get_by_ano):
        empenhos_2018 = EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA[2018]
        empenhos_2019 = EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA[2019]

        cod_contrato = 555
        ano_exercicio = 2018
        mock_get_by_ano.side_effect = [empenhos_2018, empenhos_2019]

        with freeze_time('2019-1-1'):
            ret = sof_api_dao.get_by_codcontrato_and_anoexercicio(
                cod_contrato=cod_contrato, ano_exercicio=ano_exercicio)

        assert ret == empenhos_2018 + empenhos_2019
        assert 2 == mock_get_by_ano.call_count
        mock_get_by_ano.assert_any_call(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=2018)
        mock_get_by_ano.assert_any_call(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=2019)

    @patch('contratos.dao.sof_api.requests.get')
    def test_get_by_ano_empenho(self, mock_get):
        cod_contrato = 5555
        ano_exercicio = 2019
        ano_empenho = 2019

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = SOF_API_REQUEST_RETURN_DICT
        url = (
            'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
            f'v2.1.0/consultaEmpenhos?anoEmpenho={ano_empenho}&mesEmpenho=12'
            f'&anoExercicio={ano_exercicio}'
            f'&codContrato={cod_contrato}&codOrgao=16'
        )
        headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}

        ret = sof_api_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert SOF_API_REQUEST_RETURN_DICT["lstEmpenhos"] == ret
        mock_get.assert_called_once_with(url, headers=headers)

    @patch.object(EmpenhosFailedRequestsDao, 'create')
    @patch('contratos.dao.sof_api.requests.get')
    def test_get_by_ano_empenho_saves_failed_request(
            self, mock_get, mock_save_failed):
        cod_contrato = 5555
        ano_exercicio = 2019
        ano_empenho = 2019

        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = SOF_API_REQUEST_RETURN_DICT

        ret = sof_api_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert ret is None
        mock_save_failed.assert_called_once_with(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho, error_code=500)

    @patch.object(EmpenhosFailedRequestsDao, 'create')
    @patch('contratos.dao.sof_api.requests.get')
    def test_get_by_ano_empenho_saves_requests_exception(
            self, mock_get, mock_save_failed):
        cod_contrato = 5555
        ano_exercicio = 2019
        ano_empenho = 2019

        mock_get.side_effect = Exception()

        ret = sof_api_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert ret is None
        mock_save_failed.assert_called_once_with(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho, error_code=-1)


class TestContratosCategoriasFromToDao:

    @pytest.fixture()
    def file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_CategoriaContratoFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in CategoriaContratoFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_extract_data(self, file_fixture):
        ssheet = mommy.make(
            CategoriaContratoFromToSpreadsheet,
            spreadsheet=File(file_fixture))
        # data is extracted on save

        fts = CategoriaContratoFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        indexers = ['2018.16.2100.3.3.90.30.00.1',
                    '2018.16.2100.3.3.90.30.00.14']

        assert fts[0].indexer == indexers[0]
        assert fts[0].categoria_name == 'categoria'
        assert fts[0].categoria_desc == 'categoria desc'

        assert fts[1].indexer == indexers[1]
        assert fts[1].categoria_name == 'outra categoria'
        assert fts[1].categoria_desc == 'outra categoria desc'

        ssheet.refresh_from_db()
        assert ssheet.extracted
        assert indexers == ssheet.added_fromtos
        assert [] == ssheet.not_added_fromtos

    def test_extract_data_when_indexer_already_exists(self, file_fixture):
        mommy.make(
            CategoriaContratoFromTo,
            indexer='2018.16.2100.3.3.90.30.00.1',
            categoria_name='old categoria',
            categoria_desc='old categoria desc')

        ssheet = mommy.make(
            CategoriaContratoFromToSpreadsheet,
            spreadsheet=File(file_fixture))
        # data is extracted on save

        fts = CategoriaContratoFromTo.objects.all()
        assert 2 == len(fts)

        indexers = ['2018.16.2100.3.3.90.30.00.1',
                    '2018.16.2100.3.3.90.30.00.14']

        assert fts[0].indexer == indexers[0]
        assert fts[0].categoria_name == 'old categoria'
        assert fts[0].categoria_desc == 'old categoria desc'

        assert fts[1].indexer == indexers[1]
        assert fts[1].categoria_name == 'outra categoria'
        assert fts[1].categoria_desc == 'outra categoria desc'

        ssheet.refresh_from_db()
        assert ssheet.extracted
        assert [indexers[1]] == ssheet.added_fromtos
        assert [indexers[0]] == ssheet.not_added_fromtos
