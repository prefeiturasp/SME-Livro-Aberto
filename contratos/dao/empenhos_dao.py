import requests

from django.conf import settings
from django.utils import timezone

from contratos.models import EmpenhoSOFCache, EmpenhoSOFFailedAPIRequest


def get_by_codcontrato_and_anoexercicio(*, cod_contrato, ano_exercicio):
    current_year = timezone.now().year
    years = range(ano_exercicio, current_year + 1)

    empenhos_list = []
    for year in years:
        data = _get_by_ano_empenho(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
            ano_empenho=year)
        if data:
            empenhos_list += data
    return empenhos_list


def _get_by_ano_empenho(*, cod_contrato, ano_exercicio, ano_empenho):
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
        _save_failed_api_request(
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
        _save_failed_api_request(
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


def _save_failed_api_request(*, cod_contrato, ano_exercicio, ano_empenho,
                             error_code):
    return EmpenhoSOFFailedAPIRequest.objects.create(
        cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
        ano_empenho=ano_empenho, error_code=error_code)


def create(*, data):
    return EmpenhoSOFCache.objects.create(**data)
