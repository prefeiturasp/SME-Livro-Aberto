from budget_execution.models import Execucao, Grupo, Subgrupo
from from_to_handler.models import DotacaoFromTo


def apply_dotacoes_grupo_subgrupo_fromto():
    fts = DotacaoFromTo.objects.all()

    for ft in fts:
        apply_dotacao_fromto(ft)


def apply_dotacao_fromto(dotacao_fromto):
    ft = dotacao_fromto
    execucoes = Execucao.objects.filter_by_indexer(ft.indexer)
    if not execucoes:
        return

    grupo = get_or_create_grupo(ft.grupo_code, ft.grupo_desc)
    subgrupo = get_or_create_subgrupo(
        ft.subgrupo_code, grupo, ft.subgrupo_desc)

    for ex in execucoes:
        ex.subgrupo = subgrupo
        ex.save()


def get_or_create_grupo(grupo_id, grupo_desc):
    grupo, _ = Grupo.objects.get_or_create(
        id=grupo_id, defaults={'desc': grupo_desc})

    return grupo


def get_or_create_subgrupo(subgrupo_code, grupo, subgrupo_desc):
    subgrupo, _ = Subgrupo.objects.get_or_create(
        code=subgrupo_code, grupo=grupo, defaults={'desc': subgrupo_desc})
    return subgrupo
