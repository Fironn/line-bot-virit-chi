from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.parse

def tran(text):
    # ja = 'こんにちは'
    url_text = "https://translate.google.co.jp/#view=home&op=translate&sl=ja&tl=th&text={0}".format(text)
    url = urllib.parse.quote_plus(url_text, "/:?=&#")

    driver = webdriver.PhantomJS()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    res=soup.find(class_="translation")
    print(res.span.text)
    
    return res.span.text
