from typing import NamedTuple

from openpyxl import load_workbook


class OrcamentoColumns(NamedTuple):
    id: str
    description: str
    other_col: dict = None


MODELS = {
    "Orgao": OrcamentoColumns('H', 'J', {'initials': 'I'}),
    # "ProjetoAtividade": OrcamentoColumns('U', 'V', {'type': 'S'}),
    "Categoria": OrcamentoColumns('Y', 'Z'),
}


def import_fk_object(ws, row, name):
    id_col = MODELS[name].id
    desc_col = MODELS[name].description
    # other_col_dict = MODELS[name].other_col

    import ipdb
    ipdb.set_trace()
    row = str(row)
    id = int(ws[id_col + row].value)
    description = ws[desc_col + row].value
    # other_col =

    # save object

    return id


def import_orcamento_csv():
    filepath = ('./budget_execution/data/'
                'orcamento-1541109528703.xlsx')
    wb = load_workbook(filepath)
    ws = wb['data']

    row = 2
    row_is_valid = True
    while row_is_valid:
        try:
            year = int(ws['d' + str(row)].value)
        except TypeError:
            row_is_valid = False
            continue
        orgao_id = import_fk_object(ws, row, 'Orgao')
        # projeto_id = import_projeto(row)
        # categoria_id = import_categoria
        row += 1


def run():
    import_orcamento_csv()
