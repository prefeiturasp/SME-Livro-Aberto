from budget_execution.models import Execucao, Orcamento, Empenho


def import_orcamentos():
    orcamentos = Orcamento.objects.filter(execucao__isnull=True)

    for orcamento in orcamentos:
        execucao = Execucao.objects.get_or_create_by_orcamento(orcamento)
        orcamento.execucao = execucao
        orcamento.save()


def import_empenhos():
    empenhos = Empenho.objects.filter(execucao__isnull=True)

    for empenho in empenhos:
        execucao = Execucao.objects.update_by_empenho(empenho)

        if execucao:
            empenho.execucao = execucao
            empenho.save()
