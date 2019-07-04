from django.core.management import call_command
from django.utils import timezone

from budget_execution.constants import SME_ORGAO_ID
from budget_execution.models import (
    Execucao, ExecucaoTemp, Orcamento, OrcamentoRaw, Orgao,
    Empenho, EmpenhoRaw, MinimoLegal, ProjetoAtividade)
from from_to_handler.models import (DotacaoFromTo, FonteDeRecursoFromTo,
                                    SubelementoFromTo, GNDFromTo)


def erase_current_year_data():
    current_year = timezone.now().year

    # Execucao.objects.filter(year__year=current_year).delete()
    Orcamento.objects.filter(cd_ano_execucao=current_year).delete()
    Empenho.objects.filter(an_empenho=current_year).delete()


def load_2003_2017_execucoes_from_json(path="data/2003_2017_everything.json"):
    if (Execucao.objects.count() or Orcamento.objects.count()
            or Orgao.objects.count() or ProjetoAtividade.objects.count()):
        raise Exception(
            """
            This service should be runned with an empty DB. Only the tables
            orcamento_raw_load and empenhos can be filled. All the other ones
            must be empty
            """)
    call_command('loaddata', path)


def load_data_from_orcamento_raw(load_everything=False):
    """
    The load_everything arg means everything after 2017, because data until
    2017 is loaded via json.
    """
    if not load_everything:
        print("Loading current year data from orcamento_raw_load")
        orcamentos_raw = OrcamentoRaw.objects.filter(
            cd_ano_execucao=timezone.now().year)
    else:
        print("Loading everything newer than 2017 from orcamento_raw_load")
        orcamentos_raw = OrcamentoRaw.objects.filter(cd_ano_execucao__gt=2017)

    orcamentos = []
    for orc_raw in orcamentos_raw:
        orcamentos.append(
            Orcamento.objects.create_or_update_orcamento_from_raw(orc_raw))

    # needed, otherwise duplicated execucoes would be created and the sum of
    # orcado_atualizado would be greater than expected
    # TODO: remove it
    # Execucao.objects.erase_execucoes_without_orcamento()
    return len(orcamentos)


def load_data_from_empenhos_raw(load_everything=False):
    """
    The load_everything arg means everything after 2017, because data until
    2017 is loaded via json.
    """
    if not load_everything:
        print("Loading current year data from empenhos_raw_load")
        empenhos_raw = EmpenhoRaw.objects.filter(
            an_empenho=timezone.now().year)
    else:
        print("Loading everything newer than 2017 from empenhos_raw_load")
        empenhos_raw = EmpenhoRaw.objects.filter(an_empenho__gt=2017)

    empenhos = []
    for emp_raw in empenhos_raw:
        empenhos.append(
            Empenho.objects.create_from_empenho_raw(emp_raw))

    return len(empenhos)


def import_orcamentos(load_everything=False):
    if not load_everything:
        print("Importing current orcamentos from current year")
        orcamentos = Orcamento.objects.filter(
            cd_ano_execucao=timezone.now().year,
            execucao__isnull=True, cd_orgao=SME_ORGAO_ID,
        )
    else:
        print("Importing current orcamentos from 2018+")
        orcamentos = Orcamento.objects.filter(
            cd_ano_execucao__gt=2017,
            execucao__isnull=True, cd_orgao=SME_ORGAO_ID,
        )

    for orcamento in orcamentos:
        execucao = ExecucaoTemp.objects.get_or_create_by_orcamento(orcamento)
        if isinstance(execucao, ExecucaoTemp):
            orcamento.execucao_temp = execucao
            orcamento.save()
        else:
            print(execucao['error'])


def import_empenhos(load_everything=False):
    if not load_everything:
        print("Importing current empenhos from current year")
        empenhos = Empenho.objects.filter(
            an_empenho=timezone.now().year,
            execucao__isnull=True, cd_orgao=SME_ORGAO_ID,
        )
    else:
        print("Importing current empenhos from 2018+")
        empenhos = Empenho.objects.filter(
            an_empenho__gt=2017,
            execucao__isnull=True, cd_orgao=SME_ORGAO_ID,
        )

    for empenho in empenhos:
        execucao = ExecucaoTemp.objects.update_by_empenho(empenho)

        if execucao:
            empenho.execucao_temp = execucao
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
