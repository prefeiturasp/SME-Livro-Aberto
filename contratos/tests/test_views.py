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

    def get_execucao(self, **kwargs):
        return mommy.make('ExecucaoContrato', categoria=self.categoria,
                **kwargs)

    def test_render_correct_template(self):
        self.get_execucao()
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/home.html')

    def test_empty_state(self):
        response = self.get()
        assert {} == response.data['big_number']
        assert [] == response.data['destinations']
        assert None == response.data['dt_updated']
        assert [] == response.data['top5']

    def test_most_recent_year_as_default(self):
        year = 1500
        empenhado = 42
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.context['filter_form']['year'].value()
        assert empenhado == response.data['big_number']['empenhado']
        assert 1 == len(response.data['destinations'])

        year = 2018
        empenhado = 10
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.context['filter_form']['year'].value()
        assert empenhado == response.data['big_number']['empenhado']
        assert 1 == len(response.data['destinations'])

        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.context['filter_form']['year'].value()
        assert 20 == response.data['big_number']['empenhado']
        assert 1 == len(response.data['destinations'])

        empenhado = 17
        self.get_execucao(year=date(1998, 1, 1), valor_empenhado=empenhado)
        response = self.get()
        assert year == response.context['filter_form']['year'].value()
        assert 20 == response.data['big_number']['empenhado']
        assert 1 == len(response.data['destinations'])

    def test_filter_by_year(self):
        year = 1500
        empenhado = 42
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get(year=year)
        assert str(year) == response.context['filter_form']['year'].value()
        assert empenhado == response.data['big_number']['empenhado']

        year = 2018
        empenhado = 10
        self.get_execucao(year=date(year, 1, 1), valor_empenhado=empenhado)
        response = self.get(year=year)
        assert str(year) == response.context['filter_form']['year'].value()
        assert empenhado == response.data['big_number']['empenhado']

        year = 3000
        response = self.get(year=year)
        assert 400 == response.status_code


class TestHomeViewCategory(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:home')
        return self.client.get(url, kwargs)

    def test_filter_by_category(self):
        category = mommy.make('CategoriaContrato',
            name='Alimentação', slug='alimentacao')
        mommy.make('ExecucaoContrato', categoria=category)

        response = self.get(category=category.id)
        assert str(category.id) == response.context['filter_form']['category'].value()
        assert 1 == len(response.context['top5'])
        assert category.name == response.context['top5'][0]['categoria_name']

        other_category = mommy.make('CategoriaContrato',
            name='Parcerias', slug='parcerias')
        mommy.make('ExecucaoContrato', categoria=other_category)
        response = self.get(category=other_category.id)
        assert str(other_category.id) == response.context['filter_form']['category'].value()
        assert 1 == len(response.context['top5'])
        assert other_category.name == response.context['top5'][0]['categoria_name']

        response = self.get()
        assert None == response.context['filter_form']['category'].value()
        assert 2 == len(response.context['top5'])

        invalid = 'invalid category'
        response = self.get(category=invalid)
        assert 400 == response.status_code

    def test_filter_by_category_shoultnt_touch_upper_sections(self):
        empenhado = 40
        category = mommy.make('CategoriaContrato',
            name='Alimentação', slug='alimentacao')
        mommy.make('ExecucaoContrato', categoria=category,
                valor_empenhado=empenhado)

        other_empenhado = 2
        other_category = mommy.make('CategoriaContrato',
            name='Parcerias', slug='parcerias')
        mommy.make('ExecucaoContrato', categoria=other_category,
                valor_empenhado=other_empenhado)

        response = self.get(category=category.id)
        assert 42 == response.data['big_number']['empenhado']
        assert 1 == len(response.context['top5'])
        assert category.name == response.context['top5'][0]['categoria_name']


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


class TestSaibaMaisView(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:saiba_mais')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/saiba_mais.html')
