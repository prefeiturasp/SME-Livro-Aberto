from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from budget_execution.models import Execucao
from geologia.serializers import GeologiaSerializer


class TestHomeView(APITestCase):

    def get(self, programa_id=None):
        url = reverse('geologia:home')
        if programa_id:
            url += '?programa_id={}'.format(programa_id)
        return self.client.get(url)

    def test_serializes_geologia_data(self):
        mommy.make(Execucao, subgrupo__id=1, _quantity=2)
        execucoes = Execucao.objects.all()
        serializer = GeologiaSerializer(execucoes)

        response = self.get()
        assert serializer.data == response.data

    def test_filters_execucoes_without_subgrupo(self):
        mommy.make(Execucao, subgrupo=None, _quantity=2)
        mommy.make(Execucao, subgrupo__id=1, _quantity=2)
        execucoes = Execucao.objects.filter(subgrupo__isnull=False)
        serializer = GeologiaSerializer(execucoes)

        response = self.get()
        assert serializer.data == response.data

    def test_serializes_geologia_data_with_programa(self):
        mommy.make(Execucao, subgrupo__id=1, programa__id=1, _quantity=2)
        mommy.make(Execucao, subgrupo__id=1, programa__id=2, _quantity=1)
        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer(execucoes, programa_id=1)

        response = self.get(programa_id=1)
        assert serializer.data == response.data
