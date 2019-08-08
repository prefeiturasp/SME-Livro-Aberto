from copy import deepcopy
from datetime import datetime


CONTRATO_RAW_DATA = {
    "anoExercicio": 2019,
    "codContrato": 2222,
    "codModalidadeContrato": 2,
    "txtDescricaoModalidadeContrato": "desc modalidade",
    "txtObjetoContrato": "desc objeto",
}


SOF_API_EMPENHOS_DATA = [
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
        "valTotalEmpenhado": 1160,
    },
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
        "txtDescricaoElemento": "Outros Serviços de Terceiros - Pessoa",
        "txtDescricaoFonteRecurso": "Tesouro Municipal",
        "txtDescricaoFuncao": "Educação",
        "txtDescricaoItemDespesa": "Gerenciamento",
        "txtDescricaoPrograma": "Acesso a educação e qualidade do ensino",
        "txtDescricaoProjetoAtividade": "Ações e Materiais de Apoio",
        "txtRazaoSocial": "YONE DIAS YAMASSAKI -EPP",
        "txtDescricaoSubElemento": "Serviços Técnicos Profissionais",
        "txtDescricaoSubFuncao": "Educação Básica",
        "valAnuladoEmpenho": 0,
        "valEmpenhadoLiquido": 17400,
        "valLiquidado": 0,
        "valPagoExercicio": 0,
        "valPagoRestos": 0,
        "valTotalEmpenhado": 17400,
    }
]

SOF_API_REQUEST_RETURN_DICT = {
    "metadados": {
        "txtStatus": "OK",
        "txtMensagemErro": None,
        "qtdPaginas": 1
    },
    "lstEmpenhos": deepcopy(SOF_API_EMPENHOS_DATA),
}


empenho_contrato_data = {
    "anoExercicio": 2019,
    "codContrato": 5555,
    "codModalidadeContrato": 2,
    "txtDescricaoModalidadeContrato": "desc modalidade",
    "txtObjetoContrato": "desc objeto",
}


GENERATE_EXECUCOES_CONTRATOS_EMPENHOS_DATA = [
    {**empenho_dict, **empenho_contrato_data}
    for empenho_dict in deepcopy(SOF_API_EMPENHOS_DATA)]


BUILD_EMPENHOS_DATA_SOF_API_SERVICE_OUTPUT = {
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
    "valTotalEmpenhado": 1160,
    "anoExercicio": 2019,
    "codContrato": 5555,
    "codModalidadeContrato": 2,
    "txtDescricaoModalidadeContrato": "desc modalidade",
    "txtObjetoContrato": "desc objeto",
}


EMPENHOS_DAO_CREATE_DATA = deepcopy(BUILD_EMPENHOS_DATA_SOF_API_SERVICE_OUTPUT)

EMPENHOS_DAO_GET_BY_ANO_EMPENHO_DATA = {
    2018: [
        {
            "anoEmpenho": 2018,
            "codCategoria": 3,
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 1160,
            "valLiquidado": 1160,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 1160
        },
        {
            "anoEmpenho": 2018,
            "codCategoria": 3,
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 200,
            "valLiquidado": 100,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 100
        },
    ],
    2019: [
        {
            "anoEmpenho": 2019,
            "codCategoria": 3,
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 1160,
            "valLiquidado": 1160,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 1160
        },
    ]
}


EMPENHOS_FAILED_API_REQUESTS_CREATE_DATA = {
    "cod_contrato": 555,
    "ano_exercicio": 2018,
    "ano_empenho": 2019,
    "error_code": 500,
}


EXECUCAO_CONTRATO_CREATE_DATA = {
    "cod_contrato": 555,
    "empenho_indexer": '2018.16.2100.3.3.90.30.00.1',
    "year": datetime.strptime(str(2019), "%Y"),
    "valor_empenhado": 200.2,
    "valor_liquidado": 150.1,
    "modalidade_id": 11,
    "objeto_contrato_id": 22,
    "fornecedor_id": 33,
}
