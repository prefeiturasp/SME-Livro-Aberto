#####################
# packages
#####################

import requests, logging, os, time, re
import pandas as pd


#####################
# coleta de empenho
#####################

def select_empenho(url, key, year, cod, ex_year):

    output = pd.DataFrame()

    try:
        response = requests.get(url, headers={'Authorization': key})
        response.raise_for_status()

    except Exception as e:

        log.error('Problema na coleta: {error}'.format(error = e))
        pd.DataFrame([url], columns=['URL']).to_csv('missed_urls.csv', mode='a', index=False,  header=False)

        if 'HTTPSConnectionPool' in str(e):
            time.sleep(5*60)

    else:

        json_data = response.json()
        output = pd.DataFrame(json_data["lstEmpenhos"])

        if json_data["metadados"]["qtdPaginas"] > 1:

            tam = json_data["metadados"]["qtdPaginas"] + 1

            for i in range(2,tam):

                log.error('pagina: ' + str(i))
                response = requests.get('https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v2.1.0/consultaEmpenhos?anoEmpenho='+ str(year) +'&mesEmpenho=12&anoExercicio='+str(ex_year)+'&codContrato='+ str(cod) +'&codOrgao=16&numPagina=' + str(i)  , headers={'Authorization': key})
                log.error('url select_empenho: ' + url)
                json_data = response.json()
                aux = pd.DataFrame(json_data["lstEmpenhos"])
                output = output.append(aux)

    return output


def consolida_empenho(dirContrato, key, year):

    contrato = pd.read_excel(dirContrato)
    contrato = contrato[contrato.anoExercicio.isin([2019,2019])]
    # contrato = contrato[contrato.anoExercicio.isin([2018,2019])]
    dados = pd.DataFrame()

    for i in range(0,contrato.shape[0]):

        print("consolida empenho: {}".format(i))
        cod = contrato['codContrato'].iloc[i]
        ex_year = contrato['anoExercicio'].iloc[i]
        log.info('contrato: ' + str(cod) + ' ano: '+ str(ex_year) + ' ano do empenho: ' + str(year))

        url = 'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v2.1.0/consultaEmpenhos?anoEmpenho='+ str(year) +'&mesEmpenho=12&anoExercicio='+str(ex_year)+'&codContrato='+ str(cod) +'&codOrgao=16&numPagina=1'

        print("select empenho: {}-{}-{}".format(ex_year, cod, i))
        aux = select_empenho(url = url, key = key, year = year, cod = cod, ex_year = ex_year)

        if aux.empty:
            next

        aux['anoExercicio'] = ex_year
        aux['codContrato'] = cod
        dados = dados.append(aux)

        aux.to_csv('empenho{}-{}-{}.csv'.format(ex_year, cod, i), index=False, encoding='latin1')
        # aux.to_csv('empenho.csv', mode='a', index=False,  header=False, encoding='latin1')

    return(dados)


def consolida_ano_empenho(dirContrato, key, start, end):


    for i in range(start, end):
        log.info('ano: ' + str(i))

        print('consolida ano empenho: {}'.format(i))
        aux = consolida_empenho(dirContrato, key, i)
        print('rodou aux')
        print(aux)
        if i == start:
            aux.to_csv('empenho.csv', index=False, encoding='latin1')
        else:
            aux.to_csv('empenho.csv', mode='a', index=False,  header=False, encoding='latin1')

    return(None)

def concatena_bases_empenho(dirBases, start, end):

    for i in range(start, end):
        aux = pd.read_csv('empenho_%s.xlsx' % i)
        planilha+=pd.DataFrame(aux)

    planilha.to_excel(dir + 'empenho_consolidado.xlsx')

    print('success')
    return


