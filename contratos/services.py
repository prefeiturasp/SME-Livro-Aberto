import requests

from django.conf import settings

from contratos.models import ContratoRaw, EmpenhoSOFCache


def update_empenho_sof_cache_table():
    ano_exercicio = 2019
    for contrato in ContratoRaw.objects.all():
        sof_data = get_empenhos_for_contrato(
            contrato.codcontrato, ano_exercicio)
        empenhos_data = build_empenhos_data(
            sof_data=sof_data,
            ano_exercicio=ano_exercicio,
            cod_contrato=contrato.codcontrato)
        save_empenhos_cache(empenhos_data)


def get_empenhos_for_contrato(cod_contrato, ano_exercicio):
    url = (
        'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
        'v2.1.0/consultaEmpenhos?anoEmpenho=2019&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        '&codContrato={}&codOrgao=16'
    )
    headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
    response = requests.get(url.format(cod_contrato), headers=headers)
    return response.json()


def build_empenhos_data(sof_data, ano_exercicio, cod_contrato):
    empenhos_data = sof_data['lstEmpenhos']
    for data in empenhos_data:
        data['anoExercicio'] = ano_exercicio
        data['codContrato'] = cod_contrato
    return empenhos_data


def save_empenhos_cache(empenhos_data):
    for data in empenhos_data:
        EmpenhoSOFCache.objects.create(**empenhos_data)
