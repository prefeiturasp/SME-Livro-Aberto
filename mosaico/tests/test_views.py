import pytest

from datetime import date

from model_mommy.mommy import make
from rest_framework.test import APITestCase

from django.urls import reverse

from budget_execution.models import Execucao, FonteDeRecursoGrupo, Subgrupo
from mosaico.serializers import GrupoSerializer, SubgrupoSerializer


class TestHomeView(APITestCase):
    def get(self):
        url = reverse('mosaico:home')
        return self.client.get(url)

    def test_redirect_to_most_recent_year(self):
        year = 1500
        redirect_url = reverse('mosaico:grupos', kwargs=dict(year=year))
        make('Execucao', year=date(year, 1, 1))
        response = self.get()
        self.assertRedirects(response, redirect_url,
                             fetch_redirect_response=False)

        year = 2018
        redirect_url = reverse('mosaico:grupos',
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
        url = reverse('mosaico:grupos', args=[2018])
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

    def test_view_works_when_queryset_is_empty(self):
        make(FonteDeRecursoGrupo, id=3)
        response = self.get(fonte_grupo_id=3)
        assert [] == response.data['execucoes']


class TestSubgruposListView(APITestCase):

    def get(self, fonte_grupo_id=None):
        url = reverse('mosaico:subgrupos', args=[2018, 1])
        if fonte_grupo_id:
            url += '?fonte_grupo_id={}'.format(fonte_grupo_id)
        return self.client.get(url)

    @pytest.fixture(autouse=True)
    def initial(self):
        subgrupo1 = make(Subgrupo, id=96, grupo__id=1)
        subgrupo2 = make(Subgrupo, id=97, grupo__id=1)
        subgrupo3 = make(Subgrupo, id=98, grupo__id=1)

        make(Execucao,
             subgrupo=subgrupo1,
             fonte_grupo__id=1,
             year=date(2018, 1, 1),
             _quantity=2)
        make(Execucao,
             subgrupo=subgrupo2,
             fonte_grupo__id=1,
             year=date(2018, 1, 1),
             _quantity=2)
        make(Execucao,
             subgrupo=subgrupo3,
             fonte_grupo__id=2,
             year=date(2018, 1, 1),
             _quantity=2)

    def test_serializes_execucoes_data(self):
        execucoes = Execucao.objects.all().distinct('subgrupo')
        serializer = SubgrupoSerializer(execucoes, many=True)
        expected = serializer.data

        response = self.get()
        data = response.data['execucoes']
        assert 3 == len(data)
        assert expected == data

    def test_filters_by_fonte_grupo_querystring_data(self):
        execucoes = Execucao.objects.filter(fonte_grupo__id=1) \
            .distinct('subgrupo')
        serializer = SubgrupoSerializer(execucoes, many=True)
        expected = serializer.data

        response = self.get(fonte_grupo_id=1)
        data = response.data['execucoes']
        assert 2 == len(data)
        assert expected == data

    def test_view_works_when_queryset_is_empty(self):
        make(FonteDeRecursoGrupo, id=3)
        response = self.get(fonte_grupo_id=3)
        assert [] == response.data['execucoes']
