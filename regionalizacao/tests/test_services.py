import pytest

from itertools import cycle
from unittest import TestCase

from model_mommy import mommy

from regionalizacao.models import (
    Distrito, DistritoZonaFromTo, Escola, EtapaTipoEscolaFromTo, PtrfFromTo,
    TipoEscola)
from regionalizacao.services import (
    apply_distrito_zona_fromto,
    apply_etapa_tipo_escola_fromto,
    apply_ptrf_fromto,
)


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


@pytest.mark.django_db
class TestApplyEtapaTipoEscolaFromTo(TestCase):

    def test_apply_etapa_tipo_escola_fromto(self):
        mommy.make(TipoEscola, code='CEMEI', desc=None, etapa=None)
        mommy.make(TipoEscola, code='EMEF', desc=None, etapa=None)

        mommy.make(EtapaTipoEscolaFromTo, tipoesc='CEMEI', desctipoesc='desc 1',
                   etapa='Infantil')
        mommy.make(EtapaTipoEscolaFromTo, tipoesc='EMEF', desctipoesc="desc 2",
                   etapa='Fundamental')

        apply_etapa_tipo_escola_fromto()

        tipos = TipoEscola.objects.all().order_by('code')
        assert tipos[0].desc == "desc 1"
        assert tipos[0].etapa == "Infantil"
        assert tipos[1].desc == "desc 2"
        assert tipos[1].etapa == "Fundamental"


@pytest.mark.django_db
class TestApplyPtrfFromTo(TestCase):

    def test_apply_ptrf_fromto(self):
        mommy.make(Escola, codesc='01', year=2019, ptrf=None)
        mommy.make(Escola, codesc='02', year=2019, ptrf=None)
        mommy.make(Escola, codesc='01', year=2020, ptrf=None)

        ft1 = mommy.make(PtrfFromTo, codesc='01', year=2019, vlrepasse=50)
        ft2 = mommy.make(PtrfFromTo, codesc='02', year=2019, vlrepasse=60)

        apply_ptrf_fromto()

        escolas = Escola.objects.all().order_by('year', 'codesc')
        assert escolas[0].ptrf == ft1.vlrepasse
        assert escolas[1].ptrf == ft2.vlrepasse
        assert escolas[2].ptrf is None
