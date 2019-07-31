SOF_API_REQUEST_RETURN_DICT = {
    "metadados": {
        "txtStatus": "OK",
        "txtMensagemErro": None,
        "qtdPaginas": 1
    },
    "lstEmpenhos": [
        {
            "anoEmpenho": 2019,
            "codCategoria": 3,
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
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 1160,
            "valLiquidado": 1160,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 1160
        }
    ]
}


EMPENHOS_DAO_CREATE_DATA = {
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
}


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
