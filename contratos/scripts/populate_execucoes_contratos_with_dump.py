from contratos.services import infrastructure as services


def run(*args):
    services.populate_execucoes_contratos_with_dump()
