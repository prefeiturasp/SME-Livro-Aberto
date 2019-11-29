from collections import namedtuple

from django.db import IntegrityError, transaction
from openpyxl import load_workbook

from regionalizacao.models import (
    DistritoZonaFromTo,
    EtapaTipoEscolaFromTo,
    PtrfFromTo,
    UnidadeRecursosFromTo,
    Dre,
    TipoEscola,
    Distrito,
    Escola,
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

    def get_all(self):
        return self.model.objects.all().order_by('coddist')


class EtapaTipoEscolaFromToDao(FromToDao):

    def __init__(self):
        self.model = EtapaTipoEscolaFromTo
        self.sheet_columns = [
            SheetColumn('tipoesc', 'a'),
            SheetColumn('desctipoesc', 'b'),
            SheetColumn('etapa', 'c'),
        ]

    def get_all(self):
        return self.model.objects.all().order_by('tipoesc')


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


# TODO: add unit tests
class TipoEscolaDao:

    def __init__(self):
        self.model = TipoEscola

    def get(self, code):
        try:
            return self.model.objects.get(code=code)
        except self.model.DoesNotExist:
            return None

    def get_or_create(self, code):
        return self.model.objects.get_or_create(code=code)


# TODO: add unit tests
class DistritoDao:

    def __init__(self):
        self.model = Distrito

    def get(self, coddist):
        try:
            return self.model.objects.get(coddist=coddist)
        except self.model.DoesNotExist:
            return None

    def get_or_create(self, coddist, name):
        return self.model.objects.get_or_create(
            coddist=coddist, defaults={'name': name})


# TODO: add unit tests
class EscolaDao:

    def __init__(self):
        self.model = Escola
        self.dres_dao = DreDao()
        self.tipos_dao = TipoEscolaDao()
        self.distritos_dao = DistritoDao()

    def update_or_create(self, **kwargs):
        dre, _ = self.dres_dao.update_or_create(
            code=kwargs['dre'], name=kwargs['diretoria'])
        tipo, _ = self.tipos_dao.get_or_create(code=kwargs['tipoesc'])
        distrito, _ = self.distritos_dao.get_or_create(
            coddist=kwargs['coddist'], name=kwargs['distrito'])

        escola_data = dict(
            dre=dre,
            tipoesc=tipo,
            distrito=distrito,
            codesc=kwargs['codesc'],
            nomesc=kwargs['nomesc'],
            endereco=kwargs['endereco'],
            numero=kwargs['numero'],
            bairro=kwargs['bairro'],
            cep=kwargs['cep'],
            rede=kwargs['rede'],
            latitude=kwargs['latitude'],
            longitude=kwargs['longitude'],
            total_vagas=kwargs['total_vagas'],
        )

        try:
            with transaction.atomic():
                escola = self.create(**escola_data)
            created = True
        except IntegrityError:
            escola = self.update(**escola_data)
            created = False

        return escola, created

    def create(self, **data):
        return self.model.objects.create(**data)

    def update(self, **data):
        codesc = data.pop('codesc')
        escola = self.model.objects.get(codesc=codesc)

        for field_name, value in data.items():
            setattr(escola, field_name, value)
        escola.save()
        return escola
