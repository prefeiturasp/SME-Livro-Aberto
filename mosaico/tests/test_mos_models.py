import os

import pytest

from datetime import date

from model_mommy import mommy

from django.core.files import File

from budget_execution.models import MinimoLegal
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
            year=2018,
            spreadsheet=File(file_fixture),
            title_25percent="25 PERCENT TEST BEGIN",
            limit_25percent="25 PERCENT TEST FINISH",
            title_6percent="6 PERCENT TEST BEGIN",
            limit_6percent="6 PERCENT TEST FINISH",
        )
        ssheet_obj.extract_data()

        mls = MinimoLegal.objects.all().order_by('id')
        assert 5 == len(mls)

        # 25 percent dotação
        assert mls[0].year == date(2018, 1, 1)
        assert mls[0].projeto_id == 1111
        assert mls[0].projeto_desc == "Project test 1"
        assert mls[0].orcado_atualizado == 100
        assert mls[0].empenhado_liquido == 50

        # 6 percent dotação
        assert mls[3].year == date(2018, 1, 1)
        assert mls[3].projeto_id == 4444
        assert mls[3].projeto_desc == "Project test 4"
        assert mls[3].orcado_atualizado == 400
        assert mls[3].empenhado_liquido == 200
