from django.db import IntegrityError, transaction

from openpyxl import load_workbook

from regionalizacao.models import (
    DistritoZonaFromTo,
    PtrfFromTo,
)


class PtrfFromToDao:
    def extract_spreadsheet(self, sheet):
        filepath = sheet.spreadsheet.path
        wb = load_workbook(filepath)
        ws = wb.worksheets[0]

        row = 2
        row_is_valid = True
        added = []
        not_added = []
        while row_is_valid:
            codesc = ws['a' + str(row)].value
            if not codesc:
                row_is_valid = False
                continue
            vlrepasse = ws['d' + str(row)].value

            ft = PtrfFromTo()
            ft.codesc = codesc
            ft.vlrepasse = vlrepasse
            try:
                with transaction.atomic():
                    ft.save()
                added.append(ft.codesc)
            except IntegrityError:
                not_added.append(ft.codesc)

            row += 1

        sheet.added_fromtos = added
        sheet.not_added_fromtos = not_added
        sheet.extracted = True
        sheet.save()
        return added, not_added


class DistritoZonaFromToDao:
    def extract_spreadsheet(self, sheet):
        filepath = sheet.spreadsheet.path
        wb = load_workbook(filepath)
        ws = wb.worksheets[0]

        row = 2
        row_is_valid = True
        added = []
        not_added = []
        while row_is_valid:
            coddist = ws['a' + str(row)].value
            if not coddist:
                row_is_valid = False
                continue
            zona = ws['c' + str(row)].value

            ft = DistritoZonaFromTo()
            ft.coddist = coddist
            ft.zona = zona
            try:
                with transaction.atomic():
                    ft.save()
                added.append(ft.coddist)
            except IntegrityError:
                not_added.append(ft.coddist)

            row += 1

        sheet.added_fromtos = added
        sheet.not_added_fromtos = not_added
        sheet.extracted = True
        sheet.save()
        return added, not_added
