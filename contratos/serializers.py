from contratos.services import application as services


class ExecucaoContratoSerializer:

    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        self.categoria_id = kwargs['categoria_id']

    @property
    def data(self):
        # TODO: add tests
        return {
            'big_number': services.serialize_big_number_data(self.queryset),
            'destinations': services.serialize_destinations(self.queryset),
            'top5': services.serialize_top5(self.queryset, self.categoria_id),
        }
