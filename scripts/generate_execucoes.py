from budget_execution import services


def run():
    services.import_orcamentos()
    print("Orcamento imported")
    services.import_empenhos()
    print("Empenhos imported")
    services.import_minimo_legal()
    print("Minimo Legal imported")
    services.apply_fromto()
    print("From to applied")
