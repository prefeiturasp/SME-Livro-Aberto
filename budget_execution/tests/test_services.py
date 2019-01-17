import pytest

from decimal import Decimal

from model_mommy import mommy

from budget_execution import services
from budget_execution.models import (
    Execucao,
    Orcamento,
    Orgao,
    ProjetoAtividade,
    Categoria,
    Gnd,
    Modalidade,
    Elemento,
    FonteDeRecurso,
    Subfuncao,
    Programa,
)


@pytest.mark.django_db
class TestGenerateExecucoes:

    def test_import_orcamento(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                               _fill_optional=True)
        services.import_orcamento()

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
        assert execucao.orgao_id == orcamento.cd_orgao
        assert execucao.projeto_id == orcamento.cd_projeto_atividade
        assert execucao.categoria_id == orcamento.ds_categoria_despesa
        assert execucao.gnd_id == orcamento.cd_grupo_despesa
        assert execucao.modalidade_id == orcamento.cd_modalidade
        assert execucao.elemento_id == orcamento.cd_elemento
        assert execucao.fonte_id == orcamento.cd_fonte
        assert execucao.subfuncao_id == orcamento.cd_subfuncao
        assert execucao.programa_id == orcamento.cd_programa

        assert execucao.orcado_atualizado == Decimal(
            str(round(orcamento.vl_orcado_atualizado, 2)))

        orcamento.refresh_from_db()
        assert orcamento.execucao == execucao
