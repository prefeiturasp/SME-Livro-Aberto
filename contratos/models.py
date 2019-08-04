from django.contrib.postgres.fields import ArrayField
from django.db import models


class ExecucaoContrato(models.Model):
    cod_contrato = models.IntegerField()
    empenho_indexer = models.CharField(max_length=28)
    year = models.DateField()
    valor_empenhado = models.FloatField()
    valor_liquidado = models.FloatField()
    modalidade = models.ForeignKey("ContratoModalidade",
                                   on_delete=models.PROTECT)
    objeto_contrato = models.ForeignKey("ObjetoContrato",
                                        on_delete=models.PROTECT)
    fornecedor = models.ForeignKey("Fornecedor", on_delete=models.PROTECT)
    # from-to field
    categoria = models.ForeignKey("ContratoCategoria", null=True,
                                  on_delete=models.PROTECT)

    def __str__(self):
        return (f'{self.year}: {self.cod_contrato} - '
                f'{self.objeto_contrato.desc}')


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
    valaditamentos = models.FloatField(blank=True, null=True)
    valanulacao = models.FloatField(blank=True, null=True)
    valanuladoempenho = models.FloatField(blank=True, null=True)
    valempenhadoliquido = models.FloatField(blank=True, null=True)
    valliquidado = models.FloatField(blank=True, null=True)
    valpago = models.FloatField(blank=True, null=True)
    valprincipal = models.FloatField(blank=True, null=True)
    valreajustes = models.FloatField(blank=True, null=True)
    valtotalempenhado = models.FloatField(blank=True, null=True)
    data_extracao = models.DateField(blank=True, null=True)
    dt_data_loaded = models.CharField(max_length=26, blank=True, null=True)

    class Meta:
        db_table = 'contratos_raw_load'


class EmpenhoSOFCache(models.Model):
    # contrato fields
    codContrato = models.IntegerField(blank=True, null=True)
    anoExercicio = models.IntegerField(blank=True, null=True)
    codModalidadeContrato = models.IntegerField(blank=True, null=True)
    txtDescricaoModalidade = models.TextField(blank=True, null=True)
    txtObjetoContrato = models.TextField(blank=True, null=True)
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
    codProcesso = models.BigIntegerField(blank=True, null=True)
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

    @property
    def indexer(self):
        s = self
        return (
            f'{s.anoEmpenho}.{s.codOrgao}.{s.codProjetoAtividade}.'
            f'{s.codCategoria}.{s.codGrupo}.{s.codModalidade}.'
            f'{s.codElemento}.{s.codFonteRecurso}.{s.codSubElemento}'
        )


class EmpenhoSOFCacheTemp(models.Model):
    # contrato fields
    codContrato = models.IntegerField(blank=True, null=True)
    anoExercicio = models.IntegerField(blank=True, null=True)
    codModalidadeContrato = models.IntegerField(blank=True, null=True)
    txtDescricaoModalidade = models.TextField(blank=True, null=True)
    txtObjetoContrato = models.TextField(blank=True, null=True)
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
    codProcesso = models.BigIntegerField(blank=True, null=True)
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


class EmpenhoSOFFailedAPIRequest(models.Model):
    cod_contrato = models.IntegerField()
    ano_exercicio = models.IntegerField()
    ano_empenho = models.IntegerField()
    error_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=150)

    def __str__(self):
        return self.razao_social


class ObjetoContrato(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class ContratoModalidade(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()

    def __str__(self):
        return self.desc


class ContratoCategoria(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class ContratoCategoriaFromTo(models.Model):
    """
    Aggregates contratos empenhos in categories. Theese categories are the
    ones shown on frontend.
    """
    indexer = models.CharField('Indexador', max_length=28, unique=True)
    categoria_name = models.CharField('Nome da categoria', max_length=30)
    categoria_desc = models.CharField(
        'Descrição da categoria', max_length=400)

    class Meta:
        verbose_name = 'De-Para: Contratos Categorias'
        verbose_name_plural = 'De-Para: Contratos Categorias'

    def __str__(self):
        return f'{self.indexer} - {self.categoria_name}'


class ContratoCategoriaFromToSpreadsheet(models.Model):
    spreadsheet = models.FileField(
        'Planilha', upload_to='contratos/contratos_categoria_spreadsheets')
    created_at = models.DateTimeField(auto_now_add=True)
    extracted = models.BooleanField(default=False, editable=False)
    # fields used to store which FromTos where successfully added
    added_fromtos = ArrayField(models.CharField(max_length=28), null=True,
                               editable=False)
    not_added_fromtos = ArrayField(models.CharField(max_length=28), null=True,
                                   editable=False)

    class Meta:
        verbose_name = 'Planilha De-Para: Contratos Categorias'
        verbose_name_plural = 'Planilha De-Para: Contratos Categorias'

    def __str__(self):
        return f'{self.spreadsheet.name.split("/")[-1]}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.extracted:
            self.extract_data()

    def extract_data(self):
        from contratos.dao import contratos_categorias_fromto_dao

        contratos_categorias_fromto_dao.extract_spreadsheet(self)
