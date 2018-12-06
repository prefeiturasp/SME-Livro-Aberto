from from_to_handler import models


def run():
    models.DotacaoFromTo.apply_all()
    print("Dotação Grupo Subgrupo applied")
    models.FonteDeRecursoFromTo.apply_all()
    print("Fonte de recurso applied")
    models.SubelementoFromTo.apply_all()
    print("Subelemento applied")
    models.GNDFromTo.apply_all()
    print("Gnd applied")
