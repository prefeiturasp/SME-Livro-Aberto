import pytest

from datetime import date
from decimal import Decimal
from itertools import cycle
from unittest.mock import Mock, patch

from freezegun import freeze_time
from model_mommy import mommy

from budget_execution.models import Execucao, GndGeologia, Subfuncao, Subgrupo
from from_to_handler.models import Deflator
from geologia.serializers import (
    GeologiaDownloadSerializer, GeologiaSerializer, GndGeologiaSerializer,
    SubfuncaoSerializer)


@pytest.mark.django_db
@pytest.fixture
def orcado_fixture():
    gnds_dict = [
        {'gnd_geologia__desc': 'gnd1', 'gnd_geologia__slug': 'g1',
         'orcado': Decimal(10)},
        {'gnd_geologia__desc': 'gnd2', 'gnd_geologia__slug': 'g2',
         'orcado': Decimal(20)},
        {'gnd_geologia__desc': 'gnd3', 'gnd_geologia__slug': 'g3',
         'orcado': Decimal(30)},
    ]
    orcado_total = Decimal(60)
    return gnds_dict, orcado_total


@pytest.fixture
def empenhado_fixture():
    gnds_dict = [
        {'gnd_geologia__desc': 'gnd1', 'gnd_geologia__slug': 'g1',
         'empenhado': Decimal(10)},
        {'gnd_geologia__desc': 'gnd2', 'gnd_geologia__slug': 'g2',
         'empenhado': Decimal(20)},
        # must support None for empenhado
        {'gnd_geologia__desc': 'gnd3', 'gnd_geologia__slug': 'g3',
         'empenhado': None},
    ]
    empenhado_total = Decimal(30)
    return gnds_dict, empenhado_total


@pytest.mark.django_db
class TestGeologiaSerializerCore:

    @pytest.fixture(autouse=True)
    def deflators(self):
        mommy.make(
            Deflator,
            year=date(2017, 1, 1),
            index_number=Decimal(0.2))

        mommy.make(
            Deflator,
            year=date(2018, 1, 1),
            index_number=Decimal(0.5))

    def test_get_orcado_gnds_list(self, orcado_fixture):
        gnds, orcado_total = orcado_fixture

        deflator = Deflator.objects.get(year__year=2017)

        expected = []
        for gnd in gnds:
            orcado = gnd['orcado'] / deflator.index_number

            gnd_dict = {
                "name": gnd['gnd_geologia__desc'],
                "slug": gnd['gnd_geologia__slug'],
                "value": orcado,
                "percent": orcado / orcado_total
            }
            expected.append(gnd_dict)

        serializer = GeologiaSerializer([])
        ret = serializer._get_orcado_gnds_list(gnds, orcado_total,
                                               deflator.year)

        assert expected == ret

    def test_get_empenhado_gnds_list(self, empenhado_fixture):
        gnds, empenhado_total = empenhado_fixture

        deflator = Deflator.objects.get(year__year=2018)

        expected = []
        for gnd in gnds:
            if gnd['empenhado'] is None:
                gnd['empenhado'] = 0

            empenhado = gnd['empenhado'] / deflator.index_number

            expected.append({
                "name": gnd['gnd_geologia__desc'],
                "slug": gnd['gnd_geologia__slug'],
                "value": empenhado,
                "percent": empenhado / empenhado_total
            })

        serializer = GeologiaSerializer([])
        ret = serializer._get_empenhado_gnds_list(
            gnds, empenhado_total, deflator.year)

        assert expected == ret

    def test_get_empenhado_gnd_list_when_total_is_none(self):
        gnds_dicts = [
            {'gnd_geologia__desc': 'gnd1', 'gnd_geologia__slug': 'g1',
             'empenhado': None},
            {'gnd_geologia__desc': 'gnd2', 'gnd_geologia__slug': 'g2',
             'empenhado': None},
        ]
        empenhado_total = None

        serializer = GeologiaSerializer([])
        assert serializer._get_empenhado_gnds_list(gnds_dicts, empenhado_total,
                                                   year=date(2017, 1, 1))

    def test_calculate_percent(self):
        serializer = GeologiaSerializer([])
        assert 0 == serializer._calculate_percent(None, 100)
        assert 0 == serializer._calculate_percent(10, None)
        assert 0.1 == serializer._calculate_percent(10, 100)

    @patch.object(GeologiaSerializer, '_get_empenhado_data_by_year')
    @patch.object(GeologiaSerializer, '_get_orcado_data_by_year')
    def test_returns_date_updated(self, mock_orcado, mock_empenhado):
        mock_orcado.return_value = 'mock_o'
        mock_empenhado.return_value = 'mock_e'

        subgrupo = mommy.make(Subgrupo, grupo__id=1)
        with freeze_time('2019-01-01'):
            mommy.make('Execucao', subgrupo=subgrupo)

        # not expected
        with freeze_time('2000-01-01'):
            mommy.make('Execucao', subgrupo=subgrupo)

        serializer = GeologiaSerializer(Execucao.objects.all())
        assert '01/01/2019' == serializer.data['dt_updated']


