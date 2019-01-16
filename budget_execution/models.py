from datetime import date

from django.db import models
from django.urls import reverse_lazy


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

    def filter_by_subelemento_fromto_code(self, code):
        """Uses subelemento fromto code to return a queryset of
        Execucao containing all that matches the code."""

        info = map(int, code.split('.'))
        info = list(info)

        return self.filter(
                categoria_id=info[0],
                gnd_id=info[1],
                modalidade_id=info[2],
                elemento_id=info[3],
                subelemento_id=info[4])


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
    fonte_grupo = models.ForeignKey('FonteDeRecursoGrupo', models.SET_NULL,
                                    null=True)
    gnd_geologia = models.ForeignKey('GndGeologia', models.SET_NULL, null=True)
    subelemento_friendly = models.ForeignKey(
        'SubelementoFriendly', models.SET_NULL, null=True)

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

    def get_url(self, area):
        # simples areas
        if area == 'grupos':
            args = []
        elif area == 'subgrupos':
            args = [self.subgrupo.grupo_id]
        elif area == 'elementos':
            args = [self.subgrupo.grupo_id, self.subgrupo_id]
        elif area == 'subelementos':
            args = [self.subgrupo.grupo_id, self.subgrupo_id, self.elemento_id]

        # tecnico areas
        elif area == 'subfuncoes':
            args = []
        elif area == 'programas':
            args = [self.subfuncao_id]
        elif area == 'projetos':
            args = [self.subfuncao_id, self.programa_id]

        return reverse_lazy(f'mosaico:{area}', args=args)


