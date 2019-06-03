from budget_execution import services


def run():
    services.load_data_from_orcamento_raw()
    print("Data loaded from orcamento_raw_load")
    services.import_orcamentos()
    print("Orcamento imported")
    services.import_empenhos()
    print("Empenhos imported")
    services.import_minimo_legal()
    print("Minimo Legal imported")
    services.apply_fromto()
    print("From to applied")
