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
