# SME-Livro-Aberto
Projeto de Transparência Orçamentária da Secretaria Municipal da Educação de São Paulo

[![Maintainability](https://api.codeclimate.com/v1/badges/e03a41104c1e2a928c2e/maintainability)](https://codeclimate.com/github/prefeiturasp/SME-Livro-Aberto/maintainability)

Para carregar os dados no banco, siga os seguintes passos. É preciso que seja feito em um banco vazio.

Rode as migrações
`python manage.py migrate`

Carregue os dados dos De-Para
`python manage.py loaddata data/fromto.json`

Carregue as execuções
`python manage.py loaddata data/execucoes.json`

Aplique os De-Para
`python manage.py runscript apply_fromto`
