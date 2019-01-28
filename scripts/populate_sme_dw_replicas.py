# THIS SCRIPT IS NOT SUPPOSED TO BE RUNNED. it was used only during
# development. In production, those tables should be populated by SME team
# via airflow

import pandas

from datetime import datetime

from budget_execution.models import Empenho, Orcamento


def import_orcamento():
    # replace with the path for any dump csv of dw_orcamento
    df = pandas.read_csv(
        '/home/diego/Projects/fgv/transparencia/dump-csv/replica-orcamento.csv')

    for i, row in df.iterrows():
        orcamento = Orcamento()
        for col_name, value in row.items():
            if col_name[:3] == 'dt_':
                try:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

            orcamento.__setattr__(col_name, value)
        orcamento.save()


def import_empenhos():
    # replace with the path for any dump csv of dw_empenhos
    df = pandas.read_csv(
        '/home/diego/Projects/fgv/transparencia/dump-csv/replica-empenhos.csv')

    for i, row in df.iterrows():
        empenho = Empenho()
        for col_name, value in row.items():
            if col_name[:3] == 'dt_':
                try:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

            empenho.__setattr__(col_name, value)
        empenho.save()


def run():
    # import_orcamento()
    # import_empenhos()
    pass
