# source: https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python
# CUIDADO COM BLOCK: https://stackoverflow.com/questions/22657548/is-it-ok-to-scrape-data-from-google-results#:~:text=Also%20the%20block%20will%20not,not%20if%20you%20keep%20going.
# Melhor não rodar mais de 8 search requests por hora

from encodings import utf_8
import requests
import urllib
import pandas as pd
import empresas_aux
from requests_html import HTMLSession
from time import sleep

def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com.br/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    #css_identifier_text = ".VwiC3b"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:
        print(result.find(css_identifier_title, first=True).text)
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            #'text': result.find(css_identifier_text, first=True).text
        }
        
        output.append(item)
        
    return output

def google_search(query):
    response = get_results(query)
    return parse_results(response)

def save_search(termo,path1):
    results = google_search(termo)
    save = termo.replace(".com","").replace(":"," ")
    path = path1+f'{save}_v2.csv'
    df = pd.DataFrame(results)
    print(df.head(10))
    df.to_csv(path, mode='w', header=True,encoding='utf-8-sig')

path1 = r'C:\gitrepos\contact-info-scraping\contatos\''
termo_complem = " sustentabilidade site:linkedin.com"
for e in empresas_aux.lista_empresas[21:31]:
    save_search(e+termo_complem,path1)
    sleep(600)

#save_search("BCO BRASIL"+termo_complem,path1)

#termo_pesquisa = input("Termo de pesquisa:\n")

