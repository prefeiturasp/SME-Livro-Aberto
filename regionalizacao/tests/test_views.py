from datetime import date

from django.urls import reverse
from model_mommy import mommy
from rest_framework.test import APITestCase

from regionalizacao.models import (
    Escola, EscolaInfo, TipoEscola, Distrito, Dre)


class HomeViewTestCase(APITestCase):

    def setUp(self):
        self.year = date.today().year
        escola1 = mommy.make(Escola, codesc='01')
        escola2 = mommy.make(Escola, codesc='02')
        escola3 = mommy.make(Escola, codesc='03')

        distrito_s = mommy.make(Distrito, zona='Sul', name='Distrito s',
                                coddist=1)
        distrito_n = mommy.make(Distrito, zona='Norte', name='Distrito n',
                                coddist=2)
        tipo_i = mommy.make(TipoEscola, code='TI', etapa='Ensino Infantil',
                            desc='desc TI')
        tipo_f = mommy.make(TipoEscola, code='TF', etapa='Ensino Fundamental',
                            desc='desc TF')
        tipo_i2 = mommy.make(TipoEscola, code='EI', etapa='Ensino Infantil',
                             desc='desc EI')
        dre_x = mommy.make(Dre, name='Dre x', code='x')
        dre_y = mommy.make(Dre, name='Dre y', code='y')

        self.info1 = mommy.make(
            EscolaInfo, escola=escola1, nomesc='Escola 1', distrito=distrito_s,
            dre=dre_x, budget_total=100, tipoesc=tipo_i, year=self.year,
            rede='DIR')
        self.info2 = mommy.make(
            EscolaInfo, escola=escola2,  nomesc='Escola 2', distrito=distrito_s,
            dre=dre_y, budget_total=200, tipoesc=tipo_f, year=self.year,
            rede='DIR')
        self.info3 = mommy.make(
            EscolaInfo, escola=escola3, distrito=distrito_n, dre=dre_y,
            budget_total=55, tipoesc=tipo_i2, year=self.year, rede='DIR')

        # escola 1 info from previous year
        self.info1_b = mommy.make(
            EscolaInfo, escola=escola1, nomesc='Escola 1', distrito=distrito_s,
            dre=dre_x, budget_total=2, tipoesc=tipo_i, year=self.year-1,
            rede='DIR')

    @property
    def url(self):
        return reverse('regionalizacao:home')

    def get(self, **kwargs):
        return self.client.get(self.url, kwargs)


