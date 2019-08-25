from django.contrib.postgres.fields import ArrayField
from django.db import models


class ExecucaoContrato(models.Model):
    cod_contrato = models.IntegerField()
    empenho_indexer = models.CharField(max_length=28)
    year = models.DateField()
    valor_empenhado = models.FloatField()
    valor_liquidado = models.FloatField()
    modalidade = models.ForeignKey("ModalidadeContrato",
                                   on_delete=models.PROTECT)
    objeto_contrato = models.ForeignKey("ObjetoContrato",
                                        on_delete=models.PROTECT)
    fornecedor = models.ForeignKey("Fornecedor", on_delete=models.PROTECT)
    # from-to field
    categoria = models.ForeignKey("CategoriaContrato", null=True,
                                  on_delete=models.PROTECT)

    def __str__(self):
        return (f'{self.year}: {self.cod_contrato} - '
                f'{self.objeto_contrato.desc}')


class ContratoRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    codContrato = models.IntegerField(
        db_column='codcontrato', blank=True, null=True)
    anoExercicioContrato = models.IntegerField(
        db_column='anoexercicio', blank=True, null=True)
    codModalidadeContrato = models.IntegerField(
        db_column='codmodalidade', blank=True, null=True)
    txtDescricaoModalidadeContrato = models.TextField(
        db_column='txtdescricaomodalidade', blank=True, null=True)
    txtObjetoContrato = models.TextField(
        db_column='txtobjetocontrato', blank=True, null=True)
    codEmpresaContrato = models.IntegerField(
        db_column='codempresa', blank=True, null=True)
    codOrgaoContrato = models.IntegerField(
        db_column='codorgao', blank=True, null=True)
    txtDescricaoOrgaoContrato = models.TextField(
        db_column='txtdescricaoorgao', blank=True, null=True)
    codProcessoContrato = models.BigIntegerField(
        db_column='codprocesso', blank=True, null=True)
    codTipoContratacaoContrato = models.IntegerField(
        db_column='codtipocontratacao', blank=True, null=True)
    txtTipoContratacaoContrato = models.TextField(
        db_column='txttipocontratacao', blank=True, null=True)
    datAssinaturaContrato = models.CharField(
        db_column='datassinaturacontrato', max_length=26, blank=True, null=True)
    datPublicacaoContrato = models.CharField(
        db_column='datpublicacaocontrato', max_length=26, blank=True, null=True)
    datVigenciaContrato = models.CharField(
        db_column='datvigencia', max_length=26, blank=True, null=True)
    numOriginalContrato = models.TextField(
        db_column='numoriginalcontrato', blank=True, null=True)
    txtRazaoSocialContrato = models.TextField(
        db_column='txtrazaosocial', blank=True, null=True)
    valAditamentosContrato = models.FloatField(
        db_column='valaditamentos', blank=True, null=True)
    valAnulacaoContrato = models.FloatField(
        db_column='valanulacao', blank=True, null=True)
    valAnuladoEmpenhoContrato = models.FloatField(
        db_column='valanuladoempenho', blank=True, null=True)
    valEmpenhadoLiquidoContrato = models.FloatField(
        db_column='valempenhadoliquido', blank=True, null=True)
    valliquidadoContrato = models.FloatField(
        db_column='valliquidado', blank=True, null=True)
    valPagoContrato = models.FloatField(
        db_column='valpago', blank=True, null=True)
    valPrincipalContrato = models.FloatField(
        db_column='valprincipal', blank=True, null=True)
    valReajustesContrato = models.FloatField(
        db_column='valreajustes', blank=True, null=True)
    valTotalEmpenhadoContrato = models.FloatField(
        db_column='valtotalempenhado', blank=True, null=True)
    dataExtracaoContrato = models.CharField(
        db_column='data_extracao', max_length=26, blank=True, null=True)
    dtDataLoadedContrato = models.CharField(
        db_column='dt_data_loaded', max_length=26, blank=True, null=True)

    class Meta:
        db_table = 'contratos_raw_load'


