import os

import pytest

from model_mommy import mommy

from django.core.files import File

from budget_execution.models import MinimoLegalExecucao
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
        ssheet_obj = mommy.make(
            MinimoLegalSpreadsheetModel,
            spreadsheet=File(file_fixture),
            title_25percent="25 PERCENT TEST BEGIN",
            limit_25percent="25 PERCENT TEST FINISH",
            title_6percent="6 PERCENT TEST BEGIN",
            limit_6percent="6 PERCENT TEST FINISH",
        )
        ssheet_obj.extract_data()

        assert 5 == MinimoLegalExecucao.objects.count()
