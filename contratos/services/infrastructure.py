import os
import zipfile

from django.core.management import call_command

from contratos.constants import (
    CONTRATOS_RAW_DUMP_DIR_PATH, CONTRATOS_RAW_DUMP_FILENAME,
    EXECUCOES_CONTRATOS_DUMP_DIR_PATH,
    EXECUCOES_CONTRATOS_DUMP_FILENAME)
from contratos.models import (
    ExecucaoContrato, CategoriaContrato, ModalidadeContrato, ObjetoContrato,
    Fornecedor)


def populate_contratos_raw_load_with_dump():
    """
    Carrega informações pré-processadas de contratos_raw_load (tabela contendo 
    dados de contratos do AirFlow) no banco de dados para instalação
    do app Contrato Social.
    """
    filepath = f'{CONTRATOS_RAW_DUMP_DIR_PATH}{CONTRATOS_RAW_DUMP_FILENAME}'
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(CONTRATOS_RAW_DUMP_DIR_PATH)

    json_filename = zip_ref.filelist[0].filename
    json_filepath = f'{CONTRATOS_RAW_DUMP_DIR_PATH}{json_filename}'

    try:
        call_command('loaddata', json_filepath)
    except Exception as e:
        print(e)
        os.remove(json_filepath)
    os.remove(json_filepath)


def populate_execucoes_contratos_with_dump():
    """
    Carrega informações pré-processadas de contratos 
    no banco de dados para instalação do app Contrato Social.
    """
    filepath = (f'{EXECUCOES_CONTRATOS_DUMP_DIR_PATH}'
                f'{EXECUCOES_CONTRATOS_DUMP_FILENAME}')
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(EXECUCOES_CONTRATOS_DUMP_DIR_PATH)

    json_filename = zip_ref.filelist[0].filename
    json_filepath = f'{EXECUCOES_CONTRATOS_DUMP_DIR_PATH}{json_filename}'

    ExecucaoContrato.objects.all().delete()
    CategoriaContrato.objects.all().delete()
    ModalidadeContrato.objects.all().delete()
    ObjetoContrato.objects.all().delete()
    Fornecedor.objects.all().delete()

    try:
        call_command('loaddata', json_filepath)
    except Exception as e:
        print(e)
        os.remove(json_filepath)
    os.remove(json_filepath)
