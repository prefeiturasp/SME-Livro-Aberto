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

        distrito_s = mommy.make(Distrito, zona='Sul', name='Distrito s',
                                coddist=1)
        distrito_n = mommy.make(Distrito, zona='Norte', name='Distrito n',
                                coddist=2)
        tipo_i = mommy.make(TipoEscola, code='TI', etapa='Ensino Infantil')
        tipo_f = mommy.make(TipoEscola, code='TF', etapa='Ensino Fundamental')
        dre_x = mommy.make(Dre, name='Dre x', code='x')
        dre_y = mommy.make(Dre, name='Dre y', code='y')

        self.info1 = mommy.make(
            EscolaInfo, escola=escola1, distrito=distrito_s, dre=dre_x,
            budget_total=100, tipoesc=tipo_i, year=year,
            rede='DIR')
        self.info2 = mommy.make(
            EscolaInfo, escola=escola2, distrito=distrito_s, dre=dre_y,
            budget_total=200, tipoesc=tipo_f, year=year,
            rede='DIR')
        self.info3 = mommy.make(
            EscolaInfo, escola=escola3, distrito=distrito_n, dre=dre_y,
            budget_total=55, tipoesc=tipo_i, year=year,
            rede='DIR')

    @property
    def url(self):
        return reverse('regionalizacao:home')

    def get(self, **kwargs):
        return self.client.get(self.url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/home.html')

    def test_returns_city_data(self):
        response = self.get()

        expected = {
            'total': 355,
            'places': [
                {
                    'name': 'Sul',
                    'total': 300,
                    'url': f'{self.url}?zona=Sul',
                },
                {
                    'name': 'Norte',
                    'total': 55,
                    'url': f'{self.url}?zona=Norte',
                },
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
                {
                    'code': 'y',
                    'name': 'Dre y',
                    'total': 200,
                    'url': f'{self.url}?zona=Sul&dre=y',
                },
                {
                    'code': 'x',
                    'name': 'Dre x',
                    'total': 100,
                    'url': f'{self.url}?zona=Sul&dre=x',
                },
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

    def test_returns_dre_data(self):
        response = self.get(zona='Sul', dre='y')

        # TODO: botar slug
        expected = {
            'total': 255,
            'places': [
                {
                    'code': 1,
                    'name': 'Distrito s',
                    'total': 200,
                    'url': f'{self.url}?zona=Sul&dre=y&distrito=1',
                },
                {
                    'code': 2,
                    'name': 'Distrito n',
                    'total': 55,
                    'url': f'{self.url}?zona=Sul&dre=y&distrito=2',
                },
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
                    'total': 55,
                },
            ]
        }

        assert expected == response.data

    def test_returns_distrito_data(self):
        escola1_recursos = {
            "total": 100,
            "ptrf": 100,
            "grupos": [],
        }
        self.info1.nomesc = "Escola 1"
        self.info1.endereco = "Rua 1"
        self.info1.numero = 10
        self.info1.bairro = 'Bairro 1'
        self.info1.cep = '10100000'
        self.info1.recursos = escola1_recursos
        self.info1.save()

        escola2_recursos = {
            "total": 200,
            "ptrf": 200,
            "grupos": [],
        }

        self.info2.nomesc = "Escola 2"
        self.info2.endereco = "Rua 2"
        self.info2.numero = 20
        self.info2.bairro = 'Bairro 2'
        self.info2.cep = '20200000'
        self.info2.recursos = escola2_recursos
        self.info2.save()

        self.info1.refresh_from_db()
        self.info2.refresh_from_db()

        response = self.get(zona='Sul', dre='y', distrito=1)

        expected = {
            'total': 300,
            'places': [
                {
                    'name': 'TF - Escola 2',
                    'address': 'Rua 2, 20 - Bairro 2',
                    'cep': 20200000,
                    'total': 200,
                    'recursos': escola2_recursos,
                    'latitude': str(self.info2.latitude),
                    'longitude': str(self.info2.longitude),
                },
                {
                    'name': 'TI - Escola 1',
                    'address': 'Rua 1, 10 - Bairro 1',
                    'cep': 10100000,
                    'total': 100,
                    'recursos': escola1_recursos,
                    'latitude': str(self.info1.latitude),
                    'longitude': str(self.info1.longitude),
                },
            ],
        }

        assert expected == response.data


class TestSaibaMaisView(APITestCase):

    def get(self, **kwargs):
        url = reverse('regionalizacao:saiba_mais')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/saiba_mais.html')
