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
    # contrato fields
    codContrato = models.IntegerField(blank=True, null=True)
    anoExercicio = models.IntegerField(blank=True, null=True)
    # empenho fields
    anoEmpenho = models.IntegerField(blank=True, null=True)
    codCategoria = models.IntegerField(blank=True, null=True)
    txtCategoriaEconomica = models.CharField(blank=True, max_length=250,
                                             null=True)
    codElemento = models.IntegerField(blank=True, null=True)
    codEmpenho = models.IntegerField(blank=True, null=True)
    codEmpresa = models.IntegerField(blank=True, null=True)
    codFonteRecurso = models.IntegerField(blank=True, null=True)
    codFuncao = models.IntegerField(blank=True, null=True)
    codGrupo = models.IntegerField(blank=True, null=True)
    txtGrupoDespesa = models.CharField(blank=True, max_length=250, null=True)
    codItemDespesa = models.IntegerField(blank=True, null=True)
    codModalidade = models.IntegerField(blank=True, null=True)
    txtModalidadeAplicacao = models.CharField(blank=True, max_length=250,
                                              null=True)
    codOrgao = models.IntegerField(blank=True, null=True)
    codProcesso = models.IntegerField(blank=True, null=True)
    codPrograma = models.IntegerField(blank=True, null=True)
    codProjetoAtividade = models.IntegerField(blank=True, null=True)
    codSubElemento = models.IntegerField(blank=True, null=True)
    codSubFuncao = models.IntegerField(blank=True, null=True)
    codUnidade = models.IntegerField(blank=True, null=True)
    datEmpenho = models.CharField(blank=True, max_length=15, null=True)
    mesEmpenho = models.IntegerField(blank=True, null=True)
    nomEmpresa = models.CharField(blank=True, max_length=250, null=True)
    numCpfCnpj = models.CharField(blank=True, max_length=14, null=True)
    numReserva = models.IntegerField(blank=True, null=True)
    txtDescricaoOrgao = models.CharField(blank=True, max_length=150,
                                         null=True)
    txtDescricaoUnidade = models.CharField(blank=True, max_length=200,
                                           null=True)
    txtDescricaoElemento = models.CharField(blank=True, max_length=200,
                                            null=True)
    txtDescricaoFonteRecurso = models.CharField(blank=True, max_length=150,
                                                null=True)
    txtDescricaoFuncao = models.CharField(blank=True, max_length=150,
                                          null=True)
    txtDescricaoItemDespesa = models.CharField(blank=True, max_length=150,
                                               null=True)
    txtDescricaoPrograma = models.CharField(blank=True, max_length=150,
                                            null=True)
    txtDescricaoProjetoAtividade = models.CharField(blank=True, max_length=150,
                                                    null=True)
    txtRazaoSocial = models.CharField(blank=True, max_length=200, null=True)
    txtDescricaoSubElemento = models.CharField(blank=True, max_length=150,
                                               null=True)
    txtDescricaoSubFuncao = models.CharField(blank=True, max_length=150,
                                             null=True)
    valAnuladoEmpenho = models.FloatField(blank=True, null=True)
    valEmpenhadoLiquido = models.FloatField(blank=True, null=True)
    valLiquidado = models.FloatField(blank=True, null=True)
    valPagoExercicio = models.FloatField(blank=True, null=True)
    valPagoRestos = models.FloatField(blank=True, null=True)
    valTotalEmpenhado = models.FloatField(blank=True, null=True)
