from contratos.dao import contratos_raw_dao, empenhos_dao


def update_empenho_sof_cache_table():
    for contrato in contratos_raw_dao.get_all():
        get_empenhos_for_contrato_and_save(
            cod_contrato=contrato.codcontrato,
            ano_exercicio=contrato.anoexercicio)
        print(f'empenhos for contrato {contrato.codcontrato} saved')


def get_empenhos_for_contrato_and_save(*, cod_contrato, ano_exercicio):
    sof_data = empenhos_dao.get_by_codcontrato_and_anoexercicio(
        cod_contrato=cod_contrato,
        ano_exercicio=ano_exercicio)
    empenhos_data = build_empenhos_data(
        sof_data=sof_data,
        ano_exercicio=ano_exercicio,
        cod_contrato=cod_contrato)
    save_empenhos_sof_cache(empenhos_data=empenhos_data)


def build_empenhos_data(*, sof_data, ano_exercicio, cod_contrato):
    empenhos_data = sof_data['lstEmpenhos']
    for data in empenhos_data:
        data['anoExercicio'] = ano_exercicio
        data['codContrato'] = cod_contrato
    return empenhos_data


def save_empenhos_sof_cache(*, empenhos_data):
    for data in empenhos_data:
        empenhos_dao.create(data=data)
