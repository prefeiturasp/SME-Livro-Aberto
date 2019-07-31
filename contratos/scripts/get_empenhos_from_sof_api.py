from contratos import services
from contratos.models import EmpenhoSOFFailedAPIRequest


def run(*args):
    print("Fetching empenhos from SOF API and saving to temp table")
    services.fetch_empenhos_from_sof_and_save_to_temp_table()

    if EmpenhoSOFFailedAPIRequest.objects.count() > 0:
        print("Retrying failed API requests")
        services.retry_empenhos_sof_failed_api_requests()
