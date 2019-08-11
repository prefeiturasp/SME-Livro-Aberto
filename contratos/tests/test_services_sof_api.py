import pytest

from collections import namedtuple
from copy import deepcopy
from itertools import cycle
from unittest import TestCase
from unittest.mock import call, patch, Mock

from model_mommy import mommy

from contratos.services import sof_api as services
from contratos.constants import CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT
from contratos.dao import empenhos_dao, empenhos_temp_dao
from contratos.dao.dao import ContratosRawDao
from contratos.exceptions import ContratosEmpenhosDifferenceOverLimit
from contratos.models import ContratoRaw, EmpenhoSOFCacheTemp
from contratos.tests.fixtures import (
    CONTRATO_RAW_DATA, SOF_API_REQUEST_RETURN_DICT)


MockedContratoRaw = namedtuple('MockedContratoRaw',
                               ['codcontrato', 'anoexercicio'])


@patch('contratos.services.sof_api.get_empenhos_for_contrato_and_save')
def test_fetch_empenhos_from_sof_and_save_to_temp_table(
        mock_get_and_save_empenhos):
    m_contratos_dao = Mock(spec=ContratosRawDao)
    mocked_contratos = [MockedContratoRaw(111, 2018),
                        MockedContratoRaw(222, 2019)]
    m_contratos_dao.get_all.return_value = mocked_contratos

    services.fetch_empenhos_from_sof_and_save_to_temp_table(m_contratos_dao)

    assert 2 == mock_get_and_save_empenhos.call_count
    for contrato in mocked_contratos:
        mock_get_and_save_empenhos.assert_any_call(contrato=contrato)


@patch('contratos.services.sof_api.save_empenhos_sof_cache')
@patch('contratos.services.sof_api.build_empenhos_data')
@patch('contratos.dao.empenhos_dao.get_by_codcontrato_and_anoexercicio')
def test_get_empenhos_for_contrato_and_save(
        mock_get_empenhos, mock_build_data, mock_save_empenhos):
    contrato = mommy.prepare(ContratoRaw, _fill_optional=True)

    mocked_empenhos_data_return = ['empenhos_data']

    mock_get_empenhos.return_value = SOF_API_REQUEST_RETURN_DICT
    mock_build_data.return_value = mocked_empenhos_data_return

    services.get_empenhos_for_contrato_and_save(contrato=contrato)

    mock_get_empenhos.assert_called_once_with(
        cod_contrato=contrato.codContrato,
        ano_exercicio=contrato.anoExercicioContrato)
    mock_build_data.assert_called_once_with(
        sof_data=SOF_API_REQUEST_RETURN_DICT,
        contrato=contrato)
    mock_save_empenhos.assert_called_once_with(
        empenhos_data=mocked_empenhos_data_return)


def test_build_empenhos_data():
    contrato_data = CONTRATO_RAW_DATA
    contrato = mommy.prepare(ContratoRaw, **contrato_data, _fill_optional=True)

    empenhos_data = services.build_empenhos_data(
        sof_data=deepcopy(SOF_API_REQUEST_RETURN_DICT["lstEmpenhos"]),
        contrato=contrato)

    expected = []
    for emp_dict in SOF_API_REQUEST_RETURN_DICT['lstEmpenhos']:
        for field in contrato._meta.fields:
            if field.primary_key is True:
                continue
            emp_dict[field.name] = getattr(contrato, field.name)
        expected.append(emp_dict)

    assert expected == empenhos_data


@patch('contratos.dao.empenhos_temp_dao.create')
def test_save_empenhos_sof_cache(mock_create):
    empenhos_data = SOF_API_REQUEST_RETURN_DICT['lstEmpenhos']

    services.save_empenhos_sof_cache(empenhos_data=empenhos_data)

    assert 2 == mock_create.call_count
    calls_list = mock_create.call_args_list
    assert call(data=empenhos_data[0]) in calls_list
    assert call(data=empenhos_data[1]) in calls_list


MockedFailedRequest = namedtuple(
    'MockedFailedRequest',
    ['cod_contrato', 'ano_exercicio', 'ano_empenho'])


