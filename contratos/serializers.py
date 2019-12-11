from rest_framework import serializers

from contratos.models import EmpenhoSOFCache
from contratos.services import application as services


class ExecucaoContratoSerializer:

    def __init__(self, queryset_year_filtered, queryset):
        self.qs = queryset
        self.qs_year_filtered = queryset_year_filtered

    @property
    def data(self):
        return {
            'big_number': services.serialize_big_number_data(self.qs_year_filtered),
            'destinations': services.serialize_destinations(self.qs_year_filtered),
            'top5': services.serialize_top5(self.qs),
            'dt_updated': services.serialize_date_updated(),
        }


class EmpenhoSOFCacheSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmpenhoSOFCache
        exclude = ['id']
