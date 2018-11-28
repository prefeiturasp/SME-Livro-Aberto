from datetime import date

from django.db import models


class ExecucaoQuerySet(models.QuerySet):

    def get_by_indexer(self, indexer):
        info = map(int, indexer.split('.'))
        info = list(info)

        return self.get(
                year=date(info[0], 1, 1),
                orgao_id=info[1],
                projeto_id=info[2],
                categoria_id=info[3],
                gnd_id=info[4],
                modalidade_id=info[5],
                elemento_id=info[6],
                fonte_id=info[7],
                subelemento_id=info[8])

    def filter_by_indexer(self, indexer):
        """Uses indexer without subelemento_id to return a queryset of
        Execucao containing all that matches the indexer."""

        info = map(int, indexer.split('.'))
        info = list(info)

        return self.filter(
                year=date(info[0], 1, 1),
                orgao_id=info[1],
                projeto_id=info[2],
                categoria_id=info[3],
                gnd_id=info[4],
                modalidade_id=info[5],
                elemento_id=info[6],
                fonte_id=info[7])


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
    # FROM-TO Fields
    subgrupo = models.ForeignKey('Subgrupo', models.SET_NULL, null=True)

    objects = ExecucaoQuerySet.as_manager()

    class Meta:
        unique_together = (
            'year', 'orgao', 'projeto', 'categoria', 'gnd', 'modalidade',
            'elemento', 'fonte', 'subelemento')

    @property
    def indexer(self):
        s = self
        return (
            f'{s.year.strftime("%Y")}.{s.orgao_id}.{s.projeto_id}.'
            f'{s.categoria_id}.{s.gnd_id}.{s.modalidade_id}.{s.elemento_id}.'
            f'{s.fonte_id}.{s.subelemento_id}')


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


# FROM-TO Models
class Grupo(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=100)


class SubgrupoQuerySet(models.QuerySet):

    def get_by_code(self, code):
        info = map(int, code.split('.'))
        info = list(info)

        return self.get(grupo_id=info[0], _code=info[1])


class Subgrupo(models.Model):
    _code = models.IntegerField()
    grupo = models.ForeignKey("Grupo", models.CASCADE)
    description = models.CharField(max_length=100)

    objects = SubgrupoQuerySet.as_manager()

    class Meta:
        unique_together = ('_code', 'grupo')

    @property
    def code(self):
        return f'{self.grupo.id}.{self._code}'
