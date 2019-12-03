from datetime import date

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Escola(models.Model):
    codesc = models.CharField(max_length=7, unique=True)


class EscolaInfo(models.Model):
    REDES = (
        ('DIR', 'Rede direta SME'),
        ('CON', 'Rede parceira contratada'),
    )

    escola = models.ForeignKey('Escola', on_delete=models.CASCADE,
                               related_name='infos')
    year = models.PositiveSmallIntegerField(default=date.today().year)
    dre = models.ForeignKey('Dre', on_delete=models.PROTECT)
    tipoesc = models.ForeignKey('TipoEscola', on_delete=models.PROTECT)
    distrito = models.ForeignKey('Distrito', on_delete=models.PROTECT)
    nomesc = models.CharField(max_length=120)
    endereco = models.CharField(max_length=200)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=100)
    cep = models.IntegerField()
    rede = models.CharField(max_length=3, choices=REDES)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    total_vagas = models.IntegerField()

    class Meta:
        unique_together = ('escola', 'year')

    def __str__(self):
        return f'{self.escola.codesc}: {self.nomesc}'


class Budget(models.Model):
    escola = models.ForeignKey('Escola', on_delete=models.CASCADE,
                               related_name='budgets')
    year = models.PositiveSmallIntegerField(default=date.today().year)
    ptrf = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('escola', 'year')

    def __str__(self):
        return f'{self.year} - {self.escola.codesc}'


class Recurso(models.Model):
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE,
                               related_name='recursos')
    subgrupo = models.ForeignKey('Subgrupo', on_delete=models.CASCADE)
    cost = models.FloatField(null=True)
    label = models.CharField(max_length=150, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('budget', 'subgrupo')

    def __str__(self):
        return f'{self.subgrupo} - {self.cost}'


class Subgrupo(models.Model):
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    class Meta:
        unique_together = ('grupo', 'name')

    def __str__(self):
        return f'{self.name}'


class Grupo(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return f'{self.name}'


class Dre(models.Model):
    '''Diretoria Regional Escolar'''
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.code} - {self.name}'


class TipoEscola(models.Model):
    code = models.CharField(max_length=15, unique=True)
    desc = models.CharField(max_length=100, null=True)
    etapa = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.code}'


class Distrito(models.Model):
    coddist = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    zona = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f'{self.coddist} - {self.name}'


class FromToSpreadsheet(models.Model):
    spreadsheet = models.FileField(
        'Planilha', upload_to='regionalizacao/fromto_spreadsheets')
    created_at = models.DateTimeField(auto_now_add=True)
    extracted = models.BooleanField(default=False, editable=False)
    # fields used to store which FromTos where successfully added
    added_fromtos = ArrayField(models.CharField(max_length=10), null=True,
                               editable=False)
    updated_fromtos = ArrayField(models.CharField(max_length=10), null=True,
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
    year = models.IntegerField('Ano dos dados')

    class Meta:
        verbose_name = 'Planilha PTRF'
        verbose_name_plural = 'Planilhas PTRF'

    def extract_data(self):
        from regionalizacao.dao.models_dao import PtrfFromToDao
        dao = PtrfFromToDao()
        dao.extract_spreadsheet(self)


class DistritoZonaFromToSpreadsheet(FromToSpreadsheet):
    added_fromtos = ArrayField(models.IntegerField(), null=True,
                               editable=False)
    updated_fromtos = ArrayField(models.IntegerField(), null=True,
                                 editable=False)

    class Meta:
        verbose_name = 'Planilha Distrito-Zona'
        verbose_name_plural = 'Planilhas Distrito-Zona'

    def extract_data(self):
        from regionalizacao.dao.models_dao import DistritoZonaFromToDao
        dao = DistritoZonaFromToDao()
        dao.extract_spreadsheet(self)


class EtapaTipoEscolaFromToSpreadsheet(FromToSpreadsheet):

    class Meta:
        verbose_name = 'Planilha Etapa-TipoEscola'
        verbose_name_plural = 'Planilhas Etapa-TipoEscola'

    def extract_data(self):
        from regionalizacao.dao.models_dao import EtapaTipoEscolaFromToDao
        dao = EtapaTipoEscolaFromToDao()
        dao.extract_spreadsheet(self)


class UnidadeRecursosFromToSpreadsheet(FromToSpreadsheet):
    year = models.IntegerField('Ano dos dados')

    class Meta:
        verbose_name = 'Planilha Unidade-Recursos'
        verbose_name_plural = 'Planilhas Unidade-Recursos'

    def extract_data(self):
        from regionalizacao.dao.models_dao import UnidadeRecursosFromToDao
        dao = UnidadeRecursosFromToDao()
        dao.extract_spreadsheet(self)


class PtrfFromTo(models.Model):
    year = models.IntegerField('Ano dos dados')
    codesc = models.CharField(max_length=7)
    vlrepasse = models.FloatField()

    class Meta:
        verbose_name = 'De-Para: PTRF'
        verbose_name_plural = 'De-Para: PTRF'

    def __str__(self):
        return f'{self.codesc} - {self.vlrepasse}'


class DistritoZonaFromTo(models.Model):
    coddist = models.IntegerField(unique=True)
    zona = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'De-Para: Distrito-Zona'
        verbose_name_plural = 'De-Para: Distrito-Zona'

    def __str__(self):
        return f'{self.coddist} - {self.zona}'


class EtapaTipoEscolaFromTo(models.Model):
    tipoesc = models.CharField(max_length=10, unique=True)
    desctipoesc = models.CharField(max_length=100)
    etapa = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'De-Para: Etapa-Tipo Escola'
        verbose_name_plural = 'De-Para: Etapa-Tipo Escola'

    def __str__(self):
        return f'{self.tipoesc} - {self.etapa}'


class UnidadeRecursosFromTo(models.Model):
    year = models.IntegerField('Ano dos dados')
    codesc = models.CharField(max_length=7)
    grupo = models.CharField(max_length=30)
    subgrupo = models.CharField(max_length=30, null=True, blank=True)
    valor = models.FloatField()
    label = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'De-Para: Unidade-Recursos'
        verbose_name_plural = 'De-Para: Unidade-Recursos'

    def __str__(self):
        return f'{self.codesc} - {self.grupo} - {self.subgrupo}'
