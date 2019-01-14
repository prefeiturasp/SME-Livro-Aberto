import pandas as pd


# EXTRAIR COLUNAS: F, H I
# COLUNA F: SEPARAR OS VALORES
def extract_minimo_legal_from_spreadsheet(title, end_quote, file_path):
    """
    Esse código tem como função extrair dados de uma categoria específica a ser definida e gerar uma planilha que seja simples de ser utilizada em ações automatizadas.
    :param title: Define a frase que será usada como ponto de partida para a busca. A frase deverá estar na coluna F.
    :param end_quote: Define sa fase que marcará o fim da busca. A frase deverá estar na coluna F.
    :param file_path: Path e nome do arquivo XLSX a ser tratado
    :param download_name: Nome para o novo arquivo CSV gerado
    :return: Planilha com os dados das colunas F, I & G das entre os pontos de marcação inicial e final

    >>> test_file_path = 'Demonst_Manut_Desenv_Ensino_06Bim-2017_-_versão_20180118.xlsx'
    >>> test_title = 'DESPESAS COM AÇÕES TÍPICAS DE MDE'
    >>> test_end_quote = 'TOTAL DAS DESPESAS COM AÇÕES TÍPICAS DE MDE'
    >>> test_treatment = treatment(test_title, test_end_quote, test_file_path)
    >>> test_treatment.Despesa.sum()
    14355454684.935474
    """
    #Le o arquivo
    df = pd.read_excel(file_path,
                       sheet_name=0,
                       usecols='F,H,I',
                       names=['Descrição', 'Dotação', 'Despesa']).fillna('')
    #define linha de inicio e fim da pesquisa para recuperar o dado entre essas linhas
    start_idx = df[df['Descrição'] == title].index.values[0]
    end_idx_temp = df[df['Descrição'] == end_quote].index.values[0]
    if isinstance(end_idx_temp, list):
        end_idx = end_idx_temp.values.min()
    else:
        end_idx = end_idx_temp
    cut = df.iloc[start_idx:end_idx]

    #recupera apenas os dados que comecme com 4 dígitos numéricos
    final_df = cut[cut.Descrição.fillna('').apply(lambda x: x[:4].isdigit())].copy()

    #divide o código e a Descrição em duas colunas diferentes
    final_df[['Código', 'Descrição']] = final_df.Descrição.str.split(' - ', n=1, expand=True).\
        rename(columns={0:'Código',1:'Descrição'})

    #escreve em um arquivo de csv
    return final_df[['Código', 'Descrição', 'Dotação', 'Despesa']]
