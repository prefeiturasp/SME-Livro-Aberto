from datetime import date
from decimal import Decimal
from itertools import cycle

import pytest

from model_mommy import mommy

from budget_execution.models import (
    Execucao,
    Orcamento,
    Empenho,
    Orgao,
    ProjetoAtividade,
    Categoria,
    Gnd,
    Modalidade,
    Elemento,
    FonteDeRecurso,
    Subfuncao,
    Programa,
    Grupo,
    Subgrupo,
    Subelemento,
)


@pytest.mark.django_db
class TestExecucaoManagerQuerySetMethods:

    def test_get_by_indexer(self):
        expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=10,
            subelemento__id=99)

        # not expected
        mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=10,
            subelemento__id=88)

        execucao = Execucao.objects.get_by_indexer(
            '2018.16.1011.3.3.09.10.10.99')

        assert expected == execucao

    def test_filter_by_indexer(self):
        expected = mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=10,
            _quantity=2)

        # not expected
        mommy.make(
            Execucao,
            year=date(2018, 1, 1),
            orgao__id=16,
            projeto__id=1011,
            categoria__id=3,
            gnd__id=3,
            modalidade__id=9,
            elemento__id=10,
            fonte__id=20)

        # using indexer without subelemento_id
        ret = Execucao.objects.filter_by_indexer(
            '2018.16.1011.3.3.09.10.10')

        assert 2 == len(ret)
        for e in expected:
            assert e in ret

    def test_filter_by_subelemento_fromto_code(self):
        expected = mommy.make(
            Execucao,
            categoria__id=1,
            gnd__id=1,
            modalidade__id=10,
            elemento__id=10,
            subelemento__id=1,
            _quantity=2)

        # not expected
        mommy.make(
            Execucao,
            categoria__id=1,
            gnd__id=1,
            modalidade__id=10,
            elemento__id=10,
            subelemento__id=55)

        # using indexer without subelemento_id
        ret = Execucao.objects.filter_by_subelemento_fromto_code(
            '1.1.10.10.01')

        assert 2 == len(ret)
        for e in expected:
            assert e in ret


