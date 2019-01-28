# SME-Livro-Aberto
Projeto de Transparência Orçamentária da Secretaria Municipal da Educação de São Paulo

[![Maintainability](https://api.codeclimate.com/v1/badges/e03a41104c1e2a928c2e/maintainability)](https://codeclimate.com/github/prefeiturasp/SME-Livro-Aberto/maintainability)

Para configuração inicial da aplicação:

Rode as migrações. Além de criar as tabelas da aplicação, criará também as tabelas `orcamento` e `empenhos` que serão populadas pela SME e servirão de base para a geração das execuções.
`python manage.py migrate`

Carregue os dados dos De-Para
`python manage.py loaddata data/fromto.json`

É necessário que as tabelas `orcamento` e `empenhos` já tenham sido populadas antes de rodar o script abaixo, que irá gerar as execuções. Os dados das duas tabelas serão importados e os De-Para aplicados:
`python manage.py runscript generate_execucoes`
