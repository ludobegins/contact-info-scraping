import scrapy
import re
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import pandas as pd

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
        #mail_list = re.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', html_text)
        mail_list = re.findall(r'^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$', html_text)
        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)
        
        df.to_csv(self.path, mode='a', header=False)
        #df.to_csv(self.path, mode='a', header=False)
        print('Cleaning emails...')
        df = pd.read_csv(self.path, index_col=0)
        df.columns = ['email', 'link']
        df = df.drop_duplicates(subset='email')
        #df = df[df['email'].astype(str).str.contains(f"{tag[0]}", na=False)] # só guardar os que contém nome da empresa no email - tentativa de limpar emails sujos
        df = df[~df['email'].astype(str).str.contains("png", na=False)]
        df = df[~df['email'].astype(str).str.contains("jpg", na=False)]
        df = df[~df['email'].astype(str).str.contains("gif", na=False)]
        df = df[~df['email'].astype(str).str.contains("img", na=False)]
        df = df.reset_index(drop=True)
        print(df.head(10))
        print(df.tail(10))
        df.to_csv(self.path, mode='w', header=True)