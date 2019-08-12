import os
import zipfile

from decimal import Decimal

from django.core.management import call_command
from django.db.models import Sum
from django.utils import timezone

from budget_execution import constants
from budget_execution import exceptions
from budget_execution.constants import (
    SME_ORGAO_ID, ORCAMENTO_EMPENHOS_RAW_DUMP_DIR_PATH,
    ORCAMENTO_EMPENHOS_RAW_DUMP_FILENAME)
from budget_execution.models import (
    Execucao, ExecucaoTemp, Orcamento, OrcamentoRaw, Orgao,
    Empenho, EmpenhoRaw, MinimoLegal, ProjetoAtividade)
from from_to_handler.models import (DotacaoFromTo, FonteDeRecursoFromTo,
                                    SubelementoFromTo, GNDFromTo)


def erase_data_to_be_updated(load_everything=False):
    if not load_everything:
        current_year = timezone.now().year
        Orcamento.objects.filter(cd_ano_execucao=current_year).delete()
        Empenho.objects.filter(an_empenho=current_year).delete()
    else:
        Orcamento.objects.filter(cd_ano_execucao__gt=2017).delete()
        Empenho.objects.filter(an_empenho__gt=2017).delete()

    # erasing ExecucaoTemp table
    ExecucaoTemp.objects.all().delete()


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
        print("Importing orcamentos from current year")
        orcamentos = Orcamento.objects.filter(
            cd_ano_execucao=timezone.now().year,
            execucao_temp__isnull=True, cd_orgao=SME_ORGAO_ID,
        )
    else:
        print("Importing orcamentos from 2018+")
        orcamentos = Orcamento.objects.filter(
            cd_ano_execucao__gt=2017,
            execucao_temp__isnull=True, cd_orgao=SME_ORGAO_ID,
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
        print("Importing empenhos from current year")
        empenhos = Empenho.objects.filter(
            an_empenho=timezone.now().year,
            execucao_temp__isnull=True, cd_orgao=SME_ORGAO_ID,
        )
    else:
        print("Importing empenhos from 2018+")
        empenhos = Empenho.objects.filter(
            an_empenho__gt=2017,
            execucao_temp__isnull=True, cd_orgao=SME_ORGAO_ID,
        )

    for empenho in empenhos:
        execucao = ExecucaoTemp.objects.update_by_empenho(empenho)

        if execucao:
            empenho.execucao_temp = execucao
            empenho.save()


def update_execucao_table_from_execucao_temp(load_everything=False):
    if not load_everything:
        execucoes = Execucao.objects.filter(
            year__year=timezone.now().year,
            is_minimo_legal=False,
            orgao_id=SME_ORGAO_ID)
        execucoes_temp = ExecucaoTemp.objects.filter(
            year__year=timezone.now().year,
            orgao_id=SME_ORGAO_ID)
    else:
        execucoes = Execucao.objects.filter(
            year__year__gt=2017,
            is_minimo_legal=False,
            orgao_id=SME_ORGAO_ID)
        execucoes_temp = ExecucaoTemp.objects.filter(
            year__year__gt=2017,
            orgao_id=SME_ORGAO_ID)

    verify_total_sum(execucoes, execucoes_temp)

    execucoes.delete()

    for exec_temp in execucoes_temp:
        execucao = Execucao()

        for field in exec_temp._meta.fields:
            if field.primary_key is True:
                continue
            setattr(execucao, field.name, getattr(exec_temp, field.name))

        execucao.save()
        exec_temp.delete()


def verify_total_sum(execucoes, execucoes_temp):
    orc_percent_limit = Decimal(constants.ORCADO_DIFFERENCE_PERCENT_LIMIT)
    emp_percent_limit = Decimal(constants.EMPENHADO_DIFFERENCE_PERCENT_LIMIT)

    orcado_execs = execucoes.aggregate(total=Sum('orcado_atualizado'))["total"]
    orcado_temp = execucoes_temp.aggregate(
        total=Sum('orcado_atualizado'))["total"]

    if orcado_execs:
        orc_upper_limit = orcado_execs + (orcado_execs * orc_percent_limit)
        orc_lower_limit = orcado_execs - (orcado_execs * orc_percent_limit)
        if orcado_temp > orc_upper_limit or orcado_temp < orc_lower_limit:
            msg = (
                'A diferença entre o novo somatório do valor orçado e o '
                'somatório atual é maior que o limite. As execuções não '
                'serão atualizadas.\n'
            )
            msg += f'Orcado atual: {orcado_execs} \nNovo orcado: {orcado_temp}'
            raise exceptions.OrcadoDifferenceOverLimitException(msg)

    empenhado_execs = execucoes.aggregate(
        total=Sum('empenhado_liquido'))['total']
    empenhado_temp = execucoes_temp.aggregate(
        total=Sum('empenhado_liquido'))['total']

    if empenhado_execs:
        emp_upper_limit = empenhado_execs + (
            empenhado_execs * emp_percent_limit)
        emp_lower_limit = empenhado_execs - (
            empenhado_execs * emp_percent_limit)
        if empenhado_temp > emp_upper_limit or empenhado_temp < emp_lower_limit:
            msg = (
                'A diferença entre o novo somatório do valor empenhado e o '
                'somatório atual é maior que o limite. As execuções não serão'
                ' atualizadas.\n'
                f'Empenhado atual: {empenhado_execs} \n'
                f'Novo Empenhado: {empenhado_temp}'
            )
            raise exceptions.EmpenhadoDifferenceOverLimitException


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


def populate_orcamento_empenhos_raw_load_with_dump():
    filepath = f'{ORCAMENTO_EMPENHOS_RAW_DUMP_DIR_PATH}{ORCAMENTO_EMPENHOS_RAW_DUMP_FILENAME}'  # noqa
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(ORCAMENTO_EMPENHOS_RAW_DUMP_DIR_PATH)

    json_filename = zip_ref.filelist[0].filename
    json_filepath = f'{ORCAMENTO_EMPENHOS_RAW_DUMP_DIR_PATH}{json_filename}'

    try:
        call_command('loaddata', json_filepath)
    except Exception as e:
        print(e)
        os.remove(json_filepath)
    os.remove(json_filepath)
