import os

import pytest

from model_mommy import mommy

from django.core.files import File

from mosaico.models import MinimoLegalSpreadsheetModel


class TestMinimoLegalSpreadsheetModel:

    @pytest.fixture()
    def file_fixture(self, db):
        filepath = os.path.join(
            os.path.dirname(__file__), 'data/test_MinimoLegalSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in MinimoLegalSpreadsheetModel.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_extract_data(self, file_fixture):
        ssheet_obj = mommy.make(MinimoLegalSpreadsheetModel,
                                spreadsheet=File(file_fixture))
        assert False
        pass
