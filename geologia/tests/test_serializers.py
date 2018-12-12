import pytest

from datetime import date
from decimal import Decimal
from itertools import cycle
from unittest.mock import Mock, patch

from model_mommy import mommy

from budget_execution.models import Execucao, Subfuncao
from geologia.serializers import GeologiaSerializer


@pytest.fixture
def orcado_fixture():
    gnds_dict = [
        {'gnd_gealogia__desc': 'gnd1', 'orcado': Decimal(10)},
        {'gnd_gealogia__desc': 'gnd2', 'orcado': Decimal(20)},
        {'gnd_gealogia__desc': 'gnd3', 'orcado': Decimal(30)},
    ]
    orcado_total = Decimal(60)
    return gnds_dict, orcado_total


@pytest.fixture
def empenhado_fixture():
    gnds_dict = [
        {'gnd_gealogia__desc': 'gnd1', 'empenhado': Decimal(10)},
        {'gnd_gealogia__desc': 'gnd2', 'empenhado': Decimal(20)},
        # must support None for empenhado
        {'gnd_gealogia__desc': 'gnd3', 'empenhado': None},
    ]
    empenhado_total = Decimal(30)
    return gnds_dict, empenhado_total


@pytest.mark.django_db
class TestGeologiaSerializerCore:
    def test_get_orcado_gnds_list(self, orcado_fixture):
        gnds, orcado_total = orcado_fixture

        expected = [
            {
                "name": gnd['gnd_gealogia__desc'],
                "value": gnd['orcado'],
                "percent": gnd['orcado'] / orcado_total
            }
            for gnd in gnds
        ]

        serializer = GeologiaSerializer([])
        ret = serializer._get_orcado_gnds_list(gnds, orcado_total)

        assert expected == ret

    def test_get_empenhado_gnds_list(self, empenhado_fixture):
        gnds, empenhado_total = empenhado_fixture
        expected = []
        for gnd in gnds:
            if gnd['empenhado'] is None:
                gnd['empenhado'] = 0

            expected.append({
                "name": gnd['gnd_gealogia__desc'],
                "value": gnd['empenhado'],
                "percent": gnd['empenhado'] / empenhado_total
            })

        serializer = GeologiaSerializer([])
        ret = serializer._get_empenhado_gnds_list(
            gnds, empenhado_total)

        assert expected == ret

    def test_get_empenhado_gnd_list_when_total_is_none(self):
        gnds_dicts = [
            {'gnd_gealogia__desc': 'gnd1', 'empenhado': None},
            {'gnd_gealogia__desc': 'gnd2', 'empenhado': None},
        ]
        empenhado_total = None

        serializer = GeologiaSerializer([])
        assert serializer._get_empenhado_gnds_list(gnds_dicts, empenhado_total)

    def test_calculate_percent(self):
        serializer = GeologiaSerializer([])
        assert 0 == serializer._calculate_percent(None, 100)
        assert 0 == serializer._calculate_percent(10, None)
        assert 0.1 == serializer._calculate_percent(10, 100)


