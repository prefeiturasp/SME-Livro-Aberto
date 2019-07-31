from contratos.models import EmpenhoSOFCacheTemp


def create(*, data):
    return EmpenhoSOFCacheTemp.objects.create(**data)


def get_all():
    return EmpenhoSOFCacheTemp.objects.all()
