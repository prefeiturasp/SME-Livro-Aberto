from datetime import date

from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from regionalizacao.models import (
    Escola, EscolaInfo, TipoEscola, Distrito, Dre)


class TestHomeView(APITestCase):

    def setUp(self):
        year = date.today().year
        escola1 = mommy.make(Escola, codesc='01')
        escola2 = mommy.make(Escola, codesc='02')
        escola3 = mommy.make(Escola, codesc='03')

        distrito_s = mommy.make(Distrito, zona='Sul')
        distrito_n = mommy.make(Distrito, zona='Norte')
        tipo_i = mommy.make(TipoEscola, etapa='Ensino Infantil')
        tipo_f = mommy.make(TipoEscola, etapa='Ensino Fundamental')
        dre_x = mommy.make(Dre, name='Dre x', code='x')
        dre_y = mommy.make(Dre, name='Dre y', code='y')

        mommy.make(EscolaInfo, escola=escola1, distrito=distrito_s, dre=dre_x,
                   budget_total=100, tipoesc=tipo_i, year=year,
                   rede='DIR')
        mommy.make(EscolaInfo, escola=escola2, distrito=distrito_s, dre=dre_y,
                   budget_total=200, tipoesc=tipo_f, year=year,
                   rede='DIR')
        mommy.make(EscolaInfo, escola=escola3, distrito=distrito_n, dre=dre_y,
                   budget_total=55, tipoesc=tipo_i, year=year,
                   rede='DIR')

    def get(self, **kwargs):
        url = reverse('regionalizacao:home')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/home.html')

    def test_returns_city_data(self):
        response = self.get()

        expected = {
            'total': 355,
            'places': [
                {'name': 'Sul', 'total': 300},
                {'name': 'Norte', 'total': 55},
            ],
            'etapas': [
                {
                    'name': 'Ensino Infantil',
                    'unidades': 2,
                    'total': 155,
                },
                {
                    'name': 'Ensino Fundamental',
                    'unidades': 1,
                    'total': 200,
                }
            ]
        }

        assert expected == response.data

    def test_returns_zona_data(self):
        response = self.get(zona='Sul')

        expected = {
            'total': 300,
            'places': [
                {'code': 'y', 'name': 'Dre y', 'total': 200},
                {'code': 'x', 'name': 'Dre x', 'total': 100},
            ],
            'etapas': [
                {
                    'name': 'Ensino Fundamental',
                    'unidades': 1,
                    'total': 200,
                },
                {
                    'name': 'Ensino Infantil',
                    'unidades': 1,
                    'total': 100,
                },
            ]
        }

        assert expected == response.data


class TestSaibaMaisView(APITestCase):

    def get(self, **kwargs):
        url = reverse('regionalizacao:saiba_mais')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/saiba_mais.html')
