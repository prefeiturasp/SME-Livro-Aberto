from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models


YEAR_CHOICES = [(y, y) for y in range(2011, date.today().year + 1)]


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
    added_fromtos = ArrayField(models.IntegerField(), null=True,
                               editable=False)
    not_added_fromtos = ArrayField(models.IntegerField(), null=True,
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
    year = models.IntegerField('Ano dos dados', choices=YEAR_CHOICES)

    class Meta:
        verbose_name = 'Planilha PTRF'
        verbose_name_plural = 'Planilhas PTRF'

    def extract_data(self):
        from regionalizacao.dao.models_dao import PtrfFromToDao
        dao = PtrfFromToDao()
        dao.extract_spreadsheet(self)


class PtrfFromTo(models.Model):
    year = models.IntegerField('Ano dos dados', choices=YEAR_CHOICES)
    codesc = models.IntegerField()
    vlrepasse = models.FloatField()

    class Meta:
        verbose_name = 'De-Para: PTRF'
        verbose_name_plural = 'De-Para: PTRF'

    def __str__(self):
        return f'{self.codesc} - {self.vlrepasse}'


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

    class Meta:
        verbose_name = 'De-Para: Distrito-Zona'
        verbose_name_plural = 'De-Para: Distrito-Zona'

    def __str__(self):
        return f'{self.coddist} - {self.zona}'


class EtapaTipoEscolaFromToSpreadsheet(FromToSpreadsheet):
    added_fromtos = ArrayField(models.CharField(max_length=10), null=True,
                               editable=False)
    not_added_fromtos = ArrayField(models.CharField(max_length=10), null=True,
                                   editable=False)

    class Meta:
        verbose_name = 'Planilha Etapa-TipoEscola'
        verbose_name_plural = 'Planilhas Etapa-TipoEscola'

    def extract_data(self):
        from regionalizacao.dao.models_dao import EtapaTipoEscolaFromToDao
        dao = EtapaTipoEscolaFromToDao()
        dao.extract_spreadsheet(self)


class EtapaTipoEscolaFromTo(models.Model):
    tipoesc = models.CharField(max_length=10, unique=True)
    desctipoesc = models.CharField(max_length=100)
    etapa = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'De-Para: Etapa-Tipo Escola'
        verbose_name_plural = 'De-Para: Etapa-Tipo Escola'

    def __str__(self):
        return f'{self.tipoesc} - {self.etapa}'


class UnidadeRecursosFromToSpreadsheet(FromToSpreadsheet):
    year = models.IntegerField('Ano dos dados', choices=YEAR_CHOICES)

    class Meta:
        verbose_name = 'Planilha Unidade-Recursos'
        verbose_name_plural = 'Planilhas Unidade-Recursos'

    def extract_data(self):
        from regionalizacao.dao.models_dao import UnidadeRecursosFromToDao
        dao = UnidadeRecursosFromToDao()
        dao.extract_spreadsheet(self)


class UnidadeRecursosFromTo(models.Model):
    year = models.IntegerField('Ano dos dados', choices=YEAR_CHOICES)
    codesc = models.IntegerField()
    grupo = models.CharField(max_length=30)
    subgrupo = models.CharField(max_length=30, null=True, blank=True)
    valor = models.FloatField()
    label = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'De-Para: Unidade-Recursos'
        verbose_name_plural = 'De-Para: Unidade-Recursos'

    def __str__(self):
        return f'{self.codesc} - {self.grupo} - {self.subgrupo}'
