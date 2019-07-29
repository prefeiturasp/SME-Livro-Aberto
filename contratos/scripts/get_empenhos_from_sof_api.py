from contratos import services
from contratos.models import EmpenhoSOFFailedAPIRequest


def run(*args):
    print("Fetching empenhos from SOF API")
    services.update_empenho_sof_cache_table()

    if EmpenhoSOFFailedAPIRequest.objects.count() > 0:
        print("Retrying failed API requests")
        services.retry_empenhos_sof_failed_api_requests()
