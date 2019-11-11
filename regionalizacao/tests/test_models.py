import pytest

from unittest import TestCase
from unittest.mock import Mock, patch

from model_mommy import mommy

from regionalizacao.dao import models_dao
from regionalizacao.models import (
    DistritoZonaFromToSpreadsheet,
    PtrfFromToSpreadsheet,
)


@pytest.mark.django_db
class TestPtrfFromToSpreadsheet(TestCase):

    @patch.object(PtrfFromToSpreadsheet, 'extract_data')
    def test_calls_extract_data_on_save(self, mocked_extract):
        mommy.make(PtrfFromToSpreadsheet, extracted=False)
        mocked_extract.assert_called_once_with()

    @patch.object(PtrfFromToSpreadsheet, 'extract_data')
    def test_doesnt_call_extract_data_extracted_is_true(self, mocked_extract):
        mommy.make(PtrfFromToSpreadsheet, extracted=True)
        assert 0 == mocked_extract.call_count

    @patch.object(models_dao, 'PtrfFromToDao')
    def test_extract_data_calls_extract_service(self, MockDao):
        mocked_dao = Mock()
        MockDao.return_value = mocked_dao

        sheet = mommy.make(PtrfFromToSpreadsheet, extracted=False)

        mocked_dao.extract_spreadsheet.assert_called_once_with(sheet)


@pytest.mark.django_db
class TestDistritoZonaFromToSpreadsheet(TestCase):

    @patch.object(DistritoZonaFromToSpreadsheet, 'extract_data')
    def test_calls_extract_data_on_save(self, mocked_extract):
        mommy.make(DistritoZonaFromToSpreadsheet, extracted=False)
        mocked_extract.assert_called_once_with()

    @patch.object(DistritoZonaFromToSpreadsheet, 'extract_data')
    def test_doesnt_call_extract_data_extracted_is_true(self, mocked_extract):
        mommy.make(DistritoZonaFromToSpreadsheet, extracted=True)
        assert 0 == mocked_extract.call_count

    @patch.object(models_dao, 'DistritoZonaFromToDao')
    def test_extract_data_calls_extract_service(self, MockDao):
        mocked_dao = Mock()
        MockDao.return_value = mocked_dao

        sheet = mommy.make(DistritoZonaFromToSpreadsheet, extracted=False)

        mocked_dao.extract_spreadsheet.assert_called_once_with(sheet)
