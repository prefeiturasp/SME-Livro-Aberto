import requests

from datetime import date

from regionalizacao.constants import EOL_API_URL
from regionalizacao.dao.models_dao import EscolaDao


def update_escola_table(years):
    escola_dao = EscolaDao()
    url = f'{EOL_API_URL}livroaberto_escolas/'

    print('Fetching schools data from EOL API')
    response = requests.get(url)
    results = response.json()['results']

    print('Saving data')
    created_count = 0
    current_year = date.today().year
    for escola_dict in results:
        escola_data = dict(
            dre=escola_dict["dre"],
            codesc=escola_dict["codesc"],
            tipoesc=escola_dict["tipoesc"],
            nomesc=escola_dict["nomesc"],
            diretoria=escola_dict["diretoria"],
            endereco=escola_dict["endereco"],
            numero=escola_dict["numero"],
            bairro=escola_dict["bairro"],
            cep=escola_dict["cep"],
            situacao=escola_dict["situacao"],
            coddist=escola_dict["coddist"],
            distrito=escola_dict["distrito"],
            rede=escola_dict["rede"],
            latitude=escola_dict["latitude"],
            longitude=escola_dict["longitude"],
            total_vagas=escola_dict["total_vagas"],
        )

        # current year info should always be updated
        _, created = escola_dao.update_or_create(**escola_data)
        if created:
            created_count += 1

        for year in years:
            if year != current_year:
                created = escola_dao.create_for_previous_year(
                    **escola_data, year=year)
                if created:
                    created_count += 1

    return created_count
