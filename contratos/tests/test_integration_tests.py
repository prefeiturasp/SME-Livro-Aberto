import pytest

from model_mommy import mommy

from contratos.dao.dao import (
    EmpenhosSOFCacheDao, ExecucoesContratosDao, FornecedoresDao,
    ModalidadesContratosDao, ObjetosContratosDao)
from contratos.models import (
    EmpenhoSOFCache, ExecucaoContrato, ModalidadeContrato, ObjetoContrato,
    Fornecedor)
from contratos.use_cases import GenerateExecucoesContratosUseCase
from contratos.tests.fixtures import GENERATE_EXECUCOES_CONTRATOS_EMPENHOS_DATA


@pytest.mark.django_db
def test_generate_execucoes_contratos():
    assert 0 == ExecucaoContrato.objects.count()

    empenhos_data = GENERATE_EXECUCOES_CONTRATOS_EMPENHOS_DATA

    for data in empenhos_data:
        mommy.make(EmpenhoSOFCache, **data)

    uc = GenerateExecucoesContratosUseCase(
        empenhos_dao=EmpenhosSOFCacheDao(),
        execucoes_dao=ExecucoesContratosDao(),
        modalidades_dao=ModalidadesContratosDao(),
        objetos_dao=ObjetosContratosDao(),
        fornecedores_dao=FornecedoresDao())
    uc.execute()

    assert 2 == ExecucaoContrato.objects.count()
    assert 1 == ModalidadeContrato.objects.count()
    assert 1 == ObjetoContrato.objects.count()
    assert 1 == Fornecedor.objects.count()
