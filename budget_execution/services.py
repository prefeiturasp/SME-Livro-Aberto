from django.db.models import Q
from django.utils import timezone

from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import (Execucao, Orcamento, OrcamentoRaw,
                                     Empenho, EmpenhoRaw, MinimoLegal)
from from_to_handler.models import (DotacaoFromTo, FonteDeRecursoFromTo,
                                    SubelementoFromTo, GNDFromTo)


def load_data_from_orcamento_raw(load_everything=False):
    if not load_everything:
        print("Loading current year data from orcamento_raw_load")
        orcamentos_raw = OrcamentoRaw.objects.filter(
            cd_ano_execucao=timezone.now().year)
    else:
        print("Loading everything from orcamento_raw_load")
        orcamentos_raw = OrcamentoRaw.objects.all()

    orcamentos = []
    for orc_raw in orcamentos_raw:
        orcamentos.append(
            Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw))

    # needed, otherwise duplicated execucoes would be created and the sum of
    # orcado_atualizado would be greater than expected
    Execucao.objects.erase_execucoes_without_orcamento()
    return len(orcamentos)


def load_data_from_empenhos_raw():
    """ Currently not being used. Wasn't working as expected. """
    empenhos_raw = EmpenhoRaw.objects.all()

    empenhos = []
    for emp_raw in empenhos_raw:
        empenhos.append(
            Empenho.objects.create_from_empenho_raw(emp_raw))

    return len(empenhos)


def import_orcamentos():
    orcamentos = Orcamento.objects.filter(
        execucao__isnull=True, cd_orgao=SME_ORGAO_ID,
    )

    for orcamento in orcamentos:
        execucao = Execucao.objects.get_or_create_by_orcamento(orcamento)
        if isinstance(execucao, Execucao):
            orcamento.execucao = execucao
            orcamento.save()
        else:
            print(execucao['error'])


def import_empenhos():
    empenhos = Empenho.objects.filter(
        execucao__isnull=True, cd_orgao=SME_ORGAO_ID,
    )

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