@pytest.mark.django_db
class TestExecucaoManagerGetOrCreateByOrcamento:

    def test_creates_new_execucao(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                               _fill_optional=True)
        ret = Execucao.objects.get_or_create_by_orcamento(orcamento)

        execucoes = Execucao.objects.all()
        assert 1 == len(execucoes)
        assert 1 == Orgao.objects.count()
        assert 1 == ProjetoAtividade.objects.count()
        assert 1 == Categoria.objects.count()
        assert 1 == Gnd.objects.count()
        assert 1 == Modalidade.objects.count()
        assert 1 == Elemento.objects.count()
        assert 1 == FonteDeRecurso.objects.count()
        assert 1 == Subfuncao.objects.count()
        assert 1 == Programa.objects.count()

        execucao = execucoes[0]
        assert execucao == ret
        assert execucao.orgao_id == orcamento.cd_orgao
        assert execucao.projeto_id == orcamento.cd_projeto_atividade
        assert execucao.categoria_id == orcamento.ds_categoria_despesa
        assert execucao.gnd_id == orcamento.cd_grupo_despesa
        assert execucao.modalidade_id == orcamento.cd_modalidade
        assert execucao.elemento_id == orcamento.cd_elemento
        assert execucao.fonte_id == orcamento.cd_fonte
        assert execucao.subfuncao_id == orcamento.cd_subfuncao
        assert execucao.programa_id == orcamento.cd_programa

        assert execucao.year.year == orcamento.cd_ano_execucao
        assert execucao.orcado_atualizado == Decimal(
            str(round(orcamento.vl_orcado_atualizado, 2)))

        assert execucao.orgao.desc == orcamento.ds_orgao
        assert execucao.orgao.initials == orcamento.sg_orgao
        assert execucao.projeto.desc == orcamento.ds_projeto_atividade
        assert execucao.projeto.type == orcamento.tp_projeto_atividade
        assert execucao.categoria.desc == orcamento.ds_categoria
        assert execucao.gnd.desc == orcamento.ds_grupo_despesa
        assert execucao.modalidade.desc == orcamento.ds_modalidade
        assert execucao.fonte.desc == orcamento.ds_fonte
        assert execucao.subfuncao.desc == orcamento.ds_subfuncao
        assert execucao.programa.desc == orcamento.ds_programa

    def test_updates_existing_execucao(self):
        previous_orcado = 100
        mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado)

        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=1,
            cd_projeto_atividade=1, ds_categoria_despesa=1, cd_grupo_despesa=1,
            cd_modalidade=1, cd_elemento=1, cd_fonte=1, execucao=None,
            _fill_optional=True,
        )

        ret = Execucao.objects.get_or_create_by_orcamento(orcamento)

        execucoes = Execucao.objects.all()
        assert 1 == len(execucoes)
        assert 1 == Orgao.objects.count()
        assert 1 == ProjetoAtividade.objects.count()
        assert 1 == Categoria.objects.count()
        assert 1 == Gnd.objects.count()
        assert 1 == Modalidade.objects.count()
        assert 1 == Elemento.objects.count()
        assert 1 == FonteDeRecurso.objects.count()

        execucao = execucoes[0]
        assert execucao == ret
        assert execucao.orgao_id == orcamento.cd_orgao
        assert execucao.projeto_id == orcamento.cd_projeto_atividade
        assert execucao.categoria_id == orcamento.ds_categoria_despesa
        assert execucao.gnd_id == orcamento.cd_grupo_despesa
        assert execucao.modalidade_id == orcamento.cd_modalidade
        assert execucao.elemento_id == orcamento.cd_elemento
        assert execucao.fonte_id == orcamento.cd_fonte

        assert execucao.orcado_atualizado == Decimal(
            str(round(previous_orcado + orcamento.vl_orcado_atualizado, 2)))

    def test_updates_all_existing_execucao(self):
        """
        If there's more than one existing execucao with the same
        'year.orgao.projeto.categoria.gnd.modalidade.elemento.fonte' it's
        because there are subelementos. The orcado_atualizado is the same
        for all execucoes in this case.
        """
        previous_orcado = 100
        mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, subelemento__id=cycle([1, 2]),
            orcado_atualizado=previous_orcado, _quantity=2)

        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=1,
            cd_projeto_atividade=1, ds_categoria_despesa=1, cd_grupo_despesa=1,
            cd_modalidade=1, cd_elemento=1, cd_fonte=1, execucao=None,
            _fill_optional=True,
        )

        ret = Execucao.objects.get_or_create_by_orcamento(orcamento)

        execucoes = Execucao.objects.all()
        assert 2 == len(execucoes)
        assert 1 == Orgao.objects.count()
        assert 1 == ProjetoAtividade.objects.count()
        assert 1 == Categoria.objects.count()
        assert 1 == Gnd.objects.count()
        assert 1 == Modalidade.objects.count()
        assert 1 == Elemento.objects.count()
        assert 1 == FonteDeRecurso.objects.count()

        assert ret in execucoes

        for execucao in execucoes:
            assert execucao.orcado_atualizado == Decimal(
                str(round(previous_orcado + orcamento.vl_orcado_atualizado, 2)))


