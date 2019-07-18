import pytest

from unittest import TestCase
from unittest.mock import patch

from django.conf import settings
from model_mommy import mommy

from contratos.dao import contratos_raw_dao, empenhos_dao
from contratos.models import ContratoRaw


SOF_RETURN_DICT = {
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


@pytest.mark.django_db
class ContratoRawDAOTestCase(TestCase):

    def test_get_all(self):
        expected_contratos = mommy.make(ContratoRaw, _quantity=2)

        ret = contratos_raw_dao.get_all()

        assert 2 == len(ret)
        for contrato in expected_contratos:
            assert contrato in ret


@pytest.mark.django_db
class EmpenhoDAOTestCase(TestCase):

    @patch('contratos.dao.empenhos_dao.requests.get')
    def test_get_by_codcontrato_and_anoexercicio(self, mock_get):
        cod_contrato = 5555
        ano_exercicio = 2019

        mock_get.return_value.json.return_value = SOF_RETURN_DICT
        url = (
            'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/'
            'v2.1.0/consultaEmpenhos?anoEmpenho=2019&mesEmpenho=12'
            f'&anoExercicio={ano_exercicio}'
            '&codContrato={}&codOrgao=16'
        )
        headers = {'Authorization': f'Bearer {settings.PRODAM_KEY}'}

        ret = empenhos_dao.get_by_codcontrato_and_anoexercicio(
            cod_contrato=cod_contrato, ano_exercicio=ano_exercicio)

        assert SOF_RETURN_DICT == ret
        mock_get.assert_called_once_with(url.format(cod_contrato),
                                         headers=headers)
