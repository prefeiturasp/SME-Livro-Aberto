from copy import deepcopy
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from model_mommy import mommy

from contratos.constants import CATEGORIA_FROM_TO_SLUG
from contratos.dao.models_dao import (
    CategoriasContratosDao, CategoriasContratosFromToDao, FornecedoresDao,
    EmpenhosSOFCacheDao, ExecucoesContratosDao,
    ModalidadesContratosDao, ObjetosContratosDao)
from contratos.models import (
    CategoriaContrato, CategoriaContratoFromTo, ExecucaoContrato, Fornecedor,
    EmpenhoSOFCache, ModalidadeContrato, ObjetoContrato)
from contratos.use_cases import (
    ApplyCategoriasContratosFromToUseCase,
    GenerateExecucoesContratosUseCase)


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

    def test_execute_erases_execucoes_and_calls_create_execucao_for_each_empenho(self):  # noqa
        empenhos = mommy.prepare(EmpenhoSOFCache, _fill_optional=True,
                                 _quantity=2)
        self.m_empenhos_dao.get_all.return_value = empenhos
        self.uc._create_execucao_by_empenho = Mock()

        self.uc.execute()

        self.m_execucoes_dao.erase_all.assert_called_once_with()

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


class TestApplyCategoriasContratosFromToUseCase(TestCase):

    def setUp(self):
        self.m_execucoes_dao = Mock(spec=ExecucoesContratosDao)
        self.m_categorias_fromto_dao = Mock(spec=CategoriasContratosFromToDao)
        self.m_categorias_dao = Mock(spec=CategoriasContratosDao)
        self.uc = ApplyCategoriasContratosFromToUseCase(
            execucoes_dao=self.m_execucoes_dao,
            categorias_fromto_dao=self.m_categorias_fromto_dao,
            categorias_dao=self.m_categorias_dao)

    def test_use_case_constructor(self):
        assert self.uc.execucoes_dao == self.m_execucoes_dao
        assert self.uc.categorias_fromto_dao == self.m_categorias_fromto_dao
        assert self.uc.categorias_dao == self.m_categorias_dao

    def test_execute_calls_apply_fromto_for_each_fromto(self):
        fromtos = mommy.prepare(CategoriaContratoFromTo, _fill_optional=True,
                                _quantity=2)
        self.m_categorias_fromto_dao.get_all.return_value = fromtos
        self.uc._apply_fromto = Mock()

        self.uc.execute()

        self.m_categorias_fromto_dao.get_all.assert_called_once_with()
        assert 2 == self.uc._apply_fromto.call_count
        for fromto in fromtos:
            self.uc._apply_fromto.assert_any_call(fromto)

    def test_apply_fromto(self):
        slugs_dict = deepcopy(CATEGORIA_FROM_TO_SLUG)
        categoria_name, categoria_slug = slugs_dict.popitem()
        m_categoria = mommy.prepare(
            CategoriaContrato, name=categoria_name, _fill_optional=True)
        self.m_categorias_dao.get_or_create.return_value = (m_categoria, True)

        m_execucao = mommy.prepare(ExecucaoContrato, categoria=None,
                                   _fill_optional=True)
        self.m_execucoes_dao.filter_by_indexer.return_value = [m_execucao]

        fromto = mommy.prepare(
            CategoriaContratoFromTo, categoria_name=categoria_name,
            _fill_optional=True)
        self.uc._apply_fromto(fromto)

        self.m_categorias_dao.get_or_create.assert_called_once_with(
            name=fromto.categoria_name,
            defaults={
                'desc': fromto.categoria_desc,
                'slug': categoria_slug,
            })
        self.m_execucoes_dao.filter_by_indexer.assert_called_once_with(
            fromto.indexer)
        self.m_execucoes_dao.update_with.assert_called_once_with(
            execucao=m_execucao, categoria_id=m_categoria.id)
