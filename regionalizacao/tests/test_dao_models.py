import os

import pytest

from django.core.files import File
from model_mommy import mommy

from regionalizacao.models import (
    PtrfFromTo,
    PtrfFromToSpreadsheet,
    DistritoZonaFromTo,
    DistritoZonaFromToSpreadsheet,
    EtapaTipoEscolaFromTo,
    EtapaTipoEscolaFromToSpreadsheet,
)


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
        # data is extracted on save

        fts = PtrfFromTo.objects.all().order_by('id')
        assert 2 == len(fts)

        codescs = [400003, 400010]

        assert fts[0].codesc == codescs[0]
        assert fts[0].vlrepasse == 2.55

        assert fts[1].codesc == codescs[1]
        assert fts[1].vlrepasse == 1.99

        sheet.refresh_from_db()
        assert sheet.extracted is True
        assert codescs == sheet.added_fromtos
        assert [] == sheet.not_added_fromtos


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
        assert [] == sheet.not_added_fromtos


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
        assert [] == sheet.not_added_fromtos
