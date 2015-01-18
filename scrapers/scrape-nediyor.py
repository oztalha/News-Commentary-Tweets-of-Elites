# -*- coding: utf-8 -*-
"""
Created on Thu Jan 08 15:41:01 2015

@author: Talha
"""

from selenium import webdriver
import pandas as pd
import time

#initialize variables
df = pd.DataFrame(columns=('title', 'twcount', 'href'))
driver = webdriver.Firefox()

# nediyor.com gundem sayfasi
#driver.get('http://nediyor.com/haberler/gundem/') 
driver.get('file:///Users/toz/Documents/workspace/TR-2014/nediyor.html')
#ime.sleep(60) #sayfanin tamamen yuklenmesini beklememiz gerekiyor

"""
# Post islem icin benim indirmis oldugum nediyor.html'i kullanabilirsiniz
# eger kendiniz indirmek isterseniz lazy loading problemini cozmek icin: 
# sayfanin sonuna git - her defasinda 18 yeni haber yukleniyor
for i in range(1000):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
"""
errors = []
news = driver.find_elements_by_xpath("//div[@class='brick brick-big']")
for i,haber in enumerate(news):
    try:
        title = haber.find_element_by_tag_name("h2").find_element_by_tag_name("a")
        twcount = haber.find_element_by_xpath("div[@class='tweet-count']").find_element_by_tag_name("a").text
        # print i, title.text , twcount, title.get_attribute("href")
        df.loc[len(df)+1]=[title.text , twcount, title.get_attribute("href")]
    except:
        errors.append(i)

df['twcount']=df['twcount'].astype(int)
df.to_csv("TR-news-headlines.csv",encoding='utf-8',index=False)