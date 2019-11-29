from regionalizacao.dao.models_dao import DistritoDao, DistritoZonaFromToDao


def apply_distrito_zona_fromto():
    ft_dao = DistritoZonaFromToDao()
    distritos_dao = DistritoDao()

    fts = ft_dao.get_all()

    for ft in fts:
        distrito = distritos_dao.get(coddist=ft.coddist)
        if distrito:
            distrito.zona = ft.zona
            distrito.save()
