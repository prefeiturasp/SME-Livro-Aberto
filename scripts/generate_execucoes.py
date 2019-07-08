from budget_execution import services


def run(*args):
    load_everything = bool("load_everything" in args)

    services.erase_data_to_be_updated(load_everything)

    services.load_data_from_orcamento_raw(load_everything)
    print("Data loaded from orcamento_raw_load")
    services.load_data_from_empenhos_raw(load_everything)
    print("Data loaded from empenhos_raw_load")

    print("Generating execucoes:")
    print("Importing Minimo Legal")
    services.import_minimo_legal()

    print("Importing orcamentos to ExecucaoTemp")
    services.import_orcamentos(load_everything)
    print("Moving execucoes from ExecucaoTemp to Execucao")
    services.import_empenhos(load_everything)
    print("Moving execucoes from ExecucaoTemp to Execucao")
    services.update_execucao_table_from_execucao_temp(load_everything)
    print("Applying From To")
    services.apply_fromto()
    print("Execucoes generated")
