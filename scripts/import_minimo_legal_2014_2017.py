# # This script was meant to be runned only once during the development.
# # It shouldn't be used anymore. The data gathered by this script is in
# # a json file (data/minimo_legal_2014_2017.json) that
# # needs to be loaded manually with `manage.py loaddata`

import pandas

from datetime import date

from budget_execution.models import MinimoLegal


PATH = ('./data/minimo_legal_2014_2017.xlsx')


def import_spreadsheet():
    dataframe = pandas.read_excel(PATH)

    for i, row in dataframe.iterrows():
        MinimoLegal.objects.create_or_update(
            projeto_id=row['Código'],
            year=row['Ano'],
            projeto_desc=row['Descrição'],
            orcado_atualizado=row['Dotação'],
            empenhado_liquido=row['Despesa'],
        )
    print('Spreadsheet {} imported'.format(PATH))


def run():
    import_spreadsheet()