@pytest.mark.django_db
class TestGeologiaSerializerCamadas:

    @pytest.fixture(autouse=True)
    def deflators(self):
        mommy.make(
            Deflator,
            year=date(2017, 1, 1),
            index_number=Decimal(0.2))

        mommy.make(
            Deflator,
            year=date(2018, 1, 1),
            index_number=Decimal(0.5))

    @patch.object(GeologiaSerializer, '_get_empenhado_data_by_year')
    @patch.object(GeologiaSerializer, '_get_orcado_data_by_year')
    def test_prepare_camadas_data(self, mock_orcado, mock_empenhado):
        mock_orcado.return_value = 'mock_o'
        mock_empenhado.return_value = 'mock_e'

        execs_2017 = mommy.make(
            Execucao,
            year=date(2017, 1, 1),
            _quantity=2)
        execs_2018 = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            _quantity=2)
        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer(execucoes)
        ret = serializer.prepare_data()

        expected = {
            'orcado': ['mock_o', 'mock_o'],
            'empenhado': ['mock_e', 'mock_e'],
        }

        assert expected == ret

        execs = [execs_2017, execs_2018]
        for exec_year, call in zip(execs, mock_orcado.mock_calls):
            assert set(exec_year) == set(call[1][0])
        for exec_year, call in zip(execs, mock_empenhado.mock_calls):
            assert set(exec_year) == set(call[1][0])

    @patch.object(GeologiaSerializer, "_get_orcado_gnds_list",
                  Mock(return_value=[]))
    def test_get_orcado_data_by_year(self, orcado_fixture):
        gnds, orcado_total = orcado_fixture

        year = date(2017, 1, 1)
        deflator = Deflator.objects.get(year=year)
        orcado_total = orcado_total / deflator.index_number

        mommy.make(
            Execucao,
            year=year,
            orcado_atualizado=cycle([gnd['orcado'] for gnd in gnds]),
            _quantity=3)
        execucoes = Execucao.objects.all()

        expected = {
            "year": year.strftime("%Y"),
            "total": orcado_total,
            "gnds": [],
        }

        serializer = GeologiaSerializer([])
        ret = serializer._get_orcado_data_by_year(execucoes)

        assert expected == ret

    @patch.object(GeologiaSerializer, "_get_empenhado_gnds_list",
                  Mock(return_value=[]))
    def test_get_empenhado_data_by_year(self, empenhado_fixture):
        gnds, empenhado_total = empenhado_fixture

        year = date(2017, 1, 1)
        deflator = Deflator.objects.get(year=year)
        empenhado_total = empenhado_total / deflator.index_number

        mommy.make(
            Execucao,
            year=year,
            empenhado_liquido=cycle([gnd['empenhado'] for gnd in gnds]),
            _quantity=3)
        execucoes = Execucao.objects.all()

        expected = {
            "year": year.strftime("%Y"),
            "total": empenhado_total,
            "gnds": [],
        }

        serializer = GeologiaSerializer([])
        ret = serializer._get_empenhado_data_by_year(execucoes)

        assert expected == ret


