from datetime import date

from django.db import models

from budget_execution.models import MinimoLegal
from mosaico import services


class MinimoLegalSpreadsheetModel(models.Model):
    YEAR_CHOICES = [(y, y) for y in range(2011, date.today().year + 1)]

    spreadsheet = models.FileField(
        'Planilha', upload_to='mosaico/minimo_legal_spreadsheets')
    year = models.IntegerField('Ano dos dados', choices=YEAR_CHOICES)
    title_25percent = models.CharField('Título do grupo de dados - 25%',
                                       max_length=200)
    limit_25percent = models.CharField('Texto limite do grupo de dados - 25%',
                                       max_length=200)
    title_6percent = models.CharField('Título do grupo de dados - 6%',
                                      max_length=200)
    limit_6percent = models.CharField('Texto limite do grupo de dados - 6%',
                                      max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    data_extracted = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = 'Dados do Mínimo Legal (31%)'
        verbose_name_plural = 'Dados do Mínimo Legal (31%)'

    def __str__(self):
        return f'{self.spreadsheet.name.split("/")[-1]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.data_extracted:
            # self.extract_data()
            pass

    def extract_data(self):
        if self.data_extracted:
            return

        data = services.extract_minimo_legal_from_spreadsheet(self)

        for index, row in data.iterrows():
            MinimoLegal.objects.create_or_update(
                year=self.year,
                projeto_id=row['Código'],
                projeto_desc=row['Descrição'],
                orcado_atualizado=row['Dotação'],
                empenhado_liquido=row['Despesa'],
            )
        self.data_extracted = True
        self.save()
