from regionalizacao.models import *
from regionalizacao.services import *


def update_2018_create_2019():
    print("# extrair recursos 2019")
    u = UnidadeRecursosFromToSpreadsheet.objects.get(year=2019)
    u.extract_data()
    print("# extrair ptrf 2019")
    p = PtrfFromToSpreadsheet.objects.get(year=2019)
    p.extract_data()
    print("# explodir todos os escola info 2018")
    EscolaInfo.objects.all().delete()
    print("# explodir budgets e recursos 2018")
    Budget.objects.all().delete()
    print("# criar objetos EscolaInfo 2018 e 2019")
    years = [2018, 2019]
    update_data_from_eol_api(years)
    print("# normalizar códigos EOL para 6 dígitos nos recursos PTRF 2019")
    normalize_ptrf()
    print("# criar recursos PTRF")
    apply_ptrf_fromto()
    print("# criar recursos Pessoal e Kit Material")
    apply_unidade_recursos_fromto()
    print("# popular EscolaInfos com recursos")
    populate_escola_info_budget_data()
    print("# criar e popular escola restante: 400761")
    checar_escolas_que_nao_tem_escola_info_2019()
    print("# popular EscolaInfos de escolas parceiras com recusos mensais")
    update_recursos_com_verbas()
    print("# migração das DREs")
    update_dres_por_zona()
    print("# normalizar DREs")
    normalize_dres()

