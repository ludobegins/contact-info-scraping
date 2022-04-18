# source: https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python

import requests
import urllib
import pandas as pd
import empresas_aux
from requests_html import HTMLSession

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
    print(query)
    response = get_source("https://www.google.com.br/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    #css_identifier_text = ".VwiC3b"
    
    results = response.html.find(css_identifier_result)
    print(results)

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
    path = path1+f'{termo}.csv'
    df = pd.DataFrame(results)
    df.to_csv(path, mode='w', header=True)

path1 = r'C:\gitrepos\contact-info-scraping\contatos\''
termo_complem = " sustentabilidade linkedin"
for e in empresas_aux.lista_empresas[:1]:
    save_search(e+termo_complem,path1)

#termo_pesquisa = input("Termo de pesquisa:\n")

