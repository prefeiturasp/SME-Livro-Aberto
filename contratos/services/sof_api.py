from django.db.utils import IntegrityError

from contratos.constants import CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT
from contratos.dao import sof_api_dao
from contratos.dao.models_dao import (
    ContratosRawDao,
    EmpenhosSOFCacheDao,
    EmpenhosSOFCacheTempDao,
    EmpenhosFailedRequestsDao,
)
from contratos.exceptions import ContratosEmpenhosDifferenceOverLimit


def get_empenhos_for_contratos_from_sof_api():
    """
    Este método tem como principal responsabilidade
    realizar a junção entre os dados de contratos disponibilizados
    pelo Airflow na tabela contratos_raw e capturar os dados de
    empenhos de acordo com o código do contrato e o ano de empenho.
    """
    contratos_raw_dao = ContratosRawDao()
    empenhos_dao = EmpenhosSOFCacheDao()
    empenhos_temp_dao = EmpenhosSOFCacheTempDao()
    empenhos_failed_requests_dao = EmpenhosFailedRequestsDao()

    empenhos_temp_dao.erase_all()
    empenhos_failed_requests_dao.erase_all()

    print("Fetching empenhos from SOF API and saving to temp table")
    fetch_empenhos_from_sof_and_save_to_temp_table(
        contratos_raw_dao=contratos_raw_dao,
        empenhos_temp_dao=empenhos_temp_dao)

    while empenhos_failed_requests_dao.count_all() > 0:
        print("Retrying failed API requests")
        retry_empenhos_sof_failed_api_requests(
            contratos_raw_dao, empenhos_failed_requests_dao, empenhos_temp_dao)

    print("Verifying count of lines in temp table")
    verify_table_lines_count(
        empenhos_dao=empenhos_dao, empenhos_temp_dao=empenhos_temp_dao)

    print("Moving data from temp table to the real table")
    update_empenho_sof_cache_from_temp_table(
        empenhos_dao=empenhos_dao, empenhos_temp_dao=empenhos_temp_dao)


def fetch_empenhos_from_sof_and_save_to_temp_table(
        contratos_raw_dao, empenhos_temp_dao):
    """
    Para cada registro de contrato, realiza a conexão com API SOF
    e baixa os dados de empenhos em /getempenhos e salva na tabela
    empenhos_sof_cache (tabela temporária criada para, antes de
    exibir os dados, validar se há discrepância percentual dos
    resultados).
    :param contrato: objeto contrato
    :param empenhos_temp_dao: objeto de destino dos dados de empenhos
    """
    for contrato in contratos_raw_dao.get_all():
        count = get_empenhos_for_contrato_and_save(
            contrato=contrato, empenhos_temp_dao=empenhos_temp_dao)
        print(f'{count} empenhos saved for contrato {contrato.codContrato}')


def get_empenhos_for_contrato_and_save(*, contrato, empenhos_temp_dao,
                                       ano_empenho=None):
    """
    Realiza a chamada na API SOF para obter os dados de empenho de contratos:
    :param contrato: objeto contrato (contendo os atributos de contratos a serem
    utilizados na consulta de empenho)
    :param empenhos_temp_dao: objeto de destino dos dados de empenhos
    :param ano_empenho: ano do empenho correspondente ao contrato a ser baixado
    da API.
    """
    cod_contrato = contrato.codContrato
    ano_exercicio = contrato.anoExercicioContrato

    if not ano_empenho:
        sof_data = sof_api_dao.get_by_codcontrato_and_anoexercicio(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio)
    else:
        sof_data = sof_api_dao.get_by_ano_empenho(
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
    """
    Este método faz a junção das bases de contrato e os empenhos
    recolhidos da API SOF
    """
    empenhos_data = sof_data.copy()
    for data in empenhos_data:
        for field in contrato._meta.fields:
            if field.primary_key is True:
                continue
            data[field.name] = getattr(contrato, field.name)
    return empenhos_data


def save_empenhos_sof_cache(*, empenhos_data, empenhos_temp_dao):
    """
    Salva os dados de empenhos em tabela temporária para fazer a comparação dos
    dados obtidos de contratos comparados ao período anterior.
    """
    for data in empenhos_data:
        try:
            empenhos_temp_dao.create(data=data)
        except IntegrityError:
            # duplicate data is not saved
            pass

    return len(empenhos_data)


def retry_empenhos_sof_failed_api_requests(
        contratos_raw_dao, empenhos_failed_requests_dao, empenhos_temp_dao):
    """
    Este método conecta à api sof para tentar novamente a consulta por
    empenhos que falharam na primeira tentativa.
    """
    for failed_request in empenhos_failed_requests_dao.get_all():
        contrato = contratos_raw_dao.get(
            codContrato=failed_request.cod_contrato,
            anoExercicioContrato=failed_request.ano_exercicio)

        count = get_empenhos_for_contrato_and_save(
            contrato=contrato,
            empenhos_temp_dao=empenhos_temp_dao,
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
    try:
        limit = float(CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT)
    except ValueError:
        raise Exception(
            'CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT shoud be integer. '
            f'Current value: {CONTRATOS_EMPENHOS_DIFFERENCE_PERCENT_LIMIT}')
    empenhos_count = empenhos_dao.count_all()
    empenhos_temp_count = empenhos_temp_dao.count_all()

    if empenhos_count:
        percent_limit = round(limit * 100)
        upper_limit = empenhos_count + (empenhos_count * limit)
        lower_limit = empenhos_count - (empenhos_count * limit)
        if empenhos_temp_count > upper_limit:
            msg = (
                f'O número de linhas na tabela temporária é {percent_limit}% '
                'maior que o da tabela de produção. Os valores não serão '
                'atualizados.'
            )
            raise ContratosEmpenhosDifferenceOverLimit(msg)

        if empenhos_temp_count < lower_limit:
            msg = (
                f'O número de linhas na tabela temporária é {percent_limit}% '
                'menor que o da tabela de produção. Os valores não serão '
                'atualizados.'
            )
            raise ContratosEmpenhosDifferenceOverLimit(msg)


def retry_failed_requests_and_update_sof_cache_table():
    """
    Executa as etapas pós download de empenhos (fetch_empenhos) do script
    `get_empenhos_for_contratos_from_sof_api`. Utilizado qdo acontece algum
    erro durante o processo, após os empenhos terem sido baixados.
    """
    contratos_raw_dao = ContratosRawDao()
    empenhos_dao = EmpenhosSOFCacheDao()
    empenhos_temp_dao = EmpenhosSOFCacheTempDao()
    empenhos_failed_requests_dao = EmpenhosFailedRequestsDao()

    while empenhos_failed_requests_dao.count_all() > 0:
        print("Retrying failed API requests")
        retry_empenhos_sof_failed_api_requests(
            contratos_raw_dao, empenhos_failed_requests_dao, empenhos_temp_dao)

    print("Verifying count of lines in temp table")
    verify_table_lines_count(
        empenhos_dao=empenhos_dao, empenhos_temp_dao=empenhos_temp_dao)

    print("Moving data from temp table to the real table")
    update_empenho_sof_cache_from_temp_table(
        empenhos_dao=empenhos_dao, empenhos_temp_dao=empenhos_temp_dao)