class Categoria(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class Gnd(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class Elemento(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100, null=True)


class FonteDeRecurso(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class Modalidade(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class Orgao(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)
    initials = models.CharField(max_length=10)


class Programa(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class ProjetoAtividade(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=255)
    type = models.CharField(max_length=50)


class Subelemento(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class Subfuncao(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


# FROM-TO Models
class Grupo(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class SubgrupoQuerySet(models.QuerySet):

    def get_by_code(self, code):
        info = map(int, code.split('.'))
        info = list(info)

        return self.get(grupo_id=info[0], code=info[1])


class Subgrupo(models.Model):
    code = models.IntegerField()
    grupo = models.ForeignKey("Grupo", models.CASCADE)
    desc = models.CharField(max_length=100)

    objects = SubgrupoQuerySet.as_manager()

    class Meta:
        unique_together = ('code', 'grupo')

    @property
    def full_code(self):
        return f'{self.grupo.id}.{self.code}'


class FonteDeRecursoGrupo(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class GndGeologia(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)
    slug = models.CharField(max_length=20, null=True)


class SubelementoFriendly(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.CharField(max_length=100)


class Orcamento(models.Model):
    """SME dw_orcamento table replica"""
    cd_key = models.TextField(blank=True, null=True)
    dt_inicial = models.DateTimeField(blank=True, null=True)
    dt_final = models.DateTimeField(blank=True, null=True)
    cd_ano_execucao = models.BigIntegerField(blank=True, null=True)
    cd_exercicio = models.BigIntegerField(blank=True, null=True)
    nm_administracao = models.TextField(blank=True, null=True)
    cd_exercicio_empresa_id = models.BigIntegerField(blank=True, null=True)
    cd_orgao = models.BigIntegerField(blank=True, null=True)
    sg_orgao = models.TextField(blank=True, null=True)
    ds_orgao = models.TextField(blank=True, null=True)
    cd_unidade = models.BigIntegerField(blank=True, null=True)
    ds_unidade = models.TextField(blank=True, null=True)
    cd_funcao = models.BigIntegerField(blank=True, null=True)
    ds_funcao = models.TextField(blank=True, null=True)
    cd_subfuncao = models.BigIntegerField(blank=True, null=True)
    ds_subfuncao = models.TextField(blank=True, null=True)
    cd_programa = models.BigIntegerField(blank=True, null=True)
    ds_programa = models.TextField(blank=True, null=True)
    tp_projeto_atividade = models.TextField(blank=True, null=True)
    tp_papa = models.TextField(blank=True, null=True)
    cd_projeto_atividade = models.BigIntegerField(blank=True, null=True)
    ds_projeto_atividade = models.TextField(blank=True, null=True)
    cd_despesa = models.BigIntegerField(blank=True, null=True)
    ds_despesa = models.TextField(blank=True, null=True)
    ds_categoria_despesa = models.BigIntegerField(blank=True, null=True)
    ds_categoria = models.TextField(blank=True, null=True)
    cd_grupo_despesa = models.BigIntegerField(blank=True, null=True)
    ds_grupo_despesa = models.TextField(blank=True, null=True)
    cd_modalidade = models.BigIntegerField(blank=True, null=True)
    ds_modalidade = models.TextField(blank=True, null=True)
    cd_elemento = models.BigIntegerField(blank=True, null=True)
    cd_fonte = models.BigIntegerField(blank=True, null=True)
    ds_fonte = models.TextField(blank=True, null=True)
    vl_orcado_inicial = models.BigIntegerField(blank=True, null=True)
    vl_orcado_atualizado = models.FloatField(blank=True, null=True)
    vl_congelado = models.FloatField(blank=True, null=True)
    vl_orcado_disponivel = models.FloatField(blank=True, null=True)
    vl_reservado_liquido = models.FloatField(blank=True, null=True)
    vl_empenhado_liquido = models.FloatField(blank=True, null=True)
    vl_empenhado_liquido_atual = models.FloatField(blank=True, null=True)
    vl_liquidado = models.FloatField(blank=True, null=True)
    vl_liquidado_atual = models.FloatField(blank=True, null=True)
    vl_pago = models.FloatField(blank=True, null=True)
    vl_pago_atual = models.FloatField(blank=True, null=True)
    vl_saldo_empenho = models.FloatField(blank=True, null=True)
    vl_saldo_reserva = models.FloatField(blank=True, null=True)
    vl_saldo_dotacao = models.FloatField(blank=True, null=True)
    dt_extracao = models.DateTimeField(blank=True, null=True)
    dt_data_loaded = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'orcamento'


class Empenho(models.Model):
    """SME dw_orcamento table replica"""
    cd_key = models.TextField(blank=True, null=True)
    an_empenho = models.BigIntegerField(blank=True, null=True)
    cd_categoria = models.BigIntegerField(blank=True, null=True)
    cd_elemento = models.TextField(blank=True, null=True)
    cd_empenho = models.BigIntegerField(blank=True, null=True)
    cd_empresa = models.TextField(blank=True, null=True)
    cd_fonte_de_recurso = models.TextField(blank=True, null=True)
    cd_funcao = models.TextField(blank=True, null=True)
    cd_grupo = models.BigIntegerField(blank=True, null=True)
    cd_item_despesa = models.TextField(blank=True, null=True)
    cd_modalidade = models.BigIntegerField(blank=True, null=True)
    cd_orgao = models.TextField(blank=True, null=True)
    cd_programa = models.TextField(blank=True, null=True)
    cd_projeto_atividade = models.TextField(blank=True, null=True)
    cd_subelemento = models.TextField(blank=True, null=True)
    cd_subfuncao = models.TextField(blank=True, null=True)
    cd_unidade = models.TextField(blank=True, null=True)
    dt_empenho = models.DateTimeField(blank=True, null=True)
    mes_empenho = models.BigIntegerField(blank=True, null=True)
    nm_empresa = models.TextField(blank=True, null=True)
    dc_cpf_cnpj = models.TextField(blank=True, null=True)
    cd_reserva = models.BigIntegerField(blank=True, null=True)
    dc_categoria_economica = models.TextField(blank=True, null=True)
    dc_elemento = models.TextField(blank=True, null=True)
    dc_fonte_de_recurso = models.TextField(blank=True, null=True)
    dc_funcao = models.TextField(blank=True, null=True)
    dc_item_despesa = models.TextField(blank=True, null=True)
    dc_orgao = models.TextField(blank=True, null=True)
    dc_programa = models.TextField(blank=True, null=True)
    dc_projeto_atividade = models.TextField(blank=True, null=True)
    dc_subelemento = models.TextField(blank=True, null=True)
    dc_subfuncao = models.TextField(blank=True, null=True)
    dc_unidade = models.TextField(blank=True, null=True)
    dc_grupo_despesa = models.TextField(blank=True, null=True)
    dc_modalidade = models.TextField(blank=True, null=True)
    dc_razao_social = models.TextField(blank=True, null=True)
    vl_empenho_anulado = models.FloatField(blank=True, null=True)
    vl_empenho_liquido = models.FloatField(blank=True, null=True)
    vl_liquidado = models.FloatField(blank=True, null=True)
    vl_pago = models.FloatField(blank=True, null=True)
    vl_pago_restos = models.BigIntegerField(blank=True, null=True)
    vl_empenhado = models.FloatField(blank=True, null=True)
    dt_data_loaded = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'empenhos'
