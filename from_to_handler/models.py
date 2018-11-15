from django.db import models


class FonteDeRecursoFromTo(models.Model):
    """ Creates groups of Fontes de Recurso. """
    code = models.IntegerField()
    name = models.CharField(max_length=100)
    group_code = models.IntegerField()
    group_name = models.CharField(max_length=100)
