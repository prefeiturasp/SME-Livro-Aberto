from contratos.dao import contratos_raw_dao, empenhos_dao


def update_empenho_sof_cache_table():
    for contrato in contratos_raw_dao.get_all():
        count = get_empenhos_for_contrato_and_save(
            cod_contrato=contrato.codcontrato,
            ano_exercicio=contrato.anoexercicio)
        print(f'{count} empenhos saved for contrato {contrato.codcontrato}')


def get_empenhos_for_contrato_and_save(*, cod_contrato, ano_exercicio):
    sof_data = empenhos_dao.get_by_codcontrato_and_anoexercicio(
        cod_contrato=cod_contrato,
        ano_exercicio=ano_exercicio)
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
        empenhos_dao.create(data=data)

    return len(empenhos_data)
