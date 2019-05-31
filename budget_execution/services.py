from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import (Execucao, Orcamento, OrcamentoRaw,
                                     Empenho, EmpenhoRaw, MinimoLegal)
from from_to_handler.models import (DotacaoFromTo, FonteDeRecursoFromTo,
                                    SubelementoFromTo, GNDFromTo)


def load_data_from_orcamento_raw():
    orcamentos_raw = OrcamentoRaw.objects.all()

    orcamentos = []
    for orc_raw in orcamentos_raw:
        orcamentos.append(
            Orcamento.objects.create_from_orcamento_raw(orc_raw))

    return len(orcamentos)


def load_data_from_empenhos_raw():
    empenhos_raw = EmpenhoRaw.objects.all()

    empenhos = []
    for emp_raw in empenhos_raw:
        empenhos.append(
            Empenho.objects.create_from_empenho_raw(emp_raw))

    return len(empenhos)


def import_orcamentos():
    orcamentos = Orcamento.objects.filter(execucao__isnull=True,
                                          cd_orgao=SME_ORGAO_ID)

    for orcamento in orcamentos:
        execucao = Execucao.objects.get_or_create_by_orcamento(orcamento)
        if isinstance(execucao, Execucao):
            orcamento.execucao = execucao
            orcamento.save()
        else:
            print(execucao['error'])


def import_empenhos():
    empenhos = Empenho.objects.filter(execucao__isnull=True,
                                      cd_orgao=SME_ORGAO_ID)

    for empenho in empenhos:
        execucao = Execucao.objects.update_by_empenho(empenho)

        if execucao:
            empenho.execucao = execucao
            empenho.save()


def import_minimo_legal():
    mls = MinimoLegal.objects.filter(execucao__isnull=True)

    for ml in mls:
        execucao = Execucao.objects.create_by_minimo_legal(ml)

        if execucao:
            ml.execucao = execucao
            ml.save()


def apply_fromto():
    DotacaoFromTo.apply_all()
    FonteDeRecursoFromTo.apply_all()
    SubelementoFromTo.apply_all()
    GNDFromTo.apply_all()
