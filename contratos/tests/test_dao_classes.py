from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock, patch

from contratos.dao.dao import (
    EmpenhosSOFCacheDao, ExecucoesContratosDao, FornecedoresDao,
    ModalidadesContratosDao, ObjetosContratosDao)
from contratos.models import (
    EmpenhoSOFCache, ExecucaoContrato, Fornecedor, ModalidadeContrato,
    ObjetoContrato)
from contratos.tests.fixtures import EXECUCAO_CONTRATO_CREATE_DATA


class EmpenhoSOFCacheDAOTestCase(TestCase):

    @patch.object(EmpenhoSOFCache.objects, 'all')
    def test_get_all(self, mock_all):
        dao = EmpenhosSOFCacheDao()

        mocked_contratos = [Mock(spec=EmpenhoSOFCache),
                            Mock(spec=EmpenhoSOFCache)]
        mock_all.return_value = mocked_contratos

        ret = dao.get_all()
        assert ret == mocked_contratos
        mock_all.assert_called_once_with()


class ExecucaoContratoDAOTestCase(TestCase):

    @patch.object(ExecucaoContrato.objects, 'create')
    def test_create(self, mock_create):
        dao = ExecucoesContratosDao()

        mocked_execucao = Mock(spec=ExecucaoContrato)
        mock_create.return_value = mocked_execucao

        data = deepcopy(EXECUCAO_CONTRATO_CREATE_DATA)
        ret = dao.create(**data)
        assert ret == mocked_execucao
        mock_create.assert_called_once_with(**data)


class ModalidadeContratoDAOTestCase(TestCase):

    @patch.object(ModalidadeContrato.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = ModalidadesContratosDao()

        mocked_return = (Mock(spec=ModalidadeContrato), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "modalidade"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)


class ObjetoContratoDAOTestCase(TestCase):

    @patch.object(ObjetoContrato.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = ObjetosContratosDao()

        mocked_return = (Mock(spec=ObjetoContrato), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "objeto"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)


class FornecedorDAOTestCase(TestCase):

    @patch.object(Fornecedor.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = FornecedoresDao()

        mocked_return = (Mock(spec=Fornecedor), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "fornecedor"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)
