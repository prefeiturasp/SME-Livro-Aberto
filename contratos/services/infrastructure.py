import os
import zipfile

from django.core.management import call_command

from contratos.constants import (
    CONTRATOS_RAW_DUMP_DIR_PATH, CONTRATOS_RAW_DUMP_FILENAME)


def populate_contratos_raw_load_with_dump():
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
