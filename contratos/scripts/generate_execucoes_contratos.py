from contratos.services import domain as services


def run(*args):
    services.generate_execucoes_contratos_and_apply_fromto()
