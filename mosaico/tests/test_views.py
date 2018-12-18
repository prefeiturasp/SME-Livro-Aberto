import pytest

from datetime import date

from model_mommy.mommy import make
from rest_framework.test import APITestCase

from django.urls import reverse

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

    def get(self, fonte_grupo_id=None):
        url = reverse('mosaico:home_simples', args=[2018])
        if fonte_grupo_id:
            url += '?fonte_grupo_id={}'.format(fonte_grupo_id)
        return self.client.get(url)

    @pytest.fixture(autouse=True)
    def initial(self):
        make(Execucao,
             subgrupo__grupo__id=1,
             fonte_grupo__id=1,
             year=date(2018, 1, 1),
             _quantity=2)
        make(Execucao,
             subgrupo__grupo__id=2,
             fonte_grupo__id=1,
             year=date(2018, 1, 1),
             _quantity=2)
        make(Execucao,
             subgrupo__grupo__id=3,
             fonte_grupo__id=2,
             year=date(2018, 1, 1),
             _quantity=2)

    def test_serializes_execucoes_data(self):
        execucoes = Execucao.objects.all().distinct('subgrupo__grupo')
        serializer = GrupoSerializer(execucoes, many=True)
        expected = serializer.data

        response = self.get()
        assert expected == response.data['execucoes']

    def test_filters_by_fonte_grupo_querystring_data(self):
        execucoes = Execucao.objects.filter(fonte_grupo__id=1) \
            .distinct('subgrupo__grupo')
        serializer = GrupoSerializer(execucoes, many=True)
        expected = serializer.data

        response = self.get(fonte_grupo_id=1)
        assert expected == response.data['execucoes']
