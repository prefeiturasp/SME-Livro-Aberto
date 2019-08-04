from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock, patch

from model_mommy import mommy

from contratos.dao.dao import (
    CategoriasContratosDao, CategoriasContratosFromToDao, EmpenhosSOFCacheDao,
    ExecucoesContratosDao, FornecedoresDao, ModalidadesContratosDao,
    ObjetosContratosDao)
from contratos.models import (
    CategoriaContrato, CategoriaContratoFromTo, EmpenhoSOFCache,
    ExecucaoContrato, Fornecedor, ModalidadeContrato,
    ObjetoContrato)
from contratos.tests.fixtures import EXECUCAO_CONTRATO_CREATE_DATA


class EmpenhosSOFCacheDAOTestCase(TestCase):

    @patch.object(EmpenhoSOFCache.objects, 'all')
    def test_get_all(self, mock_all):
        dao = EmpenhosSOFCacheDao()

        mocked_contratos = [Mock(spec=EmpenhoSOFCache),
                            Mock(spec=EmpenhoSOFCache)]
        mock_all.return_value = mocked_contratos

        ret = dao.get_all()
        assert ret == mocked_contratos
        mock_all.assert_called_once_with()


class ExecucoesContratosDAOTestCase(TestCase):

    def setUp(self):
        self.dao = ExecucoesContratosDao()

    @patch.object(ExecucaoContrato.objects, 'create')
    def test_create(self, mock_create):
        mocked_execucao = Mock(spec=ExecucaoContrato)
        mock_create.return_value = mocked_execucao

        data = deepcopy(EXECUCAO_CONTRATO_CREATE_DATA)
        ret = self.dao.create(**data)
        assert ret == mocked_execucao
        mock_create.assert_called_once_with(**data)

    @patch.object(ExecucaoContrato.objects, 'get')
    def test_get_by_indexer(self, mock_get):
        mocked_execucao = Mock(spec=ExecucaoContrato)
        mock_get.return_value = mocked_execucao

        indexer = '2018.16.2100.3.3.90.30.00.1'
        ret = self.dao.get_by_indexer(indexer=indexer)
        assert ret == mocked_execucao
        mock_get.assert_called_once_with(empenho_indexer=indexer)

    def test_update_with(self):
        execucao = mommy.prepare(ExecucaoContrato, categoria=None,
                                 _fill_optional=True)
        execucao.save = Mock()

        categoria = mommy.prepare(CategoriaContrato, id=1, _fill_optional=True)
        data = {"categoria_id": categoria.id}

        self.dao.update_with(execucao=execucao, **data)
        assert categoria.id == execucao.categoria_id
        execucao.save.assert_called_once_with()


class ModalidadesContratosDAOTestCase(TestCase):

    @patch.object(ModalidadeContrato.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = ModalidadesContratosDao()

        mocked_return = (Mock(spec=ModalidadeContrato), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "modalidade"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)


class ObjetosContratosDAOTestCase(TestCase):

    @patch.object(ObjetoContrato.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = ObjetosContratosDao()

        mocked_return = (Mock(spec=ObjetoContrato), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "objeto"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)


class FornecedoresDAOTestCase(TestCase):

    @patch.object(Fornecedor.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = FornecedoresDao()

        mocked_return = (Mock(spec=Fornecedor), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "fornecedor"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)


class CategoriasContratosFromToDaoTestCase(TestCase):

    @patch.object(CategoriaContratoFromTo.objects, 'all')
    def test_get_all(self, mock_all):
        dao = CategoriasContratosFromToDao()

        mocked_fromtos = [Mock(spec=CategoriaContratoFromTo),
                          Mock(spec=CategoriaContratoFromTo)]
        mock_all.return_value = mocked_fromtos

        ret = dao.get_all()
        assert ret == mocked_fromtos
        mock_all.assert_called_once_with()


class CategoriasContratosDAOTestCase(TestCase):

    @patch.object(CategoriaContrato.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = CategoriasContratosDao()

        mocked_return = (Mock(spec=CategoriaContrato), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "categoria contrato"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)
