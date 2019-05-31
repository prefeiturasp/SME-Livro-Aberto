from budget_execution import services


def run():
    services.load_data_from_orcamento_raw()
    print("Orcamento loaded")
    services.load_data_from_empenhos_raw()
    print("Empenhos loaded")
