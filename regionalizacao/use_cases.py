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

    def execute(self, **filters):
        workbook = self.data_handler.Workbook(write_only=True)

        escolas_qs = self.info_dao.filter(**filters)
        serializer = self.info_serializer_class(escolas_qs, many=True)
        data = serializer.data

        year, rede = self._create_unidades_sheet(workbook, data)
        self._create_recursos_sheet(workbook, year)

        filename = f'regionalizacao_{year}_{rede}.xlsx'
        filepath = os.path.join(GENERATED_XLSX_PATH, filename)
        workbook.save(filepath)

        print(f'Spreadsheet generated: {filepath}')

    def _create_unidades_sheet(self, workbook, data):
        sheet = workbook.create_sheet(index=0, title='unidades')

        escola1 = data[0]
        year = escola1['ano']
        rede = 'diretas' if escola1['rede'] == 'DIR' else 'contradas'

        fields_list = list(escola1.keys())
        sheet.append(fields_list)

        for escola in data:
            sheet.append(list(escola.values()))
        return year, rede

    def _create_recursos_sheet(self, workbook, year):
        sheet = workbook.create_sheet(index=1, title='recursos')

        recursos_qs = self.recursos_dao.filter(year=year)
        serializer = self.recursos_serializer_class(recursos_qs, many=True)
        data = serializer.data

        recurso1 = data[0]
        fields_list = list(recurso1.keys())
        sheet.append(fields_list)

        for recurso in data:
            sheet.append(list(recurso.values()))
