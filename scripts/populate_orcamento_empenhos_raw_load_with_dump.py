from budget_execution import services


def run(*args):
    services.populate_orcamento_empenhos_raw_load_with_dump()
