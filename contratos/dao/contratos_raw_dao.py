from contratos.models import ContratoRaw


def get_all():
    return ContratoRaw.objects.all()
