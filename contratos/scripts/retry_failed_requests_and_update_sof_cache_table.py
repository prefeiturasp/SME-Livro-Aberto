from contratos.services import sof_api as services


def run(*args):
    services.retry_failed_requests_and_update_sof_cache_table()
