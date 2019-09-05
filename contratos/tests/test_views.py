from datetime import date
from django.test import RequestFactory
from django.urls import reverse

from model_mommy import mommy
from rest_framework.test import APITestCase

from contratos.models import EmpenhoSOFCache
from contratos.serializers import EmpenhoSOFCacheSerializer


class TestHomeView(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:home')
        return self.client.get(url, kwargs)

    def setUp(self):
        self.categoria = mommy.make('CategoriaContrato',
            name='Alimentação', slug='alimentacao')

    @property
    def empty_state(self):
        return {
            'big_number': {},
            'destinations': [],
            'dt_updated': None,
            'filters': {
                'categorias': [],
                'selected_categoria': None,
                'selected_year': None,
                'years': []
            },
            'top5': [],
        }

    def get_execucao(self, **kwargs):
        return mommy.make('ExecucaoContrato', categoria=self.categoria,
                **kwargs)

    def test_render_correct_template(self):
        self.get_execucao()
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/home.html')

    def test_empty_state(self):
        response = self.get()
        assert self.empty_state == response.data

    def test_most_recent_year_as_default(self):
        year = 1500
        empenhado = 42
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.data['filters']['selected_year']
        assert empenhado == response.data['big_number']['empenhado']

        year = 2018
        empenhado = 10
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.data['filters']['selected_year']
        assert empenhado == response.data['big_number']['empenhado']

        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.data['filters']['selected_year']
        assert 20 == response.data['big_number']['empenhado']

        empenhado = 17
        self.get_execucao(year=date(1998, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.data['filters']['selected_year']
        assert 20 == response.data['big_number']['empenhado']

    def test_filter_by_year(self):
        year = 1500
        empenhado = 42
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get(year=year)
        assert year == response.data['filters']['selected_year']
        assert empenhado == response.data['big_number']['empenhado']

        year = 2018
        empenhado = 10
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get(year=year)
        assert year == response.data['filters']['selected_year']
        assert empenhado == response.data['big_number']['empenhado']

        year = 3000
        response = self.get(year=year)
        assert 400 == response.status_code

class TestDownloadView(APITestCase):

    def setUp(self):
        self.curr_year = date.today().year
        mommy.make(EmpenhoSOFCache, anoExercicioContrato=2018,
                   _fill_optional=True, _quantity=2)
        mommy.make(EmpenhoSOFCache, anoExercicioContrato=self.curr_year,
                   _fill_optional=True, _quantity=3)
        self.url = reverse('contratos:download')

    def get(self, **kwargs):
        return self.client.get(self.url, kwargs)

    # def prepare_expected_data(self, year=None):
    #     factory = RequestFactory()
    #     if year:
    #         empenhos = EmpenhoSOFCache.objects.filter(anoExercicioContrato=year)
    #         request = factory.get(self.url, {'year': year})
    #     else:
    #         empenhos = EmpenhoSOFCache.objects.filter(
    #             anoExercicioContrato=self.curr_year)
    #         request = factory.get(self.url)

    #     return EmpenhoSOFCacheSerializer(
    #         empenhos, many=True, context={'request': request}).data

    # def test_renderers_xlsx(self):
    #     response = self.get()
    #     assert 'xlsx' == response.accepted_renderer.format

    # def test_downloads_current_year_data_when_no_year_is_passed(self):
    #     expected = self.prepare_expected_data()
    #     data = self.get().data
    #     assert 3 == len(data)
    #     assert expected == data

    # def test_downloads_2018_data(self):
    #     expected = self.prepare_expected_data(year=2018)
    #     data = self.get(year=2018).data
    #     assert 2 == len(data)
    #     assert expected == data


class TestSobreView(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:sobre')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/sobre.html')
