import pytest
import requests

from unittest import TestCase
from unittest.mock import patch

from model_mommy import mommy

from regionalizacao.dao.eol_api_dao import (
    update_dre_table,
    update_tipo_escola_table,
)
from regionalizacao.models import Dre, TipoEscola


@pytest.mark.django_db
class TestUpdateDreTable(TestCase):

    @patch.object(requests, 'get')
    def test_populate_dre_table(self, mock_get):
        api_return = {
            "results": [
                {
                    "dre": "BT",
                    "diretoria": "DIRETORIA REGIONAL DE EDUCACAO BUTANTA",
                },
                {
                    "dre": "SA",
                    "diretoria": "DIRETORIA REGIONAL DE EDUCACAO SANTO AMARO"
                },
            ],
        }
        mock_get.return_value = api_return

        created, updated = update_dre_table()
        assert 2 == created
        assert 0 == updated

        dres = Dre.objects.all().order_by('code')
        assert 2 == dres.count()

        for dre, expected in zip(dres, api_return['results']):
            assert dre.code == expected['dre']
            assert dre.name == expected['diretoria']

    @patch.object(requests, 'get')
    def test_updates_existing_dre(self, mock_get):
        mommy.make(Dre, code="BT", name="old name")

        api_return = {
            "results": [
                {
                    "dre": "BT",
                    "diretoria": "DIRETORIA REGIONAL DE EDUCACAO BUTANTA",
                },
                {
                    "dre": "SA",
                    "diretoria": "DIRETORIA REGIONAL DE EDUCACAO SANTO AMARO"
                },
            ],
        }
        mock_get.return_value = api_return

        created, updated = update_dre_table()
        assert 1 == created
        assert 1 == updated

        dres = Dre.objects.all().order_by('code')
        assert 2 == dres.count()

        for dre, expected in zip(dres, api_return['results']):
            assert dre.code == expected['dre']
            assert dre.name == expected['diretoria']


@pytest.mark.django_db
class TestUpdateTipoEscolaTable(TestCase):

    @patch.object(requests, 'get')
    def test_populate_tipo_escola_table(self, mock_get):
        api_return = {
            "results": [
                {
                    "tipoesc": "CIEJA",
                },
                {
                    "tipoesc": "MOVA",
                },
            ],
        }
        mock_get.return_value = api_return

        created = update_tipo_escola_table()
        assert 2 == created

        tipos = TipoEscola.objects.all().order_by('code')
        assert 2 == tipos.count()

        for tipo, expected in zip(tipos, api_return['results']):
            assert tipo.code == expected['tipoesc']

    @patch.object(requests, 'get')
    def test_ignores_when_tipo_already_exist(self, mock_get):
        mommy.make(TipoEscola, code="CIEJA")

        api_return = {
            "results": [
                {
                    "tipoesc": "CIEJA",
                },
                {
                    "tipoesc": "MOVA",
                },
            ],
        }
        mock_get.return_value = api_return

        created = update_tipo_escola_table()
        assert 1 == created

        tipos = TipoEscola.objects.all().order_by('code')
        assert 2 == tipos.count()

        for tipo, expected in zip(tipos, api_return['results']):
            assert tipo.code == expected['tipoesc']
