import os

from regionalizacao.constants import GENERATED_XLSX_PATH


class GenerateXlsxFilesUseCase:

    def __init__(self, info_dao, recursos_dao, info_serializer_class,
                 recursos_serializer_class, data_handler):
        self.info_dao = info_dao
        self.recursos_dao = recursos_dao
        self.info_serializer_class = info_serializer_class
        self.recursos_serializer_class = recursos_serializer_class
        self.data_handler = data_handler

        self.escolas_qs = self.info_dao.get_all()
        self.recursos_qs = self.recursos_dao.get_all()

    def execute(self):
        years = self.escolas_qs.values_list('year', flat=True).distinct()

        for year in years:
            print(f'Generating spreadsheet for {year}')
            self._generate_spreadsheet_for_year(year)

    def _generate_spreadsheet_for_year(self, year):
        workbook = self.data_handler.Workbook(write_only=True)

        self._create_unidades_sheet(workbook, year)
        self._create_recursos_sheet(workbook, year)

        filename = f'regionalizacao_{year}.xlsx'
        filepath = os.path.join(GENERATED_XLSX_PATH, filename)
        workbook.save(filepath)

        print(f'Spreadsheet generated: {filepath}')

    def _create_unidades_sheet(self, workbook, year):
        sheet = workbook.create_sheet(index=0, title='unidades')

        escolas_qs = self.escolas_qs.filter(year=year)
        serializer = self.info_serializer_class(escolas_qs, many=True)
        data = serializer.data

        escola1 = data[0]
        fields_list = list(escola1.keys())
        sheet.append(fields_list)

        for escola in data:
            sheet.append(list(escola.values()))

    def _create_recursos_sheet(self, workbook, year):
        sheet = workbook.create_sheet(index=1, title='recursos')

        recursos_qs = self.recursos_qs.filter(year=year)
        serializer = self.recursos_serializer_class(recursos_qs, many=True)
        data = serializer.data

        recurso1 = data[0]
        fields_list = list(recurso1.keys())
        sheet.append(fields_list)

        for recurso in data:
            sheet.append(list(recurso.values()))
