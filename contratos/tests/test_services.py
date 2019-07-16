from unittest.mock import call, patch

from contratos import services


def test_build_empenhos_data():
    sof_return_dict = {
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

    cod_contrato = 5555
    ano_exercicio = 2019

    empenhos_data = services.build_empenhos_data(
        sof_data=sof_return_dict, ano_exercicio=ano_exercicio,
        cod_contrato=cod_contrato)

    expected = []
    for emp_dict in sof_return_dict['lstEmpenhos']:
        emp_dict.update({'anoExercicio': ano_exercicio,
                         'codContrato': cod_contrato})
        expected.append(emp_dict)

    assert expected == empenhos_data


@patch('contratos.services.EmpenhoSOFCache')
def test_save_empenhos_sof_cache(mock_Empenho):
    empenhos_data = [
        {
            "anoEmpenho": 2019,
            "codCategoria": 3,
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 17400,
            "valLiquidado": 0,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 17400,
            "anoExercicio": 2019,
            "codContrato": 5555,
        },
        {
            "anoEmpenho": 2019,
            "codCategoria": 3,
            "valAnuladoEmpenho": 0,
            "valEmpenhadoLiquido": 1160,
            "valLiquidado": 1160,
            "valPagoExercicio": 0,
            "valPagoRestos": 0,
            "valTotalEmpenhado": 1160,
            "anoExercicio": 2019,
            "codContrato": 5555,
        }
    ]
    services.save_empenhos_sof_cache(empenhos_data=empenhos_data)

    assert 2 == mock_Empenho.objects.create.call_count
    calls_list = mock_Empenho.objects.create.call_args_list
    assert call(**empenhos_data[0]) in calls_list
    assert call(**empenhos_data[1]) in calls_list
