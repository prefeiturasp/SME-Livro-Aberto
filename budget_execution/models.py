import math

from datetime import date
from decimal import Decimal

from django.db import models
from django.urls import reverse_lazy


class ExecucaoManager(models.Manager):

    def get_or_create_by_orcamento(self, orcamento):
        """
        If there's more than one existing execucao with the same
        'year.orgao.projeto.categoria.gnd.modalidade.elemento.fonte' it's
        because there are subelementos. The orcado_atualizado is the same
        for all execucoes in this case.
        """
        execucoes = self.filter_by_indexer(orcamento.indexer)
        if not execucoes:
            execucao = self.create_by_orcamento(orcamento)
        else:
            for execucao in execucoes:
                execucao.orcado_atualizado += Decimal(
                    filter_nan(orcamento.vl_orcado_atualizado))
                execucao.save()

        return execucao

    def create_by_orcamento(self, orcamento):
        execucao = self.model()

        execucao.year = date(orcamento.cd_ano_execucao, 1, 1)
        execucao.orgao = Orgao.objects.get_or_create(
            id=orcamento.cd_orgao,
            defaults={"desc": orcamento.ds_orgao,
                      "initials": orcamento.sg_orgao},
        )[0]
        execucao.projeto = ProjetoAtividade.objects.get_or_create(
            id=orcamento.cd_projeto_atividade,
            defaults={"desc": orcamento.ds_projeto_atividade,
                      "type": orcamento.tp_projeto_atividade},
        )[0]
        execucao.categoria = Categoria.objects.get_or_create(
            id=orcamento.ds_categoria_despesa,
            defaults={"desc": orcamento.ds_categoria},
        )[0]
        execucao.gnd = Gnd.objects.get_or_create(
            id=orcamento.cd_grupo_despesa,
            defaults={"desc": orcamento.ds_grupo_despesa}
        )[0]
        execucao.modalidade = Modalidade.objects.get_or_create(
            id=orcamento.cd_modalidade,
            defaults={"desc": orcamento.ds_modalidade}
        )[0]
        execucao.elemento = Elemento.objects.get_or_create(
            id=orcamento.cd_elemento,
            # elemento.desc is populated by Empenho
        )[0]
        execucao.fonte = FonteDeRecurso.objects.get_or_create(
            id=orcamento.cd_fonte,
            defaults={"desc": orcamento.ds_fonte}
        )[0]
        execucao.subfuncao = Subfuncao.objects.get_or_create(
            id=orcamento.cd_subfuncao,
            defaults={"desc": orcamento.ds_subfuncao}
        )[0]
        execucao.programa = Programa.objects.get_or_create(
            id=orcamento.cd_programa,
            defaults={"desc": orcamento.ds_programa}
        )[0]

        execucao.orcado_atualizado = filter_nan(orcamento.vl_orcado_atualizado)

        execucao.save()

        return execucao

    def update_by_empenho(self, empenho):
        execucoes = self.filter_by_indexer(empenho.indexer)

        try:
            execucao = execucoes.get(subelemento_id=empenho.cd_subelemento)
            execucao.empenhado_liquido += Decimal(
                filter_nan(empenho.vl_empenho_liquido))
            execucao.save()
        except Execucao.DoesNotExist:
            execucao_without_subelemento = execucoes.filter(
                subelemento__isnull=True).first()

            if execucao_without_subelemento:
                execucao = self.update_with_new_subelemento_by_empenho(
                    execucao_without_subelemento, empenho)
            else:
                # creating new execucao based on an existing one with
                # same indexer
                base_execucao = execucoes.order_by("-orcado_atualizado").first()
                execucao = self.create_by_existing_one_and_empenho(
                    base_execucao, empenho)

        return execucao

    def update_with_new_subelemento_by_empenho(self, execucao, empenho):
        execucao.subelemento = Subelemento.objects.get_or_create(
            id=empenho.cd_subelemento,
            defaults={"desc": empenho.dc_subelemento}
        )[0]
        execucao.empenhado_liquido = filter_nan(
            empenho.vl_empenho_liquido)
        execucao.save()

        execucao.elemento.desc = empenho.dc_elemento
        execucao.elemento.save()

        return execucao

    def create_by_existing_one_and_empenho(self, execucao, empenho):
        if not execucao:
            return None

        execucao.id = None
        execucao.orcado_atualizado = 0
        execucao.subelemento = Subelemento.objects.get_or_create(
            id=empenho.cd_subelemento,
            defaults={"desc": empenho.dc_subelemento}
        )[0]
        execucao.empenhado_liquido = filter_nan(
            empenho.vl_empenho_liquido)
        execucao.save()

        return execucao

    def create_by_minimo_legal(self, minimo_legal):
        orcamento = Orcamento.objects.filter(
            cd_ano_execucao=minimo_legal.year.year,
            cd_projeto_atividade=minimo_legal.projeto_id).first()

        if not orcamento:
            return

        execucao = self.create_by_orcamento(orcamento)
        execucao.orcado_atualizado = filter_nan(minimo_legal.orcado_atualizado)

        empenhado = filter_nan(minimo_legal.empenhado_liquido)
        if empenhado:
            execucao.empenhado_liquido = empenhado
        else:
            # filter_nan returns 0, but we want it saved as None
            execucao.empenhado_liquido = None

        execucao.is_minimo_legal = True
        execucao.save()

        execucao.projeto.desc = minimo_legal.projeto_desc
        execucao.projeto.save()

        orcamento.execucao = execucao
        orcamento.save()

        return execucao

    def get_by_indexer(self, indexer):
        info = map(int, indexer.split('.'))
        info = list(info)

        return self.get_queryset().get(
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

        return self.get_queryset().filter(
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

        return self.get_queryset().filter(
                categoria_id=info[0],
                gnd_id=info[1],
                modalidade_id=info[2],
                elemento_id=info[3],
                subelemento_id=info[4])

    def get_date_updated(self):
        last_execucao = self.get_queryset().order_by('-dt_updated') \
            .first()
        if last_execucao:
            return last_execucao.dt_updated.strftime('%d/%m/%Y')
        else:
            return None


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
    # used to differ execucoes from SME and execucoes from Minimo Legal
    is_minimo_legal = models.BooleanField(default=False)

    # FROM-TO Fields
    subgrupo = models.ForeignKey('Subgrupo', models.SET_NULL, null=True)
    fonte_grupo = models.ForeignKey('FonteDeRecursoGrupo', models.SET_NULL,
                                    null=True)
    gnd_geologia = models.ForeignKey('GndGeologia', models.SET_NULL, null=True)
    subelemento_friendly = models.ForeignKey(
        'SubelementoFriendly', models.SET_NULL, null=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(db_index=True, auto_now=True)

    objects = ExecucaoManager()

    class Meta:
        unique_together = (
            'year', 'orgao', 'projeto', 'categoria', 'gnd', 'modalidade',
            'elemento', 'fonte', 'subelemento')
        index_together = [
            'year', 'orgao', 'projeto', 'categoria', 'gnd', 'modalidade',
            'elemento', 'fonte']

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
    desc = models.TextField()


class Gnd(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()


class Elemento(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField(null=True)


class FonteDeRecurso(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()


class Modalidade(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()


class Orgao(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()
    initials = models.TextField()


class Programa(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()


class ProjetoAtividade(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()
    type = models.TextField()


class Subelemento(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()


class Subfuncao(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()


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
    id = models.IntegerField(primary_key=True)
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
    vl_orcado_inicial = models.FloatField(blank=True, null=True)
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
    dt_data_loaded = models.DateTimeField(auto_now_add=True)
    # fk is filled when the routine that generates the Execucao objects
    # is runned.
    execucao = models.ForeignKey('Execucao', models.SET_NULL, blank=True,
                                 null=True)

    class Meta:
        db_table = 'orcamento'
        index_together = ['cd_ano_execucao', 'cd_projeto_atividade']

    @property
    def indexer(self):
        s = self
        return (
            f'{s.cd_ano_execucao}.{s.cd_orgao}.{s.cd_projeto_atividade}.'
            f'{s.ds_categoria_despesa}.{s.cd_grupo_despesa}.{s.cd_modalidade}.'
            f'{s.cd_elemento}.{s.cd_fonte}')


class Empenho(models.Model):
    """SME dw_empenhos table replica"""
    id = models.IntegerField(primary_key=True)
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
    vl_pago_restos = models.FloatField(blank=True, null=True)
    vl_empenhado = models.FloatField(blank=True, null=True)
    dt_data_loaded = models.DateTimeField(auto_now_add=True)
    # fk is filled when the routine that generates the Execucao objects
    # is runned.
    execucao = models.ForeignKey('Execucao', models.SET_NULL, blank=True,
                                 null=True)

    class Meta:
        db_table = 'empenhos'

    @property
    def indexer(self):
        s = self
        return (
            f'{s.an_empenho}.{s.cd_orgao}.{s.cd_projeto_atividade}.'
            f'{s.cd_categoria}.{s.cd_grupo}.{s.cd_modalidade}.'
            f'{s.cd_elemento}.{s.cd_fonte_de_recurso}.{s.cd_subelemento}')


class OrcamentoRaw(models.Model):
    """SME raw_orcamento table replica"""
    id = models.IntegerField(primary_key=True)
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
    vl_orcado_inicial = models.FloatField(blank=True, null=True)
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
    dt_data_loaded = models.DateTimeField(auto_now_add=True)
    execucao_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'orcamento_raw_load'
        index_together = ['cd_ano_execucao', 'cd_projeto_atividade']

    @property
    def indexer(self):
        s = self
        return (
            f'{s.cd_ano_execucao}.{s.cd_orgao}.{s.cd_projeto_atividade}.'
            f'{s.ds_categoria_despesa}.{s.cd_grupo_despesa}.{s.cd_modalidade}.'
            f'{s.cd_elemento}.{s.cd_fonte}')


class EmpenhoRaw(models.Model):
    """SME raw_empenhos table replica"""
    id = models.IntegerField(primary_key=True)
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
    vl_pago_restos = models.FloatField(blank=True, null=True)
    vl_empenhado = models.FloatField(blank=True, null=True)
    dt_data_loaded = models.DateTimeField(auto_now_add=True)
    execucao_id = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'empenhos_raw_load'

    @property
    def indexer(self):
        s = self
        return (
            f'{s.an_empenho}.{s.cd_orgao}.{s.cd_projeto_atividade}.'
            f'{s.cd_categoria}.{s.cd_grupo}.{s.cd_modalidade}.'
            f'{s.cd_elemento}.{s.cd_fonte_de_recurso}.{s.cd_subelemento}')


class MinimoLegalManager(models.Manager):

    def create_or_update(self, year, projeto_id, projeto_desc,
                         orcado_atualizado, empenhado_liquido):
        ml, created = self.get_or_create(
            projeto_id=projeto_id,
            year=date(year, 1, 1),
            defaults={
                'projeto_desc': projeto_desc,
                'orcado_atualizado': orcado_atualizado,
                'empenhado_liquido': empenhado_liquido,
            })

        if not created:
            ml.orcado_atualizado += Decimal(orcado_atualizado)
            ml.empenhado_liquido += Decimal(empenhado_liquido)
            ml.save()

        return ml


class MinimoLegal(models.Model):
    year = models.DateField()
    projeto_id = models.IntegerField()
    projeto_desc = models.CharField(max_length=250)
    orcado_atualizado = models.DecimalField(max_digits=17, decimal_places=2)
    empenhado_liquido = models.DecimalField(max_digits=17, decimal_places=2)
    execucao = models.ForeignKey('Execucao', models.SET_NULL, blank=True,
                                 null=True)

    objects = MinimoLegalManager()

    class Meta:
        unique_together = ('year', 'projeto_id')


# TODO: add test for the NaN verification
def filter_nan(value):
    if (type(value) == float or type(value) == Decimal) and math.isnan(value):
        return 0
    else:
        return value
