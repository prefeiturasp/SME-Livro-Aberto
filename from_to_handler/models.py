from django.db import models


class FonteDeRecursoFromTo(models.Model):
    """ Creates groups of Fontes de Recurso """
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    group_code = models.IntegerField()
    group_name = models.CharField(max_length=100)


class SubelementoFromTo(models.Model):
    """ Adds a friendly name to Subelementos """
    code = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)
    new_code = models.IntegerField()
    new_name = models.CharField(max_length=100)
