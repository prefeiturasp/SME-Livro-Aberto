from django.db import models


class ContratoRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    anoexercicio = models.IntegerField(blank=True, null=True)
    codcontrato = models.IntegerField(blank=True, null=True)
    codempresa = models.IntegerField(blank=True, null=True)
    codmodalidade = models.IntegerField(blank=True, null=True)
    codorgao = models.IntegerField(blank=True, null=True)
    codprocesso = models.BigIntegerField(blank=True, null=True)
    codtipocontratacao = models.IntegerField(blank=True, null=True)
    datassinaturacontrato = models.DateField(blank=True, null=True)
    datpublicacaocontrato = models.DateField(blank=True, null=True)
    datvigencia = models.DateField(blank=True, null=True)
    numoriginalcontrato = models.CharField(max_length=20, blank=True, null=True)
    txtdescricaomodalidade = models.CharField(max_length=21, blank=True,
                                              null=True)
    txtdescricaoorgao = models.CharField(max_length=32, blank=True, null=True)
    txtobjetocontrato = models.CharField(max_length=1000, blank=True, null=True)
    txtrazaosocial = models.CharField(max_length=36, blank=True, null=True)
    txttipocontratacao = models.CharField(max_length=67, blank=True, null=True)
    valaditamentos = models.DecimalField(max_digits=9, decimal_places=2,
                                         blank=True, null=True)
    valanulacao = models.DecimalField(max_digits=10, decimal_places=2,
                                      blank=True, null=True)
    valanuladoempenho = models.DecimalField(max_digits=11, decimal_places=2,
                                            blank=True, null=True)
    valempenhadoliquido = models.DecimalField(max_digits=11, decimal_places=2,
                                              blank=True, null=True)
    valliquidado = models.DecimalField(max_digits=10, decimal_places=2,
                                       blank=True, null=True)
    valpago = models.DecimalField(max_digits=11, decimal_places=2,
                                  blank=True, null=True)
    valprincipal = models.DecimalField(max_digits=12, decimal_places=2,
                                       blank=True, null=True)
    valreajustes = models.DecimalField(max_digits=8, decimal_places=2,
                                       blank=True, null=True)
    valtotalempenhado = models.DecimalField(max_digits=11, decimal_places=2,
                                            blank=True, null=True)
    data_extracao = models.DateField(blank=True, null=True)
    dt_data_loaded = models.CharField(max_length=26, blank=True, null=True)

    class Meta:
        db_table = 'contratos_raw_load'


class EmpenhoSOFCache(models.Model):
    cod_contrato = models.IntegerField(blank=True, null=True)
    ano_empenho = models.IntegerField(blank=True, null=True)
    cod_categoria = models.IntegerField(blank=True, null=True)
    txt_categoria_economica = models.CharField(max_length=250, blank=True,
                                               null=True)
    cod_elemento = models.IntegerField(blank=True, null=True)
    cod_empenho = models.IntegerField(blank=True, null=True)
    cod_empresa = models.IntegerField(blank=True, null=True)
    cod_fonte_recurso = models.IntegerField(blank=True, null=True)
    cod_funcao = models.IntegerField(blank=True, null=True)
    cod_grupo = models.IntegerField(blank=True, null=True)
    txt_grupo_despesa = models.CharField(max_length=250, blank=True, null=True)
    cod_item_despesa = models.IntegerField(blank=True, null=True)
    cod_modalidade = models.IntegerField(blank=True, null=True)
    txt_modalidade_aplicacao = models.CharField(max_length=250, blank=True,
                                                null=True)
    cod_orgao = models.IntegerField(blank=True, null=True)
    cod_processo = models.IntegerField(blank=True, null=True)
    cod_programa = models.IntegerField(blank=True, null=True)
    cod_projeto_atividade = models.IntegerField(blank=True, null=True)
    cod_sub_elemento = models.IntegerField(blank=True, null=True)
    cod_sub_funcao = models.IntegerField(blank=True, null=True)
    cod_unidade = models.IntegerField(blank=True, null=True)
    dat_empenho = models.CharField(max_length=15, blank=True, null=True)
    mes_empenho = models.IntegerField(blank=True, null=True)
    nom_empresa = models.CharField(max_length=250, blank=True, null=True)
    num_cpf_cnpj = models.CharField(max_length=14, blank=True, null=True)
    num_teserva = models.IntegerField(blank=True, null=True)
    txt_descricao_orgao = models.CharField(max_length=150, blank=True,
                                           null=True)
    txt_descricao_unidade = models.CharField(max_length=200, blank=True,
                                             null=True)
    txt_descricao_elemento = models.CharField(max_length=200, blank=True,
                                              null=True)
    txt_descricao_fonte_recurso = models.CharField(max_length=150, blank=True,
                                                   null=True)
    txt_descricao_funcao = models.CharField(max_length=150, blank=True,
                                            null=True)
    txt_descricao_item_despesa = models.CharField(max_length=150, blank=True,
                                                  null=True)
    txt_descricao_programa = models.CharField(max_length=150, blank=True,
                                              null=True)
    txt_descricao_projeto_atividade = models.CharField(max_length=150,
                                                       blank=True, null=True)
    txt_razao_social = models.CharField(max_length=200, blank=True, null=True)
    txt_descricao_subelemento = models.CharField(max_length=150, blank=True,
                                                 null=True)
    txt_descricao_subfuncao = models.CharField(max_length=150, blank=True,
                                               null=True)
    val_anulado_empenho = models.FloatField(blank=True, null=True)
    val_empenhado_liquido = models.FloatField(blank=True, null=True)
    val_liquidado = models.FloatField(blank=True, null=True)
    val_pago_exercicio = models.FloatField(blank=True, null=True)
    val_pago_restos = models.FloatField(blank=True, null=True)
    val_total_empenhado = models.FloatField(blank=True, null=True)
