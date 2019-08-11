from contratos.models import (
    CategoriaContrato,
    CategoriaContratoFromTo,
    ContratoRaw,
    Fornecedor,
    EmpenhoSOFCache,
    ExecucaoContrato,
    ModalidadeContrato,
    ObjetoContrato)


class EmpenhosSOFCacheDao:

    def __init__(self):
        self.model = EmpenhoSOFCache

    def get_all(self):
        return self.model.objects.all()


class ContratosRawDao:

    def __init__(self):
        self.model = ContratoRaw

    def get_all(self):
        return self.model.objects.all()

    def get(self, **data):
        return self.model.objects.get(**data)


class ExecucoesContratosDao:

    def __init__(self):
        self.model = ExecucaoContrato

    def create(self, **data):
        return self.model.objects.create(**data)

    def get_by_indexer(self, indexer):
        return self.model.objects.get(empenho_indexer=indexer)

    def update_with(self, execucao, **data):
        for field, value in data.items():
            setattr(execucao, field, value)
        return execucao.save()


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


class CategoriasContratosFromToDao:

    def __init__(self):
        self.model = CategoriaContratoFromTo

    def get_all(self):
        return self.model.objects.all()


class CategoriasContratosDao:

    def __init__(self):
        self.model = CategoriaContrato

    def get_or_create(self, **data):
        return self.model.objects.get_or_create(**data)
