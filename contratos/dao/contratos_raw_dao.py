from contratos.models import ContratoRaw


def get_all():
    return ContratoRaw.objects.all()


def get(**data):
    return ContratoRaw.objects.get(**data)
