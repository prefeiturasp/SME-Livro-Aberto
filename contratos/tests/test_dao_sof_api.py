from unittest import TestCase
from unittest.mock import patch

from django.conf import settings

from freezegun import freeze_time

from contratos.constants import PRODAM_URL
from contratos.dao import sof_api_dao
from contratos.dao.models_dao import EmpenhosFailedRequestsDao
from contratos.tests.fixtures import (
    EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA,
    SOF_API_REQUEST_RETURN_DICT)


class EmpenhoDAOTestCase(TestCase):

    @patch('contratos.dao.sof_api_dao.get_by_ano_empenho')
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

    @patch('contratos.dao.sof_api_dao.requests.get')
    def test_get_by_ano_empenho(self, mock_get):
        cod_contrato = 5555
        ano_exercicio = 2019
        ano_empenho = 2019

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = SOF_API_REQUEST_RETURN_DICT
        url = (
            f'{PRODAM_URL}?anoEmpenho={ano_empenho}&mesEmpenho=12'
            f'&anoExercicio={ano_exercicio}'
            f'&codContrato={cod_contrato}&codOrgao=16'
        )
        headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}

        ret = sof_api_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert SOF_API_REQUEST_RETURN_DICT["lstEmpenhos"] == ret
        mock_get.assert_called_once_with(url, headers=headers, timeout=20)

    @patch.object(EmpenhosFailedRequestsDao, 'create')
    @patch('contratos.dao.sof_api_dao.requests.get')
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
    @patch('contratos.dao.sof_api_dao.requests.get')
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
