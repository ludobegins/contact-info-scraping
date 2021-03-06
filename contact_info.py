# fonte: https://medium.com/@rodrigonader/web-scraping-to-extract-contact-information-part-1-mailing-lists-854e8a8844d2

import logging
import os
#from unittest import runner
import pandas as pd
import re
import scrapy
#import scrapy.crawler as crawler
from scrapy.crawler import CrawlerProcess
#from scrapy.crawler import CrawlerRunner
#from twisted.internet import reactor
#from multiprocessing import Process, Queue
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
from scrapy_proxy_pool.policy import BanDetectionPolicy
import empresas_aux

logging.getLogger('scrapy').propagate = False

class BanDetectionPolicyNotText(BanDetectionPolicy):

    def response_is_ban(self, request, response):
        # if self.BANNED_PATTERN.search(response.text): <-this line caused error
        #    return True

        if response.status not in self.NOT_BAN_STATUSES:
            return True
        if response.status == 200 and not len(response.body):
            return True

def get_urls(tag, n, language):
    urls = [url for url in search(tag, stop=n, lang=language)][:n]
    return urls

class MailSpider(scrapy.Spider):
    
    name = 'email'
    PROXY_POOL_BAN_POLICY = 'BanDetectionPolicyNotText'
    
    def parse(self, response):
        
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link) 
            
    def parse_link(self, response):
        
        for word in self.reject:
            if word in str(response.url):
                return
            
        html_text = str(response.text)
        mail_list = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', html_text)
        #mail_list = re.findall(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$', html_text)
        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)
        df.to_csv(self.path, mode='a', header=False)
        #df.to_csv(self.path, mode='a', header=False)


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

""" def f(q,spider,start_urls,path,reject):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(spider, start_urls, path, reject)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e) 

def run_spider(spider,start_urls,path,reject):
    q = Queue()
    p = Process(target=f, args=(q,spider,start_urls,path,reject))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result  """

def get_info(tag, n, language, path, termo_obri, reject=[]):
    
    create_file(path)
    df = pd.DataFrame(columns=['email', 'link'], index=[0])
    df.to_csv(path, mode='w', header=True)
    
    print('Collecting Google urls...')
    google_urls = get_urls(tag, n, language)
    print(google_urls)
    print('Searching for emails...')
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    process = CrawlerProcess(headers)
    process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    process.start()
    
    print('Cleaning emails...')
    df = pd.read_csv(path, index_col=0)
    df.columns = ['email', 'link']
    df = df.drop_duplicates(subset='email')
    #df = df[df['email'].astype(str).str.contains(f"{tag[0]}", na=False)] # s?? guardar os que cont??m nome da empresa no email - tentativa de limpar emails sujos
    termos_cancelados = ["png","jpg","gif","img",".js","slick-carousel","react"]
    for tc in termos_cancelados:
        df = df[~df['email'].astype(str).str.contains(tc, na=False)]
    if termo_obri != "*":
        df = df[df['email'].astype(str).str.contains(termo_obri, na=False)]
    df = df.reset_index(drop=True)
    df.to_csv(path, mode='w', header=True)
    
    return df

def main():
    bad_words = ['twitter','facebook','instagram','youtube']
    termo_pesquisa = input("Com qual termo de pesquisa deseja procurar emails? \n")
    num_urls = int(input("Quantas URLs do Google deseja scrape?\n"))
    if input("Algum termo espec??fico deve estar nos emails? s/n \n") == "s":
        termo_obri = input("Qual termo? \n")
    else:
        termo_obri = "*"
    path1 = r'C:\gitrepos\contact-info-scraping\contatos\''
    df = get_info(termo_pesquisa, num_urls, 'pt-BR', path1+f'{termo_pesquisa}_{num_urls}.csv', termo_obri, bad_words)
    print(df.head(10))

if __name__ == '__main__':
    main()