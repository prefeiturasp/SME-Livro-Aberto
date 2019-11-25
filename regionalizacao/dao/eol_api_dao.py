import requests

from regionalizacao.constants import EOL_API_URL
from regionalizacao.dao.models_dao import DreDao


def update_dre_table():
    dre_dao = DreDao()
    url = f'{EOL_API_URL}escolas/'

    response = requests.get(url)
    results = response['results']

    created_count = 0
    updated_count = 0
    for dre_dict in results:
        _, created = dre_dao.update_or_create(
            code=dre_dict['dre'],
            name=dre_dict['diretoria'],
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    return created_count, updated_count
