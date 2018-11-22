# # This script was meant to be runned only once during the development.
# # It shouldn't be used anymore. The data gathered by this script is in
# # a json file (from_to_handler/migrations/data/from_to.py) that is loaded
# # by a datamigration (migration 0009 in from_to_handler).


import datetime

from openpyxl import load_workbook

from from_to_handler.models import (
    Deflator,
    DotacaoFromTo,
    FonteDeRecursoFromTo,
    GNDFromTo,
    SubelementoFromTo,
)


def import_fontes_de_recurso():
    filepath = './from_to_handler/de-paras/DE-PARA Fontes de Recurso.xlsx'
    wb = load_workbook(filepath)
    ws = wb['Plan1']

    row = 2
    row_is_valid = True
    while row_is_valid:
        try:
            code = int(ws['a' + str(row)].value)
        except TypeError:
            row_is_valid = False
            continue
        name = ws['b' + str(row)].value
        group_code = int(ws['c' + str(row)].value)
        group_name = ws['d' + str(row)].value

        fdr = FonteDeRecursoFromTo()
        fdr.code = code
        fdr.name = name
        fdr.group_code = group_code
        fdr.group_name = group_name
        fdr.save()

        row += 1


def import_subelementos():
    filepath = './from_to_handler/de-paras/DE-PARA Sub-elementos.xlsx'
    wb = load_workbook(filepath)
    ws = wb['Plan1']

    row = 2
    row_is_valid = True
    while row_is_valid:
        code = ws['a' + str(row)].value
        if not code:
            row_is_valid = False
            continue
        description = ws['b' + str(row)].value
        new_code = int(ws['c' + str(row)].value)
        new_name = ws['d' + str(row)].value

        se = SubelementoFromTo()
        se.code = code
        se.description = description
        se.new_code = new_code
        se.new_name = new_name
        se.save()

        row += 1


def import_dotacoes():
    filepath = ('./from_to_handler/de-paras/'
                'DE-PARA Dotações Subgrupos Grupos.xlsx')
    wb = load_workbook(filepath)
    ws = wb['De Para Final']

    row = 2
    row_is_valid = True
    while row_is_valid:
        indexer = ws['b' + str(row)].value
        if not indexer:
            row_is_valid = False
            continue
        group_code = int(ws['f' + str(row)].value)
        group_description = ws['g' + str(row)].value
        subgroup_code = int(ws['d' + str(row)].value.split('.')[1])
        subgroup_description = ws['e' + str(row)].value

        dot = DotacaoFromTo()
        dot.indexer = indexer
        dot.group_code = group_code
        dot.group_description = group_description
        dot.subgroup_code = subgroup_code
        dot.subgroup_description = subgroup_description
        dot.save()

        row += 1


def import_gnd():
    filepath = ('./from_to_handler/de-paras/'
                'DE-PARA Grupos de Despesa e Elementos.xlsx')
    wb = load_workbook(filepath)
    ws = wb['Plan1']

    row = 2
    row_is_valid = True
    while row_is_valid:
        try:
            gnd_code = int(ws['e' + str(row)].value)
        except TypeError:
            row_is_valid = False
            continue
        gnd_description = ws['a' + str(row)].value
        elemento_code = int(ws['d' + str(row)].value)
        elemento_description = ws['c' + str(row)].value
        new_gnd_code = int(ws['f' + str(row)].value)
        new_gnd_description = ws['b' + str(row)].value

        gnd = GNDFromTo()
        gnd.gnd_code = gnd_code
        gnd.gnd_description = gnd_description
        gnd.elemento_code = elemento_code
        gnd.elemento_description = elemento_description
        gnd.new_gnd_code = new_gnd_code
        gnd.new_gnd_description = new_gnd_description
        gnd.save()

        row += 1


def import_deflator():
    filepath = ('./from_to_handler/de-paras/'
                'Deflator Setembro 2018.xlsx')
    wb = load_workbook(filepath, data_only=True)
    ws = wb['Anual']

    row = 2
    row_is_valid = True
    while row_is_valid:
        year = ws['a' + str(row)].value
        if not year:
            row_is_valid = False
            continue
        index_number = ws['b' + str(row)].value
        variation_percent = ws['c' + str(row)].value

        defl = Deflator()
        defl.year = datetime.date(int(year), 1, 1)
        defl.index_number = index_number
        defl.variation_percent = variation_percent * 100
        defl.save()

        row += 1


def run():
    # import_fontes_de_recurso()
    # import_subelementos()
    # import_dotacoes()
    # import_gnd()
    # import_deflator()
    pass
