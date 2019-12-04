import pytest

from datetime import date
from itertools import cycle
from unittest import TestCase

from model_mommy import mommy

from regionalizacao.models import (
    Distrito, DistritoZonaFromTo, Escola, EtapaTipoEscolaFromTo, PtrfFromTo,
    TipoEscola, UnidadeRecursosFromTo, Recurso, Grupo, Subgrupo, Budget)
from regionalizacao.services import (
    apply_distrito_zona_fromto,
    apply_etapa_tipo_escola_fromto,
    apply_ptrf_fromto,
    apply_unidade_recursos_fromto,
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
        escola1 = mommy.make(Escola, codesc='01')
        escola2 = mommy.make(Escola, codesc='02')
        mommy.make(Budget, escola=escola1, year=2019, ptrf=None)
        mommy.make(Budget, escola=escola2, year=2019, ptrf=None)
        mommy.make(Budget, escola=escola1, year=2020, ptrf=None)

        ft1 = mommy.make(PtrfFromTo, codesc='01', year=2019, vlrepasse=50)
        ft2 = mommy.make(PtrfFromTo, codesc='02', year=2019, vlrepasse=60)

        apply_ptrf_fromto()

        budgets = Budget.objects.all().order_by('year', 'escola__codesc')
        assert budgets[0].ptrf == ft1.vlrepasse
        assert budgets[1].ptrf == ft2.vlrepasse
        assert budgets[2].ptrf is None


@pytest.mark.django_db
class TestApplyUnidadeRecursosFromTo(TestCase):

    def test_apply_creates_new_budget_instance(self):
        escola = mommy.make(Escola, codesc='01')
        year = date.today().year
        other_budget = mommy.make(Budget, escola=escola, year=year-1)

        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=15, label='Unidades')
        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=50.23, label='R$')

        apply_unidade_recursos_fromto()

        assert 2 == Budget.objects.count()
        assert 1 == Recurso.objects.count()
        assert 1 == Subgrupo.objects.count()
        assert 1 == Grupo.objects.count()

        budget = Budget.objects.all().order_by('-year').first()
        assert budget.escola == escola
        assert budget.year == year
        other_budget.refresh_from_db()
        assert other_budget.escola == escola
        assert other_budget.year == year - 1
        assert other_budget.recursos.count() == 0

        recurso = Recurso.objects.first()
        assert budget == recurso.budget
        assert 'Kit fundamental' == recurso.subgrupo.name
        assert 'Material escolar' == recurso.subgrupo.grupo.name
        assert 15 == recurso.amount
        assert 'Unidades' == recurso.label
        assert 50.23 == recurso.cost

    def test_apply_updates_existing_budget_instance(self):
        escola = mommy.make(Escola, codesc='01')
        year = date.today().year
        budget = mommy.make(Budget, escola=escola, year=year)
        other_budget = mommy.make(Budget, escola=escola, year=year-1)

        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=15, label='Unidades')
        mommy.make(
            UnidadeRecursosFromTo, codesc='01', year=year,
            grupo='Material escolar', subgrupo='Kit fundamental',
            valor=50.23, label='R$')

        apply_unidade_recursos_fromto()

        assert 2 == Budget.objects.count()
        assert 1 == Recurso.objects.count()
        assert 1 == Subgrupo.objects.count()
        assert 1 == Grupo.objects.count()

        budget.refresh_from_db()
        assert budget.escola == escola
        assert budget.year == year
        other_budget.refresh_from_db()
        assert other_budget.escola == escola
        assert other_budget.year == year - 1
        assert other_budget.recursos.count() == 0

        recurso = Recurso.objects.first()
        assert budget == recurso.budget
        assert 'Kit fundamental' == recurso.subgrupo.name
        assert 'Material escolar' == recurso.subgrupo.grupo.name
        assert 15 == recurso.amount
        assert 'Unidades' == recurso.label
        assert 50.23 == recurso.cost
