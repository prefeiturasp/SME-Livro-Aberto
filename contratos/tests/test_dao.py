from unittest import TestCase
from unittest.mock import Mock, patch

from django.conf import settings
from freezegun import freeze_time
from model_mommy import mommy

from contratos.dao import contratos_raw_dao, empenhos_dao, empenhos_temp_dao, \
    empenhos_failed_requests_dao
from contratos.models import (
    ContratoRaw, EmpenhoSOFCache, EmpenhoSOFCacheTemp,
    EmpenhoSOFFailedAPIRequest)
from contratos.tests.fixtures import (
    EMPENHOS_DAO_CREATE_DATA,
    EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA,
    SOF_API_REQUEST_RETURN_DICT)


class ContratoRawDAOTestCase(TestCase):

    @patch.object(ContratoRaw.objects, 'all')
    def test_get_all(self, mock_all):
        mocked_contratos = [Mock(spec=ContratoRaw),
                            Mock(spec=ContratoRaw)]
        mock_all.return_value = mocked_contratos

        ret = contratos_raw_dao.get_all()
        assert ret == mocked_contratos
        mock_all.assert_called_once_with()


class EmpenhoDAOTestCase(TestCase):

    @patch('contratos.dao.empenhos_dao.get_by_ano_empenho')
    def test_get_by_codcontrato_and_anoexercicio(self, mock_get_by_ano):
        empenhos_2018 = EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA[2018]
        empenhos_2019 = EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA[2019]

        cod_contrato = 555
        ano_exercicio = 2018
        mock_get_by_ano.side_effect = [empenhos_2018, empenhos_2019]

        with freeze_time('2019-1-1'):
            ret = empenhos_dao.get_by_codcontrato_and_anoexercicio(
                cod_contrato=cod_contrato, ano_exercicio=ano_exercicio)

        assert ret == empenhos_2018 + empenhos_2019
        assert 2 == mock_get_by_ano.call_count
        mock_get_by_ano.assert_any_call(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=2018)
        mock_get_by_ano.assert_any_call(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=2019)

    @patch('contratos.dao.empenhos_dao.requests.get')
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

        ret = empenhos_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert SOF_API_REQUEST_RETURN_DICT["lstEmpenhos"] == ret
        mock_get.assert_called_once_with(url, headers=headers)

    @patch('contratos.dao.empenhos_failed_requests_dao.create')
    @patch('contratos.dao.empenhos_dao.requests.get')
    def test_get_by_ano_empenho_saves_failed_request(
            self, mock_get, mock_save_failed):
        cod_contrato = 5555
        ano_exercicio = 2019
        ano_empenho = 2019

        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = SOF_API_REQUEST_RETURN_DICT

        ret = empenhos_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert ret is None
        mock_save_failed.assert_called_once_with(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho, error_code=500)

    @patch('contratos.dao.empenhos_failed_requests_dao.create')
    @patch('contratos.dao.empenhos_dao.requests.get')
    def test_get_by_ano_empenho_saves_requests_exception(
            self, mock_get, mock_save_failed):
        cod_contrato = 5555
        ano_exercicio = 2019
        ano_empenho = 2019

        mock_get.side_effect = Exception()

        ret = empenhos_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

        assert ret is None
        mock_save_failed.assert_called_once_with(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho, error_code=-1)

    @patch('contratos.dao.empenhos_failed_requests_dao'
           '.EmpenhoSOFFailedAPIRequest')
    def test_save_failed_api_request(self, mock_EmpenhoFailed):
        failed_request_data = {
            "cod_contrato": 555,
            "ano_exercicio": 2018,
            "ano_empenho": 2019,
            "error_code": 500,
        }
        mocked_return = Mock(EmpenhoSOFFailedAPIRequest, autospec=True)
        mock_EmpenhoFailed.objects.create.return_value = mocked_return

        ret = empenhos_failed_requests_dao.create(**failed_request_data)
        assert ret == mocked_return
        mock_EmpenhoFailed.objects.create.assert_called_once_with(
            **failed_request_data)

    @patch('contratos.dao.empenhos_dao.EmpenhoSOFCache')
    def test_create(self, mock_Empenho):
        empenho_data = EMPENHOS_DAO_CREATE_DATA
        mocked_return = Mock(EmpenhoSOFCache, autospec=True)
        mock_Empenho.objects.create.return_value = mocked_return

        ret = empenhos_dao.create(data=empenho_data)
        mock_Empenho.objects.create.assert_called_once_with(**empenho_data)
        assert ret == mocked_return

    @patch('contratos.dao.empenhos_dao.EmpenhoSOFCache')
    def test_create_from_temp_table_data(self, mock_EmpenhoSOF):
        mocked_empenho = Mock(spec=EmpenhoSOFCache)
        mock_EmpenhoSOF.return_value = mocked_empenho

        empenho_temp = mommy.prepare(EmpenhoSOFCacheTemp, _fill_optional=True)

        empenho = empenhos_dao.create_from_temp_table_obj(
            empenho_temp=empenho_temp)

        for field in empenho_temp._meta.fields:
            if field.primary_key is True:
                continue
            assert (getattr(empenho, field.name)
                    == getattr(empenho_temp, field.name))
        mocked_empenho.save.assert_called_once_with()


class EmpenhosTempDaoTestCase(TestCase):

    @patch.object(EmpenhoSOFCacheTemp.objects, 'all')
    def test_get_all(self, mock_all):
        mocked_empenhos = [Mock(spec=EmpenhoSOFCacheTemp),
                           Mock(spec=EmpenhoSOFCacheTemp)]
        mock_all.return_value = mocked_empenhos

        ret = empenhos_temp_dao.get_all()
        assert ret == mocked_empenhos
        mock_all.assert_called_once_with()
