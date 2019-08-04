from contratos.models import (
    Fornecedor, EmpenhoSOFCache, ExecucaoContrato, ModalidadeContrato,
    ObjetoContrato)


class EmpenhosSOFCacheDao:

    def __init__(self):
        self.model = EmpenhoSOFCache

    def get_all(self):
        return self.model.objects.all()


class ExecucoesContratosDao:

    def __init__(self):
        self.model = ExecucaoContrato

    def create(self, **data):
        return self.model.objects.create(**data)


class ModalidadesContratosDao:

    def __init__(self):
        self.model = ModalidadeContrato

    def get_or_create(self, **data):
        return self.model.objects.get_or_create(**data)


class ObjetosContratosDao:

    def __init__(self):
        self.model = ObjetoContrato

    def get_or_create(self, **data):
        return self.model.objects.get_or_create(**data)


class FornecedoresDao:

    def __init__(self):
        self.model = Fornecedor

    def get_or_create(self, **data):
        return self.model.objects.get_or_create(**data)
