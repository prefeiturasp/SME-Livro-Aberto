from copy import deepcopy
from unittest import TestCase
from unittest.mock import Mock, patch

from model_mommy import mommy

from contratos.dao.models_dao import (
    CategoriasContratosDao,
    CategoriasContratosFromToDao,
    ContratosRawDao,
    EmpenhosSOFCacheDao,
    EmpenhosSOFCacheTempDao,
    EmpenhosFailedRequestsDao,
    ExecucoesContratosDao,
    FornecedoresDao,
    ModalidadesContratosDao,
    ObjetosContratosDao)
from contratos.models import (
    CategoriaContrato,
    CategoriaContratoFromTo,
    ContratoRaw,
    EmpenhoSOFCache,
    EmpenhoSOFCacheTemp,
    EmpenhoSOFFailedAPIRequest,
    ExecucaoContrato,
    Fornecedor,
    ModalidadeContrato,
    ObjetoContrato)
from contratos.tests.fixtures import (
    EMPENHOS_DAO_CREATE_DATA,
    EMPENHOS_FAILED_API_REQUESTS_CREATE_DATA,
    EXECUCAO_CONTRATO_CREATE_DATA,
)


class EmpenhosSOFCacheDaoTestCase(TestCase):

    def setUp(self):
        self.dao = EmpenhosSOFCacheDao()

    @patch.object(EmpenhoSOFCache.objects, 'all')
    def test_get_all(self, mock_all):
        mocked_contratos = [Mock(spec=EmpenhoSOFCache),
                            Mock(spec=EmpenhoSOFCache)]
        mock_all.return_value = mocked_contratos

        ret = self.dao.get_all()
        assert ret == mocked_contratos
        mock_all.assert_called_once_with()

    @patch.object(EmpenhoSOFCache.objects, 'count')
    def test_count_all(self, mock_count):
        mock_count.return_value = 2

        ret = self.dao.count_all()
        assert ret == 2
        mock_count.assert_called_once_with()

    @patch.object(EmpenhoSOFCache.objects, 'create')
    def test_create(self, mock_create):
        empenho_data = EMPENHOS_DAO_CREATE_DATA
        empenho = mommy.prepare(EmpenhoSOFCache, **empenho_data)
        mock_create.return_value = empenho

        ret = self.dao.create(data=empenho_data)
        mock_create.assert_called_once_with(**empenho_data)
        assert ret == empenho

    def test_create_from_temp_table_data(self):
        mocked_empenho = Mock(spec=EmpenhoSOFCache)
        self.dao.model = Mock(spec=EmpenhoSOFCache)
        self.dao.model.return_value = mocked_empenho

        empenho_temp = mommy.prepare(EmpenhoSOFCacheTemp, _fill_optional=True)

        empenho = self.dao.create_from_temp_table_obj(
            empenho_temp=empenho_temp)

        for field in empenho_temp._meta.fields:
            if field.primary_key is True:
                continue
            assert (getattr(empenho, field.name)
                    == getattr(empenho_temp, field.name))
        mocked_empenho.save.assert_called_once_with()


class EmpenhosTempDaoTestCase(TestCase):

    def setUp(self):
        self.dao = EmpenhosSOFCacheTempDao()

    @patch.object(EmpenhoSOFCacheTemp.objects, 'all')
    def test_get_all(self, mock_all):
        mocked_empenhos = [Mock(spec=EmpenhoSOFCacheTemp),
                           Mock(spec=EmpenhoSOFCacheTemp)]
        mock_all.return_value = mocked_empenhos

        ret = self.dao.get_all()
        assert ret == mocked_empenhos
        mock_all.assert_called_once_with()

    @patch.object(EmpenhoSOFCacheTemp.objects, 'create')
    def test_create(self, mock_create):
        empenho_data = EMPENHOS_DAO_CREATE_DATA
        empenho = mommy.prepare(EmpenhoSOFCacheTemp, **empenho_data)
        mock_create.return_value = empenho

        ret = self.dao.create(data=empenho_data)
        mock_create.assert_called_once_with(**empenho_data)
        assert ret == empenho

    def test_delete(self):
        empenho = mommy.prepare(EmpenhoSOFCacheTemp, _fill_optional=True)
        empenho.delete = Mock()

        self.dao.delete(empenho)

        empenho.delete.assert_called_once_with()

    @patch.object(EmpenhoSOFCacheTemp.objects, 'count')
    def test_count_all(self, mock_count):
        mock_count.return_value = 2

        ret = self.dao.count_all()
        assert ret == 2
        mock_count.assert_called_once_with()

    @patch.object(EmpenhoSOFCacheTemp.objects, 'all')
    def test_erase_all(self, mock_all):
        mocked_all_return = Mock()
        mock_all.return_value = mocked_all_return

        self.dao.erase_all()

        mock_all.assert_called_once_with()
        mocked_all_return.delete.assert_called_once_with()


class EmpenhosFailedRequestsDaoTestCase(TestCase):

    def setUp(self):
        self.dao = EmpenhosFailedRequestsDao()

    @patch.object(EmpenhoSOFFailedAPIRequest.objects, 'all')
    def test_get_all(self, mock_all):
        mocked_empenhos = [Mock(spec=EmpenhoSOFFailedAPIRequest),
                           Mock(spec=EmpenhoSOFFailedAPIRequest)]
        mock_all.return_value = mocked_empenhos

        ret = self.dao.get_all()
        assert ret == mocked_empenhos
        mock_all.assert_called_once_with()

    @patch.object(EmpenhoSOFFailedAPIRequest.objects, 'create')
    def test_create(self, mock_create):
        empenho_data = EMPENHOS_FAILED_API_REQUESTS_CREATE_DATA
        empenho = mommy.prepare(EmpenhoSOFFailedAPIRequest, **empenho_data)
        mock_create.return_value = empenho

        ret = self.dao.create(**empenho_data)

        mock_create.assert_called_once_with(**empenho_data)
        assert ret == empenho

    def test_delete(self):
        empenho = mommy.prepare(EmpenhoSOFFailedAPIRequest, _fill_optional=True)
        empenho.delete = Mock()

        self.dao.delete(empenho)

        empenho.delete.assert_called_once_with()

    @patch.object(EmpenhoSOFFailedAPIRequest.objects, 'count')
    def test_count_all(self, mock_count):
        mock_count.return_value = 2

        ret = self.dao.count_all()
        assert ret == 2
        mock_count.assert_called_once_with()


class ContratoRawDAOTestCase(TestCase):

    @patch.object(ContratoRaw.objects, 'all')
    def test_get_all(self, mock_all):
        dao = ContratosRawDao()
        mocked_contratos = [Mock(spec=ContratoRaw),
                            Mock(spec=ContratoRaw)]
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


class CategoriasContratosDaoTestCase(TestCase):

    @patch.object(CategoriaContrato.objects, 'get_or_create')
    def test_get_or_create(self, mock_get_or_create):
        dao = CategoriasContratosDao()

        mocked_return = (Mock(spec=CategoriaContrato), True)
        mock_get_or_create.return_value = mocked_return

        data = {"id": 11, "desc": "categoria contrato"}
        ret = dao.get_or_create(**data)
        assert ret == mocked_return
        mock_get_or_create.assert_called_once_with(**data)