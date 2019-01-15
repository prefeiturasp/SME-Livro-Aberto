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
            code=row['Código'],
            year=date(row['Ano'], 1, 1),
            desc=row['Descrição'],
            dotacao=row['Dotação'],
            despesa=row['Despesa'],
        )
    print('Spreadsheet {} imported'.format(PATH))


def run():
    import_spreadsheet()
