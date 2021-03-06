import os

import pytest

from django.core.files import File
from rest_framework.test import APITestCase

from model_mommy import mommy

from regionalizacao.dao.models_dao import (
    DistritoDao,
    EscolaInfoDao,
    TipoEscolaDao,
)
from regionalizacao.models import (
    PtrfFromTo,
    PtrfFromToSpreadsheet,
    DistritoZonaFromTo,
    DistritoZonaFromToSpreadsheet,
    EtapaTipoEscolaFromTo,
    EtapaTipoEscolaFromToSpreadsheet,
    UnidadeRecursosFromTo,
    UnidadeRecursosFromToSpreadsheet,
)


class TestEscolaInfoDao(APITestCase):
    def test_get_newest_year(self):
        dao = EscolaInfoDao()

        assert None == EscolaInfoDao().get_newest_year()

        mommy.make(dao.model, year=2019)
        assert 2019 == EscolaInfoDao().get_newest_year()

        mommy.make(dao.model, year=2042)
        assert 2042 == EscolaInfoDao().get_newest_year()

        mommy.make(dao.model, year=2020)
        assert 2042 == EscolaInfoDao().get_newest_year()


class TestPtrfFromToDao:

    @pytest.fixture()
    def file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_PtrfFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in PtrfFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_extract_spreadsheet(self, file_fixture):
        sheet = mommy.make(
            PtrfFromToSpreadsheet, spreadsheet=File(file_fixture))
        sheet.extract_data()

        fts = PtrfFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        codescs = ['400003', '400010']

        assert fts[0].codesc == codescs[0]
        assert fts[0].vlrepasse == 2.55
        assert fts[0].year == sheet.year

        assert fts[1].codesc == codescs[1]
        assert fts[1].vlrepasse == 1.99
        assert fts[1].year == sheet.year

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert codescs == sheet.added_fromtos
        assert [] == sheet.updated_fromtos

    def test_replace_fromtos_of_the_same_year(self, file_fixture):
        mommy.make(PtrfFromTo, year=2018, _quantity=1)
        mommy.make(PtrfFromTo, year=2019, _quantity=2)

        sheet = mommy.make(
            PtrfFromToSpreadsheet, spreadsheet=File(file_fixture), year=2019)
        sheet.extract_data()

        fts = PtrfFromTo.objects.all().order_by('id')
        assert 3 == len(fts)
        assert 2 == fts.filter(year=2019).count()
        assert 1 == fts.filter(year=2018).count()


class TestDistritoZonaFromToDao:

    @pytest.fixture()
    def file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_DistritoZonaFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in DistritoZonaFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_extract_spreadsheet(self, file_fixture):
        sheet = mommy.make(
            DistritoZonaFromToSpreadsheet, spreadsheet=File(file_fixture))
        # data is extracted on save

        fts = DistritoZonaFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        coddists = [1, 2]

        assert fts[0].coddist == coddists[0]
        assert fts[0].zona == 'LESTE'

        assert fts[1].coddist == coddists[1]
        assert fts[1].zona == 'OESTE'

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert coddists == sheet.added_fromtos
        assert [] == sheet.updated_fromtos

    def test_update_value_when_fromto_exists(self, file_fixture):
        mommy.make(DistritoZonaFromTo, coddist=1, zona='other')

        sheet = mommy.make(
            DistritoZonaFromToSpreadsheet, spreadsheet=File(file_fixture))
        # data is extracted on save

        fts = DistritoZonaFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        coddists = [1, 2]

        assert fts[0].coddist == coddists[0]
        assert fts[0].zona == 'LESTE'

        assert fts[1].coddist == coddists[1]
        assert fts[1].zona == 'OESTE'

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert [2] == sheet.added_fromtos
        assert [1] == sheet.updated_fromtos


