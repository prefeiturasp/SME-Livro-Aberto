import requests

from django.conf import settings
from django.utils import timezone

from contratos.constants import PRODAM_URL
from contratos.dao.models_dao import EmpenhosFailedRequestsDao


def get_by_codcontrato_and_anoexercicio(*, cod_contrato, ano_exercicio):
    current_year = timezone.now().year
    years = range(ano_exercicio, current_year + 1)

    empenhos_list = []
    for year in years:
        data = get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=year)
        if data:
            empenhos_list += data

    return empenhos_list


def get_by_ano_empenho(*, cod_contrato, ano_exercicio, ano_empenho):
    """
    Método responsável por executar a conexão com a API SOF e obter os 
    dados de empenhos, realizando os tratamentos de acordo com a resposta
    da API.
    Caso ocorrer algum erro, os dados são salvos no objeto empenhos_failed_requests_dao
    para posterior nova tentativa de consulta.
    :param cod_contrato: codigo do contrato a ser baixado da API
    :param ano_exercicio: ano do exercicio do contrato para compor chave composta na base
    :param ano_empenho: ano de empenho do contrato
    """
    empenhos_failed_requests_dao = EmpenhosFailedRequestsDao()
    url = (
        f'{PRODAM_URL}?anoEmpenho={ano_empenho}&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        f'&codContrato={cod_contrato}&codOrgao=16'
    )
    headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
    print(f"getting empenhos for codcontrato {cod_contrato} | ano exercicio "
          f"{ano_exercicio} | ano empenho {ano_empenho}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
    except Exception as e:
        error_code = -1
        empenhos_failed_requests_dao.create(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho,
            error_code=error_code)
        print(
            f'{error_code} API request failed for {ano_exercicio}: '
            f'{cod_contrato}')
        return None

    if response.status_code != 200:
        error_code = response.status_code
        empenhos_failed_requests_dao.create(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho,
            error_code=error_code)
        print(
            f'{error_code} API request failed for {ano_exercicio}: '
            f'{cod_contrato}')
        return None

    data = response.json()
    empenhos = data['lstEmpenhos']
    # TODO: changed in new version of sof api. add test.
    if empenhos and not isinstance(empenhos, list):
        empenhos = [empenhos]
    return empenhos