@pytest.mark.django_db
class TestExecucaoManagerUpdateByEmpenho:

    def test_updates_execucao_without_subelemento(self):
        previous_orcado = 100
        execucao = mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento_id=None,
            empenhado_liquido=None)

        assert 0 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=1, vl_empenho_liquido=222,
            execucao=None, dc_elemento="elemento_desc", _fill_optional=True,
        )

        ret = Execucao.objects.update_by_empenho(empenho)

        assert 1 == Execucao.objects.count()
        assert 1 == Subelemento.objects.count()

        execucao.refresh_from_db()
        assert execucao == ret
        assert execucao.subelemento_id == empenho.cd_subelemento
        assert execucao.empenhado_liquido == empenho.vl_empenho_liquido
        assert execucao.orcado_atualizado == previous_orcado

        assert execucao.subelemento.desc == empenho.dc_subelemento
        assert execucao.elemento.desc == empenho.dc_elemento

    def test_updates_execucao_without_subelemento_when_there_are_others(self):
        """
        filter_by_indexer returns more than one execucao. Should update any
        execucao of this indexer that doesn't have subelemento.
        """
        previous_orcado = 100
        previous_empenhado = 200
        execucao_with_empenho = mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento__id=1,
            empenhado_liquido=previous_empenhado)

        execucao = mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento=None,
            empenhado_liquido=None)

        assert 1 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=2, vl_empenho_liquido=222,
            execucao=None, _fill_optional=True,
        )

        ret = Execucao.objects.update_by_empenho(empenho)

        assert 2 == Execucao.objects.count()
        assert 2 == Subelemento.objects.count()

        execucao.refresh_from_db()
        assert execucao == ret
        assert execucao.subelemento_id == empenho.cd_subelemento
        assert execucao.empenhado_liquido == empenho.vl_empenho_liquido
        assert execucao.orcado_atualizado == previous_orcado

        execucao_with_empenho.refresh_from_db()
        assert execucao_with_empenho.subelemento_id == 1
        assert execucao_with_empenho.empenhado_liquido == previous_empenhado
        assert execucao_with_empenho.orcado_atualizado == previous_orcado

    def test_updates_execucao_with_empenho(self):
        previous_orcado = 100
        previous_empenhado = 222
        execucao = mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento__id=1,
            empenhado_liquido=previous_empenhado)

        assert 1 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=1, vl_empenho_liquido=333,
            execucao=None, _fill_optional=True,
        )

        ret = Execucao.objects.update_by_empenho(empenho)

        assert 1 == Execucao.objects.count()
        assert 1 == Subelemento.objects.count()

        execucao.refresh_from_db()
        assert execucao == ret
        assert execucao.empenhado_liquido == Decimal(
            previous_empenhado + empenho.vl_empenho_liquido)
        assert execucao.orcado_atualizado == previous_orcado

    def test_execucao_not_found_for_empenho_indexer(self):
        previous_orcado = 100
        execucao = mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento=None,
            empenhado_liquido=None)

        assert 0 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=2, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=1, vl_empenho_liquido=333,
            execucao=None, _fill_optional=True,
        )

        ret = Execucao.objects.update_by_empenho(empenho)
        assert ret is None

        assert 1 == Execucao.objects.count()
        assert 0 == Subelemento.objects.count()

        execucao.refresh_from_db()
        assert execucao.orcado_atualizado == previous_orcado
        assert execucao.empenhado_liquido is None
        assert execucao.subelemento is None


@pytest.mark.django_db
class TestExecucaoModel:

    def test_indexer(self):
        execucao = mommy.make(
            Execucao, year=date(2018, 1, 1), orgao__id=16, projeto__id=4364,
            categoria__id=3, gnd__id=1, modalidade__id=90, elemento__id=11,
            fonte__id=0, subelemento__id=2)

        assert '2018.16.4364.3.1.90.11.0.2' == execucao.indexer


@pytest.mark.django_db
class TestSubgrupoQueryset:

    def test_get_by_code(self):
        grupo = mommy.make(Grupo, id=10)
        expected = mommy.make(Subgrupo, code=5, grupo=grupo)
        # not expected
        mommy.make(Subgrupo, code=4, grupo=grupo)

        assert expected == Subgrupo.objects.get_by_code('10.5')


@pytest.mark.django_db
class TestSubgrupoModel:

    def test_full_code_property(self):
        grupo = mommy.make(Grupo, id=10)
        subgrupo = mommy.make(Subgrupo, code=5, grupo=grupo)

        assert '10.5' == subgrupo.full_code


@pytest.mark.django_db
class TestOrcamentoModel:

    def test_indexer(self):
        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=16,
            cd_projeto_atividade=4364, ds_categoria_despesa=3,
            cd_grupo_despesa=1, cd_modalidade=90, cd_elemento=11, cd_fonte=0,
            execucao=None, _fill_optional=True,
        )

        assert '2018.16.4364.3.1.90.11.0' == orcamento.indexer


@pytest.mark.django_db
class TestEmpenhoModel:

    def test_indexer(self):
        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=16, cd_projeto_atividade=4364,
            cd_categoria=3, cd_grupo=1, cd_modalidade=90, cd_elemento=11,
            cd_fonte_de_recurso=0, cd_subelemento=1, execucao=None,
            _fill_optional=True,
        )

        assert '2018.16.4364.3.1.90.11.0.1' == empenho.indexer
