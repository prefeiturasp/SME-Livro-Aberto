from rest_framework import serializers

from budget_execution import models


class ExecucaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Execucao
        fields = '__all__'
        # read_only_fields = '__all__'
