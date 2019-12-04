from datetime import date

from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from regionalizacao.models import (
    Escola, EscolaInfo, TipoEscola, Distrito)


class TestHomeView(APITestCase):

    def get(self, **kwargs):
        url = reverse('regionalizacao:home')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/home.html')

    def test_returns_city_data(self):
        year = date.today().year
        escola1 = mommy.make(Escola, codesc='01')
        escola2 = mommy.make(Escola, codesc='02')
        escola3 = mommy.make(Escola, codesc='03')

        distrito_s = mommy.make(Distrito, zona='Sul')
        distrito_n = mommy.make(Distrito, zona='Norte')
        tipo_i = mommy.make(TipoEscola, etapa='Ensino Infantil')
        tipo_f = mommy.make(TipoEscola, etapa='Ensino Fundamental')

        mommy.make(EscolaInfo, escola=escola1, distrito=distrito_s,
                   recursos={'total': 100}, tipoesc=tipo_i, year=year,
                   rede='DIR')
        mommy.make(EscolaInfo, escola=escola2, distrito=distrito_s,
                   recursos={'total': 200}, tipoesc=tipo_f, year=year,
                   rede='DIR')
        mommy.make(EscolaInfo, escola=escola3, distrito=distrito_n,
                   recursos={'total': 55}, tipoesc=tipo_i, year=year,
                   rede='DIR')

        expected = {
            'total': 355,
            'zonas': [
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

        response = self.get()

        assert expected == response.data


class TestSaibaMaisView(APITestCase):

    def get(self, **kwargs):
        url = reverse('regionalizacao:saiba_mais')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/saiba_mais.html')