@pytest.mark.django_db
class TestGeologiaSerializerSubfuncao:

    @patch.object(GeologiaSerializer, '_get_empenhado_data_by_year')
    @patch.object(GeologiaSerializer, '_get_orcado_data_by_year')
    def test_prepare_subfuncao_data(self, mock_orcado, mock_empenhado):
        mock_orcado.return_value = 'mock_o'
        mock_empenhado.return_value = 'mock_e'

        subfuncao_id = 1

        execs_2017_p1 = mommy.make(
            Execucao,
            year=date(2017, 1, 1),
            subfuncao__id=subfuncao_id,
            _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), subfuncao__id=2,
                   _quantity=2)
        execs_2018_p1 = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            subfuncao__id=subfuncao_id,
            _quantity=2)
        mommy.make(Execucao, year=date(2018, 1, 1), subfuncao__id=2,
                   _quantity=2)

        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer(execucoes, subfuncao_id=subfuncao_id)
        ret = serializer.prepare_data(subfuncao_id=subfuncao_id)

        expected = {
            'subfuncao_id': subfuncao_id,
            'orcado': ['mock_o', 'mock_o'],
            'empenhado': ['mock_e', 'mock_e'],
        }

        assert expected == ret

        execs = [execs_2017_p1, execs_2018_p1]
        for exec_year, call in zip(execs, mock_orcado.mock_calls):
            assert set(exec_year) == set(call[1][0])
        for exec_year, call in zip(execs, mock_empenhado.mock_calls):
            assert set(exec_year) == set(call[1][0])


