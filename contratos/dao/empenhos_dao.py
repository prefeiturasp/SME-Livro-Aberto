import requests

from django.conf import settings

from contratos.models import EmpenhoSOFCache


def get_by_codcontrato_and_anoexercicio(*, cod_contrato, ano_exercicio):
    url = (
        'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
        'v2.1.0/consultaEmpenhos?anoEmpenho=2019&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        '&codContrato={}&codOrgao=16'
    )
    headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
    response = requests.get(url.format(cod_contrato), headers=headers)
    return response.json()


def create(*, data):
    return EmpenhoSOFCache.objects.create(**data)
