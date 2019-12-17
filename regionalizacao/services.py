from regionalizacao.dao import eol_api_dao
from regionalizacao.dao.models_dao import (
    DistritoDao, DistritoZonaFromToDao, EtapaTipoEscolaFromToDao,
    TipoEscolaDao, PtrfFromToDao, RecursoDao, UnidadeRecursosFromToDao,
    BudgetDao, EscolaInfoDao, UnidadeRecursosFromToSpreadsheetDao,
    PtrfFromToSpreadsheetDao
)


def update_regionalizacao_data():
    print('## Extracting PTRF and UnidadeRecursos spreadsheets ##')
    extract_ptrf_and_recursos_spreadsheets()
    print('## Updating regionalizacao data from EOL API ##')
    update_data_from_eol_api()
    print('## Applying from-tos ##')
    apply_fromtos()
    print('## Populating escola_info table with budget data ##')
    populate_escola_info_budget_data()



def get_years_to_be_updated():
    ptrf_sheet_dao = PtrfFromToSpreadsheetDao()
    recursos_sheet_dao = UnidadeRecursosFromToSpreadsheetDao()

    ptrf_years = ptrf_sheet_dao.get_years_to_be_updated()
    recursos_years = recursos_sheet_dao.get_years_to_be_updated()

    return list(set(ptrf_years + recursos_years))

def extract_ptrf_and_recursos_spreadsheets():
    ptrf_sheet_dao = PtrfFromToSpreadsheetDao()
    recursos_sheet_dao = UnidadeRecursosFromToSpreadsheetDao()

    ptrf_sheet_dao.extract_new_spreadsheets()
    recursos_sheet_dao.extract_new_spreadsheets()
    # TODO: return created_at of newest spreadsheet to be saved
    # in EscolaInfo


def update_data_from_eol_api():
    eol_api_dao.update_escola_table()


def apply_fromtos():
    apply_distrito_zona_fromto()
    apply_etapa_tipo_escola_fromto()
    apply_ptrf_fromto()
    apply_unidade_recursos_fromto()


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


def apply_unidade_recursos_fromto():
    ft_dao = UnidadeRecursosFromToDao()
    recurso_dao = RecursoDao()

    fts = ft_dao.get_all()
    for ft in fts:
        recurso_dao.update_or_create(
            codesc=ft.codesc,
            year=ft.year,
            grupo_name=ft.grupo,
            subgrupo_name=ft.subgrupo,
            valor=ft.valor,
            label=ft.label)


def populate_escola_info_budget_data():
    budget_dao = BudgetDao()
    info_dao = EscolaInfoDao()

    budgets = budget_dao.get_all()
    for budget in budgets:
        recursos, total = budget_dao.build_recursos_data(budget)
        info_dao.update(
            escola_id=budget.escola.id, year=budget.year,
            budget_total=total, recursos=recursos)