@pytest.mark.django_db
class TestGeologiaSerializerSubgrupo:

    @pytest.fixture(autouse=True)
    def deflators(self):
        mommy.make(
            Deflator,
            year=date(2017, 1, 1),
            index_number=Decimal(0.2))

        mommy.make(
            Deflator,
            year=date(2018, 1, 1),
            index_number=Decimal(0.5))

    @patch.object(GeologiaSerializer, 'get_subgrupo_year_empenhado_data')
    @patch.object(GeologiaSerializer, 'get_subgrupo_year_orcado_data')
    def test_prepare_subgrupo_data(self, mock_orcado, mock_empenhado):
        mock_orcado.return_value = 'mock_o'
        mock_empenhado.return_value = 'mock_e'

        execs_2017 = mommy.make(
            Execucao,
            year=date(2017, 1, 1),
            subgrupo__id=1,
            _quantity=2)
        execs_2018 = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            subgrupo__id=1,
            _quantity=2)

        # not expected
        mommy.make(Execucao, year=date(2017, 1, 1), subgrupo=None)

        execucoes = Execucao.objects.filter(subgrupo__isnull=False)

        serializer = GeologiaSerializer(execucoes)
        ret = serializer.prepare_subgrupo_data()

        expected = {
            'orcado': ['mock_o', 'mock_o'],
            'empenhado': ['mock_e', 'mock_e'],
        }

        assert expected == ret

        execs = [execs_2017, execs_2018]
        for exec_year, call in zip(execs, mock_orcado.mock_calls):
            assert set(exec_year) == set(call[1][0])
        for exec_year, call in zip(execs, mock_empenhado.mock_calls):
            assert set(exec_year) == set(call[1][0])

    @patch.object(GeologiaSerializer, 'get_subgrupo_year_empenhado_data')
    @patch.object(GeologiaSerializer, 'get_subgrupo_year_orcado_data')
    def test_filters_data_before_2010(self, mock_orcado, mock_empenhado):
        mock_orcado.return_value = 'mock_o'
        mock_empenhado.return_value = 'mock_e'

        # not expected
        mommy.make(
            Execucao,
            year=date(2009, 1, 1),
            subgrupo__id=1)

        exec_2010 = mommy.make(
            Execucao,
            year=date(2010, 1, 1),
            subgrupo__id=1)
        execucoes = Execucao.objects.filter(subgrupo__isnull=False)

        serializer = GeologiaSerializer(execucoes)
        ret = serializer.prepare_subgrupo_data()

        expected = {
            'orcado': ['mock_o'],
            'empenhado': ['mock_e'],
        }

        assert expected == ret

        assert 1 == mock_orcado.call_count
        assert [exec_2010] == list(mock_orcado.call_args[0][0])

        assert 1 == mock_empenhado.call_count
        assert [exec_2010] == list(mock_empenhado.call_args[0][0])

    @patch.object(GeologiaSerializer, 'get_subgrupo_orcado_data')
    def test_get_subgrupo_year_orcado_data(self, mock_orcado):
        mock_orcado.return_value = 'mock_o'

        subgrupo1 = mommy.make(Subgrupo, desc="Uniceu")
        subgrupo2 = mommy.make(Subgrupo, desc="Alimentação Escolar")

        year = date(2018, 1, 1)
        execs_sub1 = mommy.make(
            Execucao,
            year=year,
            subgrupo=subgrupo1,
            _quantity=2)
        execs_sub2 = mommy.make(
            Execucao,
            year=year,
            subgrupo=subgrupo2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer([])
        ret = serializer.get_subgrupo_year_orcado_data(execucoes)

        expected = {
            'year': year.strftime('%Y'),
            'subgrupos': ['mock_o', 'mock_o'],
        }

        assert expected == ret

        execs = [execs_sub2, execs_sub1]  # Alphabetical order
        for exec_subgrupo, call in zip(execs, mock_orcado.mock_calls):
            assert set(exec_subgrupo) == set(call[1][0])

    @patch.object(GeologiaSerializer, 'get_subgrupo_empenhado_data')
    def test_get_subgrupo_year_empenhado_data(self, mock_empenhado):
        mock_empenhado.return_value = 'mock_e'

        subgrupo1 = mommy.make(Subgrupo, desc="Uniceu")
        subgrupo2 = mommy.make(Subgrupo, desc="Alimentação Escolar")

        year = date(2018, 1, 1)
        execs_sub1 = mommy.make(
            Execucao,
            year=year,
            subgrupo=subgrupo1,
            _quantity=2)
        execs_sub2 = mommy.make(
            Execucao,
            year=year,
            subgrupo=subgrupo2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer([])
        ret = serializer.get_subgrupo_year_empenhado_data(execucoes)

        expected = {
            'year': year.strftime('%Y'),
            'subgrupos': ['mock_e', 'mock_e'],
        }

        assert expected == ret

        execs = [execs_sub2, execs_sub1]  # Alphabetical order
        for exec_subgrupo, call in zip(execs, mock_empenhado.mock_calls):
            assert set(exec_subgrupo) == set(call[1][0])

    @patch.object(GeologiaSerializer, "_get_orcado_gnds_list",
                  Mock(return_value=[]))
    def test_get_subgrupo_orcado_data(self, orcado_fixture):
        gnds, orcado_total = orcado_fixture

        year = date(2017, 1, 1)
        deflator = Deflator.objects.get(year=year)
        orcado_total = orcado_total / deflator.index_number

        subgrupo = mommy.make(Subgrupo, id=1)
        mommy.make(
            Execucao,
            year=year,
            orcado_atualizado=cycle([gnd['orcado'] for gnd in gnds]),
            subgrupo=subgrupo,
            _quantity=3)
        execucoes = Execucao.objects.all()

        expected = {
            "subgrupo": subgrupo.desc,
            "total": orcado_total,
            "gnds": [],
        }

        serializer = GeologiaSerializer([])
        ret = serializer.get_subgrupo_orcado_data(execucoes)

        assert expected == ret

    @patch.object(GeologiaSerializer, "_get_empenhado_gnds_list",
                  Mock(return_value=[]))
    def test_get_subgrupo_empenhado_data(self, empenhado_fixture):
        gnds, empenhado_total = empenhado_fixture

        year = date(2017, 1, 1)
        deflator = Deflator.objects.get(year=year)
        empenhado_total = empenhado_total / deflator.index_number

        subgrupo = mommy.make(Subgrupo, id=1)
        mommy.make(
            Execucao,
            year=year,
            empenhado_liquido=cycle([gnd['empenhado'] for gnd in gnds]),
            subgrupo=subgrupo,
            _quantity=3)
        execucoes = Execucao.objects.all()

        expected = {
            'subgrupo': subgrupo.desc,
            "total": empenhado_total,
            "gnds": [],
        }

        serializer = GeologiaSerializer([])
        ret = serializer.get_subgrupo_empenhado_data(execucoes)

        assert expected == ret


@pytest.mark.django_db
class TestGeologiaSerializerGnds:
    def test_serialize_list_of_gnds(self):
        mommy.make(Execucao, subgrupo__id=1)

        gnd_1 = mommy.make('GndGeologia',  desc='Consultoria',
                           slug='consulting')
        gnd_2 = mommy.make('GndGeologia',  desc='Custeio operacional',
                           slug='operational')
        gnds = [gnd_1, gnd_2]
        expected = [dict(slug=gnd.slug, desc=gnd.desc) for gnd in gnds]

        queryset = Execucao.objects.all()
        serialized = GeologiaSerializer(queryset).data

        assert expected == serialized.get('gnds')


@pytest.mark.django_db
class TestGeologiaSerializerSubfuncoes:
    def test_serialize_list_of_subfuncoes(self):
        subfuncao_1 = mommy.make('Subfuncao',  desc='Turismo')
        subfuncao_2 = mommy.make('Subfuncao',  desc='Educação Infantil')
        subfuncoes = [subfuncao_1, subfuncao_2]
        expected = [dict(id=subfuncao.id, desc=subfuncao.desc,
                         selecionado=False)
                    for subfuncao in subfuncoes]

        # selected funcao
        subfuncao_3 = mommy.make('Subfuncao',  desc='Selected Function')
        expected.append(dict(id=subfuncao_3.id, desc=subfuncao_3.desc,
                             selecionado=True))
        expected.sort(key=lambda s: s['desc'])

        mommy.make(
            Execucao, subfuncao=cycle([subfuncao_1, subfuncao_2, subfuncao_3]),
            _quantity=3)
        queryset = Execucao.objects.all()

        # not expected
        mommy.make('Subfuncao')

        serialized = GeologiaSerializer(queryset,
                                        subfuncao_id=subfuncao_3.id).data

        assert expected == serialized.get('subfuncoes')


@pytest.mark.django_db
class TestGndGeologiaSerializer:
    def test_serialize_data(self):
        gnd = mommy.make('GndGeologia',  desc='Consultoria', slug='consulting')
        expected = dict(slug=gnd.slug, desc=gnd.desc)
        assert expected == GndGeologiaSerializer(gnd).data


@pytest.mark.django_db
class TestSubfuncaoSerializer:
    def test_serialize_data(self):
        subfuncao = mommy.make('Subfuncao',  desc='Turismo')
        expected = dict(id=subfuncao.id, desc=subfuncao.desc, selecionado=False)
        assert expected == SubfuncaoSerializer(subfuncao).data


@pytest.mark.django_db
class TestGeologiaDownloadSerializer:

    def test_serializes_camadas_chart_data(self):
        gnd1 = mommy.make(GndGeologia, desc='gnd1')
        gnd2 = mommy.make(GndGeologia, desc='gnd2')
        mommy.make(Execucao, year=date(2017, 1, 1), gnd_geologia=gnd1,
                   orcado_atualizado=100, empenhado_liquido=5, _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), gnd_geologia=gnd2,
                   orcado_atualizado=150, empenhado_liquido=15, _quantity=2)

        mommy.make(Execucao, year=date(2018, 1, 1), gnd_geologia=gnd1,
                   orcado_atualizado=10, empenhado_liquido=0.5, _quantity=2)
        mommy.make(Execucao, year=date(2018, 1, 1), gnd_geologia=gnd2,
                   orcado_atualizado=15, empenhado_liquido=2, _quantity=2)

        expected = [
            {
                "ano": 2017,
                "gnd": 'gnd1',
                "orcado": Decimal(200),
                "orcado_total": Decimal(500),
                "orcado_percentual": Decimal('0.4'),
                "empenhado": Decimal(10),
                "empenhado_total": Decimal(40),
                "empenhado_percentual": Decimal('0.25'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd2',
                "orcado": Decimal(300),
                "orcado_total": Decimal(500),
                "orcado_percentual": Decimal('0.6'),
                "empenhado": Decimal(30),
                "empenhado_total": Decimal(40),
                "empenhado_percentual": Decimal('0.75'),
            },
            {
                "ano": 2018,
                "gnd": 'gnd1',
                "orcado": Decimal(20),
                "orcado_total": Decimal(50),
                "orcado_percentual": Decimal('0.4'),
                "empenhado": Decimal(1),
                "empenhado_total": Decimal(5),
                "empenhado_percentual": Decimal('0.2'),
            },
            {
                "ano": 2018,
                "gnd": 'gnd2',
                "orcado": Decimal(30),
                "orcado_total": Decimal(50),
                "orcado_percentual": Decimal('0.6'),
                "empenhado": Decimal(4),
                "empenhado_total": Decimal(5),
                "empenhado_percentual": Decimal('0.8'),
            },
        ]

        execucoes = Execucao.objects.all()
        serializer = GeologiaDownloadSerializer(execucoes, 'camadas')

        assert expected == serializer.data

    def test_serializes_subfuncao_chart_data(self):
        subfuncao1 = mommy.make(Subfuncao, desc='subfuncao1')
        subfuncao2 = mommy.make(Subfuncao, desc='subfuncao2')
        gnd1 = mommy.make(GndGeologia, desc='gnd1')
        gnd2 = mommy.make(GndGeologia, desc='gnd2')

        mommy.make(Execucao, year=date(2017, 1, 1), subfuncao=subfuncao1,
                   gnd_geologia=gnd1, orcado_atualizado=100,
                   empenhado_liquido=5, _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), subfuncao=subfuncao1,
                   gnd_geologia=gnd2, orcado_atualizado=150,
                   empenhado_liquido=15, _quantity=2)

        mommy.make(Execucao, year=date(2017, 1, 1), subfuncao=subfuncao2,
                   gnd_geologia=gnd1, orcado_atualizado=5,
                   empenhado_liquido=1, _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), subfuncao=subfuncao2,
                   gnd_geologia=gnd2, orcado_atualizado=15,
                   empenhado_liquido=3, _quantity=2)

        mommy.make(Execucao, year=date(2018, 1, 1), subfuncao=subfuncao1,
                   gnd_geologia=gnd1, orcado_atualizado=10,
                   empenhado_liquido=0.5, _quantity=2)
        mommy.make(Execucao, year=date(2018, 1, 1), subfuncao=subfuncao1,
                   gnd_geologia=gnd2, orcado_atualizado=15,
                   empenhado_liquido=2, _quantity=2)

        expected = [
            {
                "ano": 2017,
                "gnd": 'gnd1',
                "subfuncao": 'subfuncao1',
                "orcado": Decimal(200),
                "orcado_total": Decimal(500),
                "orcado_percentual": Decimal('0.4'),
                "empenhado": Decimal(10),
                "empenhado_total": Decimal(40),
                "empenhado_percentual": Decimal('0.25'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd2',
                "subfuncao": 'subfuncao1',
                "orcado": Decimal(300),
                "orcado_total": Decimal(500),
                "orcado_percentual": Decimal('0.6'),
                "empenhado": Decimal(30),
                "empenhado_total": Decimal(40),
                "empenhado_percentual": Decimal('0.75'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd1',
                "subfuncao": 'subfuncao2',
                "orcado": Decimal(10),
                "orcado_total": Decimal(40),
                "orcado_percentual": Decimal('0.25'),
                "empenhado": Decimal(2),
                "empenhado_total": Decimal(8),
                "empenhado_percentual": Decimal('0.25'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd2',
                "subfuncao": 'subfuncao2',
                "orcado": Decimal(30),
                "orcado_total": Decimal(40),
                "orcado_percentual": Decimal('0.75'),
                "empenhado": Decimal(6),
                "empenhado_total": Decimal(8),
                "empenhado_percentual": Decimal('0.75'),
            },
            {
                "ano": 2018,
                "gnd": 'gnd1',
                "subfuncao": 'subfuncao1',
                "orcado": Decimal(20),
                "orcado_total": Decimal(50),
                "orcado_percentual": Decimal('0.4'),
                "empenhado": Decimal(1),
                "empenhado_total": Decimal(5),
                "empenhado_percentual": Decimal('0.2'),
            },
            {
                "ano": 2018,
                "gnd": 'gnd2',
                "subfuncao": 'subfuncao1',
                "orcado": Decimal(30),
                "orcado_total": Decimal(50),
                "orcado_percentual": Decimal('0.6'),
                "empenhado": Decimal(4),
                "empenhado_total": Decimal(5),
                "empenhado_percentual": Decimal('0.8'),
            },
        ]

        execucoes = Execucao.objects.all()
        serializer = GeologiaDownloadSerializer(execucoes, 'subfuncao')

        assert len(expected) == len(serializer.data)
        for item in expected:
            assert item in serializer.data

    def test_serializes_subgrupo_chart_data(self):
        subgrupo1 = mommy.make(Subgrupo, desc='subgrupo1')
        subgrupo2 = mommy.make(Subgrupo, desc='subgrupo2')
        gnd1 = mommy.make(GndGeologia, desc='gnd1')
        gnd2 = mommy.make(GndGeologia, desc='gnd2')

        mommy.make(Execucao, year=date(2017, 1, 1), subgrupo=subgrupo1,
                   gnd_geologia=gnd1, orcado_atualizado=100,
                   empenhado_liquido=5, _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), subgrupo=subgrupo1,
                   gnd_geologia=gnd2, orcado_atualizado=150,
                   empenhado_liquido=15, _quantity=2)

        mommy.make(Execucao, year=date(2017, 1, 1), subgrupo=subgrupo2,
                   gnd_geologia=gnd1, orcado_atualizado=5,
                   empenhado_liquido=1, _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), subgrupo=subgrupo2,
                   gnd_geologia=gnd2, orcado_atualizado=15,
                   empenhado_liquido=3, _quantity=2)

        mommy.make(Execucao, year=date(2018, 1, 1), subgrupo=subgrupo1,
                   gnd_geologia=gnd1, orcado_atualizado=10,
                   empenhado_liquido=0.5, _quantity=2)
        mommy.make(Execucao, year=date(2018, 1, 1), subgrupo=subgrupo1,
                   gnd_geologia=gnd2, orcado_atualizado=15,
                   empenhado_liquido=2, _quantity=2)

        expected = [
            {
                "ano": 2017,
                "gnd": 'gnd1',
                "subgrupo": 'subgrupo1',
                "orcado": Decimal(200),
                "orcado_total": Decimal(500),
                "orcado_percentual": Decimal('0.4'),
                "empenhado": Decimal(10),
                "empenhado_total": Decimal(40),
                "empenhado_percentual": Decimal('0.25'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd2',
                "subgrupo": 'subgrupo1',
                "orcado": Decimal(300),
                "orcado_total": Decimal(500),
                "orcado_percentual": Decimal('0.6'),
                "empenhado": Decimal(30),
                "empenhado_total": Decimal(40),
                "empenhado_percentual": Decimal('0.75'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd1',
                "subgrupo": 'subgrupo2',
                "orcado": Decimal(10),
                "orcado_total": Decimal(40),
                "orcado_percentual": Decimal('0.25'),
                "empenhado": Decimal(2),
                "empenhado_total": Decimal(8),
                "empenhado_percentual": Decimal('0.25'),
            },
            {
                "ano": 2017,
                "gnd": 'gnd2',
                "subgrupo": 'subgrupo2',
                "orcado": Decimal(30),
                "orcado_total": Decimal(40),
                "orcado_percentual": Decimal('0.75'),
                "empenhado": Decimal(6),
                "empenhado_total": Decimal(8),
                "empenhado_percentual": Decimal('0.75'),
            },
            {
                "ano": 2018,
                "gnd": 'gnd1',
                "subgrupo": 'subgrupo1',
                "orcado": Decimal(20),
                "orcado_total": Decimal(50),
                "orcado_percentual": Decimal('0.4'),
                "empenhado": Decimal(1),
                "empenhado_total": Decimal(5),
                "empenhado_percentual": Decimal('0.2'),
            },
            {
                "ano": 2018,
                "gnd": 'gnd2',
                "subgrupo": 'subgrupo1',
                "orcado": Decimal(30),
                "orcado_total": Decimal(50),
                "orcado_percentual": Decimal('0.6'),
                "empenhado": Decimal(4),
                "empenhado_total": Decimal(5),
                "empenhado_percentual": Decimal('0.8'),
            },
        ]

        execucoes = Execucao.objects.all()
        serializer = GeologiaDownloadSerializer(execucoes, 'subgrupo')

        assert len(expected) == len(serializer.data)
        for item in expected:
            assert item in serializer.data