class TestEtapaTipoEscolaFromToDao:

    @pytest.fixture()
    def file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_EtapaTipoEscolaFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in EtapaTipoEscolaFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_extract_spreadsheet(self, file_fixture):
        sheet = mommy.make(
            EtapaTipoEscolaFromToSpreadsheet, spreadsheet=File(file_fixture))
        # data is extracted on save

        fts = EtapaTipoEscolaFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        tipoescs = ['CCI/CIPS', 'CEI DIRET']

        assert fts[0].tipoesc == tipoescs[0]
        assert fts[0].desctipoesc == 'desc1'
        assert fts[0].etapa == 'Infantil'

        assert fts[1].tipoesc == tipoescs[1]
        assert fts[1].desctipoesc == 'desc2'
        assert fts[1].etapa == 'Infantil tb'

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert tipoescs == sheet.added_fromtos
        assert [] == sheet.updated_fromtos

    def test_update_value_when_fromto_exists(self, file_fixture):
        mommy.make(EtapaTipoEscolaFromTo, tipoesc='CCI/CIPS', etapa='other')

        sheet = mommy.make(
            EtapaTipoEscolaFromToSpreadsheet, spreadsheet=File(file_fixture))
        # data is extracted on save

        fts = EtapaTipoEscolaFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        tipoescs = ['CCI/CIPS', 'CEI DIRET']

        assert fts[0].tipoesc == tipoescs[0]
        assert fts[0].desctipoesc == 'desc1'
        assert fts[0].etapa == 'Infantil'

        assert fts[1].tipoesc == tipoescs[1]
        assert fts[1].desctipoesc == 'desc2'
        assert fts[1].etapa == 'Infantil tb'

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert ['CEI DIRET'] == sheet.added_fromtos
        assert ['CCI/CIPS'] == sheet.updated_fromtos


class TestUnidadeRecursosFromToDao:

    @pytest.fixture()
    def file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__),
            'data/test_UnidadeRecursosFromToSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in UnidadeRecursosFromToSpreadsheet.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_extract_spreadsheet(self, file_fixture):
        sheet = mommy.make(
            UnidadeRecursosFromToSpreadsheet, spreadsheet=File(file_fixture))
        sheet.extract_data()

        fts = UnidadeRecursosFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        codescs = ['400415', '400415']

        assert fts[0].codesc == codescs[0]
        assert fts[0].grupo == 'Repasse'
        assert fts[0].subgrupo == 'IPTU'
        assert fts[0].valor == 1000
        assert fts[0].label == 'R$'
        assert fts[0].year == sheet.year

        assert fts[1].codesc == codescs[1]
        assert fts[1].grupo == 'Repasse'
        assert fts[1].subgrupo == 'Vagas Contratadas'
        assert fts[1].valor == 130
        assert fts[1].label == 'Unidades'
        assert fts[1].year == sheet.year

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert codescs == sheet.added_fromtos
        assert [] == sheet.updated_fromtos

    def test_replace_fromtos_of_the_same_year(self, file_fixture):
        mommy.make(UnidadeRecursosFromTo, year=2018, _quantity=1)
        mommy.make(UnidadeRecursosFromTo, year=2019, _quantity=2)

        sheet = mommy.make(
            UnidadeRecursosFromToSpreadsheet, spreadsheet=File(file_fixture),
            year=2019)
        sheet.extract_data()

        fts = UnidadeRecursosFromTo.objects.all().order_by('id')
        assert 3 == len(fts)
        assert 2 == fts.filter(year=2019).count()
        assert 1 == fts.filter(year=2018).count()


@pytest.mark.django_db
class TestDistritoDao:

    def test_get_doesnt_raise_exception_when_tipo_doesnt_exist(self):
        dao = DistritoDao()
        distrito = dao.get(coddist=1)
        assert distrito is None


@pytest.mark.django_db
class TestTipoEscolaDao:

    def test_get_doesnt_raise_exception_when_tipo_doesnt_exist(self):
        dao = TipoEscolaDao()
        tipo = dao.get(code='xxx')
        assert tipo is None
