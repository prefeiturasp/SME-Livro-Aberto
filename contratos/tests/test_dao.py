import pytest

from unittest import TestCase

from model_mommy import mommy

from contratos.dao import contratos_raw_dao
from contratos.models import ContratoRaw


@pytest.mark.django_db
class ContratosRawDAOTestCase(TestCase):

    def test_get_all(self):
        expected_contratos = mommy.make(ContratoRaw, _quantity=2)

        ret = contratos_raw_dao.get_all()

        assert 2 == len(ret)
        for contrato in expected_contratos:
            assert contrato in ret
