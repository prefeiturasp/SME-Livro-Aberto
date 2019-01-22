from budget_execution.models import Execucao, Orcamento, Empenho
from from_to_handler.models import (DotacaoFromTo, FonteDeRecursoFromTo,
                                    SubelementoFromTo, GNDFromTo)


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


def apply_fromto():
    DotacaoFromTo.apply_all()
    FonteDeRecursoFromTo.apply_all()
    SubelementoFromTo.apply_all()
    GNDFromTo.apply_all()
