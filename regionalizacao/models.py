from django.contrib.postgres.fields import ArrayField
from django.db import models


class Escola(models.Model):
    codesc = models.IntegerField(unique=True)
    nomesc = models.CharField(max_length=120)
    endereco = models.CharField(max_length=200)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cep = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    total_vagas = models.IntegerField()


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

    def save(self, *args, **kwargs):
        super().save(*args, *kwargs)
        if not self.extracted:
            self.extract_data()

    def extract_data(self):
        return NotImplemented


class PtrfFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha PTRF'
        verbose_name_plural = 'Planilhas PTRF'

    def extract_data(self):
        from regionalizacao.dao.models_dao import PtrfFromToDao
        dao = PtrfFromToDao()
        dao.extract_spreadsheet(self)


class PtrfFromTo(models.Model):
    codesc = models.IntegerField(unique=True)
    vlrepasse = models.FloatField()


class DistritoZonaFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Distrito-Zona'
        verbose_name_plural = 'Planilhas Distrito-Zona'

    def extract_data(self):
        from regionalizacao.dao.models_dao import DistritoZonaFromToDao
        dao = DistritoZonaFromToDao()
        dao.extract_spreadsheet(self)


class DistritoZonaFromTo(models.Model):
    coddist = models.IntegerField(unique=True)
    zona = models.CharField(max_length=10)


class EtapaTipoEscolaFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Etapa-TipoEscola'
        verbose_name_plural = 'Planilhas Etapa-TipoEscola'


class EtapaTipoEscolaFromTo(models.Model):
    tipoesc = models.CharField(max_length=10)
    desctipoesc = models.CharField(max_length=100)
    etapa = models.CharField(max_length=20)


class UnidadeRecursosFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Unidade-Recursos'
        verbose_name_plural = 'Planilhas Unidade-Recursos'


class UnidadeRecursosFromTo(models.Model):
    codesc = models.IntegerField(unique=True)
    grupo = models.CharField(max_length=30)
    subgrupo = models.CharField(max_length=30, null=True, blank=True)
    valor = models.IntegerField()
    label = models.CharField(max_length=20)
