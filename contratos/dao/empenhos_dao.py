import requests

from django.conf import settings
# from django.utils import timezone

from contratos.models import EmpenhoSOFCache


def get_by_codcontrato_and_anoexercicio(*, cod_contrato, ano_exercicio):
    # current_year = timezone.now().year
    # years = range(ano_exercicio, current_year + 1)
    url = (
        'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
        'v2.1.0/consultaEmpenhos?anoEmpenho={}&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        f'&codContrato={cod_contrato}&codOrgao=16'
    )
    headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
    # for year in years:
    year = 2019
    try:
        response = requests.get(url.format(year), headers=headers)
    except Exception as e:
        import ipdb
        ipdb.set_trace()
    if response.status_code != 200:
        import ipdb
        ipdb.set_trace()
    data = response.json()
    return data['lstEmpenhos']


def create(*, data):
    return EmpenhoSOFCache.objects.create(**data)