@patch('contratos.services.sof_api.get_empenhos_for_contrato_and_save')
@patch('contratos.dao.empenhos_failed_requests_dao.delete')
@patch('contratos.dao.empenhos_failed_requests_dao.get_all')
def test_retry_empenhos_sof_failed_api_requests(
        mock_get_all_failed, mock_delete_failed, mock_get_and_save_empenhos):
    mocked_failed = [MockedFailedRequest(111, 2018, 2018),
                     MockedFailedRequest(222, 2018, 2019)]
    mock_get_all_failed.return_value = mocked_failed

    m_contratos_dao = Mock(spec=ContratosRawDao)
    contratos = mommy.prepare(ContratoRaw, codContrato=cycle([111, 222]),
                              anoExercicioContrato=2018, _quantity=2)
    m_contratos_dao.get.side_effect = contratos

    services.retry_empenhos_sof_failed_api_requests(m_contratos_dao)

    assert 2 == m_contratos_dao.get.call_count
    assert 2 == mock_get_and_save_empenhos.call_count
    for failed_request, contrato in zip(mocked_failed, contratos):
        m_contratos_dao.get.assert_any_call(
            codcontrato=failed_request.cod_contrato,
            anoexercicio=failed_request.ano_exercicio)
        mock_get_and_save_empenhos.assert_any_call(
            contrato=contrato, ano_empenho=failed_request.ano_empenho)
        mock_delete_failed.assert_any_call(failed_request)


def test_update_empenho_sof_cache_from_temp_table():
    m_empenhos_dao = Mock(spec=empenhos_dao)

    empenhos_temp = mommy.prepare(EmpenhoSOFCacheTemp, _quantity=2)
    m_empenhos_temp_dao = Mock(spec=empenhos_temp_dao)
    m_empenhos_temp_dao.get_all.return_value = empenhos_temp

    services.update_empenho_sof_cache_from_temp_table(
        empenhos_dao=m_empenhos_dao, empenhos_temp_dao=m_empenhos_temp_dao)

    m_empenhos_temp_dao.get_all.assert_called_once_with()
    assert 2 == m_empenhos_dao.create_from_temp_table_obj.call_count
    assert 2 == m_empenhos_temp_dao.delete.call_count

    for empenho_temp in empenhos_temp:
        m_empenhos_dao.create_from_temp_table_obj.assert_any_call(empenho_temp)
        m_empenhos_temp_dao.delete.assert_any_call(empenho_temp)


class TestVerifyTableLinesCount(TestCase):

    def setUp(self):
        self.m_empenhos_dao = Mock(spec=empenhos_dao)
        self.m_empenhos_dao.count_all.return_value = 100

        self.m_empenhos_temp_dao = Mock(spec=empenhos_temp_dao)
        self.m_empenhos_temp_dao.count_all.return_value = 100

    def test_verify_table_lines_count(self):
        services.verify_table_lines_count(
            empenhos_dao=self.m_empenhos_dao,
            empenhos_temp_dao=self.m_empenhos_temp_dao)

        self.m_empenhos_dao.count_all.assert_called_once_with()
        self.m_empenhos_temp_dao.count_all.assert_called_once_with()

    def test_raises_exception_when_is_under_limit(self):
        self.m_empenhos_temp_dao.count_all.return_value = (
            100 * CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT - 1)

        with pytest.raises(ContratosEmpenhosDifferenceOverLimit):
            services.verify_table_lines_count(
                empenhos_dao=self.m_empenhos_dao,
                empenhos_temp_dao=self.m_empenhos_temp_dao)

        self.m_empenhos_dao.count_all.assert_called_once_with()
        self.m_empenhos_temp_dao.count_all.assert_called_once_with()


@patch.object(services, 'ContratosRawDao')
@patch.object(services, 'update_empenho_sof_cache_from_temp_table')
@patch.object(services, 'verify_table_lines_count')
@patch.object(services, 'retry_empenhos_sof_failed_api_requests')
@patch.object(services, 'fetch_empenhos_from_sof_and_save_to_temp_table')
@patch.object(services, 'empenhos_failed_requests_dao')
@patch.object(services, 'empenhos_temp_dao')
@patch.object(services, 'empenhos_dao')
def test_get_empenhos_for_contratos(
        m_empenhos_dao, m_empenhos_temp_dao, m_empenhos_failed_dao,
        m_fetch, m_retry, m_verify, m_update, m_contratos_raw_dao):
    mocked_contratos_dao = Mock(spec=ContratosRawDao)
    m_contratos_raw_dao.return_value = mocked_contratos_dao

    m_empenhos_failed_dao.count_all.side_effect = [2, 1, 0]

    services.get_empenhos_for_contratos_from_sof_api()

    m_empenhos_temp_dao.erase_all.assert_called_once_with()
    m_fetch.assert_called_once_with(mocked_contratos_dao)
    assert 2 == m_retry.call_count
    m_verify.assert_called_once_with(
        empenhos_dao=m_empenhos_dao, empenhos_temp_dao=m_empenhos_temp_dao)
    m_update.assert_called_once_with(
        empenhos_dao=m_empenhos_dao, empenhos_temp_dao=m_empenhos_temp_dao)