class TestHomeView(HomeViewTestCase):

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/home.html')

    def test_returns_city_data(self):
        response = self.get()

        expected = {
            'current_level': 'São Paulo',
            'years': [2018, 2019],
            'total': 355,
            'places': [
                {
                    'name': 'Sul',
                    'total': 300,
                    'url': (f'{self.url}?year={self.year}&zona=Sul'
                            '&localidade=zona'),
                },
                {
                    'name': 'Norte',
                    'total': 55,
                    'url': (f'{self.url}?year={self.year}&zona=Norte'
                            '&localidade=zona'),
                },
            ],
            'etapas': [
                {
                    'name': 'Ensino Infantil',
                    'unidades': 2,
                    'total': 155,
                    'slug': 'infantil',
                    'tipos': [
                        {'code': 'EI', 'desc': 'desc EI'},
                        {'code': 'TI', 'desc': 'desc TI'},
                    ],
                },
                {
                    'name': 'Ensino Fundamental',
                    'unidades': 1,
                    'total': 200,
                    'slug': 'fundamental',
                    'tipos': [
                        {'code': 'TF', 'desc': 'desc TF'},
                    ],
                }
            ]
        }

        response.data.pop('locations')
        response.data.pop('breadcrumb')
        assert expected == response.data

    def test_returns_zona_data(self):
        response = self.get(zona='Sul')

        expected = {
            'current_level': 'Sul',
            'years': [2018, 2019],
            'total': 300,
            'places': [
                {
                    'code': 'y',
                    'name': 'Dre y',
                    'total': 200,
                    'url': (f'{self.url}?zona=Sul&year={self.year}&dre=y'
                            '&localidade=zona'),
                },
                {
                    'code': 'x',
                    'name': 'Dre x',
                    'total': 100,
                    'url': (f'{self.url}?zona=Sul&year={self.year}&dre=x'
                            '&localidade=zona'),
                },
            ],
            'etapas': [
                {
                    'name': 'Ensino Fundamental',
                    'unidades': 1,
                    'total': 200,
                    'slug': 'fundamental',
                    'tipos': [
                        {'code': 'TF', 'desc': 'desc TF'},
                    ],
                },
                {
                    'name': 'Ensino Infantil',
                    'unidades': 1,
                    'total': 100,
                    'slug': 'infantil',
                    'tipos': [
                        {'code': 'TI', 'desc': 'desc TI'},
                    ],
                },
            ]
        }

        response.data.pop('locations')
        response.data.pop('breadcrumb')
        assert expected == response.data

    def test_returns_dre_data(self):
        response = self.get(zona='Sul', dre='y')

        expected = {
            'current_level': 'Dre y',
            'years': [2018, 2019],
            'total': 255,
            'places': [
                {
                    'code': 1,
                    'name': 'Distrito s',
                    'total': 200,
                    'url': (f'{self.url}?zona=Sul&dre=y&year={self.year}'
                            f'&distrito=1&localidade=zona'),
                },
                {
                    'code': 2,
                    'name': 'Distrito n',
                    'total': 55,
                    'url': (f'{self.url}?zona=Sul&dre=y&year={self.year}'
                            f'&distrito=2&localidade=zona'),
                },
            ],
            'etapas': [
                {
                    'name': 'Ensino Fundamental',
                    'unidades': 1,
                    'total': 200,
                    'slug': 'fundamental',
                    'tipos': [
                        {'code': 'TF', 'desc': 'desc TF'},
                    ],
                },
                {
                    'name': 'Ensino Infantil',
                    'unidades': 1,
                    'total': 55,
                    'slug': 'infantil',
                    'tipos': [
                        {'code': 'EI', 'desc': 'desc EI'},
                    ],
                },
            ]
        }

        response.data.pop('locations')
        response.data.pop('breadcrumb')
        assert expected == response.data

    def test_returns_distrito_data(self):
        response = self.get(zona='Sul', dre='y', distrito=1)

        expected = {
            'current_level': 'Distrito s',
            'years': [2018, 2019],
            'total': 300,
            'places': [
                {
                    'code': '01',
                    'name': 'TI - Escola 1',
                    'latitude': str(self.info1.latitude),
                    'longitude': str(self.info1.longitude),
                    'slug': 'infantil',
                    'url': (f'{self.url}?zona=Sul&dre=y&distrito=1'
                            f'&year={self.year}&escola=01&localidade=zona'),
                },
                {
                    'code': '02',
                    'name': 'TF - Escola 2',
                    'latitude': str(self.info2.latitude),
                    'longitude': str(self.info2.longitude),
                    'slug': 'fundamental',
                    'url': (f'{self.url}?zona=Sul&dre=y&distrito=1'
                            f'&year={self.year}&escola=02&localidade=zona'),
                },
            ],
            'etapas': [
                {
                    'name': 'Ensino Fundamental',
                    'unidades': 1,
                    'total': 200,
                    'slug': 'fundamental',
                    'tipos': [
                        {'code': 'TF', 'desc': 'desc TF'},
                    ],
                },
                {
                    'name': 'Ensino Infantil',
                    'unidades': 1,
                    'total': 100,
                    'slug': 'infantil',
                    'tipos': [
                        {'code': 'TI', 'desc': 'desc TI'},
                    ],
                },
            ],
        }

        response.data.pop('locations')
        response.data.pop('breadcrumb')
        assert expected == response.data

    def test_returns_escola_data(self):
        escola1_recursos = {
            "total": 100,
            "ptrf": 100,
            "grupos": [],
        }
        self.info1.endereco = "Rua 1"
        self.info1.numero = 10
        self.info1.bairro = 'Bairro 1'
        self.info1.cep = '10100000'
        self.info1.recursos = escola1_recursos
        self.info1.save()

        response = self.get(zona='Sul', dre='y', distrito=1, escola='01')

        expected = {
            'current_level': 'TI - Escola 1',
            'years': [2018, 2019],
            'escola': {
                'name': 'TI - Escola 1',
                'address': 'Rua 1, 10 - Bairro 1',
                'cep': 10100000,
                'total': 100,
                'recursos': escola1_recursos,
                'latitude': str(self.info1.latitude),
                'longitude': str(self.info1.longitude),
            },
        }

        response.data.pop('locations')
        response.data.pop('breadcrumb')
        assert expected == response.data

    def test_filters_data_by_year(self):
        self.info1_b.endereco = "Rua 1b"
        self.info1_b.numero = 10
        self.info1_b.bairro = 'Bairro 1b'
        self.info1_b.cep = '10100000'
        self.info1_b.save()

        response = self.get(year=self.year-1, zona='Sul', dre='y', distrito=1,
                            escola='01')

        expected = {
            'current_level': 'TI - Escola 1',
            'years': [2018, 2019],
            'escola': {
                'name': 'TI - Escola 1',
                'address': 'Rua 1b, 10 - Bairro 1b',
                'cep': 10100000,
                'total': 2,
                'recursos': None,
                'latitude': str(self.info1_b.latitude),
                'longitude': str(self.info1_b.longitude),
            },
        }

        response.data.pop('locations')
        response.data.pop('breadcrumb')
        assert expected == response.data


