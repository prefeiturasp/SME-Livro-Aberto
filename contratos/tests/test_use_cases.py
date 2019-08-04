from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from model_mommy import mommy

from contratos.dao.dao import (
    FornecedoresDao, EmpenhosSOFCacheDao, ExecucoesContratosDao,
    ModalidadesContratosDao, ObjetosContratosDao)
from contratos.models import (
    Fornecedor, EmpenhoSOFCache, ModalidadeContrato, ObjetoContrato)
from contratos.use_cases import GenerateExecucoesContratosUseCase


class TestGenerateExecucoesContratosUseCase(TestCase):

    def setUp(self):
        self.m_empenhos_dao = Mock(spec=EmpenhosSOFCacheDao)
        self.m_execucoes_dao = Mock(spec=ExecucoesContratosDao)
        self.m_modalidades_dao = Mock(spec=ModalidadesContratosDao)
        self.m_objetos_dao = Mock(spec=ObjetosContratosDao)
        self.m_fornecedores_dao = Mock(spec=FornecedoresDao)
        self.uc = GenerateExecucoesContratosUseCase(
            empenhos_dao=self.m_empenhos_dao,
            execucoes_dao=self.m_execucoes_dao,
            modalidades_dao=self.m_modalidades_dao,
            objetos_dao=self.m_objetos_dao,
            fornecedores_dao=self.m_fornecedores_dao)

    def test_use_case_constructor(self):
        assert self.uc.empenhos_dao == self.m_empenhos_dao
        assert self.uc.execucoes_dao == self.m_execucoes_dao
        assert self.uc.modalidades_dao == self.m_modalidades_dao
        assert self.uc.objetos_dao == self.m_objetos_dao
        assert self.uc.fornecedores_dao == self.m_fornecedores_dao

    def test_execute_calls_create_execucao_for_each_empenho(self):
        empenhos = mommy.prepare(EmpenhoSOFCache, _fill_optional=True,
                                 _quantity=2)
        self.m_empenhos_dao.get_all.return_value = empenhos
        self.uc._create_execucao_by_empenho = Mock()

        self.uc.execute()

        self.m_empenhos_dao.get_all.assert_called_once_with()
        assert 2 == self.uc._create_execucao_by_empenho.call_count
        for empenho in empenhos:
            self.uc._create_execucao_by_empenho.assert_any_call(
                empenho=empenho)

    def test_create_execucao_by_empenho(self):
        m_modalidade = mommy.prepare(ModalidadeContrato, _fill_optional=True)
        m_objeto = mommy.prepare(ObjetoContrato, id=22, _fill_optional=True)
        m_fornecedor = mommy.prepare(Fornecedor, id=33, _fill_optional=True)

        self.m_modalidades_dao.get_or_create.return_value = (m_modalidade, True)
        self.m_objetos_dao.get_or_create.return_value = (m_objeto, True)
        self.m_fornecedores_dao.get_or_create.return_value = (
            m_fornecedor, True)

        empenho = mommy.prepare(EmpenhoSOFCache, anoEmpenho=2019,
                                _fill_optional=True)

        self.uc._create_execucao_by_empenho(empenho)

        self.m_modalidades_dao.get_or_create.assert_called_once_with(
            id=empenho.codModalidadeContrato,
            desc=empenho.txtDescricaoModalidadeContrato)
        self.m_objetos_dao.get_or_create.assert_called_once_with(
            desc=empenho.txtObjetoContrato)
        self.m_fornecedores_dao.get_or_create.assert_called_once_with(
            razao_social=empenho.txtRazaoSocial)

        expected_execucao_data = {
            "cod_contrato": empenho.codContrato,
            "empenho_indexer": empenho.indexer,
            "year": datetime.strptime(str(empenho.anoEmpenho), "%Y"),
            "valor_empenhado": empenho.valEmpenhadoLiquido,
            "valor_liquidado": empenho.valLiquidado,
            "modalidade_id": m_modalidade.id,
            "objeto_contrato_id": m_objeto.id,
            "fornecedor_id": m_fornecedor.id,
        }

        self.m_execucoes_dao.create.assert_called_once_with(
            **expected_execucao_data)
