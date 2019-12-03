from regionalizacao.dao.models_dao import (
    DistritoDao, DistritoZonaFromToDao, EscolaDao, EtapaTipoEscolaFromToDao,
    TipoEscolaDao, PtrfFromToDao, RecursoDao, UnidadeRecursosFromToDao,
    BudgetDao,
)


def apply_distrito_zona_fromto():
    ft_dao = DistritoZonaFromToDao()
    distrito_dao = DistritoDao()

    fts = ft_dao.get_all()

    for ft in fts:
        distrito = distrito_dao.get(coddist=ft.coddist)
        if distrito:
            distrito.zona = ft.zona
            distrito.save()


def apply_etapa_tipo_escola_fromto():
    ft_dao = EtapaTipoEscolaFromToDao()
    tipo_dao = TipoEscolaDao()

    fts = ft_dao.get_all()

    for ft in fts:
        tipo = tipo_dao.get(code=ft.tipoesc)
        if tipo:
            tipo.desc = ft.desctipoesc
            tipo.etapa = ft.etapa
            tipo.save()


def apply_ptrf_fromto():
    ft_dao = PtrfFromToDao()
    budget_dao = BudgetDao()

    fts = ft_dao.get_all()

    for ft in fts:
        budget_dao.update_or_create(codesc=ft.codesc, year=ft.year,
                                    ptrf=ft.vlrepasse)


