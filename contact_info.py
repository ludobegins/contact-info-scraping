# fonte: https://medium.com/@rodrigonader/web-scraping-to-extract-contact-information-part-1-mailing-lists-854e8a8844d2

import logging
import os
#from unittest import runner
import pandas as pd
import re
import scrapy
#import scrapy.crawler as crawler
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from multiprocessing import Process #, Queue
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from googlesearch import search
from scrapy_proxy_pool.policy import BanDetectionPolicy
from mail_spider import MailSpider
import empresas_aux
from time import sleep

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
    tags = tag[0] + " " + tag[1]
    urls = [url for url in search(tags, stop=n, lang=language)][:n]
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

""" def execute_crawling(start_urls,path,reject):
    process = CrawlerProcess() #{'USER_AGENT': 'Mozilla/5.0'})
    process.crawl(MailSpider, start_urls, path, reject)
    process.start() """

def get_info(n, language,reject):

    for i in range(10):
        empresa = empresas_aux.lista_empresas[i]
        path = f'{empresa}.csv'
        create_file(path)
        df = pd.DataFrame(columns=['email', 'link'], index=[0])
        df.to_csv(path, mode='w', header=True)
        print('Collecting Google urls...')
        tag = [empresa,"sustentabilidade"]
        google_urls = get_urls(tag, n, language)
        print(google_urls)
        sleep(2)
        print(f'Searching for emails...{empresa}')
        #process = CrawlerProcess() #{'USER_AGENT': 'Mozilla/5.0'})
        #process.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
        runner = CrawlerRunner()
        runner.crawl(MailSpider, start_urls=google_urls, path=path, reject=reject)
    
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    #process.start()
    
    #return df

get_info(10,"pt-BR",['instagram','facebook'])