from datetime import date
from decimal import Decimal
from itertools import cycle

import pytest

from model_mommy import mommy

from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import (
    Execucao,
    ExecucaoTemp,
    Orcamento,
    OrcamentoRaw,
    Empenho,
    EmpenhoRaw,
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
    MinimoLegal,
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
                               execucao_temp=None, _fill_optional=True)
        ret = ExecucaoTemp.objects.get_or_create_by_orcamento(orcamento)

        execucoes = ExecucaoTemp.objects.all()
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

    def test_print_error_when_ds_projeto_atividade_is_none(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                               execucao_temp=None, ds_projeto_atividade=None,
                               _fill_optional=True)
        ret = ExecucaoTemp.objects.get_or_create_by_orcamento(orcamento)
        assert (f"orcamento id {orcamento.id}: column "
                "ds_projeto_atividade can't be null") == ret['error']

    def test_updates_existing_execucao(self):
        previous_orcado = 100
        mommy.make(
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado)

        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=1,
            cd_projeto_atividade=1, ds_categoria_despesa=1, cd_grupo_despesa=1,
            cd_modalidade=1, cd_elemento=1, cd_fonte=1, execucao=None,
            execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.get_or_create_by_orcamento(orcamento)

        execucoes = ExecucaoTemp.objects.all()
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
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, subelemento__id=cycle([1, 2]),
            orcado_atualizado=previous_orcado, _quantity=2)

        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=1,
            cd_projeto_atividade=1, ds_categoria_despesa=1, cd_grupo_despesa=1,
            cd_modalidade=1, cd_elemento=1, cd_fonte=1, execucao=None,
            execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.get_or_create_by_orcamento(orcamento)

        execucoes = ExecucaoTemp.objects.all()
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
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento_id=None,
            empenhado_liquido=None)

        assert 0 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=1, vl_empenho_liquido=222,
            execucao=None, dc_elemento="elemento_desc",
            execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.update_by_empenho(empenho)

        assert 1 == ExecucaoTemp.objects.count()
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
        execucao of this indexer that doesn't have subelemento if there's one
        """
        previous_orcado = 100
        previous_empenhado = 200
        execucao_with_empenho = mommy.make(
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento__id=1,
            empenhado_liquido=previous_empenhado)

        execucao = mommy.make(
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento=None,
            empenhado_liquido=None)

        assert 1 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=2, vl_empenho_liquido=222,
            execucao=None, execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.update_by_empenho(empenho)

        assert 2 == ExecucaoTemp.objects.count()
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

    def test_creates_new_execucao_when_theres_no_one_without_subelemento(self):
        """
        filter_by_indexer returns more than one execucao and there's no one
        without subelemento. A new execucao should be created with same data as
        another one with the same indexer, but with correct subelemento and
        empenhado_liquido (from Empenho) and orcado_atualizado == 0 (so it won't
        affect the Sum of orcado_total) It won't an execucao with
        orcado_atualizado == 0 to appear on the chart, because, at subelemento
        level, we show the values of the previous level (elemento), so it will
        always be a sum.
        """
        previous_orcado = 100
        previous_empenhado = 200
        execucao_with_empenho = mommy.make(
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento__id=1,
            empenhado_liquido=previous_empenhado)

        assert 1 == ExecucaoTemp.objects.count()
        assert 1 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=2, vl_empenho_liquido=222,
            execucao=None, execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.update_by_empenho(empenho)

        assert 2 == ExecucaoTemp.objects.count()
        assert 2 == Subelemento.objects.count()

        assert ret.subelemento_id == empenho.cd_subelemento
        assert ret.empenhado_liquido == empenho.vl_empenho_liquido
        assert ret.orcado_atualizado == 0

        execucao_with_empenho.refresh_from_db()
        assert execucao_with_empenho.subelemento_id == 1
        assert execucao_with_empenho.empenhado_liquido == previous_empenhado
        assert execucao_with_empenho.orcado_atualizado == previous_orcado

    def test_updates_execucao_with_empenho(self):
        previous_orcado = 100
        previous_empenhado = 222
        execucao = mommy.make(
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento__id=1,
            empenhado_liquido=previous_empenhado)

        assert 1 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=1, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=1, vl_empenho_liquido=333.33,
            execucao=None, execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.update_by_empenho(empenho)

        assert 1 == ExecucaoTemp.objects.count()
        assert 1 == Subelemento.objects.count()

        execucao.refresh_from_db()
        assert execucao == ret
        assert execucao.empenhado_liquido == Decimal(
            str(round(previous_empenhado + empenho.vl_empenho_liquido, 2)))
        assert execucao.orcado_atualizado == previous_orcado

    def test_execucao_not_found_for_empenho_indexer(self):
        previous_orcado = 100
        execucao = mommy.make(
            ExecucaoTemp, year=date(2018, 1, 1), orgao__id=1, projeto__id=1,
            categoria__id=1, gnd__id=1, modalidade__id=1, elemento__id=1,
            fonte__id=1, orcado_atualizado=previous_orcado, subelemento=None,
            empenhado_liquido=None)

        assert 0 == Subelemento.objects.count()

        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=2, cd_projeto_atividade=1,
            cd_categoria=1, cd_grupo=1, cd_modalidade=1, cd_elemento=1,
            cd_fonte_de_recurso=1, cd_subelemento=1, vl_empenho_liquido=333,
            execucao=None, execucao_temp=None, _fill_optional=True,
        )

        ret = ExecucaoTemp.objects.update_by_empenho(empenho)
        assert ret is None

        assert 1 == ExecucaoTemp.objects.count()
        assert 0 == Subelemento.objects.count()

        execucao.refresh_from_db()
        assert execucao.orcado_atualizado == previous_orcado
        assert execucao.empenhado_liquido is None
        assert execucao.subelemento is None


@pytest.mark.django_db
class TestExecucaoManagerCreateByMinimoLegal:

    def test_updates_execucao(self):
        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_projeto_atividade=1111,
            execucao=None, execucao_temp=None, _fill_optional=True)

        ml = mommy.make(MinimoLegal, year=date(2018, 1, 1), projeto_id=1111,
                        projeto_desc="projeto desc", orcado_atualizado=55,
                        empenhado_liquido=22)

        Execucao.objects.create_by_minimo_legal(ml)

        execucoes = Execucao.objects.all()
        assert 1 == len(execucoes)

        orcamento.refresh_from_db()
        execucao = execucoes[0]
        assert execucao.projeto.id == 1111
        assert execucao.projeto.desc == "projeto desc"
        assert execucao.orcado_atualizado == 55
        assert execucao.empenhado_liquido == 22
        assert execucao.orgao.id == orcamento.cd_orgao
        assert execucao.subfuncao.id == orcamento.cd_subfuncao
        assert execucao.programa.id == orcamento.cd_programa
        assert execucao.is_minimo_legal

        assert orcamento.execucao == execucao

    def test_do_nothing_if_there_is_no_orcamento(self):
        ml = mommy.make(MinimoLegal, year=date(2018, 1, 1), projeto_id=1111,
                        projeto_desc="projeto desc", orcado_atualizado=55,
                        empenhado_liquido=22)

        result = Execucao.objects.create_by_minimo_legal(ml)
        assert not result
        assert 0 == Execucao.objects.count()


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
class TestOrcamentoManagerCreateFromOrcamentoRaw:

    def assert_fields(self, orc, orc_raw):
        assert orc.cd_key == orc_raw.cd_key
        assert orc.dt_inicial == orc_raw.dt_inicial
        assert orc.dt_final == orc_raw.dt_final
        assert orc.cd_ano_execucao == orc_raw.cd_ano_execucao
        assert orc.cd_exercicio == orc_raw.cd_exercicio
        assert orc.nm_administracao == orc_raw.nm_administracao
        assert orc.cd_orgao == orc_raw.cd_orgao
        assert orc.sg_orgao == orc_raw.sg_orgao
        assert orc.ds_orgao == orc_raw.ds_orgao
        assert orc.cd_unidade == orc_raw.cd_unidade
        assert orc.ds_unidade == orc_raw.ds_unidade
        assert orc.cd_funcao == orc_raw.cd_funcao
        assert orc.ds_funcao == orc_raw.ds_funcao
        assert orc.cd_subfuncao == orc_raw.cd_subfuncao
        assert orc.ds_subfuncao == orc_raw.ds_subfuncao
        assert orc.cd_programa == orc_raw.cd_programa
        assert orc.ds_programa == orc_raw.ds_programa
        assert orc.tp_projeto_atividade == orc_raw.tp_projeto_atividade
        assert orc.tp_papa == orc_raw.tp_papa
        assert orc.cd_projeto_atividade == orc_raw.cd_projeto_atividade
        assert orc.ds_projeto_atividade == orc_raw.ds_projeto_atividade
        assert orc.cd_despesa == orc_raw.cd_despesa
        assert orc.ds_despesa == orc_raw.ds_despesa
        assert orc.ds_categoria_despesa == orc_raw.ds_categoria_despesa
        assert orc.ds_categoria == orc_raw.ds_categoria
        assert orc.cd_grupo_despesa == orc_raw.cd_grupo_despesa
        assert orc.ds_grupo_despesa == orc_raw.ds_grupo_despesa
        assert orc.cd_modalidade == orc_raw.cd_modalidade
        assert orc.ds_modalidade == orc_raw.ds_modalidade
        assert orc.cd_elemento == orc_raw.cd_elemento
        assert orc.cd_fonte == orc_raw.cd_fonte
        assert orc.ds_fonte == orc_raw.ds_fonte
        assert orc.vl_orcado_inicial == orc_raw.vl_orcado_inicial
        assert orc.vl_orcado_atualizado == orc_raw.vl_orcado_atualizado
        assert orc.vl_congelado == orc_raw.vl_congelado
        assert orc.vl_orcado_disponivel == orc_raw.vl_orcado_disponivel
        assert orc.vl_reservado_liquido == orc_raw.vl_reservado_liquido
        assert orc.vl_empenhado_liquido == orc_raw.vl_empenhado_liquido
        assert orc.vl_empenhado_liquido_atual \
            == orc_raw.vl_empenhado_liquido_atual
        assert orc.vl_liquidado == orc_raw.vl_liquidado
        assert orc.vl_liquidado_atual == orc_raw.vl_liquidado_atual
        assert orc.vl_pago == orc_raw.vl_pago
        assert orc.vl_pago_atual == orc_raw.vl_pago_atual
        assert orc.vl_saldo_empenho == orc_raw.vl_saldo_empenho
        assert orc.vl_saldo_reserva == orc_raw.vl_saldo_reserva
        assert orc.vl_saldo_dotacao == orc_raw.vl_saldo_dotacao
        assert orc.dt_extracao == orc_raw.dt_extracao

    def test_create_new_orcamento(self):
        orc_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        assert 0 == Orcamento.objects.count()

        orc = Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw)

        assert 1 == Orcamento.objects.count()
        assert orc.execucao is None
        assert orc.execucao_temp is None
        self.assert_fields(orc, orc_raw)

    def test_update_existing_orcamento(self):
        orc_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        mommy.make(
            Orcamento,
            cd_ano_execucao=orc_raw.cd_ano_execucao,
            cd_orgao=orc_raw.cd_orgao,
            cd_projeto_atividade=orc_raw.cd_projeto_atividade,
            ds_categoria_despesa=orc_raw.ds_categoria_despesa,
            cd_grupo_despesa=orc_raw.cd_grupo_despesa,
            cd_modalidade=orc_raw.cd_modalidade,
            cd_elemento=orc_raw.cd_elemento,
            cd_fonte=orc_raw.cd_fonte,
            cd_unidade=orc_raw.cd_unidade,
            cd_subfuncao=orc_raw.cd_subfuncao,
            execucao=None,
            execucao_temp=None,
            vl_orcado_atualizado=100,
            _fill_optional=True)

        assert 1 == Orcamento.objects.count()

        orc = Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw)

        assert 1 == Orcamento.objects.count()
        assert 0 == Execucao.objects.count()
        assert 0 == ExecucaoTemp.objects.count()
        assert orc.execucao is None
        assert orc.execucao_temp is None
        self.assert_fields(orc, orc_raw)

    def test_update_existing_orcamento_when_execucao_exists(self):
        orc_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            _fill_optional=True)

        mommy.make(
            Orcamento,
            cd_ano_execucao=orc_raw.cd_ano_execucao,
            cd_orgao=orc_raw.cd_orgao,
            cd_projeto_atividade=orc_raw.cd_projeto_atividade,
            ds_categoria_despesa=orc_raw.ds_categoria_despesa,
            cd_grupo_despesa=orc_raw.cd_grupo_despesa,
            cd_modalidade=orc_raw.cd_modalidade,
            cd_elemento=orc_raw.cd_elemento,
            cd_fonte=orc_raw.cd_fonte,
            cd_unidade=orc_raw.cd_unidade,
            cd_subfuncao=orc_raw.cd_subfuncao,
            execucao=None,
            execucao_temp__id=1,
            vl_orcado_atualizado=100,
            _fill_optional=True)

        assert 1 == Orcamento.objects.count()
        assert 1 == ExecucaoTemp.objects.count()

        orc = Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw)

        assert 1 == Orcamento.objects.count()
        assert 0 == ExecucaoTemp.objects.count()
        assert orc.execucao is None
        assert orc.execucao_temp is None
        self.assert_fields(orc, orc_raw)

    def test_doesnt_update_when_orcado_is_equal(self):
        orc_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            vl_orcado_atualizado=1000,
            _fill_optional=True)

        orc = mommy.make(
            Orcamento,
            id=2222,
            cd_ano_execucao=orc_raw.cd_ano_execucao,
            cd_orgao=orc_raw.cd_orgao,
            cd_projeto_atividade=orc_raw.cd_projeto_atividade,
            ds_categoria_despesa=orc_raw.ds_categoria_despesa,
            cd_grupo_despesa=orc_raw.cd_grupo_despesa,
            cd_modalidade=orc_raw.cd_modalidade,
            cd_elemento=orc_raw.cd_elemento,
            cd_fonte=orc_raw.cd_fonte,
            cd_unidade=orc_raw.cd_unidade,
            cd_subfuncao=orc_raw.cd_subfuncao,
            vl_orcado_atualizado=orc_raw.vl_orcado_atualizado,
            execucao=None,
            execucao_temp=None,
            _fill_optional=True)

        assert 1 == Orcamento.objects.count()
        assert 0 == Execucao.objects.count()
        assert 0 == ExecucaoTemp.objects.count()

        Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw)
        orc.refresh_from_db()

        assert 1 == Orcamento.objects.count()
        assert 0 == Execucao.objects.count()
        assert 0 == ExecucaoTemp.objects.count()
        assert 2222 == orc.id
        assert orc.execucao is None
        assert orc.execucao_temp is None

    def test_doesnt_update_when_orcado_is_equal_and_execucao_exists(self):
        orc_raw = mommy.make(
            OrcamentoRaw, cd_ano_execucao=2018, cd_orgao=SME_ORGAO_ID,
            vl_orcado_atualizado=1000,
            _fill_optional=True)

        orc = mommy.make(
            Orcamento,
            id=3333,
            cd_ano_execucao=orc_raw.cd_ano_execucao,
            cd_orgao=orc_raw.cd_orgao,
            cd_projeto_atividade=orc_raw.cd_projeto_atividade,
            ds_categoria_despesa=orc_raw.ds_categoria_despesa,
            cd_grupo_despesa=orc_raw.cd_grupo_despesa,
            cd_modalidade=orc_raw.cd_modalidade,
            cd_elemento=orc_raw.cd_elemento,
            cd_fonte=orc_raw.cd_fonte,
            cd_unidade=orc_raw.cd_unidade,
            cd_subfuncao=orc_raw.cd_subfuncao,
            vl_orcado_atualizado=orc_raw.vl_orcado_atualizado,
            execucao=None,
            execucao_temp__id=1,
            _fill_optional=True)

        assert 1 == Orcamento.objects.count()
        assert 0 == Execucao.objects.count()
        assert 1 == ExecucaoTemp.objects.count()

        Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw)
        orc.refresh_from_db()

        assert 1 == Orcamento.objects.count()
        assert 0 == Execucao.objects.count()
        assert 1 == ExecucaoTemp.objects.count()
        assert 3333 == orc.id
        assert orc.execucao_id is None
        assert 1 == orc.execucao_temp_id


@pytest.mark.django_db
class TestOrcamentoModel:

    def test_indexer(self):
        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=16,
            cd_projeto_atividade=4364, ds_categoria_despesa=3,
            cd_grupo_despesa=1, cd_modalidade=90, cd_elemento=11, cd_fonte=0,
            execucao=None, execucao_temp=None, _fill_optional=True,
        )

        assert '2018.16.4364.3.1.90.11.0' == orcamento.indexer

    def test_raw_indexer(self):
        orcamento = mommy.make(
            Orcamento, cd_ano_execucao=2018, cd_orgao=16,
            cd_projeto_atividade=4364, ds_categoria_despesa=3,
            cd_grupo_despesa=1, cd_modalidade=90, cd_elemento=11, cd_fonte=0,
            cd_unidade=2222, cd_subfuncao=311,
            execucao=None, execucao_temp=None, _fill_optional=True,
        )

        assert '2018.16.4364.3.1.90.11.0.2222.311' == orcamento.raw_indexer


@pytest.mark.django_db
class TestEmpenhoManagerCreateFromEmpenhoRaw:

    def assert_fields(self, emp, emp_raw):
        assert emp.execucao is None
        assert emp.execucao_temp is None
        assert emp.empenho_raw == emp_raw
        assert emp.cd_key == emp_raw.cd_key
        assert emp.an_empenho == emp_raw.an_empenho
        assert emp.cd_categoria == emp_raw.cd_categoria
        assert emp.cd_elemento == emp_raw.cd_elemento
        assert emp.cd_empenho == emp_raw.cd_empenho
        assert emp.cd_empresa == emp_raw.cd_empresa
        assert emp.cd_fonte_de_recurso == emp_raw.cd_fonte_de_recurso
        assert emp.cd_funcao == emp_raw.cd_funcao
        assert emp.cd_grupo == emp_raw.cd_grupo
        assert emp.cd_item_despesa == emp_raw.cd_item_despesa
        assert emp.cd_modalidade == emp_raw.cd_modalidade
        assert emp.cd_orgao == emp_raw.cd_orgao
        assert emp.cd_programa == emp_raw.cd_programa
        assert emp.cd_projeto_atividade == emp_raw.cd_projeto_atividade
        assert emp.cd_subelemento == emp_raw.cd_subelemento
        assert emp.cd_subfuncao == emp_raw.cd_subfuncao
        assert emp.cd_unidade == emp_raw.cd_unidade
        assert emp.dt_empenho == emp_raw.dt_empenho
        assert emp.mes_empenho == emp_raw.mes_empenho
        assert emp.nm_empresa == emp_raw.nm_empresa
        assert emp.dc_cpf_cnpj == emp_raw.dc_cpf_cnpj
        assert emp.cd_reserva == emp_raw.cd_reserva
        assert emp.dc_categoria_economica == emp_raw.dc_categoria_economica
        assert emp.dc_elemento == emp_raw.dc_elemento
        assert emp.dc_fonte_de_recurso == emp_raw.dc_fonte_de_recurso
        assert emp.dc_funcao == emp_raw.dc_funcao
        assert emp.dc_item_despesa == emp_raw.dc_item_despesa
        assert emp.dc_orgao == emp_raw.dc_orgao
        assert emp.dc_programa == emp_raw.dc_programa
        assert emp.dc_projeto_atividade == emp_raw.dc_projeto_atividade
        assert emp.dc_subelemento == emp_raw.dc_subelemento
        assert emp.dc_subfuncao == emp_raw.dc_subfuncao
        assert emp.dc_unidade == emp_raw.dc_unidade
        assert emp.dc_grupo_despesa == emp_raw.dc_grupo_despesa
        assert emp.dc_modalidade == emp_raw.dc_modalidade
        assert emp.dc_razao_social == emp_raw.dc_razao_social
        assert emp.vl_empenho_anulado == emp_raw.vl_empenho_anulado
        assert emp.vl_empenho_liquido == emp_raw.vl_empenho_liquido
        assert emp.vl_liquidado == emp_raw.vl_liquidado
        assert emp.vl_pago == emp_raw.vl_pago
        assert emp.vl_pago_restos == emp_raw.vl_pago_restos
        assert emp.vl_empenhado == emp_raw.vl_empenhado

    @pytest.fixture
    def empenho_raw(self):
        return mommy.make(
            EmpenhoRaw, an_empenho=2018, cd_orgao=SME_ORGAO_ID,
            cd_elemento='1',            # had to set it manually because these
            cd_fonte_de_recurso='5',    # are text fields. this modeling came
            cd_projeto_atividade='5',   # from SME
            cd_subfuncao='5',
            cd_unidade='5',
            _fill_optional=True)

    def test_create_new_empenho(self, empenho_raw):
        assert 0 == Empenho.objects.count()

        emp = Empenho.objects.create_from_empenho_raw(empenho_raw)

        assert 1 == Empenho.objects.count()
        self.assert_fields(emp, empenho_raw)


@pytest.mark.django_db
class TestEmpenhoModel:

    def test_indexer(self):
        empenho = mommy.make(
            Empenho, an_empenho=2018, cd_orgao=16, cd_projeto_atividade=4364,
            cd_categoria=3, cd_grupo=1, cd_modalidade=90, cd_elemento=11,
            cd_fonte_de_recurso=0, cd_subelemento=1, execucao=None,
            execucao_temp=None, _fill_optional=True,
        )

        assert '2018.16.4364.3.1.90.11.0.1' == empenho.indexer


@pytest.mark.django_db
class TestMinimoLegalManagerCreateOrUpdate:

    def test_creates_execucao(self):
        MinimoLegal.objects.create_or_update(
            year=2018, projeto_id=1111, projeto_desc="projeto desc",
            orcado_atualizado=200, empenhado_liquido=100)

        execs = MinimoLegal.objects.all()
        assert 1 == len(execs)
        assert date(2018, 1, 1) == execs[0].year
        assert 1111 == execs[0].projeto_id
        assert "projeto desc" == execs[0].projeto_desc
        assert 200 == execs[0].orcado_atualizado
        assert 100 == execs[0].empenhado_liquido

    def test_updates_existing_execucao(self):
        mommy.make(MinimoLegal, year=date(2018, 1, 1), projeto_id=1111,
                   projeto_desc="projeto desc", orcado_atualizado=200,
                   empenhado_liquido=100)

        MinimoLegal.objects.create_or_update(
            year=2018, projeto_id=1111, projeto_desc="projeto desc",
            orcado_atualizado=50, empenhado_liquido=25)

        execs = MinimoLegal.objects.all()
        assert 1 == len(execs)
        assert date(2018, 1, 1) == execs[0].year
        assert 1111 == execs[0].projeto_id
        assert "projeto desc" == execs[0].projeto_desc
        assert 250 == execs[0].orcado_atualizado
        assert 125 == execs[0].empenhado_liquido
