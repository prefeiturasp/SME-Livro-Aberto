import pytest

from unittest import TestCase
from unittest.mock import Mock, patch

from django.conf import settings
from model_mommy import mommy

from contratos.dao import contratos_raw_dao, empenhos_dao
from contratos.models import ContratoRaw, EmpenhoSOFCache


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

    @patch('contratos.dao.empenhos_dao.EmpenhoSOFCache')
    def test_create(self, mock_Empenho):
        empenho_data = {
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
        mocked_return = Mock(EmpenhoSOFCache, autospec=True)
        mock_Empenho.objects.create.return_value = mocked_return

        ret = empenhos_dao.create(data=empenho_data)
        mock_Empenho.objects.create.assert_called_once_with(**empenho_data)
        assert ret == mocked_return
