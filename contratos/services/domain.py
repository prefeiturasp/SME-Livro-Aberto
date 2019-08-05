from contratos.dao.dao import (
    CategoriasContratosDao, CategoriasContratosFromToDao, EmpenhosSOFCacheDao,
    ExecucoesContratosDao, FornecedoresDao, ModalidadesContratosDao,
    ObjetosContratosDao)
from contratos.use_cases import (
    ApplyCategoriasContratosFromToUseCase,
    GenerateExecucoesContratosUseCase)


def generate_execucoes_contratos_and_apply_fromto():
    print("Generating execucões contratos")
    generate_execucoes_uc = GenerateExecucoesContratosUseCase(
        empenhos_dao=EmpenhosSOFCacheDao(),
        execucoes_dao=ExecucoesContratosDao(),
        modalidades_dao=ModalidadesContratosDao(),
        objetos_dao=ObjetosContratosDao(),
        fornecedores_dao=FornecedoresDao())
    generate_execucoes_uc.execute()

    print("Applying from-to")
    apply_fromto_uc = ApplyCategoriasContratosFromToUseCase(
        execucoes_dao=ExecucoesContratosDao(),
        categorias_fromto_dao=CategoriasContratosFromToDao(),
        categorias_dao=CategoriasContratosDao())
    apply_fromto_uc.execute()
