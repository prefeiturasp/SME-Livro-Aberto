import requests

from django.conf import settings

from contratos.models import EmpenhoSOFCache
from contratos.dao import contratos_raw_dao

# {
#     "anoEmpenho": 2019,
#     "codCategoria": 3,
#     "txtCategoriaEconomica": "Despesas Correntes",
#     "codElemento": "39",
#     "codEmpenho": 61374,
#     "codEmpresa": "01",
#     "codFonteRecurso": "00",
#     "codFuncao": "12",
#     "codGrupo": 3,
#     "txtGrupoDespesa": "Outras Despesas Correntes",
#     "codItemDespesa": "01",
#     "codModalidade": 90,
#     "txtModalidadeAplicacao": "Aplicações Diretas",
#     "codOrgao": "16",
#     "codProcesso": 6016201900321630,
#     "codPrograma": "3026",
#     "codProjetoAtividade": "2831",
#     "codSubElemento": "41",
#     "codSubFuncao": "368",
#     "codUnidade": "22",
#     "datEmpenho": "10/07/2019",
#     "mesEmpenho": 12,
#     "nomEmpresa": "PREFEITURA DO MUNICÍPIO DE SÃO PAULO",
#     "numCpfCnpj": "26092777000117",
#     "numReserva": 41070,
#     "txtDescricaoOrgao": "Secretaria Municipal de Educação",
#     "txtDescricaoUnidade": "Diretoria Regional de Educação Butantã",
#     "txtDescricaoElemento": "Outros Serviços de Terceiros - Pessoa Jur",
#     "txtDescricaoFonteRecurso": "Tesouro Municipal",
#     "txtDescricaoFuncao": "Educação",
#     "txtDescricaoItemDespesa": "Coffee Break",
#     "txtDescricaoPrograma": "Acesso a educação e qualidade do ensino",
#     "txtDescricaoProjetoAtividade": "Ações e Materiais de Apoio Did",
#     "txtRazaoSocial": "YONE DIAS YAMASSAKI -EPP",
#     "txtDescricaoSubElemento": "Fornecimento de Alimentação",
#     "txtDescricaoSubFuncao": "Educação Básica",
#     "valAnuladoEmpenho": 0,
#     "valEmpenhadoLiquido": 1160,
#     "valLiquidado": 1160,
#     "valPagoExercicio": 0,
#     "valPagoRestos": 0,
#     "valTotalEmpenhado": 1160,
#     "anoExercicio": 2019,
#     "codContrato": 5555,
# }


def update_empenho_sof_cache_table():
    for contrato in contratos_raw_dao.get_all():
        get_empenhos_for_contrato_and_save(
            cod_contrato=contrato.codcontrato,
            ano_exercicio=contrato.anoexercicio)
        print(f'empenhos for contrato {contrato.codcontrato} saved')


def get_empenhos_for_contrato_and_save(*, cod_contrato, ano_exercicio):
    sof_data = get_empenhos_for_contrato(
        cod_contrato=cod_contrato,
        ano_exercicio=ano_exercicio)
    empenhos_data = build_empenhos_data(
        sof_data=sof_data,
        ano_exercicio=ano_exercicio,
        cod_contrato=cod_contrato)
    save_empenhos_sof_cache(empenhos_data=empenhos_data)


def get_empenhos_for_contrato(*, cod_contrato, ano_exercicio):
    url = (
        'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
        'v2.1.0/consultaEmpenhos?anoEmpenho=2019&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        '&codContrato={}&codOrgao=16'
    )
    headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
    response = requests.get(url.format(cod_contrato), headers=headers)
    return response.json()


def build_empenhos_data(*, sof_data, ano_exercicio, cod_contrato):
    empenhos_data = sof_data['lstEmpenhos']
    for data in empenhos_data:
        data['anoExercicio'] = ano_exercicio
        data['codContrato'] = cod_contrato
    return empenhos_data


def save_empenhos_sof_cache(*, empenhos_data):
    for data in empenhos_data:
        EmpenhoSOFCache.objects.create(**data)
