import pytest

from unittest import TestCase
from unittest.mock import patch

from model_mommy import mommy

from regionalizacao import services
from regionalizacao.models import PtrfFromToSpreadsheet


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

    @patch.object(services, 'extract_ptrf_spreadsheet')
    def test_extract_data_calls_extract_service(self, mock_extract):
        mock_extract.return_value = (['added'], ['not_added'])
        sheet = mommy.make(PtrfFromToSpreadsheet, extracted=False)

        sheet.refresh_from_db()
        assert sheet.added_fromtos == ['added']
        assert sheet.not_added_fromtos == ['not_added']
        assert sheet.extracted is True
