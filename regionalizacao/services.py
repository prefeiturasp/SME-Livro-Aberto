import openpyxl

from datetime import date

from regionalizacao.dao import eol_api_dao
from regionalizacao.dao.models_dao import (
    DistritoDao, DistritoZonaFromToDao, EtapaTipoEscolaFromToDao,
    TipoEscolaDao, PtrfFromToDao, RecursoDao, UnidadeRecursosFromToDao,
    BudgetDao, EscolaInfoDao, UnidadeRecursosFromToSpreadsheetDao,
    PtrfFromToSpreadsheetDao, UpdateHistoryDao
)
from regionalizacao.models import UnidadeValoresVerbaFromTo, EscolaInfo, Budget
from regionalizacao.use_cases import GenerateXlsxFilesUseCase


def update_regionalizacao_data():
    """
    Verifica se há novas planilhas importadas. Se sim, extrai as planilhas e
    faz todo o resto do processo de atualização. Se não, termina o script
    sem alterar a Data de Atualização que aparece na interface.
    """
    print('## Extracting PTRF and UnidadeRecursos spreadsheets ##')
    new_data_added = extract_ptrf_and_recursos_spreadsheets()
    if not new_data_added:
        print('No new spreadsheets were found. Exiting script.')
        return

    print('## Verifying new data from spreadsheets ##')
    years = get_years_to_be_updated()
    print('## Updating regionalizacao data from EOL API ##')
    update_data_from_eol_api(years)
    print('## Applying from-tos ##')
    apply_fromtos()
    print('## Populating escola_info table with budget data ##')
    populate_escola_info_budget_data()
    print('## Generating download spreadsheets ##')
    generate_xlsx_files()
    update_updated_at_date()


def update_regionalizacao_data_forced():
    """
    Faz todo o resto do processo de atualização independente se há novas
    planilhas importadas ou não. Altera a Data de Atualização mesmo que
    nada tenha sido atualizado.
    """
    print('## Verifying new data from spreadsheets ##')
    years = get_years_to_be_updated()
    print('## Updating regionalizacao data from EOL API ##')
    update_data_from_eol_api(years)
    print('## Extracting PTRF and UnidadeRecursos spreadsheets ##')
    extract_ptrf_and_recursos_spreadsheets()
    print('## Applying from-tos ##')
    apply_fromtos()
    print('## Populating escola_info table with budget data ##')
    populate_escola_info_budget_data()
    print('## Generating download spreadsheets ##')
    generate_xlsx_files()
    update_updated_at_date()


def update_data_from_eol_api(years):
    eol_api_dao.update_escola_table(years)


def get_years_to_be_updated():
    ptrf_sheet_dao = PtrfFromToSpreadsheetDao()
    recursos_sheet_dao = UnidadeRecursosFromToSpreadsheetDao()
    escola_info_dao = EscolaInfoDao()

    ptrf_years = ptrf_sheet_dao.get_years_to_be_updated()
    recursos_years = recursos_sheet_dao.get_years_to_be_updated()
    years_list = ptrf_years + recursos_years

    # current year escola info should always be updated if there's already data
    # saved, even though theres no new resource or ptrf data.
    newest_year = escola_info_dao.get_newest_year()
    if newest_year == date.today().year:
        years_list.append(newest_year)

    return list(set(years_list))


def extract_ptrf_and_recursos_spreadsheets():
    ptrf_sheet_dao = PtrfFromToSpreadsheetDao()
    recursos_sheet_dao = UnidadeRecursosFromToSpreadsheetDao()

    ptrf_extracted = ptrf_sheet_dao.extract_new_spreadsheets()
    recursos_extracted = recursos_sheet_dao.extract_new_spreadsheets()

    return bool(ptrf_extracted or recursos_extracted)


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


def generate_xlsx_files():
    from regionalizacao.serializers import (EscolaInfoDownloadSerializer,
                                            UnidadeRecursosFromToSerializer)
    info_dao = EscolaInfoDao()
    recursos_dao = UnidadeRecursosFromToDao()

    uc = GenerateXlsxFilesUseCase(
        info_dao=info_dao,
        recursos_dao=recursos_dao,
        info_serializer_class=EscolaInfoDownloadSerializer,
        recursos_serializer_class=UnidadeRecursosFromToSerializer,
        data_handler=openpyxl,
    )

    uc.execute()


def update_updated_at_date():
    dao = UpdateHistoryDao()
    dao.create()


def get_dt_updated():
    dao = UpdateHistoryDao()
    dt_updated = dao.get_last_update_date()
    if not dt_updated:
        return get_sheets_last_created_at()
    return dt_updated


def get_sheets_last_created_at():
    ptrf_sheet_dao = PtrfFromToSpreadsheetDao()
    recursos_sheet_dao = UnidadeRecursosFromToSpreadsheetDao()

    ptrf_date = ptrf_sheet_dao.get_last_created_at()
    recursos_date = recursos_sheet_dao.get_last_created_at()

    if ptrf_date and recursos_date:
        return max([ptrf_date, recursos_date])
    elif ptrf_date:
        return ptrf_date
    elif recursos_date:
        return recursos_date
    return None


def update_recursos_com_verbas():
    unidades_verba_valores = UnidadeValoresVerbaFromTo.objects.filter(
        situacao__iexact='aprovado',
        data_do_encerramento__isnull=True
    )
    for unidade in unidades_verba_valores:
        try:
            budget = Budget.objects.get(escola__codesc=unidade.codigo_escola, year=unidade.year)
            budget.valor_mensal = unidade.valor_mensal or 0
            budget.verba_locacao = unidade.verba_locacao or 0
            budget.valor_mensal_iptu = unidade.valor_mensal_iptu or 0
            budget.save()
            escola_info = EscolaInfo.objects.get(escola__codesc=unidade.codigo_escola, year=unidade.year)
            if not escola_info.recursos:
                escola_info.recursos = {}
            escola_info.recursos.update({
                'valor_mensal': budget.valor_mensal,
                'verba_locacao': budget.verba_locacao,
                'valor_mensal_iptu': budget.valor_mensal_iptu
            })
            if not escola_info.budget_total:
                escola_info.budget_total = 0
            escola_info.budget_total += budget.valor_mensal + budget.verba_locacao + budget.valor_mensal_iptu
            escola_info.save()
            print(unidade.codigo_escola + ': deu certo')
        except Budget.DoesNotExist:
            print(unidade.codigo_escola + ': budget n existe')
            if EscolaInfo.objects.filter(escola__codesc=unidade.codigo_escola, year=unidade.year).exists():
                print('TEM ESCOLA INFO')
                escola_info = EscolaInfo.objects.get(escola__codesc=unidade.codigo_escola, year=unidade.year)
                budget = Budget(
                    escola=escola_info.escola,
                    year=unidade.year,
                    valor_mensal=unidade.valor_mensal or 0,
                    verba_locacao=unidade.verba_locacao or 0,
                    valor_mensal_iptu=unidade.valor_mensal_iptu or 0
                )
                budget.save()
                if not escola_info.recursos:
                    escola_info.recursos = {}
                escola_info.recursos.update({
                    'valor_mensal': budget.valor_mensal,
                    'verba_locacao': budget.verba_locacao,
                    'valor_mensal_iptu': budget.valor_mensal_iptu
                })
                if not escola_info.budget_total:
                    escola_info.budget_total = 0
                escola_info.budget_total += budget.valor_mensal + budget.verba_locacao + budget.valor_mensal_iptu
                escola_info.save()
            else:
                print('nao tem escola info')
        except EscolaInfo.DoesNotExist:
            print(unidade.codigo_escola + ': escola info n existe')

