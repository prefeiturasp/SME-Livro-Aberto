# SME-Livro-Aberto
Projeto de Transparência Orçamentária da Secretaria Municipal da Educação de São Paulo

[![Maintainability](https://api.codeclimate.com/v1/badges/e03a41104c1e2a928c2e/maintainability)](https://codeclimate.com/github/prefeiturasp/SME-Livro-Aberto/maintainability)

## Desenvolvimento

Para configurações do ambiente de desenvolvimento, acesse [CONTRIBUTING](CONTRIBUTING.md).

## Configuração inicial das aplicações Mosaico e Geologia

Rode as migrações. Além de criar as tabelas da aplicação, criará também as tabelas `orcamento_raw_load` e `empenhos_raw_load` que serão populadas pela SME e servirão de base para a geração das execuções.

```bash
$ python manage.py migrate
```

Para carregar o dump das tabelas `orcamento_raw_load` e `empenhos_raw_load`:
```bash
$ python manage.py runscript populate_orcamento_empenhos_raw_load_with_dump
```

É necessário que as tabelas `orcamento_raw_load` e `empenhos` já tenham sido populadas antes de rodar o script abaixo. Será feito:

1) Carga do json `data/2003_2017_everything.json` que contém:
  a) Execuções de 2003 a 2017 (SME e Mínimo Legal)
  b) De-Para de 2010 a 2018
  c) Dados dos gnds
  d) Dados de Mĩnimo Legal de 2014 a 2017

2) Carga da tabela `orcamento` com os dados (2018+) da `orcamento_raw_load`

3) Geração das novas execuções (2018+) a partir das tabelas `orcamento` e `empenhos` (que deverá ser populada pela SME)

4) Aplicação dos De-Para
```bash
$ python manage.py runscript load_2003_2017_execucoes_and_generate_new_ones
```

### Gerando novas execuções

Após a configuração inicial da aplicação, o script abaixo deve ser rodado regularmente para atualizar a base de dados gerando as novas execuções a partir dos novos dados que a SME carrega nas tabelas `orcamento_raw_load` e `empenos`. O que será feito:
1) Atualização da tabela `orcamento` a partir dos dados do ano corrente da tabela `orcamento_raw_load`
2) Considerando apenas o ano corrente, geração de novas execuções e atualização de existentes a partir dos dados das tabelas `orcamento` e `empenhos`
3) Aplicação dos De-Para
```bash
$ python manage.py runscript generate_execucoes
```

## Configuração inicial da aplicação Contratos

As aplicações usam o mesmo banco, então ao rodar as migrações nas configurações do Mosaico e do Geologia, as tabelas de Contratos também foram criadas, inbclusive a tabela `contratos_raw_load` que será populada pela SME.

Para carregar o dump da tabela `contratos_raw_load`:
```bash
$ python manage.py runscript populate_contratos_raw_load_with_dump
```

### Gerando novas execuções de contratos

Para gerar as execuções de contratos precisamos buscar os dados dos empenhos na API da SOF e cruzar com os dados de contratos passados pela SME.

O script abaixo varre a tabela `contratos_raw_load`, busca na API da SOF e salva no banco da aplicação os empenhos referentes a cada um dos contratos da tabela:
```bash
$ python manage.py runscript get_empenhos_for_contratos_from_sof_api
```

E este gera as execuções, fazendo o cruzamento dos dados das duas tabelas e aplicando o de-para de categorias:
```bash
$ python manage.py runscript generate_execucoes_contratos_and_apply_fromto
```
