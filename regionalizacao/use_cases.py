import os

from regionalizacao.constants import GENERATED_XLSX_PATH


class GenerateXlsxFilesUseCase:

    def __init__(self, dao, serializer_class, data_handler):
        self.info_dao = dao
        self.serializer_class = serializer_class
        self.data_handler = data_handler

    def execute(self, **filters):
        escolas_qs = self.info_dao.filter(**filters)
        serializer = self.serializer_class(escolas_qs, many=True)
        data = serializer.data

        escola1 = data[0]
        year = escola1['ano']
        rede = 'diretas' if escola1['rede'] == 'DIR' else 'contradas'

        filename = f'regionalizacao_{year}_{rede}.xlsx'
        filepath = os.path.join(GENERATED_XLSX_PATH, filename)
        workbook = self.data_handler.Workbook(write_only=True)
        sheet = workbook.create_sheet(index=0, title='unidades')

        fields_list = list(escola1.keys())
        sheet.append(fields_list)

        for escola in data:
            sheet.append(list(escola.values()))
        workbook.save(filepath)

        print(f'Spreadsheet generated: {filepath}')