def coleta_missed_urls(urls):

    for url in urls:
        log.info('Coletando url: '+url)
        output = pd.DataFrame()
        cod = int(re.search('codContrato=(.+?)&', url).group(1))
        ex_year = int(re.search('anoExercicio=(.+?)&', url).group(1))

        try:
            response = requests.get(url, headers={'Authorization': key})
            response.raise_for_status()

        except Exception as e:

            log.error('Problema na coleta: {error}'.format(error = e))
            pd.DataFrame([url], columns=['URL']).to_csv('missed_urls_2.csv', mode='a', index=False,  header=False)

            if 'HTTPSConnectionPool' in str(e):
                time.sleep(5*60)

        else:

            json_data = response.json()
            output = pd.DataFrame(json_data["lstEmpenhos"])

            if json_data["metadados"]["qtdPaginas"] > 1:

                tam = json_data["metadados"]["qtdPaginas"] + 1

                for i in range(2,tam):

                    log.error('pagina: ' + str(i))
                    response = requests.get(url[:-1]+str(i)  , headers={'Authorization': key})
                    log.error('url select_empenho: ' + url)
                    json_data = response.json()
                    aux = pd.DataFrame(json_data["lstEmpenhos"])
                    output = output.append(aux)


        output['anoExercicio'] = ex_year
        output['codContrato'] = cod

        if not os.path.isfile('empenhos_recuperados.csv'):
            output.to_csv('empenhos_recuperados.csv', index=False)
        else:
            output.to_csv('empenhos_recuperados.csv', mode='a', index=False, header=False)


#####################
# coleta de contrato
#####################

def get_deputy_speech(url, key, ano):

    response = requests.get(url, headers={'Authorization': key})

    try:
        response.raise_for_status()
    except Exception as e:
        log.error('Problema na coleta: {error}'.format(error = e))
    else:
        json_data = response.json()
        # contratos
        output = pd.DataFrame(json_data["lstContratos"])
        # empenho
        # output = pd.DataFrame(json_data["lstEmpenhos"])

    if json_data["metadados"]["qtdPaginas"] > 1:

        tam = json_data["metadados"]["qtdPaginas"] + 1

        for i in range(2,tam):
            print('pagina: ' + str(i))
            # contrato
            response = requests.get('https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v2.1.0/consultaContrato?anoContrato='+str(ano)+'&numPagina=' + str(i) + '&codOrgao=16'  , headers={'Authorization': key})
            # empenho
            # response = requests.get('https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v2.1.0/consultaEmpenhos?anoEmpenho='+str(ano)+'&mesEmpenho=12&codOrgao=16&numPagina='+str(i)  , headers={'Authorization': key})
            json_data = response.json()
            aux = pd.DataFrame(json_data["lstContratos"])
            # aux = pd.DataFrame(json_data["lstEmpenhos"])
            output = output.append(aux)

    return output

def api_prodam(start, end, key):
    dados = []
    for i in range(start,end):
        print('ano: ' + str(i))
        # contrato
        url = 'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v2.1.0/consultaContrato?anoContrato='+str(i)+'&numPagina=1&codOrgao=16'
        # empenho
        # url = 'https://gatewayapi.prodam.sp.gov.br:443/financas/orcamento/sof/v2.1.0/consultaEmpenhos?anoEmpenho='+str(i)+'&mesEmpenho=12&codOrgao=16&numPagina=1'
        aux = get_deputy_speech(url, key, i)
        if i == start:
            dados = aux
        else:
            dados = dados.append(aux)

    return(dados)



if __name__ == '__main__':

    os.chdir('.')
    logging.basicConfig(filename = 'coleta_empenhos.log',level=logging.INFO)
    log = logging.getLogger()

    from decouple import config
    log.info('Inciando coleta de empenhos.')
    PRODAM_KEY = config('PRODAM_KEY')

    key = f'Bearer {PRODAM_KEY}'
    dirContrato = './contratos/_script/contrato.xlsx'
    start = 2019
    end = 2020
    # dados = api_prodam(start, end, key)
    consolida_ano_empenho(dirContrato, key, start, end)

    # missed_urls = pd.read_csv('missed_urls.csv', header=None)
    # missed_urls = missed_urls[0].to_list()
    # coleta_missed_urls(missed_urls)
