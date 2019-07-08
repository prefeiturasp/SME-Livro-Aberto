from budget_execution import services


def run(*args):
    print("Loading execucoes from 2003 to 2017")
    services.load_2003_2017_execucoes_from_json()
    print("2003-2017 execucoes loaded")

    print("Loading 2018+ data from orcamento_raw_load")
    services.load_data_from_orcamento_raw(load_everything=True)

    print("Loading 2018+ data from empenhos_raw_load")
    services.load_data_from_empenhos_raw(load_everything=True)

    print("Generating execucoes:")
    print("Importing Minimo Legal")
    services.import_minimo_legal()

    print("Importing orcamentos to ExecucaoTemp")
    services.import_orcamentos(load_everything=True)
    print("Importing empenhos to ExecucaoTemp")
    services.import_empenhos(load_everything=True)
    print("Moving execucoes from ExecucaoTemp to Execucao")
    services.update_execucao_table_from_execucao_temp(load_everything=True)
    print("Applying From To")
    services.apply_fromto()
    print("Execucoes generated")
