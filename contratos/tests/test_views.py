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

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/home.html')


class TestDownloadView(APITestCase):

    def setUp(self):
        self.curr_year = date.today().year
        mommy.make(EmpenhoSOFCache, anoEmpenho=2018, _fill_optional=True,
                   _quantity=2)
        mommy.make(EmpenhoSOFCache, anoEmpenho=self.curr_year,
                   _fill_optional=True, _quantity=3)
        self.url = reverse('contratos:download')

    def get(self, **kwargs):
        return self.client.get(self.url, kwargs)

    def prepare_expected_data(self, year=None):
        factory = RequestFactory()
        if year:
            empenhos = EmpenhoSOFCache.objects.filter(anoEmpenho=year)
            request = factory.get(self.url, {'year': year})
        else:
            empenhos = EmpenhoSOFCache.objects.filter(anoEmpenho=self.curr_year)
            request = factory.get(self.url)

        return EmpenhoSOFCacheSerializer(
            empenhos, many=True, context={'request': request}).data

    def test_renderers_xlsx(self):
        response = self.get()
        assert 'xlsx' == response.accepted_renderer.format

    def test_downloads_current_year_data_when_no_year_is_passed(self):
        expected = self.prepare_expected_data()
        data = self.get().data
        assert 3 == len(data)
        assert expected == data

    def test_downloads_2018_data(self):
        expected = self.prepare_expected_data(year=2018)
        data = self.get(year=2018).data
        assert 2 == len(data)
        assert expected == data


class TestSobreView(APITestCase):

    def get(self, **kwargs):
        url = reverse('contratos:sobre')
        return self.client.get(url, kwargs)

    def test_render_correct_template(self):
        response = self.get()
        self.assertTemplateUsed(response, 'contratos/sobre.html')
