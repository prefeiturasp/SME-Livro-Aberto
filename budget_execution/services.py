from budget_execution.models import Execucao, Orcamento


def import_orcamentos():
    orcamentos = Orcamento.objects.filter(execucao__isnull=True)

    for orcamento in orcamentos:
        execucao = Execucao.objects.get_or_create_by_orcamento(orcamento)
        orcamento.execucao = execucao
        orcamento.save()
