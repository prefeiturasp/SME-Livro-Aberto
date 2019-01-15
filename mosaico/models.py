from django.db import models


class MinimoLegalSpreadsheetModel(models.Model):
    spreadsheet = models.FileField(
        'Planilha', upload_to='mosaico/minimo_legal_spreadsheets')
    title_25percent = models.CharField('Título do grupo de dados - 25%',
                                       max_length=200)
    limit_25percent = models.CharField('Texto limite do grupo de dados - 25%',
                                       max_length=200)
    title_6percent = models.CharField('Título do grupo de dados - 6%',
                                      max_length=200)
    limit_6percent = models.CharField('Texto limite do grupo de dados - 6%',
                                      max_length=200)

    class Meta:
        verbose_name = 'Dados do Mínimo Legal (31%)'
        verbose_name_plural = 'Dados do Mínimo Legal (31%)'

    def __str__(self):
        return f'{self.spreadsheet.name.split("/")[2]}'
