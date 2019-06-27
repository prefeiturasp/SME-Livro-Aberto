from budget_execution import services


def run(*args):
    load_everything = bool("load_everything" in args)

    services.erase_current_year_data()

    services.load_data_from_orcamento_raw(load_everything)
    print("Data loaded from orcamento_raw_load")
    services.load_data_from_empenhos_raw(load_everything)
    print("Data loaded from empenhos_raw_load")

    services.import_orcamentos(load_everything)
    print("Orcamento imported")
    services.import_empenhos(load_everything)
    print("Empenhos imported")
    services.import_minimo_legal()
    print("Minimo Legal imported")
    services.apply_fromto()
    print("From to applied")
