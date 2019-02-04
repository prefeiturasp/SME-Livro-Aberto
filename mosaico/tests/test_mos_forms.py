import os

import pytest

from model_mommy import mommy

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.test import Client
from django.urls import reverse

from mosaico.models import MinimoLegalSpreadsheetModel


class TestMinimoLegalSpreadsheetAdminForm:

    @pytest.fixture()
    def file_fixture(self, db):
        user = mommy.make(User, username='admin', is_staff=True,
                          is_superuser=True)
        user.set_password('admin')
        user.save()

        filepath = os.path.join(
            os.path.dirname(__file__), 'data/test_MinimoLegalSpreadsheet.xlsx')
        with open(filepath, 'rb') as f:
            yield f

        for ssheet_obj in MinimoLegalSpreadsheetModel.objects.all():
            ssheet_obj.spreadsheet.delete()

    def test_prevents_upload_of_already_uploaded_file(self, file_fixture):
        spreadsheet_obj = mommy.make(
            MinimoLegalSpreadsheetModel,
            year=2018,
            spreadsheet=File(file_fixture),
            title_25percent="25 PERCENT TEST BEGIN",
            limit_25percent="25 PERCENT TEST FINISH",
            title_6percent="6 PERCENT TEST BEGIN",
            limit_6percent="6 PERCENT TEST FINISH",
        )
        assert 1 == MinimoLegalSpreadsheetModel.objects.count()

        client = Client()
        client.login(username='admin', password='admin')
        url = reverse('admin:mosaico_minimolegalspreadsheetmodel_add')

        fake_file = ContentFile(b'file content')
        fake_file.name = spreadsheet_obj.spreadsheet.name
        data = {
            'year': 2018,
            'spreadsheet': fake_file,
            'title_25percent': "25 PERCENT TEST BEGIN",
            'limit_25percent': "25 PERCENT TEST FINISH",
            'title_6percent': "6 PERCENT TEST BEGIN",
            'limit_6percent': "6 PERCENT TEST FINISH",
        }

        client.post(url, data)
        assert 1 == MinimoLegalSpreadsheetModel.objects.count()
