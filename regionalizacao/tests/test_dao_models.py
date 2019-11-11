import os

import pytest

from django.core.files import File
from model_mommy import mommy

from regionalizacao.models import (
    PtrfFromTo,
    PtrfFromToSpreadsheet,
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
        assert list(map(str, codescs)) == sheet.added_fromtos
        assert [] == sheet.not_added_fromtos
