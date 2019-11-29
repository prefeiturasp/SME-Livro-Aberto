import pytest

from itertools import cycle
from unittest import TestCase

from model_mommy import mommy

from regionalizacao.models import Distrito, DistritoZonaFromTo
from regionalizacao.services import apply_distrito_zona_fromto


@pytest.mark.django_db
class TestApplyDistritoZonaFromTo(TestCase):

    def test_apply_distrito_zona_fromto(self):
        mommy.make(Distrito, coddist=cycle([1, 2]), zona=None, _quantity=2)
        mommy.make(Distrito, coddist=3, zona=None)

        mommy.make(DistritoZonaFromTo, coddist=cycle([1, 2]), zona="Norte",
                   _quantity=2)
        mommy.make(DistritoZonaFromTo, coddist=3, zona="Sul")

        apply_distrito_zona_fromto()

        distritos = Distrito.objects.all().order_by('coddist')
        assert distritos[0].zona == "Norte"
        assert distritos[1].zona == "Norte"
        assert distritos[2].zona == "Sul"