class TestHomeViewLocationsGraphData(HomeViewTestCase):

    def test_returns_locations_data(self):
        response = self.get()
        expected = [
            {
                'name': 'Sul',
                'total': 300,
            },
            {
                'name': 'Norte',
                'total': 55,
            },
        ]

        assert expected == response.data['locations']

    def test_show_data_by_dre(self):
        dre_z = mommy.make(Dre, name='Dre z', code='z')

        mommy.make(
            EscolaInfo, dre=dre_z, budget_total=10, year=self.year,
            rede='DIR')

        response = self.get(localidade='dre')
        expected = [
            {
                'name': 'Dre y',
                'total': 255,
            },
            {
                'name': 'Dre x',
                'total': 100,
            },
            {
                'name': 'Dre z',
                'total': 10,
            },
        ]

        assert expected == response.data['locations']

    def test_map_level_does_not_affect_locations_data(self):
        expected = [
            {
                'name': 'Sul',
                'total': 300,
            },
            {
                'name': 'Norte',
                'total': 55,
            },
        ]

        response = self.get(zona='Sul')
        assert expected == response.data['locations']
        response = self.get(zona='Sul', dre='y')
        assert expected == response.data['locations']
        response = self.get(zona='Sul', dre='y', distrito=1)
        assert expected == response.data['locations']
        response = self.get(zona='Sul', dre='y', distrito=1, escola='01')
        assert expected == response.data['locations']


class TestHomeViewBreadcrumb(HomeViewTestCase):

    def test_returns_breadcrumb(self):
        response = self.get(zona='Sul', dre='x', distrito=1, escola='01')
        expected = [
            {
                'name': 'São Paulo',
                'url': f'{self.url}?year={self.year}&localidade=zona',
            },
            {
                'name': 'Sul',
                'url': (f'{self.url}?zona=Sul&year={self.year}'
                        '&localidade=zona'),
            },
            {
                'name': 'Dre x',
                'url': (f'{self.url}?zona=Sul&dre=x&year={self.year}'
                        '&localidade=zona'),
            },
            {
                'name': 'Distrito s',
                'url': (f'{self.url}?zona=Sul&dre=x&distrito=1&year={self.year}'
                        '&localidade=zona'),
            },
            {
                'name': 'TI - Escola 1',
                'url': (f'{self.url}?zona=Sul&dre=x&distrito=1&escola=01'
                        f'&year={self.year}&localidade=zona'),
            },
        ]

        assert expected == response.data['breadcrumb']


class TestSaibaMaisView(APITestCase):

    def get(self, **kwargs):
        url = reverse('regionalizacao:saiba_mais')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'regionalizacao/saiba_mais.html')
