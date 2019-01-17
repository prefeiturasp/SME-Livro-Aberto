from datetime import date

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


def import_orcamento():
    orcamentos = Orcamento.objects.filter(execucao__isnull=True)

    for orcamento in orcamentos:
        execucao = Execucao()
        execucao.year = date(orcamento.cd_ano_execucao, 1, 1)
        execucao.orgao = Orgao.objects.get_or_create(
            id=orcamento.cd_orgao,
            defaults={"desc": orcamento.ds_orgao,
                      "initials": orcamento.sg_orgao},
        )[0]
        execucao.projeto = ProjetoAtividade.objects.get_or_create(
            id=orcamento.cd_projeto_atividade,
            defaults={"desc": orcamento.ds_projeto_atividade,
                      "type": orcamento.tp_projeto_atividade},
        )[0]
        execucao.categoria = Categoria.objects.get_or_create(
            id=orcamento.ds_categoria_despesa,
            defaults={"desc": orcamento.ds_categoria},
        )[0]
        execucao.gnd = Gnd.objects.get_or_create(
            id=orcamento.cd_grupo_despesa,
            defaults={"desc": orcamento.ds_grupo_despesa}
        )[0]
        execucao.modalidade = Modalidade.objects.get_or_create(
            id=orcamento.cd_modalidade,
            defaults={"desc": orcamento.ds_modalidade}
        )[0]
        execucao.elemento = Elemento.objects.get_or_create(
            id=orcamento.cd_elemento,
            # elemento.desc is populated by Empenho
        )[0]
        execucao.fonte = FonteDeRecurso.objects.get_or_create(
            id=orcamento.cd_fonte,
            defaults={"desc": orcamento.ds_fonte}
        )[0]
        execucao.subfuncao = Subfuncao.objects.get_or_create(
            id=orcamento.cd_subfuncao,
            defaults={"desc": orcamento.ds_subfuncao}
        )[0]
        execucao.programa = Programa.objects.get_or_create(
            id=orcamento.cd_programa,
            defaults={"desc": orcamento.ds_programa}
        )[0]

        execucao.orcado_atualizado = orcamento.vl_orcado_atualizado
        execucao.save()
        orcamento.execucao = execucao
        orcamento.save()
