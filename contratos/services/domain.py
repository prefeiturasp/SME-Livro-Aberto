import openpyxl

from contratos.dao.models_dao import (
    CategoriasContratosDao, CategoriasContratosFromToDao, EmpenhosSOFCacheDao,
    ExecucoesContratosDao, FornecedoresDao, ModalidadesContratosDao,
    ObjetosContratosDao)
from contratos.use_cases import (
    ApplyCategoriasContratosFromToUseCase,
    GenerateExecucoesContratosUseCase,
    GenerateXlsxFilesUseCase)


def generate_execucoes_contratos_and_apply_fromto():
    """
    Método que gera as execuções (dados a serem exibidos na ferramenta)
    e aplica as junções dos arquivos, gerando ao final a planilha para
    download dos dados
    """
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

    print("Generating xlsx files")
    generate_xlsx_uc = GenerateXlsxFilesUseCase(
        empenhos_dao=EmpenhosSOFCacheDao(),
        data_handler=openpyxl)
    generate_xlsx_uc.execute()
