import pytest

from datetime import date
from decimal import Decimal
from itertools import cycle

from model_mommy import mommy

from django.test import RequestFactory
from django.urls import reverse

from budget_execution.models import Execucao, Subgrupo
from from_to_handler.models import Deflator
from mosaico.serializers import (
    BaseExecucaoSerializer,
    GrupoSerializer,
    SubgrupoSerializer,
    ElementoSerializer,
    SubelementoSerializer,
    SubfuncaoSerializer,
    ProgramaSerializer,
    ProjetoAtividadeSerializer,

    TimeseriesSerializer,
)


@pytest.mark.django_db
class TestTimeseriesSerializer:

    @pytest.fixture(autouse=True)
    def initial(self):
        mommy.make(
            Execucao,
            orcado_atualizado=cycle([50, 100, 150]),
            empenhado_liquido=cycle([5, 10, 15]),
            year=date(2017, 1, 1),
            _quantity=3)

        mommy.make(
            Execucao,
            orcado_atualizado=cycle([10, 20, 30]),
            empenhado_liquido=cycle([1, 2, 3]),
            year=date(2018, 1, 1),
            _quantity=3)

        mommy.make(
            Deflator,
            year=date(2017, 1, 1),
            index_number=Decimal(0.2))

        mommy.make(
            Deflator,
            year=date(2018, 1, 1),
            index_number=Decimal(0.5))

    def test_serializes_data_correctly(self):
        execucoes = Execucao.objects.all()

        expected = {
            '2017': {
                "orcado": 300,
                "empenhado": 30,
            },
            '2018': {
                "orcado": 60,
                "empenhado": 6,
            },
        }

        serializer = TimeseriesSerializer(execucoes)

        assert expected == serializer.data

    def test_serializes_deflated_data(self):
        execucoes = Execucao.objects.all()

        expected = {
            '2017': {
                "orcado": 300 / 0.2,
                "empenhado": 30 / 0.2,
            },
            '2018': {
                "orcado": 60 / 0.5,
                "empenhado": 6 / 0.5,
            },
        }

        serializer = TimeseriesSerializer(execucoes, deflate=True)

        assert expected == serializer.data

    def test_serializes_normal_data_when_deflator_doesnt_exist(self):
        mommy.make(
            Execucao,
            orcado_atualizado=cycle([10, 20, 30]),
            empenhado_liquido=cycle([1, 2, 3]),
            year=date(2016, 1, 1),
            _quantity=3)

        execucoes = Execucao.objects.all()

        expected = {
            '2016': {
                "orcado": 60,
                "empenhado": 6,
            },
            '2017': {
                "orcado": 300 / 0.2,
                "empenhado": 30 / 0.2,
            },
            '2018': {
                "orcado": 60 / 0.5,
                "empenhado": 6 / 0.5,
            },
        }

        serializer = TimeseriesSerializer(execucoes, deflate=True)

        assert expected == serializer.data


class BaseTestCase:

    def get_serializer(self, queryset):

        factory = RequestFactory()
        request = factory.get(self.base_url)
        serializer = self.serializer_class

        return serializer(queryset, many=True,
                          context={'request': request})

    def assert_get_url(self, execucoes, serializer):
        item = serializer.data[0]
        expected = self.next_level_base_url(item) \
            + serializer.child._query_params
        assert expected == item['url']

    def get_filtered_queryset(self):
        return Execucao.objects.filter(year__year=2018, fonte_grupo_id=1)


