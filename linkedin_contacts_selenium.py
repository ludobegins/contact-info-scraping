from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
import requests
import urllib
import empresas_aux
from requests_html import HTMLSession


inp = "bradesco sustentabilidade site:linkedin.com"
query = urllib.parse.quote_plus(inp)
url = "https://www.google.com.br/search?q=" + query
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
sleep(20)

titles = driver.find_elements(By.CLASS_NAME,"LC20lb")

for t in titles:
    print(t.text)