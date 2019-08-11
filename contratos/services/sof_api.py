from contratos.constants import CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT
from contratos.dao import empenhos_dao
from contratos.dao.dao import (
    ContratosRawDao,
    EmpenhosSOFCacheTempDao,
    EmpenhosFailedRequestsDao,
)
from contratos.exceptions import ContratosEmpenhosDifferenceOverLimit


def get_empenhos_for_contratos_from_sof_api():
    contratos_raw_dao = ContratosRawDao()
    empenhos_temp_dao = EmpenhosSOFCacheTempDao()
    empenhos_failed_requests_dao = EmpenhosFailedRequestsDao()

    empenhos_temp_dao.erase_all()

    print("Fetching empenhos from SOF API and saving to temp table")
    fetch_empenhos_from_sof_and_save_to_temp_table(
        contratos_raw_dao=contratos_raw_dao,
        empenhos_temp_dao=empenhos_temp_dao)

    while empenhos_failed_requests_dao.count_all() > 0:
        print("Retrying failed API requests")
        retry_empenhos_sof_failed_api_requests(
            contratos_raw_dao, empenhos_failed_requests_dao)

    print("Verifying count of lines in temp table")
    verify_table_lines_count(
        empenhos_dao=empenhos_dao, empenhos_temp_dao=empenhos_temp_dao)

    print("Moving data from temp table to the real table")
    update_empenho_sof_cache_from_temp_table(
        empenhos_dao=empenhos_dao, empenhos_temp_dao=empenhos_temp_dao)


def fetch_empenhos_from_sof_and_save_to_temp_table(
        contratos_raw_dao, empenhos_temp_dao):
    for contrato in contratos_raw_dao.get_all():
        count = get_empenhos_for_contrato_and_save(
            contrato=contrato, empenhos_temp_dao=empenhos_temp_dao)
        print(f'{count} empenhos saved for contrato {contrato.codcontrato}')


def get_empenhos_for_contrato_and_save(*, contrato, empenhos_temp_dao,
                                       ano_empenho=None):
    cod_contrato = contrato.codContrato
    ano_exercicio = contrato.anoExercicioContrato

    if not ano_empenho:
        sof_data = empenhos_dao.get_by_codcontrato_and_anoexercicio(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio)
    else:
        sof_data = empenhos_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

    if not sof_data:
        return 0

    empenhos_data = build_empenhos_data(sof_data=sof_data, contrato=contrato)
    count = save_empenhos_sof_cache(empenhos_data=empenhos_data,
                                    empenhos_temp_dao=empenhos_temp_dao)
    return count


def build_empenhos_data(*, sof_data, contrato):
    empenhos_data = sof_data.copy()
    for data in empenhos_data:
        for field in contrato._meta.fields:
            if field.primary_key is True:
                continue
            data[field.name] = getattr(contrato, field.name)
    return empenhos_data


def save_empenhos_sof_cache(*, empenhos_data, empenhos_temp_dao):
    for data in empenhos_data:
        empenhos_temp_dao.create(data=data)

    return len(empenhos_data)


def retry_empenhos_sof_failed_api_requests(
        contratos_raw_dao, empenhos_failed_requests_dao):
    for failed_request in empenhos_failed_requests_dao.get_all():
        contrato = contratos_raw_dao.get(
            codcontrato=failed_request.cod_contrato,
            anoexercicio=failed_request.ano_exercicio)

        count = get_empenhos_for_contrato_and_save(
            contrato=contrato,
            ano_empenho=failed_request.ano_empenho,
        )
        empenhos_failed_requests_dao.delete(failed_request)
        print(
            f'{count} empenhos saved for contrato {failed_request.cod_contrato}'
        )


def update_empenho_sof_cache_from_temp_table(*, empenhos_dao,
                                             empenhos_temp_dao):
    for empenho_temp in empenhos_temp_dao.get_all():
        empenhos_dao.create_from_temp_table_obj(empenho_temp)
        empenhos_temp_dao.delete(empenho_temp)
    print("Empenhos copied from temp table to EmpenhoSOFCache table")


def verify_table_lines_count(*, empenhos_dao, empenhos_temp_dao):
    limit = CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT
    empenhos_count = empenhos_dao.count_all()
    empenhos_temp_count = empenhos_temp_dao.count_all()

    if empenhos_count and empenhos_temp_count < empenhos_count * limit:
        percent_limit = round((1 - limit) * 100)
        msg = (
            f'O número de linhas na tabela temporária é {percent_limit}% '
            'menor que o da tabela de produção. Os valores não serão '
            'atualizados'
        )
        raise ContratosEmpenhosDifferenceOverLimit(msg)
