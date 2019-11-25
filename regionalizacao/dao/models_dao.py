from collections import namedtuple

from django.db import IntegrityError, transaction
from openpyxl import load_workbook

from regionalizacao.models import (
    DistritoZonaFromTo,
    EtapaTipoEscolaFromTo,
    PtrfFromTo,
    UnidadeRecursosFromTo,
    Dre,
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
        updated = []
        while row_is_valid:
            ft_key_name = self.sheet_columns[0].name
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

            # saving fromto object
            try:
                with transaction.atomic():
                    ft.save()
                added.append(ft_key)
            except IntegrityError:
                old_ft = self.model.objects.get(**{ft_key_name: ft_key})
                old_ft.delete()
                ft.save()
                updated.append(ft_key)

            row += 1

        sheet.added_fromtos = added
        sheet.updated_fromtos = updated
        sheet.extracted = True
        sheet.save()
        return added, updated


class PtrfFromToDao(FromToDao):

    def __init__(self):
        self.model = PtrfFromTo
        self.sheet_columns = [
            SheetColumn('codesc', 'a'),
            SheetColumn('vlrepasse', 'd'),
        ]

    def extract_spreadsheet(self, sheet):
        year_fromtos = self.model.objects.filter(year=sheet.year)
        year_fromtos.delete()
        return super().extract_spreadsheet(sheet)


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

    def extract_spreadsheet(self, sheet):
        year_fromtos = self.model.objects.filter(year=sheet.year)
        year_fromtos.delete()
        return super().extract_spreadsheet(sheet)


# TODO: add unit tests
class DreDao:

    def __init__(self):
        self.model = Dre

    def update_or_create(self, code, name):
        try:
            with transaction.atomic():
                dre = self.create(code=code, name=name)
            created = True
        except IntegrityError:
            dre = self.update(code=code, name=name)
            created = False

        return dre, created

    def create(self, code, name):
        return self.model.objects.create(code=code, name=name)

    def update(self, code, name):
        dre = self.model.objects.get(code=code)
        dre.name = name
        dre.save()
        return dre