@pytest.mark.django_db
class TestBaseExecucaoSerializer(BaseTestCase):

    serializer_class = GrupoSerializer

    @property
    def base_url(self):
        return reverse('mosaico:grupos')

    def next_level_base_url(self, item):
        return reverse('mosaico:subgrupos', args=[item['grupo_id']])

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.all().order_by('subgrupo__grupo__id')
        return self.get_serializer(qs)

    @pytest.fixture
    def execucoes(self):
        return mommy.make(
            Execucao,
            subgrupo__grupo__id=1,
            orcado_atualizado=cycle([50, 100, 150]),
            empenhado_liquido=cycle([5, 10, 15]),
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            _quantity=3)

    def test_get_orcado_total(self, execucoes, serializer):
        data = serializer.data
        expected = sum(execucao.orcado_atualizado for execucao in execucoes)
        assert expected == data[0]['orcado_total']

    def test_get_empenhado_total(self, execucoes, serializer):
        data = serializer.data
        expected = sum(execucao.empenhado_liquido for execucao in execucoes)
        assert expected == data[0]['empenhado_total']

    def test_get_percentual_empenhado(self, execucoes, serializer):
        data = serializer.data
        orcado = sum(execucao.orcado_atualizado for execucao in execucoes)
        empenhado = sum(execucao.empenhado_liquido for execucao in execucoes)
        expected = empenhado / orcado
        assert str(expected) == str(data[0]['percentual_empenhado'])

    def test_get_percentual_with_empenhado_null(self):
        mommy.make(
            Execucao,
            subgrupo__grupo__id=1,
            empenhado_liquido=None,
            year=date(2019, 1, 1),
            _quantity=3)

        qs = Execucao.objects.all().order_by('subgrupo__grupo__id')
        data = self.get_serializer(qs).data
        assert 0 == data[0]['percentual_empenhado']

    def test_serializers_are_subclasses(self):
        assert issubclass(GrupoSerializer, BaseExecucaoSerializer)
        assert issubclass(SubgrupoSerializer, BaseExecucaoSerializer)
        assert issubclass(ElementoSerializer, BaseExecucaoSerializer)
        assert issubclass(SubelementoSerializer, BaseExecucaoSerializer)
        assert issubclass(SubfuncaoSerializer, BaseExecucaoSerializer)
        assert issubclass(ProgramaSerializer, BaseExecucaoSerializer)
        assert issubclass(ProjetoAtividadeSerializer, BaseExecucaoSerializer)


class TestGrupoSerializer(TestBaseExecucaoSerializer):

    def test_get_url(self, execucoes, serializer):
        self.assert_get_url(execucoes, serializer)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        expected = qs.filter(subgrupo__grupo__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))


@pytest.mark.django_db
class TestSubgrupoSerializer(BaseTestCase):

    serializer_class = SubgrupoSerializer

    @property
    def base_url(self):
        return reverse('mosaico:subgrupos', args=[1])

    def next_level_base_url(self, item):
        return reverse('mosaico:elementos', args=[1, item['subgrupo_id']])

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.filter(subgrupo__grupo__id=1) \
            .order_by('subgrupo_id')
        return self.get_serializer(qs)

    @pytest.fixture
    def execucoes(self):
        subgrupo = mommy.make(Subgrupo, id=1, grupo__id=1)

        return mommy.make(
            Execucao,
            subgrupo=subgrupo,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            _quantity=2)

    def test_get_url(self, execucoes, serializer):
        self.assert_get_url(execucoes, serializer)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        expected = qs.filter(subgrupo__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))


@pytest.mark.django_db
class TestElementoSerializer(BaseTestCase):

    serializer_class = ElementoSerializer

    @property
    def base_url(self):
        return reverse('mosaico:elementos', args=[1, 1])

    def next_level_base_url(self, item):
        return reverse('mosaico:subelementos',
                       args=[1, 1, item['elemento_id']])

    @pytest.fixture
    def execucoes(self):
        subgrupo = mommy.make(Subgrupo, id=1, grupo__id=1)

        # not expected
        mommy.make(
            Execucao,
            elemento__id=2,
            subgrupo=subgrupo,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            orcado_atualizado=1)

        return mommy.make(
            Execucao,
            elemento__id=1,
            subgrupo=subgrupo,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            orcado_atualizado=1,
            _quantity=2)

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.filter(subgrupo__id=1).order_by('elemento_id')
        return self.get_serializer(qs)

    def test_get_url(self, execucoes, serializer):
        self.assert_get_url(execucoes, serializer)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        expected = qs.filter(subgrupo__id=1, elemento__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))


