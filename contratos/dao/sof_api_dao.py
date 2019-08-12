import requests

from django.conf import settings
from django.utils import timezone

from contratos.dao.dao import EmpenhosFailedRequestsDao
from contratos.models import EmpenhoSOFCache


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
    empenhos_failed_requests_dao = EmpenhosFailedRequestsDao()
    url = (
        'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
        f'v2.1.0/consultaEmpenhos?anoEmpenho={ano_empenho}&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        f'&codContrato={cod_contrato}&codOrgao=16'
    )
    headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
    print(f"getting empenhos for contrato {ano_exercicio}: {cod_contrato}")
    try:
        response = requests.get(url, headers=headers)
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
    return data['lstEmpenhos']
