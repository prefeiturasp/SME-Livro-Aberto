from contratos.dao import contratos_raw_dao, empenhos_dao, empenhos_temp_dao, \
    empenhos_failed_requests_dao


def fetch_empenhos_from_sof_and_save_to_temp_table():
    for contrato in contratos_raw_dao.get_all():
        count = get_empenhos_for_contrato_and_save(
            cod_contrato=contrato.codcontrato,
            ano_exercicio=contrato.anoexercicio)
        print(f'{count} empenhos saved for contrato {contrato.codcontrato}')


def get_empenhos_for_contrato_and_save(*, cod_contrato, ano_exercicio,
                                       ano_empenho=None):

    if not ano_empenho:
        sof_data = empenhos_dao.get_by_codcontrato_and_anoexercicio(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio)
    else:
        sof_data = empenhos_dao.get_by_ano_empenho(
            cod_contrato=cod_contrato,
            ano_exercicio=ano_exercicio,
            ano_empenho=ano_empenho)

    if not sof_data:
        return 0

    empenhos_data = build_empenhos_data(
        sof_data=sof_data,
        ano_exercicio=ano_exercicio,
        cod_contrato=cod_contrato)
    count = save_empenhos_sof_cache(empenhos_data=empenhos_data)
    return count


def build_empenhos_data(*, sof_data, ano_exercicio, cod_contrato):
    empenhos_data = sof_data.copy()
    for data in empenhos_data:
        data['anoExercicio'] = ano_exercicio
        data['codContrato'] = cod_contrato
    return empenhos_data


def save_empenhos_sof_cache(*, empenhos_data):
    for data in empenhos_data:
        empenhos_temp_dao.create(data=data)

    return len(empenhos_data)


def retry_empenhos_sof_failed_api_requests():
    for failed_request in empenhos_failed_requests_dao.get_all():
        count = get_empenhos_for_contrato_and_save(
            cod_contrato=failed_request.cod_contrato,
            ano_exercicio=failed_request.ano_exercicio,
            ano_empenho=failed_request.ano_empenho,
        )
        empenhos_failed_requests_dao.delete(failed_request)
        print(
            f'{count} empenhos saved for contrato {failed_request.cod_contrato}'
        )
