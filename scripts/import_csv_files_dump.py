import datetime

from typing import NamedTuple

from django.apps import apps
from openpyxl import load_workbook

from budget_execution.models import Execucao


class OtherColumn(NamedTuple):
    name: str
    column: str


class OrcamentoColumns(NamedTuple):
    id: str
    description: str = None
    other_col: OtherColumn = None


MODELS = {
    "Orgao": OrcamentoColumns('H', 'J', OtherColumn('initials', 'I')),
    "ProjetoAtividade": OrcamentoColumns('U', 'V', OtherColumn('type', 'S')),
    "Categoria": OrcamentoColumns('Y', 'Z'),
    "Gnd": OrcamentoColumns('AA', 'AB'),
    "Modalidade": OrcamentoColumns('AC', 'AD'),
    "Elemento": OrcamentoColumns('AE'),
    "FonteDeRecurso": OrcamentoColumns('AF', 'AG'),
    "Subfuncao": OrcamentoColumns('O', 'P'),
    "Programa": OrcamentoColumns('Q', 'R'),
}


def import_fk_object(ws, row, name):
    id_col = MODELS[name].id
    desc_col = MODELS[name].description
    other_col_tuple = MODELS[name].other_col

    row = str(row)
    id = int(ws[id_col + row].value)

    Model = apps.get_model('budget_execution', name)
    if Model.objects.filter(id=id).exists():
        return id

    obj = Model()
    obj.id = id

    if desc_col:
        description = ws[desc_col + row].value
        obj.description = description.strip()

    if other_col_tuple:
        other_col = other_col_tuple.column
        other_col_name = other_col_tuple.name
        other_col_value = ws[other_col + row].value
        setattr(obj, other_col_name, other_col_value.strip())

    obj.save()

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
        projeto_id = import_fk_object(ws, row, 'ProjetoAtividade')
        categoria_id = import_fk_object(ws, row, 'Categoria')
        gnd_id = import_fk_object(ws, row, 'Gnd')
        modalidade_id = import_fk_object(ws, row, 'Modalidade')
        elemento_id = import_fk_object(ws, row, 'Elemento')
        fonte_id = import_fk_object(ws, row, 'FonteDeRecurso')
        subfuncao_id = import_fk_object(ws, row, 'Subfuncao')
        programa_id = import_fk_object(ws, row, 'Programa')

        orcado = ws['ai' + str(row)].value

        execucao = Execucao()
        execucao.year = datetime.date(year, 1, 1)
        execucao.orgao_id = orgao_id
        execucao.projeto_id = projeto_id
        execucao.categoria_id = categoria_id
        execucao.gnd_id = gnd_id
        execucao.modalidade_id = modalidade_id
        execucao.elemento_id = elemento_id
        execucao.fonte_id = fonte_id
        execucao.subfuncao_id = subfuncao_id
        execucao.programa_id = programa_id
        execucao.orcado_atualizado = orcado

        execucao.save()
        print("Saved execução " + str(execucao.id))

        row += 1


def run():
    # import_orcamento_csv()
    pass
