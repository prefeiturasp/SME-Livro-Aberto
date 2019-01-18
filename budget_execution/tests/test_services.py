import pytest

from model_mommy import mommy

from budget_execution import services
from budget_execution.models import (
    Execucao,
    Orcamento,
)


@pytest.mark.django_db
class TestGenerateExecucoes:

    def test_import_orcamento(self):
        orcamento = mommy.make(Orcamento, cd_ano_execucao=2018, execucao=None,
                               _fill_optional=True)
        services.import_orcamento()

        execucoes = Execucao.objects.all()
        execucao = execucoes[0]

        orcamento.refresh_from_db()
        assert orcamento.execucao == execucao
