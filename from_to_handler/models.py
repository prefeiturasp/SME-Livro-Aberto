from django.db import models


class FonteDeRecursoFromTo(models.Model):
    """ Creates groups of Fontes de Recurso """
    code = models.IntegerField('Código')
    name = models.CharField('Nome', max_length=100)
    group_code = models.IntegerField('Código do agrupamento')
    group_name = models.CharField('Nome do agrupamento', max_length=100)

    class Meta:
        verbose_name = 'De-Para: Fontes de Recurso'
        verbose_name_plural = 'De-Para: Fontes de Recurso'

    def __str__(self):
        return (f'{self.code}: {self.name} | '
                f'{self.group_code}: {self.group_name}')


class SubelementoFromTo(models.Model):
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


class DotacaoFromTo(models.Model):
    """ Aggregates dotações in groups and subgroups """
    indexer = models.CharField('Indexador', max_length=28, unique=True)
    group_code = models.IntegerField('Código do grupo')
    group_desc = models.CharField('Descrição do grupo', max_length=100)
    subgroup_code = models.IntegerField('Código do subgrupo')
    subgroup_desc = models.CharField('Descrição do subgrupo', max_length=100)

    class Meta:
        verbose_name = 'De-Para: Dotações Subgrupos Grupos'
        verbose_name_plural = 'De-Para: Dotações Subgrupos Grupos'

    def __str__(self):
        return (f'{self.indexer} - {self.group_code}.{self.subgroup_code} - '
                f'{self.subgroup_desc} ({self.group_desc})')


class GNDFromTo(models.Model):
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


class Deflator(models.Model):
    """ Applies the inflation correction to the values """
    year = models.DateField('Ano')
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
