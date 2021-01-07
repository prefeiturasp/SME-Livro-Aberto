# README
---

[![Maintainability](https://api.codeclimate.com/v1/badges/e03a41104c1e2a928c2e/maintainability)](https://codeclimate.com/github/prefeiturasp/SME-Livro-Aberto/maintainability)

# Contribuições

Para configurações do ambiente de desenvolvimento, acesse [CONTRIBUTING](CONTRIBUTING.md).

# Estratégia de Transformação Digital e Governo Aberto na SME

Como um governo pode atuar para garantir o bem comum de todos? Na SME, acreditamos que um dos meios para isso seja garantir transparência e prestação de contas e constante relação entre governo e sociedade para o desenvolvimento e implementação de políticas públicas. 

A Portaria SME nº 8.008, de 12 de novembro de 2018 oficializou a estratégia da Secretaria Municipal de Educação de SP para que nossas ações sejam pautadas nos princípios de Governo Aberto e para usarmos os valores e benefícios do mundo digital para melhorarmos nossos processos e serviços para os cidadãos. 
Com isso, pretendemos: 
- aumentar os níveis de transparência ativa e de abertura de dados, garantindo a proteção de dados pessoais; 
- instituir metodologias ágeis e colaborativas como parte do processo de desenvolvimento e de evolução de sistemas administrativos e de serviços digitais; 
- fortalecer o controle das políticas educacionais e da aplicação de recursos por parte da gestão e da sociedade; 
- promover espaços e metodologias de colaboração entre governo, academia, sociedade civil e setor privado. 

O [Ateliê do Software](http://forum.govit.prefeitura.sp.gov.br/uploads/default/original/1X/c88a4715eb3f9fc3ceb882c1f6afe9e308805a17.pdf) é uma das ferramentas para operacionalização. Baseado em um modelo de contratação inspirado pelos movimentos ágil e de Software Craftsmanship, trabalhamos com equipes multidisciplinares para o desenvolvimento de produtos que beneficiam toda a comunidade escolar (técnicos da SME e DREs, gestores, professores, alunos e famílias) e concretizam os objetivos da Estratégia de Transformação Digital e Governo Aberto “Pátio Digital”.

**Conteúdo:**
 1. [Sobre o Produto](#Livro-Aberto)
 2. [Como surgiu](#Como-surgiu)
 3. [Funcionalidades](#Funcionalidades)
 4. [Jornadas](#Jornadas)
 5. [Roadmap] (#Roadmap)
 5. [Como contribuir](#como-contribuir)
 6. [Instalação e Configuração](#Configuracao-do-projeto)
 
# Livro Aberto

O **Livro Aberto** é o Projeto da Secretaria Municipal de Educação de São Paulo desenvolvido pelo Pátio Digital, para dar transparência ao orçamento e ampliar participação da comunidade escolar. Foi selecionado como uma das quatro experiências inovadoras entre governos da América Latina e Caribe em 2018.

Por meio desse projeto, a SME vai apresentar uma interface didática de visualização do orçamento previsto e executado em cada ano, além de permitir que se conheçam as despesas no maior nível de detalhamento possível. 

Por fim, um módulo de consultas deve permitir que a comunidade escolar conheça os bens e serviços contratados pela SME e pelas diretorias regionais, de forma que possa apoiar a Secretaria na avaliação da qualidade e no monitoramento da execução dos contratos no território da cidade.

## **Visão de Futuro** 

Para **os cidadãos da cidade de São Paulo e as comunidades das unidades escolares municipais** 

Que **desejam informações sobre o orçamento da secretaria municipal de educação** 

O **Livro Aberto** 

É um **portal**   

Que **apresenta visualização do orçamento previsto e executado em cada ano, além de permitir que se conheçam as despesas no maior nível de detalhamento possível** 

Diferentemente de **entrar em contato com os dados apenas via Lei de Acesso à Informação** 

O Nosso produto  **permite, a partir de interface didática, que a comunidade escolar conheça os bens e serviços contratados pela SME e pelas diretorias regionais, de forma que possa apoiar a Secretaria na avaliação da qualidade e no monitoramento da execução dos contratos no território da cidade** 


## É / Não é / Faz / Não faz: 

--- 

- **É**: Sistema de consulta simplificada de dados orçamentários, contendo todas as unidades da rede, diretas e parceiras, agrupadas por zona (Centro, Norte, Leste, Sul e Oeste), diretoria regional e bairro. 

- **Não é**: Uma ferramenta que permite ajuste de dados. Também não existem informações em tempo real. Os dados são carregados no sistema pela SME, após serem consolidados. 

- **Faz**: Facilita o acesso a informação por parte de qualquer cidadão, estando disponível de forma aberta na internet, acessível a partir do site da SME. Permite consultas de forma muito simples e intuitiva, partindo do mapa da cidade de São Paulo. 

- **Não faz**: Restrição de acesso de pessoas. Atualização de dados orçamentários pela próprio site. 

## Objetivos de Negócio: 

--- 

- Aumentar consideravelmente a transparência em relação aos dados orçamentários da SME e da Prefeitura da Cidade de São Paulo. 

- Fornecedor acesso simplificado aos dados de orçamento da rede municipal de educação.  

## Personas: 

--- 

- **Cidadão**: Qualquer pessoa que acesse o site. Como não há restrição de acesso, basta acessar o link da ferramenta, disponível através do site da SME. Pode consultar todas as informações de orçamento da rede, a partir do mapa da Cidade de São Paulo. 

- **Administrador SME**: Usuário que faz a carga dos dados orçamentários de cada ano. Atualmente, a carga é feita através de scripts no servidor onde a aplicação está hospedada. 


# Funcionalidades: 

--- 

- **Seletor por Tipo de Rede**: filtra os dados em duas modalidades: unidades diretas e unidades parceiras. O padrão da posição do seletor por tipo de rede é a opção “unidades diretas”. 

- **Seletor de Período**: permite filtrar o ano de referência dos dados e das visualizações apresentadas na filtragem por região. 

- **Trilha de Navegação**: persiste com o caminho percorrido pelo usuário até o quarto nível de visualização, permitindo que o usuário aplique os filtros diretamente na trilha sem que haja necessidade de refazer toda a navegação através do mapa. A trilha funciona em conjunto com o mapa, indicando em detalhes o caminho percorrido pelo usuário através da seleção (clique) no mapa. 

- **Mapa Interativo**: Os mapas apresentados na filtragem por região tem relação direta com a ficha lateral, uma vez que a ferramenta executa a agregação ou desagregação dos dados exibidos na ficha lateral à medida que o usuário navega pelos diferentes níveis disponíveis no mapa. 

A exibição padrão do mapa é sempre o maior nível de agregação, que consiste na visualização do município de São Paulo dividido em zonas (regiões administrativas). Para descer aos níveis mais granulares de visualização do mapa, o usuário deve clicar na região de interesse dentro do mapa, para que a ferramenta faça o cálculo e exiba na ficha lateral os dados correspondentes a essa região. 


O segundo nível de exibição detalhado do mapa é a visualização da região (zona), dividida por suas Diretorias Regionais de Educação - DREs. No próximo nível de detalhamento, o mapa das regiões é substituído pelo mapa de DREs, que exibe os distritos que compõem o território administrado pela DRE selecionada. O quarto nível de detalhamento - o último e mais granular - é a visualização dos distritos, que permite identificar a localização das unidades de ensino distribuídas em cada distrito. 


Para retornar aos níveis de maior agregação, o usuário deve selecionar o nível desejado na trilha de navegação do mapa, de modo que os cálculos e exibições sejam refeitos e atualizados na filtragem por região. As subseções a seguir dão mais informações de cada nível de detalhamento apresentado no mapa interativo, bem como a sua correspondência com a ficha lateral. 

- **Ficha Lateral**: posicionada à direita da página, apresenta a especificação dos dados de acordo com os filtros de rede e de ano e os níveis de detalhamento aplicados a partir da interação do usuário com o mapa. 

# Jornadas: 

--- 


## Seleção do Tipo de Rede 

O sistema é exibido com algumas informações selecionadas por padrão. O Tipo de Rede inicia selecionado na opção **Unidades Diretas**. Com isso, no primeiro acesso do usuário serão sempre exibidas as informações de orçamento para este tipo de rede, considerando os dados para toda a cidade de São Paulo.  

O usuário tem a opção de trocar essa seleção para **Unidade Parceiras**, e assim, visualizar os dados para este outro tipo de rede. 

 
## Seleção do Período 

O sistema é exibido com algumas informações selecionadas por padrão. O Período selecionado é o ano mais atual com dados carregados. Com isso, no primeiro acesso do usuário serão exibidas as informações de orçamento para este ano, considerando os dados para toda a cidade de São Paulo.  

O usuário tem a opção de trocar o período para anos anteriores, e assim, visualizar os dados correspondentes. 


## Navegação no Mapa 

O sistema é exibido por padrão sem nenhum ponto selecionado no mapa interativo. Assim, a Ficha Lateral exibe dados de orçamento referentes a toda a cidade de São Paulo.  

O usuário pode ir avançando o nível de detalhe no mapa, selecionando primeiro uma Zona, depois DRE, Bairro, até chegar ao nível da Unidade Educacional. A cada etapa a Ficha Lateral é atualizada para corresponder a seleção, e informa dados cada vez mais específicos. A Trilha de Navegação também é atualizada, permitindo ao usuário voltar para qualquer ponto anterior da navegação. 


## Download dos Dados 

A qualquer momento o usuário pode optar por baixar os dados de orçamento para o seu próprio dispositivo. O sistema leva em consideração apenas o **Período** selecionado pelo usuário e disponibiliza em formato de Planilha Eletrônica (arquivo .xlsx) todos os dados de orçamento disponíveis para a rede. 

  

# Roadmap: 

--- 

Atualmente, não existem evoluções previstas para o sistema.  

# Como contribuir

Contribuições são **super bem vindas**! Se você tem vontade de construir o
curriculo digital conosco, veja o nosso [guia de contribuição](./CONTRIBUTING-GUIDE.md)
onde explicamos detalhadamente como trabalhamos e de que formas você pode nos
ajudar a alcançar nossos objetivos. Lembrando que todos devem seguir 
nosso [código de conduta](./CODEOFCONDUCT.md).

# Configuração do Projeto
---

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