class EmpenhoSOFCache(models.Model):
    # contrato fields shown on interface
    codContrato = models.IntegerField(blank=True, null=True)
    anoExercicioContrato = models.IntegerField(blank=True, null=True)
    codModalidadeContrato = models.IntegerField(blank=True, null=True)
    txtDescricaoModalidadeContrato = models.TextField(blank=True, null=True)
    txtObjetoContrato = models.TextField(blank=True, null=True)
    # contrato fields not shown on interface. used only on download
    codEmpresaContrato = models.IntegerField(blank=True, null=True)
    codOrgaoContrato = models.IntegerField(blank=True, null=True)
    txtDescricaoOrgaoContrato = models.TextField(blank=True, null=True)
    codProcessoContrato = models.BigIntegerField(blank=True, null=True)
    codTipoContratacaoContrato = models.IntegerField(blank=True, null=True)
    txtTipoContratacaoContrato = models.TextField(blank=True, null=True)
    datAssinaturaContrato = models.DateField(blank=True, null=True)
    datPublicacaoContrato = models.DateField(blank=True, null=True)
    datVigenciaContrato = models.DateField(blank=True, null=True)
    numOriginalContrato = models.TextField(blank=True, null=True)
    txtRazaoSocialContrato = models.TextField(blank=True, null=True)
    valAditamentosContrato = models.FloatField(blank=True, null=True)
    valAnulacaoContrato = models.FloatField(blank=True, null=True)
    valAnuladoEmpenhoContrato = models.FloatField(blank=True, null=True)
    valEmpenhadoLiquidoContrato = models.FloatField(blank=True, null=True)
    valliquidadoContrato = models.FloatField(blank=True, null=True)
    valPagoContrato = models.FloatField(blank=True, null=True)
    valPrincipalContrato = models.FloatField(blank=True, null=True)
    valReajustesContrato = models.FloatField(blank=True, null=True)
    valTotalEmpenhadoContrato = models.FloatField(blank=True, null=True)
    dataExtracaoContrato = models.DateField(blank=True, null=True)
    dtDataLoadedContrato = models.CharField(max_length=26, blank=True,
                                            null=True)
    # empenho fields
    anoEmpenho = models.IntegerField(blank=True, null=True)
    codCategoria = models.IntegerField(blank=True, null=True)
    txtCategoriaEconomica = models.TextField(blank=True, null=True)
    codElemento = models.IntegerField(blank=True, null=True)
    codEmpenho = models.IntegerField(blank=True, null=True)
    codEmpresa = models.IntegerField(blank=True, null=True)
    codFonteRecurso = models.IntegerField(blank=True, null=True)
    codFuncao = models.IntegerField(blank=True, null=True)
    codGrupo = models.IntegerField(blank=True, null=True)
    txtGrupoDespesa = models.TextField(blank=True, null=True)
    codItemDespesa = models.IntegerField(blank=True, null=True)
    codModalidade = models.IntegerField(blank=True, null=True)
    txtModalidadeAplicacao = models.TextField(blank=True, null=True)
    codOrgao = models.IntegerField(blank=True, null=True)
    codProcesso = models.BigIntegerField(blank=True, null=True)
    codPrograma = models.IntegerField(blank=True, null=True)
    codProjetoAtividade = models.IntegerField(blank=True, null=True)
    codSubElemento = models.IntegerField(blank=True, null=True)
    codSubFuncao = models.IntegerField(blank=True, null=True)
    codUnidade = models.IntegerField(blank=True, null=True)
    datEmpenho = models.CharField(blank=True, max_length=20, null=True)
    mesEmpenho = models.IntegerField(blank=True, null=True)
    nomEmpresa = models.TextField(blank=True, null=True)
    numCpfCnpj = models.CharField(blank=True, max_length=18, null=True)
    numReserva = models.IntegerField(blank=True, null=True)
    txtDescricaoOrgao = models.TextField(blank=True, null=True)
    txtDescricaoUnidade = models.TextField(blank=True, null=True)
    txtDescricaoElemento = models.TextField(blank=True, null=True)
    txtDescricaoFonteRecurso = models.TextField(blank=True, null=True)
    txtDescricaoFuncao = models.TextField(blank=True, null=True)
    txtDescricaoItemDespesa = models.TextField(blank=True, null=True)
    txtDescricaoPrograma = models.TextField(blank=True, null=True)
    txtDescricaoProjetoAtividade = models.TextField(blank=True, null=True)
    txtRazaoSocial = models.TextField(blank=True, null=True)
    txtDescricaoSubElemento = models.TextField(blank=True, null=True)
    txtDescricaoSubFuncao = models.TextField(blank=True, null=True)
    valAnuladoEmpenho = models.FloatField(blank=True, null=True)
    valEmpenhadoLiquido = models.FloatField(blank=True, null=True)
    valLiquidado = models.FloatField(blank=True, null=True)
    valPagoExercicio = models.FloatField(blank=True, null=True)
    valPagoRestos = models.FloatField(blank=True, null=True)
    valTotalEmpenhado = models.FloatField(blank=True, null=True)

    @property
    def indexer(self):
        cod_modalidade = str(self.codModalidade)
        if len(cod_modalidade) < 2:
            cod_modalidade = '0' + cod_modalidade

        cod_elemento = str(self.codElemento)
        if len(cod_elemento) < 2:
            cod_elemento = '0' + cod_elemento

        cod_fonte = str(self.codFonteRecurso)
        if len(cod_fonte) < 2:
            cod_fonte = '0' + cod_fonte

        s = self
        return (
            f'{s.anoEmpenho}.{s.codOrgao}.{s.codProjetoAtividade}.'
            f'{s.codCategoria}.{s.codGrupo}.{cod_modalidade}.'
            f'{cod_elemento}.{cod_fonte}.{s.codSubElemento}'
        )


