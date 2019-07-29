from contratos.models import EmpenhoSOFFailedAPIRequest


def create(*, cod_contrato, ano_exercicio, ano_empenho, error_code):
    return EmpenhoSOFFailedAPIRequest.objects.create(
        cod_contrato=cod_contrato, ano_exercicio=ano_exercicio,
        ano_empenho=ano_empenho, error_code=error_code)


def get_all():
    return EmpenhoSOFFailedAPIRequest.objects.all()


def delete(obj):
    obj.delete()
