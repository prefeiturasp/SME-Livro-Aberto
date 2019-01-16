from django.db import models

from budget_execution.models import (
    Execucao, FonteDeRecursoGrupo, Grupo, GndGeologia, SubelementoFriendly,
    Subgrupo)


class FromTo:

    @classmethod
    def apply_all(cls):
        fts = cls.objects.all()

        for fromto in fts:
            fromto.apply()


class FonteDeRecursoFromTo(models.Model, FromTo):
    """ Creates grupos of Fontes de Recurso """
    code = models.IntegerField('Código', unique=True)
    name = models.CharField('Nome', max_length=100)
    grupo_code = models.IntegerField('Código do agrupamento')
    grupo_name = models.CharField('Nome do agrupamento', max_length=100)

    class Meta:
        verbose_name = 'De-Para: Fontes de Recurso'
        verbose_name_plural = 'De-Para: Fontes de Recurso'

    def __str__(self):
        return (f'{self.code}: {self.name} | '
                f'{self.grupo_code}: {self.grupo_name}')

    def apply(self):
        execucoes = Execucao.objects.filter(fonte_id=self.code)
        if not execucoes:
            return

        fonte_grupo, _ = FonteDeRecursoGrupo.objects.get_or_create(
            id=self.grupo_code, defaults={'desc': self.grupo_name})

        for ex in execucoes:
            ex.fonte_grupo = fonte_grupo
            ex.save()


class SubelementoFromTo(models.Model, FromTo):
    """ Adds a friendly name to Subelementos """
    code = models.CharField('Código', max_length=28)
    desc = models.CharField('Descrição', max_length=100, blank=True, null=True)
    new_code = models.IntegerField('Código novo')
    new_name = models.CharField('Nome novo', max_length=100)

    class Meta:
        verbose_name = 'De-Para: Sub-elementos'
        verbose_name_plural = 'De-Para: Sub-elementos'

    def __str__(self):
        return (f'{self.code}: {self.desc} | '
                f'{self.new_code}: {self.new_name}')

    def apply(self):
        execucoes = Execucao.objects.filter_by_subelemento_fromto_code(
            self.code)
        if not execucoes:
            return

        subel_friendly, _ = SubelementoFriendly.objects.get_or_create(
            id=self.new_code, defaults={'desc': self.new_name})

        for ex in execucoes:
            ex.subelemento_friendly = subel_friendly
            ex.save()


class DotacaoFromTo(models.Model, FromTo):
    """ Aggregates dotações in grupos and subgrupos """
    indexer = models.CharField('Indexador', max_length=28, unique=True)
    grupo_code = models.IntegerField('Código do grupo')
    grupo_desc = models.CharField('Descrição do grupo', max_length=100)
    subgrupo_code = models.IntegerField('Código do subgrupo')
    subgrupo_desc = models.CharField('Descrição do subgrupo', max_length=100)

    class Meta:
        verbose_name = 'De-Para: Dotações Subgrupos Grupos'
        verbose_name_plural = 'De-Para: Dotações Subgrupos Grupos'

    def __str__(self):
        return (f'{self.indexer} - {self.grupo_code}.{self.subgrupo_code} - '
                f'{self.subgrupo_desc} ({self.grupo_desc})')

    def apply(self):
        execucoes = Execucao.objects.filter_by_indexer(self.indexer)
        if not execucoes:
            return

        grupo, _ = Grupo.objects.get_or_create(
            id=self.grupo_code, defaults={'desc': self.grupo_desc})
        subgrupo, _ = Subgrupo.objects.get_or_create(
            code=self.subgrupo_code, grupo=grupo,
            defaults={'desc': self.subgrupo_desc})

        for ex in execucoes:
            ex.subgrupo = subgrupo
            ex.save()


class GNDFromTo(models.Model, FromTo):
    """
    Adds a new name to Grupo de Natureza de Despesa based on the original name
    and the Elemento de Despesa
    """
    gnd_code = models.IntegerField('Código do GND')
    gnd_desc = models.CharField('Descrição original do GND', max_length=100)
    elemento_code = models.IntegerField('Código do Elemento de Despesa')
    elemento_desc = models.CharField('Descrição do Elemento de Despesa',
                                     max_length=100)
    new_gnd_code = models.IntegerField('Novo código do GND')
    new_gnd_desc = models.CharField('Nova descrição do GND',
                                    max_length=100)

    class Meta:
        verbose_name = 'De-Para: Grupos de Despesa e Elementos (GND)'
        verbose_name_plural = 'De-Para: Grupos de Despesa e Elementos (GND)'

    def __str__(self):
        return (f'{self.gnd_code}: {self.gnd_desc} - '
                f'{self.elemento_code}: {self.elemento_desc} | '
                f'{self.new_gnd_code}: {self.gnd_desc}')

    def apply(self):
        execucoes = Execucao.objects.filter(
            gnd_id=self.gnd_code, elemento_id=self.elemento_code)
        if not execucoes:
            return

        gnd_geologia, _ = GndGeologia.objects.get_or_create(
            id=self.new_gnd_code, defaults={'desc': self.new_gnd_desc})

        for ex in execucoes:
            ex.gnd_geologia = gnd_geologia
            ex.save()


class Deflator(models.Model):
    """ Applies the inflation correction to the values """
    year = models.DateField('Ano', unique=True)
    index_number = models.DecimalField('Número índice',
                                       max_digits=4, decimal_places=3,
                                       help_text='Set de 2018 = 1')
    variation_percent = models.DecimalField('Var %', max_digits=5,
                                            decimal_places=2)

    class Meta:
        verbose_name = 'Deflator'
        verbose_name_plural = 'Deflator'

    def __str__(self):
        return (f'{self.year.strftime("%Y")}: {self.index_number} - '
                f'{self.variation_percent}%')
