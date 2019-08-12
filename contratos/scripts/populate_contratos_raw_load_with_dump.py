from contratos.services import infrastructure as services


def run(*args):
    services.populate_contratos_raw_load_with_dump()
