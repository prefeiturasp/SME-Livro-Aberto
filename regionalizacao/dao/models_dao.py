from collections import namedtuple

from django.db import IntegrityError, transaction
from openpyxl import load_workbook

from regionalizacao.models import (
    DistritoZonaFromTo,
    EtapaTipoEscolaFromTo,
    PtrfFromTo,
    UnidadeRecursosFromTo,
)


SheetField = namedtuple('SheetField', ['name', 'column'])


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
            ft_key = ws[self.fields[0].column + str(row)].value
            if not ft_key:
                row_is_valid = False
                continue

            ft = self.model()
            for field in self.fields:
                value = ws[field.column + str(row)].value
                setattr(ft, field.name, value)
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
        self.fields = [
            SheetField('codesc', 'a'),
            SheetField('vlrepasse', 'd'),
        ]


class DistritoZonaFromToDao(FromToDao):

    def __init__(self):
        self.model = DistritoZonaFromTo
        self.fields = [
            SheetField('coddist', 'a'),
            SheetField('zona', 'c'),
        ]


class EtapaTipoEscolaFromToDao(FromToDao):

    def __init__(self):
        self.model = EtapaTipoEscolaFromTo
        self.fields = [
            SheetField('tipoesc', 'a'),
            SheetField('desctipoesc', 'b'),
            SheetField('etapa', 'c'),
        ]


class UnidadeRecursosFromToDao(FromToDao):

    def __init__(self):
        self.model = UnidadeRecursosFromTo
        self.fields = [
            SheetField('codesc', 'a'),
            SheetField('grupo', 'b'),
            SheetField('subgrupo', 'c'),
            SheetField('valor', 'd'),
            SheetField('label', 'e'),
        ]