@pytest.mark.django_db
class TestSubelementoSerializer(BaseTestCase):

    serializer_class = SubelementoSerializer

    @property
    def base_url(self):
        return reverse('mosaico:subelementos', args=[1, 1, 1])

    @pytest.fixture
    def execucoes(self):
        subgrupo = mommy.make(Subgrupo, id=1, grupo__id=1)

        # not expected
        mommy.make(
            Execucao,
            subelemento__id=2,
            subelemento_friendly__id=1,
            elemento__id=1,
            subgrupo=subgrupo,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            orcado_atualizado=1)

        return mommy.make(
            Execucao,
            subelemento__id=1,
            subelemento_friendly__id=1,
            elemento__id=1,
            subgrupo=subgrupo,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            orcado_atualizado=1,
            _quantity=2)

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.filter(subgrupo__id=1, elemento__id=1) \
            .order_by('subelemento_id')
        return self.get_serializer(qs)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        # SubelementoSerializer: should use execucoes from the previous level
        expected = qs.filter(subgrupo__id=1, elemento__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))


@pytest.mark.django_db
class TestSubfuncaoSerializer(BaseTestCase):

    serializer_class = SubfuncaoSerializer

    @property
    def base_url(self):
        return reverse('mosaico:subfuncoes')

    def next_level_base_url(self, item):
        return reverse('mosaico:programas', args=[item['subfuncao_id']])

    @pytest.fixture
    def execucoes(self):
        # not expected
        mommy.make(
            Execucao,
            subfuncao__id=2,
            fonte_grupo__id=1,
            year=date(2018, 1, 1))

        return mommy.make(
            Execucao,
            subfuncao__id=1,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            _quantity=2)

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.all().order_by('subfuncao_id')
        return self.get_serializer(qs)

    def test_get_url(self, execucoes, serializer):
        self.assert_get_url(execucoes, serializer)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        expected = qs.filter(subfuncao__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))


@pytest.mark.django_db
class TestProgramaSerializer(BaseTestCase):

    serializer_class = ProgramaSerializer

    @property
    def base_url(self):
        return reverse('mosaico:programas', args=[1])

    def next_level_base_url(self, item):
        return reverse('mosaico:projetos', args=[1, item['programa_id']])

    @pytest.fixture
    def execucoes(self):
        # not expected
        mommy.make(
            Execucao,
            programa__id=2,
            subfuncao__id=1,
            fonte_grupo__id=1,
            year=date(2018, 1, 1))

        return mommy.make(
            Execucao,
            programa__id=1,
            subfuncao__id=1,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            _quantity=2)

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.filter(subfuncao__id=1).order_by('programa_id')
        return self.get_serializer(qs)

    def test_get_url(self, execucoes, serializer):
        self.assert_get_url(execucoes, serializer)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        expected = qs.filter(subfuncao__id=1, programa__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))


@pytest.mark.django_db
class TestProjetoAtividadeSerializer(BaseTestCase):

    serializer_class = ProjetoAtividadeSerializer

    @property
    def base_url(self):
        return reverse('mosaico:projetos', args=[1, 1])

    @pytest.fixture
    def execucoes(self):
        # not expected
        mommy.make(
            Execucao,
            projeto__id=2,
            programa__id=2,
            subfuncao__id=1,
            fonte_grupo__id=1,
            year=date(2018, 1, 1))

        return mommy.make(
            Execucao,
            projeto__id=1,
            programa__id=1,
            subfuncao__id=1,
            fonte_grupo__id=1,
            year=date(2018, 1, 1),
            _quantity=2)

    @pytest.fixture
    def serializer(self):
        qs = Execucao.objects.filter(subfuncao__id=1, programa__id=1) \
            .order_by('projeto_id')
        return self.get_serializer(qs)

    def test_serializer__execucoes_method(self, execucoes, serializer):
        qs = self.get_filtered_queryset()
        # ProjetoAtividadeSerializer: should use execucoes from the previous
        # level
        expected = qs.filter(subfuncao__id=1, programa__id=1)
        execucao = execucoes[0]
        assert set(expected) == set(serializer.child._execucoes(execucao))