@pytest.mark.django_db
class TestGeologiaSerializerCamadas:

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
        ret = serializer.prepare_camadas_data()

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
class TestGeologiaSerializerPrograma:

    @patch.object(GeologiaSerializer, '_get_empenhado_data_by_year')
    @patch.object(GeologiaSerializer, '_get_orcado_data_by_year')
    def test_prepare_programa_data(self, mock_orcado, mock_empenhado):
        mock_orcado.return_value = 'mock_o'
        mock_empenhado.return_value = 'mock_e'

        execs_2017_p1 = mommy.make(
            Execucao,
            year=date(2017, 1, 1),
            programa_id=1,
            _quantity=2)
        mommy.make(Execucao, year=date(2017, 1, 1), programa_id=2, _quantity=2)
        execs_2018_p1 = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            programa_id=1,
            _quantity=2)
        mommy.make(Execucao, year=date(2018, 1, 1), programa_id=2, _quantity=2)

        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer(execucoes, programa_id=1)
        ret = serializer.prepare_programa_data()

        expected = {
            'programa_id': 1,
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
class TestGeologiaSerializerSubfuncao:

    @patch.object(GeologiaSerializer, 'get_subfuncao_year_empenhado_data')
    @patch.object(GeologiaSerializer, 'get_subfuncao_year_orcado_data')
    def test_prepare_subfuncao_data(self, mock_orcado, mock_empenhado):
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
        ret = serializer.prepare_subfuncao_data()

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

    @patch.object(GeologiaSerializer, 'get_subfuncao_orcado_data')
    def test_get_subfuncao_year_orcado_data(self, mock_orcado):
        mock_orcado.return_value = 'mock_o'

        year = date(2018, 1, 1)
        execs_sub1 = mommy.make(
            Execucao,
            year=year,
            subfuncao_id=1,
            _quantity=2)
        execs_sub2 = mommy.make(
            Execucao,
            year=year,
            subfuncao_id=2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer([])
        ret = serializer.get_subfuncao_year_orcado_data(execucoes)

        expected = {
            'year': year.strftime('%Y'),
            'subfuncoes': ['mock_o', 'mock_o'],
        }

        assert expected == ret

        execs = [execs_sub1, execs_sub2]
        for exec_subfuncao, call in zip(execs, mock_orcado.mock_calls):
            assert set(exec_subfuncao) == set(call[1][0])

    @patch.object(GeologiaSerializer, 'get_subfuncao_empenhado_data')
    def test_get_subfuncao_year_empenhado_data(self, mock_empenhado):
        mock_empenhado.return_value = 'mock_e'

        year = date(2018, 1, 1)
        execs_sub1 = mommy.make(
            Execucao,
            year=year,
            subfuncao_id=1,
            _quantity=2)
        execs_sub2 = mommy.make(
            Execucao,
            year=year,
            subfuncao_id=2,
            _quantity=2)
        execucoes = Execucao.objects.all()

        serializer = GeologiaSerializer([])
        ret = serializer.get_subfuncao_year_empenhado_data(execucoes)

        expected = {
            'year': year.strftime('%Y'),
            'subfuncoes': ['mock_e', 'mock_e'],
        }

        assert expected == ret

        execs = [execs_sub1, execs_sub2]
        for exec_subfuncao, call in zip(execs, mock_empenhado.mock_calls):
            assert set(exec_subfuncao) == set(call[1][0])

    @patch.object(GeologiaSerializer, "_get_orcado_gnds_list",
                  Mock(return_value=[]))
    def test_get_subfuncao_orcado_data(self, orcado_fixture):
        gnds, orcado_total = orcado_fixture

        year = date(2017, 1, 1)
        subfuncao = mommy.make(Subfuncao)
        mommy.make(
            Execucao,
            year=year,
            orcado_atualizado=cycle([gnd['orcado'] for gnd in gnds]),
            subfuncao=subfuncao,
            _quantity=3)
        execucoes = Execucao.objects.all()

        expected = {
            "subfuncao": subfuncao.desc,
            "total": orcado_total,
            "gnds": [],
        }

        serializer = GeologiaSerializer([])
        ret = serializer.get_subfuncao_orcado_data(execucoes)

        assert expected == ret

    @patch.object(GeologiaSerializer, "_get_empenhado_gnds_list",
                  Mock(return_value=[]))
    def test_get_subfuncao_empenhado_data(self, empenhado_fixture):
        gnds, empenhado_total = empenhado_fixture

        year = date(2017, 1, 1)
        subfuncao = mommy.make(Subfuncao)
        mommy.make(
            Execucao,
            year=year,
            empenhado_liquido=cycle([gnd['empenhado'] for gnd in gnds]),
            subfuncao=subfuncao,
            _quantity=3)
        execucoes = Execucao.objects.all()

        expected = {
            'subfuncao': subfuncao.desc,
            "total": empenhado_total,
            "gnds": [],
        }

        serializer = GeologiaSerializer([])
        ret = serializer.get_subfuncao_empenhado_data(execucoes)

        assert expected == ret
