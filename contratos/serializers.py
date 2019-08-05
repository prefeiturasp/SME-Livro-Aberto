class ExecucaoContratoSerializer:

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset

    @property
    def data(self):
        return {}
