from django.db import models


class Execucao(models.Model):
    year = models.DateField()
    orgao = models.ForeignKey('Orgao', models.PROTECT)
    projeto = models.ForeignKey('ProjetoAtividade', models.PROTECT)
    categoria = models.ForeignKey('Categoria', models.PROTECT)
    gnd = models.ForeignKey('Gnd', models.PROTECT)
    modalidade = models.ForeignKey('Modalidade', models.PROTECT)
    elemento = models.ForeignKey('Elemento', models.PROTECT)
    fonte = models.ForeignKey('FonteDeRecurso', models.PROTECT)
    subelemento = models.ForeignKey('Subelemento', models.PROTECT, null=True)
    subfuncao = models.ForeignKey('Subfuncao', models.PROTECT)
    programa = models.ForeignKey('Programa', models.PROTECT)
    orcado_atualizado = models.DecimalField(max_digits=17, decimal_places=2)
    empenhado_liquido = models.DecimalField(max_digits=17, decimal_places=2,
                                            null=True)


class Categoria(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Gnd(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Elemento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100, null=True)


class FonteDeRecurso(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Modalidade(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Orgao(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)


class Programa(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class ProjetoAtividade(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=50)


class Subelemento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Subfuncao(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
