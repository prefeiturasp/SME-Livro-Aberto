from contratos.models import (
    Fornecedor, EmpenhoSOFCache, ExecucaoContrato, ModalidadeContrato,
    ObjetoContrato)


class EmpenhosSOFCacheDao:

    def __init__(self):
        self.model = EmpenhoSOFCache

    def get_all(self):
        pass


class ExecucoesContratosDao:

    def __init__(self):
        self.model = ExecucaoContrato

    def create(self, **data):
        ExecucaoContrato.objects.create(**data)


class ModalidadesContratosDao:

    def __init__(self):
        self.model = ModalidadeContrato

    def get_or_create(self, **data):
        return ModalidadeContrato.objects.get_or_create(**data)


class ObjetosContratosDao:

    def __init__(self):
        self.model = ObjetoContrato

    def get_or_create(self, data):
        return ObjetoContrato.objects.get_or_create(**data)


class FornecedoresDao:

    def __init__(self):
        self.model = Fornecedor

    def get_or_create(self, data):
        return Fornecedor.objects.get_or_create(**data)
