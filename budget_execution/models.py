from django.db import models


class Categoria(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class GND(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Elemento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class FonteDeRecurso(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Modalidade(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Programa(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class ProjetoAtividade(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=255)


class Subelemento(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class Subfuncao(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)
