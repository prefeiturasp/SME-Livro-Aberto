from contratos import services


def run(*args):
    services.get_empenhos_for_contratos_from_sof_api()
