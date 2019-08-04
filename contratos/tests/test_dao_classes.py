from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock, patch

from contratos.dao.dao import EmpenhosSOFCacheDao, ExecucoesContratosDao
from contratos.models import EmpenhoSOFCache, ExecucaoContrato
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
