from typing import NamedTuple

from django.apps import apps
from openpyxl import load_workbook


class OtherColumn(NamedTuple):
    name: str
    column: str


class OrcamentoColumns(NamedTuple):
    id: str
    description: str
    other_col: OtherColumn = None


MODELS = {
    "Orgao": OrcamentoColumns('H', 'J', OtherColumn('initials', 'I')),
    # "ProjetoAtividade": OrcamentoColumns('U', 'V', {'type': 'S'}),
    "Categoria": OrcamentoColumns('Y', 'Z'),
}


def import_fk_object(ws, row, name):
    id_col = MODELS[name].id
    desc_col = MODELS[name].description
    other_col_tuple = MODELS[name].other_col

    # import ipdb
    # ipdb.set_trace()
    row = str(row)
    id = int(ws[id_col + row].value)
    description = ws[desc_col + row].value

    Model = apps.get_model('budget_execution', name)
    obj = Model()
    obj.id = id
    obj.description = description.strip()

    if other_col_tuple:
        other_col = other_col_tuple.column
        other_col_name = other_col_tuple.name
        other_col_value = ws[other_col + row].value
        setattr(obj, other_col_name, other_col_value.strip())

    # obj.save()

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
