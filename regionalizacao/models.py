from django.contrib.postgres.fields import ArrayField
from django.db import models


class FromToSpreadsheet(models.Model):
    spreadsheet = models.FileField(
        'Planilha', upload_to='regionalizacao/fromto_spreadsheets')
    created_at = models.DateTimeField(auto_now_add=True)
    extracted = models.BooleanField(default=False, editable=False)
    # fields used to store which FromTos where successfully added
    added_fromtos = ArrayField(models.CharField(max_length=28), null=True,
                               editable=False)
    not_added_fromtos = ArrayField(models.CharField(max_length=28), null=True,
                                   editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.spreadsheet.name.split("/")[-1]}'


class PtrfFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha PTRF'
        verbose_name_plural = 'Planilhas PTRF'


class DistritoZonaFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Distrito-Zona'
        verbose_name_plural = 'Planilhas Distrito-Zona'


class EtapaTipoEscolaFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Etapa-TipoEscola'
        verbose_name_plural = 'Planilhas Etapa-TipoEscola'


class UnidadeRecursosFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Unidade-Recursos'
        verbose_name_plural = 'Planilhas Unidade-Recursos'
