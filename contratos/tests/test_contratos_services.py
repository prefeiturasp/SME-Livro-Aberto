from collections import namedtuple
from unittest.mock import call, patch, Mock

from model_mommy import mommy

from contratos import services
from contratos.dao import empenhos_dao, empenhos_temp_dao
from contratos.models import EmpenhoSOFCacheTemp
from contratos.tests.fixtures import SOF_API_REQUEST_RETURN_DICT


MockedContratoRaw = namedtuple('MockedContratoRaw',
                               ['codcontrato', 'anoexercicio'])


@patch('contratos.services.get_empenhos_for_contrato_and_save')
@patch('contratos.dao.contratos_raw_dao.get_all')
def test_fetch_empenhos_from_sof_and_save_to_temp_table(
        mock_get_all, mock_get_and_save_empenhos):
    mocked_contratos = [MockedContratoRaw(111, 2018),
                        MockedContratoRaw(222, 2019)]
    mock_get_all.return_value = mocked_contratos

    services.fetch_empenhos_from_sof_and_save_to_temp_table()

    assert 2 == mock_get_and_save_empenhos.call_count
    for contrato in mocked_contratos:
        mock_get_and_save_empenhos.assert_any_call(
            cod_contrato=contrato.codcontrato,
            ano_exercicio=contrato.anoexercicio)


@patch('contratos.services.save_empenhos_sof_cache')
@patch('contratos.services.build_empenhos_data')
@patch('contratos.dao.empenhos_dao.get_by_codcontrato_and_anoexercicio')
def test_get_empenhos_for_contrato_and_save(
        mock_get_empenhos, mock_build_data, mock_save_empenhos):
    cod_contrato = 5555
    ano_exercicio = 2019
    mocked_empenhos_data_return = ['empenhos_data']

    mock_get_empenhos.return_value = SOF_API_REQUEST_RETURN_DICT
    mock_build_data.return_value = mocked_empenhos_data_return

    services.get_empenhos_for_contrato_and_save(
        cod_contrato=cod_contrato, ano_exercicio=ano_exercicio)

    mock_get_empenhos.assert_called_once_with(
        cod_contrato=cod_contrato, ano_exercicio=ano_exercicio)
    mock_build_data.assert_called_once_with(
        sof_data=SOF_API_REQUEST_RETURN_DICT,
        cod_contrato=cod_contrato,
        ano_exercicio=ano_exercicio)
    mock_save_empenhos.assert_called_once_with(
        empenhos_data=mocked_empenhos_data_return)


def test_build_empenhos_data():
    cod_contrato = 5555
    ano_exercicio = 2019

    empenhos_data = services.build_empenhos_data(
        sof_data=SOF_API_REQUEST_RETURN_DICT["lstEmpenhos"],
        ano_exercicio=ano_exercicio,
        cod_contrato=cod_contrato)

    expected = []
    for emp_dict in SOF_API_REQUEST_RETURN_DICT['lstEmpenhos']:
        emp_dict.update({'anoExercicio': ano_exercicio,
                         'codContrato': cod_contrato})
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


@patch('contratos.services.get_empenhos_for_contrato_and_save')
@patch('contratos.dao.empenhos_failed_requests_dao.delete')
@patch('contratos.dao.empenhos_failed_requests_dao.get_all')
def test_retry_empenhos_sof_failed_api_requests(
        mock_get_all_failed, mock_delete_failed, mock_get_and_save_empenhos):
    mocked_failed = [MockedFailedRequest(111, 2018, 2018),
                     MockedFailedRequest(222, 2018, 2019)]
    mock_get_all_failed.return_value = mocked_failed

    services.retry_empenhos_sof_failed_api_requests()

    assert 2 == mock_get_and_save_empenhos.call_count
    for failed_request in mocked_failed:
        mock_get_and_save_empenhos.assert_any_call(
            cod_contrato=failed_request.cod_contrato,
            ano_exercicio=failed_request.ano_exercicio,
            ano_empenho=failed_request.ano_empenho)
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
