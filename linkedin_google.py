import os
from googlesearch import search
import pandas as pd


def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)][:n]
    return urls


def ask_user(question):
    response = input(question + ' y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False

def create_file(path):
    response = False
    if os.path.exists(path):
        response = ask_user('File already exists, replace?')
        if response == False: return 
    
    with open(path, 'wb') as file: 
        file.close()


def get_info(tag, n, language, path):
    
    create_file(path)
    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)
    print(google_urls)
    df = pd.DataFrame(data=google_urls, columns=['linkedin'])
    df.to_csv(path, mode='w', header=True)
    
    return df

def main():
    termo_pesquisa = input("Com qual termo de pesquisa deseja procurar perfis do Linkedin? \n")
    num_urls = int(input("Quantas URLs do Google deseja scrape?\n"))
    path1 = r'C:\gitrepos\contact-info-scraping\contatos\''
    df = get_info(termo_pesquisa, num_urls, 'pt-BR', path1+f'{termo_pesquisa}_{num_urls}.csv')
    print(df.head(10))

if __name__ == '__main__':
    main()