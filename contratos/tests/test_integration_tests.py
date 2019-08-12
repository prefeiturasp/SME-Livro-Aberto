import pytest

from model_mommy import mommy

from contratos.dao.models_dao import (
    CategoriasContratosDao, CategoriasContratosFromToDao, EmpenhosSOFCacheDao,
    ExecucoesContratosDao, FornecedoresDao, ModalidadesContratosDao,
    ObjetosContratosDao)
from contratos.models import (
    CategoriaContrato, CategoriaContratoFromTo, EmpenhoSOFCache,
    ExecucaoContrato, ModalidadeContrato, ObjetoContrato,
    Fornecedor)
from contratos.use_cases import (
    ApplyCategoriasContratosFromToUseCase,
    GenerateExecucoesContratosUseCase)
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


@pytest.mark.django_db
def test_apply_categoria_contrato_fromto():
    assert 0 == CategoriaContrato.objects.count()

    execucoes = mommy.make(ExecucaoContrato, categoria_id=None, _quantity=2)
    fromtos = [
        mommy.make(CategoriaContratoFromTo,
                   indexer=execucoes[0].empenho_indexer,
                   _fill_optional=True),
        mommy.make(CategoriaContratoFromTo,
                   indexer=execucoes[1].empenho_indexer,
                   _fill_optional=True),
    ]

    uc = ApplyCategoriasContratosFromToUseCase(
        execucoes_dao=ExecucoesContratosDao(),
        categorias_fromto_dao=CategoriasContratosFromToDao(),
        categorias_dao=CategoriasContratosDao())
    uc.execute()

    assert 2 == CategoriaContrato.objects.count()
    for n, execucao in enumerate(execucoes):
        execucao.refresh_from_db()
        assert execucao.categoria.name == fromtos[n].categoria_name
        assert execucao.categoria.desc == fromtos[n].categoria_desc
