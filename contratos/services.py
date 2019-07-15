import requests

from django.conf import settings

from contratos.models import ContratoRaw


ret_dict = {
    "metadados": {
        "txtStatus": "OK",
        "txtMensagemErro": None,
        "qtdPaginas": 1
    },
    "lstEmpenhos": [
        {
            "anoEmpenho": 2019,
            "codCategoria": 3,
            "txtCategoriaEconomica": "Despesas Correntes",
            "codElemento": "39",
            "codEmpenho": 53783,
            "codEmpresa": "01",
            "codFonteRecurso": "00",
            "codFuncao": "12",
            "codGrupo": 3,
            "txtGrupoDespesa": "Outras Despesas Correntes",
            "codItemDespesa": "01",
            "codModalidade": 90,
            "txtModalidadeAplicacao": "Aplicações Diretas",
            "codOrgao": "16",
            "codProcesso": 6016201900321630,
            "codPrograma": "3026",
            "codProjetoAtividade": "2831",
            "codSubElemento": "05",
            "codSubFuncao": "368",
            "codUnidade": "22",
            "datEmpenho": "10/06/2019",
            "mesEmpenho": 12,
            "nomEmpresa": "PREFEITURA DO MUNICÍPIO DE SÃO PAULO",
            "numCpfCnpj": "26092777000117",
            "numReserva": 36609,
            "txtDescricaoOrgao": "Secretaria Municipal de Educação",
            "txtDescricaoUnidade": "Diretoria Regional de Educação Butantã",
            "txtDescricaoElemento": "Outros Serviços de Terceiros - Pessoa Jur",
            "txtDescricaoFonteRecurso": "Tesouro Municipal",
            "txtDescricaoFuncao": "Educação",
            "txtDescricaoItemDespesa": "Gerenciamento",
            "txtDescricaoPrograma": "Acesso a educação e qualidade do ensino",
            "txtDescricaoProjetoAtividade": "Ações e Materiais de Apoio Did",
            "txtRazaoSocial": "YONE DIAS YAMASSAKI -EPP",
            "txtDescricaoSubElemento": "Serviços Técnicos Profissionais",
            "txtDescricaoSubFuncao": "Educação Básica",
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 17400,
            "valLiquidado": 0,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 17400
        },
        {
            "anoEmpenho": 2019,
            "codCategoria": 3,
            "txtCategoriaEconomica": "Despesas Correntes",
            "codElemento": "39",
            "codEmpenho": 61374,
            "codEmpresa": "01",
            "codFonteRecurso": "00",
            "codFuncao": "12",
            "codGrupo": 3,
            "txtGrupoDespesa": "Outras Despesas Correntes",
            "codItemDespesa": "01",
            "codModalidade": 90,
            "txtModalidadeAplicacao": "Aplicações Diretas",
            "codOrgao": "16",
            "codProcesso": 6016201900321630,
            "codPrograma": "3026",
            "codProjetoAtividade": "2831",
            "codSubElemento": "41",
            "codSubFuncao": "368",
            "codUnidade": "22",
            "datEmpenho": "10/07/2019",
            "mesEmpenho": 12,
            "nomEmpresa": "PREFEITURA DO MUNICÍPIO DE SÃO PAULO",
            "numCpfCnpj": "26092777000117",
            "numReserva": 41070,
            "txtDescricaoOrgao": "Secretaria Municipal de Educação",
            "txtDescricaoUnidade": "Diretoria Regional de Educação Butantã",
            "txtDescricaoElemento": "Outros Serviços de Terceiros - Pessoa Jur",
            "txtDescricaoFonteRecurso": "Tesouro Municipal",
            "txtDescricaoFuncao": "Educação",
            "txtDescricaoItemDespesa": "Coffee Break",
            "txtDescricaoPrograma": "Acesso a educação e qualidade do ensino",
            "txtDescricaoProjetoAtividade": "Ações e Materiais de Apoio Did",
            "txtRazaoSocial": "YONE DIAS YAMASSAKI -EPP",
            "txtDescricaoSubElemento": "Fornecimento de Alimentação",
            "txtDescricaoSubFuncao": "Educação Básica",
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 1160,
            "valLiquidado": 1160,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 1160
        }
    ]
}


def update_empenho_sof_cache_table():
    ano_exercicio = 2019
    url = (
        'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
        'v2.1.0/consultaEmpenhos?anoEmpenho=2019&mesEmpenho=12'
        f'&anoExercicio={ano_exercicio}'
        '&codContrato={}&codOrgao=16'
    )
    for contrato in ContratoRaw.objects.all():
        import ipdb
        ipdb.set_trace()
        headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}
        response = requests.get(url.format(contrato.codcontrato),
                                headers=headers)
        empenhos_data = build_empenhos_data(
            response.json(), ano_exercicio, contrato.codcontrato)
        save_empenhos_cache(empenhos_data)


def build_empenhos_data(json_data, ano_exercicio, cod_contrato):
    empenhos_data = json_data['lstEmpenhos']
    for data in empenhos_data:
        data['anoExercicio'] = ano_exercicio
        data['codContrato'] = cod_contrato
    return empenhos_data


def save_empenhos_cache(empenhos_data):
    # for data in empenhos_data:
    pass