class EmpenhoSOFCacheTemp(models.Model):
    # contrato fields
    codContrato = models.IntegerField(blank=True, null=True)
    anoExercicioContrato = models.IntegerField(blank=True, null=True)
    codModalidadeContrato = models.IntegerField(blank=True, null=True)
    txtDescricaoModalidadeContrato = models.TextField(blank=True, null=True)
    txtObjetoContrato = models.TextField(blank=True, null=True)
    # contrato fields not shown on interface. used only on download
    codEmpresaContrato = models.IntegerField(blank=True, null=True)
    codOrgaoContrato = models.IntegerField(blank=True, null=True)
    txtDescricaoOrgaoContrato = models.TextField(blank=True, null=True)
    codProcessoContrato = models.BigIntegerField(blank=True, null=True)
    codTipoContratacaoContrato = models.IntegerField(blank=True, null=True)
    txtTipoContratacaoContrato = models.TextField(blank=True, null=True)
    datAssinaturaContrato = models.DateField(blank=True, null=True)
    datPublicacaoContrato = models.DateField(blank=True, null=True)
    datVigenciaContrato = models.DateField(blank=True, null=True)
    numOriginalContrato = models.TextField(blank=True, null=True)
    txtRazaoSocialContrato = models.TextField(blank=True, null=True)
    valAditamentosContrato = models.FloatField(blank=True, null=True)
    valAnulacaoContrato = models.FloatField(blank=True, null=True)
    valAnuladoEmpenhoContrato = models.FloatField(blank=True, null=True)
    valEmpenhadoLiquidoContrato = models.FloatField(blank=True, null=True)
    valliquidadoContrato = models.FloatField(blank=True, null=True)
    valPagoContrato = models.FloatField(blank=True, null=True)
    valPrincipalContrato = models.FloatField(blank=True, null=True)
    valReajustesContrato = models.FloatField(blank=True, null=True)
    valTotalEmpenhadoContrato = models.FloatField(blank=True, null=True)
    dataExtracaoContrato = models.DateField(blank=True, null=True)
    dtDataLoadedContrato = models.CharField(max_length=26, blank=True,
                                            null=True)
    # empenho fields
    anoEmpenho = models.IntegerField(blank=True, null=True)
    codCategoria = models.IntegerField(blank=True, null=True)
    txtCategoriaEconomica = models.TextField(blank=True, null=True)
    codElemento = models.IntegerField(blank=True, null=True)
    codEmpenho = models.IntegerField(blank=True, null=True)
    codEmpresa = models.IntegerField(blank=True, null=True)
    codFonteRecurso = models.IntegerField(blank=True, null=True)
    codFuncao = models.IntegerField(blank=True, null=True)
    codGrupo = models.IntegerField(blank=True, null=True)
    txtGrupoDespesa = models.TextField(blank=True, null=True)
    codItemDespesa = models.IntegerField(blank=True, null=True)
    codModalidade = models.IntegerField(blank=True, null=True)
    txtModalidadeAplicacao = models.TextField(blank=True, null=True)
    codOrgao = models.IntegerField(blank=True, null=True)
    codProcesso = models.BigIntegerField(blank=True, null=True)
    codPrograma = models.IntegerField(blank=True, null=True)
    codProjetoAtividade = models.IntegerField(blank=True, null=True)
    codSubElemento = models.IntegerField(blank=True, null=True)
    codSubFuncao = models.IntegerField(blank=True, null=True)
    codUnidade = models.IntegerField(blank=True, null=True)
    datEmpenho = models.CharField(blank=True, max_length=20, null=True)
    mesEmpenho = models.IntegerField(blank=True, null=True)
    nomEmpresa = models.TextField(blank=True, null=True)
    numCpfCnpj = models.CharField(blank=True, max_length=18, null=True)
    numReserva = models.IntegerField(blank=True, null=True)
    txtDescricaoOrgao = models.TextField(blank=True, null=True)
    txtDescricaoUnidade = models.TextField(blank=True, null=True)
    txtDescricaoElemento = models.TextField(blank=True, null=True)
    txtDescricaoFonteRecurso = models.TextField(blank=True, null=True)
    txtDescricaoFuncao = models.TextField(blank=True, null=True)
    txtDescricaoItemDespesa = models.TextField(blank=True, null=True)
    txtDescricaoPrograma = models.TextField(blank=True, null=True)
    txtDescricaoProjetoAtividade = models.TextField(blank=True, null=True)
    txtRazaoSocial = models.TextField(blank=True, null=True)
    txtDescricaoSubElemento = models.TextField(blank=True, null=True)
    txtDescricaoSubFuncao = models.TextField(blank=True, null=True)
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
    razao_social = models.TextField()

    def __str__(self):
        return self.razao_social


class ObjetoContrato(models.Model):
    desc = models.TextField()

    def __str__(self):
        return self.desc


class ModalidadeContrato(models.Model):
    id = models.IntegerField(primary_key=True)
    desc = models.TextField()

    def __str__(self):
        return self.desc


class CategoriaContrato(models.Model):
    name = models.CharField(max_length=30, unique=True)
    desc = models.CharField(max_length=400)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name


class CategoriaContratoFromTo(models.Model):
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


class CategoriaContratoFromToSpreadsheet(models.Model):
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
        from contratos.dao.models_dao import CategoriasContratosFromToDao
        dao = CategoriasContratosFromToDao()
        dao.extract_spreadsheet(self)
