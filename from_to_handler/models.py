from django.db import models


class FonteDeRecursoFromTo(models.Model):
    """ Creates groups of Fontes de Recurso """
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    group_code = models.IntegerField()
    group_name = models.CharField(max_length=100)


class SubelementoFromTo(models.Model):
    """ Adds a friendly name to Subelementos """
    code = models.CharField(max_length=28)
    description = models.CharField(max_length=100, blank=True, null=True)
    new_code = models.IntegerField()
    new_name = models.CharField(max_length=100)


class DotacaoFromTo(models.Model):
    """ Aggregates dotações in groups and subgroups """
    indexer = models.CharField(max_length=28)
    group_code = models.IntegerField()
    group_description = models.CharField(max_length=100)
    subgroup_code = models.IntegerField()
    subgroup_description = models.CharField(max_length=100)


class GNDFromTo(models.Model):
    """
    Adds a new name to Grupo de Natureza de Despesa based on the original name
    and the Elemento de Despesa
    """
    gnd_code = models.IntegerField()
    gnd_description = models.CharField(max_length=100)
    elemento_code = models.IntegerField()
    elemento_description = models.CharField(max_length=100)
    new_gnd_code = models.IntegerField()
    new_gnd_description = models.CharField(max_length=100)
