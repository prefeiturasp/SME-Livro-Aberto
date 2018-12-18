from datetime import date

from django.urls import reverse
from model_mommy.mommy import make
from rest_framework.test import APITestCase

from budget_execution.models import Execucao
from mosaico.serializers import GrupoSerializer


class TestHomeView(APITestCase):
    def get(self):
        url = reverse('mosaico:home')
        return self.client.get(url)

    def test_redirect_to_most_recent_year(self):
        year = 1500
        redirect_url = reverse('mosaico:home_simples', kwargs=dict(year=year))
        make('Execucao', year=date(year, 1, 1))
        response = self.get()
        self.assertRedirects(response, redirect_url,
                             fetch_redirect_response=False)

        year = 2018
        redirect_url = reverse('mosaico:home_simples',
                               kwargs=dict(year=year))
        make('Execucao', year=date(year, 1, 1))
        response = self.get()
        self.assertRedirects(response, redirect_url,
                             fetch_redirect_response=False)

        year = 1998
        make('Execucao', year=date(year, 1, 1))
        response = self.get()
        self.assertRedirects(response, redirect_url,
                             fetch_redirect_response=False)


class TestGruposListView(APITestCase):

    def get(self, fonte_grupo=None):
        url = reverse('mosaico:home_simples', args=[2018])
        return self.client.get(url)

    def test_serializes_execucoes_data(self):
        make(Execucao, subgrupo__grupo__id=1, year=date(2018, 1, 1),
             _quantity=2)
        make(Execucao, subgrupo__grupo__id=2, year=date(2018, 1, 1),
             _quantity=2)
        execucoes = Execucao.objects.all().distinct('subgrupo__grupo')
        serializer = GrupoSerializer(execucoes, many=True)

        response = self.get()
        assert serializer.data == response.data['execucoes']
