from collections import namedtuple

from django.db import IntegrityError, transaction
from openpyxl import load_workbook

from regionalizacao.models import (
    DistritoZonaFromTo,
    EtapaTipoEscolaFromTo,
    PtrfFromTo,
    UnidadeRecursosFromTo,
)


SheetColumn = namedtuple('SheetColumn', ['name', 'letter'])


class FromToDao:

    def extract_spreadsheet(self, sheet):
        filepath = sheet.spreadsheet.path
        wb = load_workbook(filepath)
        ws = wb.worksheets[0]

        row = 2
        row_is_valid = True
        added = []
        not_added = []
        while row_is_valid:
            ft_key = ws[self.sheet_columns[0].letter + str(row)].value
            if not ft_key:
                row_is_valid = False
                continue

            ft = self.model()
            for column in self.sheet_columns:
                value = ws[column.letter + str(row)].value
                setattr(ft, column.name, value)

            # setting year when applies
            year = getattr(sheet, 'year', None)
            if year:
                ft.year = year
            try:
                with transaction.atomic():
                    ft.save()
                added.append(ft_key)
            except IntegrityError:
                not_added.append(ft_key)

            row += 1

        sheet.added_fromtos = added
        sheet.not_added_fromtos = not_added
        sheet.extracted = True
        sheet.save()
        return added, not_added


class PtrfFromToDao(FromToDao):

    def __init__(self):
        self.model = PtrfFromTo
        self.sheet_columns = [
            SheetColumn('codesc', 'a'),
            SheetColumn('vlrepasse', 'd'),
        ]


class DistritoZonaFromToDao(FromToDao):

    def __init__(self):
        self.model = DistritoZonaFromTo
        self.sheet_columns = [
            SheetColumn('coddist', 'a'),
            SheetColumn('zona', 'c'),
        ]


class EtapaTipoEscolaFromToDao(FromToDao):

    def __init__(self):
        self.model = EtapaTipoEscolaFromTo
        self.sheet_columns = [
            SheetColumn('tipoesc', 'a'),
            SheetColumn('desctipoesc', 'b'),
            SheetColumn('etapa', 'c'),
        ]


class UnidadeRecursosFromToDao(FromToDao):

    def __init__(self):
        self.model = UnidadeRecursosFromTo
        self.sheet_columns = [
            SheetColumn('codesc', 'a'),
            SheetColumn('grupo', 'b'),
            SheetColumn('subgrupo', 'c'),
            SheetColumn('valor', 'd'),
            SheetColumn('label', 'e'),
        ]
